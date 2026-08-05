#!/usr/bin/env python3
"""Render a 1200x630 social preview image for every module.

Each module already ships a small hand-drawn SVG for its card on the hub; this
composes that artwork into a branded frame with the title and category, then
rasterises to PNG (Open Graph will not accept SVG).

Requires ImageMagick (`magick`) on PATH.
"""

import html
import os
import re
import subprocess
import sys

from lib_catalog import ROOT, by_topic, modules
from lib_pages import (STATIC_PAGES, STATIC_TITLES, TOOL_ORDER, TOOL_PAGES,
                       TOPICS, TOPIC_ORDER)

OUT_DIR = os.path.join(ROOT, "assets", "og")

W, H = 1200, 630
BG = "#050505"
GREEN = "#4ade80"
TEXT = "#f0fdf4"
MUTED = "#86efac"

FONT = "Helvetica, Arial, sans-serif"
MONO = "Courier New, monospace"

TITLE_SIZE = 56
TITLE_LEAD = 70
TEXT_X = 80
TEXT_W = 540          # wrapping width for the title column
MAX_LINES = 3


def wrap(title, size, width, max_lines):
    """Greedy wrap using an average glyph-width estimate for bold Helvetica."""
    per_char = size * 0.56
    limit = max(8, int(width / per_char))
    words, lines, cur = title.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= limit or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: limit - 1].rstrip() + "…"
    return lines


# The card artwork is authored against the site's CSS custom properties, which
# only resolve in a browser. Bake in equivalents before rasterising -- pushed
# a few stops brighter than the on-site values, because a social preview is
# viewed small and heavily compressed, where the site's near-black borders and
# surfaces would disappear entirely.
VAR_COLORS = {
    "--accent-primary": "#4ade80",
    "--text-main": "#f0fdf4",
    "--text-muted": "#86efac",
    "--border-subtle": "#3f8f63",
    "--bg-surface": "#12211a",
    "--card-bg": "#12211a",
    "--input-bg": "#16291f",
    "--accent-glow": "#4ade80",
    "--bg-body": "#0b120e",
}


def resolve_vars(markup):
    """Replace var(--name) and var(--name, fallback) with a literal colour."""
    def sub(m):
        name, fallback = m.group(1), (m.group(2) or "").strip()
        if name in VAR_COLORS:
            return VAR_COLORS[name]
        return fallback or "#4ade80"
    return re.sub(r"var\(\s*(--[a-z0-9-]+)\s*(?:,([^)]*))?\)", sub, markup)


def inner_svg(card_svg):
    """Strip the outer <svg> wrapper, returning its children and viewBox."""
    m = re.match(r"<svg[^>]*viewBox=\"([^\"]+)\"[^>]*>(.*)</svg>\s*$", card_svg.strip(), re.S)
    if not m:
        return "0 0 160 90", ""
    return m.group(1), resolve_vars(m.group(2))


def build_svg(mod):
    view, art = inner_svg(mod["svg"])
    vb = [float(x) for x in view.split()]
    vw, vh = (vb[2], vb[3]) if len(vb) == 4 else (160.0, 90.0)

    # Artwork panel on the right.
    px, py, pw, ph = 660, 140, 470, 350
    scale = min(pw * 0.95 / vw, ph * 0.95 / vh)
    ax = px + (pw - vw * scale) / 2
    ay = py + (ph - vh * scale) / 2

    lines = wrap(mod["title"], TITLE_SIZE, TEXT_W, MAX_LINES)
    # Vertically centre the title block in the text column.
    block_h = len(lines) * TITLE_LEAD
    ty = 315 - block_h / 2 + TITLE_SIZE * 0.78

    tspans = "".join(
        '<text x="%d" y="%.1f" fill="%s" font-family="%s" font-size="%d" '
        'font-weight="bold">%s</text>'
        % (TEXT_X, ty + i * TITLE_LEAD, TEXT, FONT, TITLE_SIZE, html.escape(ln))
        for i, ln in enumerate(lines)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{GREEN}" stroke-width="1" opacity="0.06"/>
    </pattern>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{GREEN}" stop-opacity="0.10"/>
      <stop offset="60%" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect width="{W}" height="{H}" fill="url(#fade)"/>
  <rect x="0" y="0" width="{W}" height="6" fill="{GREEN}"/>

  <!-- wordmark: two <text> runs rather than tspans, which the rasteriser
       does not advance correctly -->
  <circle cx="{TEXT_X + 9}" cy="86" r="9" fill="{GREEN}"/>
  <text x="{TEXT_X + 30}" y="97" fill="{TEXT}" font-family="{FONT}" font-size="34" font-weight="bold">viz</text>
  <text x="{TEXT_X + 92}" y="97" fill="{MUTED}" font-family="{FONT}" font-size="34">learn</text>

  <!-- category -->
  <text x="{TEXT_X}" y="{175}" fill="{GREEN}" font-family="{MONO}" font-size="21" letter-spacing="1">{html.escape(mod['category'].upper())}</text>
  <rect x="{TEXT_X}" y="190" width="54" height="3" rx="1.5" fill="{GREEN}"/>

  {tspans}

  <text x="{TEXT_X}" y="560" fill="{MUTED}" font-family="{FONT}" font-size="24">Interactive visual explainer &#183; vizlearn.in</text>

  <!-- artwork panel -->
  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="20" fill="#0b120e" stroke="{GREEN}" stroke-opacity="0.25" stroke-width="2"/>
  <g transform="translate({ax:.1f},{ay:.1f}) scale({scale:.4f})">{art}</g>
</svg>"""


# --------------------------------------------------------------------------
# The pages that are not modules still need a card.
# --------------------------------------------------------------------------
# A neutral mark for pages with no artwork of their own.
GENERIC_ART = (
    '<svg viewBox="0 0 160 90">'
    '<circle cx="40" cy="45" r="7" fill="var(--accent-primary)"/>'
    '<circle cx="80" cy="26" r="7" fill="var(--text-muted)"/>'
    '<circle cx="80" cy="64" r="7" fill="var(--text-muted)"/>'
    '<circle cx="120" cy="45" r="7" fill="var(--accent-primary)"/>'
    '<path d="M40 45 L80 26 M40 45 L80 64 M80 26 L120 45 M80 64 L120 45" '
    'stroke="var(--border-subtle)" stroke-width="2" fill="none"/>'
    "</svg>"
)


def extra_entries():
    """Synthetic module-shaped dicts for the hub, tracks and static pages."""
    groups = by_topic()
    out = [{"path": "index.html", "title": "Interactive AI & Algorithm Visualizations",
            "category": "VizLearn", "svg": GENERIC_ART}]

    for key in TOPIC_ORDER:
        mods = groups.get(key) or []
        t = TOPICS[key]
        out.append({
            "path": "%s/index.html" % t["dir"],
            "title": t["h1"],
            # The track's first module lends its artwork, so each track card
            # looks like the thing it opens onto.
            "category": "%d modules" % len(mods),
            "svg": mods[0]["svg"] if mods else GENERIC_ART,
        })

    for rel in STATIC_PAGES:
        out.append({"path": rel, "title": STATIC_TITLES[rel],
                    "category": "VizLearn", "svg": GENERIC_ART})

    for key in TOOL_ORDER:
        t = TOOL_PAGES[key]
        out.append({"path": t["rel"], "title": t["title"],
                    "category": "VizLearn", "svg": GENERIC_ART})
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    mods = modules() + extra_entries()
    only = sys.argv[1] if len(sys.argv) > 1 else None

    made = 0
    failed = []
    for m in mods:
        slug = m["path"].replace("/", "__").replace(".html", "")
        if only and only not in slug:
            continue
        svg_path = os.path.join(OUT_DIR, slug + ".svg")
        png_path = os.path.join(OUT_DIR, slug + ".png")
        with open(svg_path, "w", encoding="utf-8") as fh:
            fh.write(build_svg(m))
        proc = subprocess.run(
            ["magick", "-background", "none", svg_path,
             "-resize", "%dx%d" % (W, H), "-strip", "-quality", "92", png_path],
            capture_output=True, text=True,
        )
        os.remove(svg_path)
        if proc.returncode != 0 or not os.path.exists(png_path):
            failed.append((slug, proc.stderr.strip().split("\n")[0]))
            continue
        made += 1

    print("rendered %d OG images -> %s" % (made, os.path.relpath(OUT_DIR, ROOT)))
    if failed:
        print("\nFAILED (%d):" % len(failed))
        for slug, err in failed:
            print("  %-60s %s" % (slug, err))


if __name__ == "__main__":
    main()
