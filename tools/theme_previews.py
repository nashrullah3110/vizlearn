# -*- coding: utf-8 -*-
"""Candidate palettes for the site, as full dark/light pairs.

The site is themed entirely through the custom properties defined in
index.html: `:root` holds the dark palette and `body.light-mode` the light
one. Nothing else hard-codes a brand colour, so a theme is exactly these
numbers and a preview is the real page with a different set of them.

Each entry gives the handful of anchor colours that actually carry a theme.
Everything else - the glass, the borders, the glow, the grid, the input
surfaces - is derived from the accent at the same opacities the green theme
uses, so a candidate cannot accidentally be judged on a different structure.

Only `accent` and the neutrals change between themes. If a theme needs a
different *structure* it does not belong here; it belongs in a branch.
"""

# accent      : the brand colour, used for links, focus rings and highlights
# body        : page background
# surface     : cards and panels
# text        : body text
# muted       : secondary text - must stay readable on `body`
# inverse     : text sitting on top of a filled accent button
# thumb       : scrollbar thumb
THEMES = [
    {
        "slug": "midnight",
        "name": "Midnight",
        "blurb": "Indigo on near-black. Cooler and quieter than the green; "
                 "reads as tooling rather than terminal.",
        "dark":  {"accent": "#818cf8", "body": "#07070f", "surface": "#0e0e1a",
                  "text": "#eef2ff", "muted": "#a5b4fc", "inverse": "#1e1b4b",
                  "thumb": "#312e81"},
        "light": {"accent": "#4f46e5", "body": "#f5f5ff", "surface": "#ffffff",
                  "text": "#1e1b4b", "muted": "#3f3f56", "inverse": "#ffffff",
                  "thumb": "#c7d2fe"},
    },
    {
        "slug": "ember",
        "name": "Ember",
        "blurb": "Amber on warm charcoal. The only warm option here, and the "
                 "one that looks least like every other developer site.",
        "dark":  {"accent": "#fbbf24", "body": "#0c0906", "surface": "#16110b",
                  "text": "#fffbeb", "muted": "#fcd34d", "inverse": "#451a03",
                  "thumb": "#78350f"},
        "light": {"accent": "#b45309", "body": "#fffbeb", "surface": "#ffffff",
                  "text": "#451a03", "muted": "#44403c", "inverse": "#ffffff",
                  "thumb": "#fde68a"},
    },
    {
        "slug": "tide",
        "name": "Tide",
        "blurb": "Cyan on deep teal-black. Closest in feel to the current "
                 "green, so it is the low-risk change.",
        "dark":  {"accent": "#22d3ee", "body": "#04090b", "surface": "#081418",
                  "text": "#ecfeff", "muted": "#67e8f9", "inverse": "#083344",
                  "thumb": "#164e63"},
        "light": {"accent": "#0e7490", "body": "#ecfeff", "surface": "#ffffff",
                  "text": "#083344", "muted": "#334155", "inverse": "#ffffff",
                  "thumb": "#a5f3fc"},
    },
    {
        "slug": "bloom",
        "name": "Bloom",
        "blurb": "Rose on plum-black. The most opinionated of the five; "
                 "strong personality, least neutral for long reading.",
        "dark":  {"accent": "#fb7185", "body": "#0b0508", "surface": "#170a10",
                  "text": "#fff1f2", "muted": "#fda4af", "inverse": "#4c0519",
                  "thumb": "#881337"},
        "light": {"accent": "#be123c", "body": "#fff1f2", "surface": "#ffffff",
                  "text": "#4c0519", "muted": "#44403c", "inverse": "#ffffff",
                  "thumb": "#fecdd3"},
    },
    {
        "slug": "graphite",
        "name": "Graphite",
        "blurb": "Near-monochrome slate. No brand colour competing with the "
                 "visualisations, which are themselves the colour on the page.",
        "dark":  {"accent": "#cbd5e1", "body": "#0a0a0b", "surface": "#141416",
                  "text": "#f8fafc", "muted": "#94a3b8", "inverse": "#0f172a",
                  "thumb": "#334155"},
        "light": {"accent": "#334155", "body": "#f8fafc", "surface": "#ffffff",
                  "text": "#0f172a", "muted": "#475569", "inverse": "#ffffff",
                  "thumb": "#cbd5e1"},
    },
]


def rgb(hex_colour):
    h = hex_colour.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgba(hex_colour, alpha):
    r, g, b = rgb(hex_colour)
    return "rgba(%d, %d, %d, %s)" % (r, g, b, alpha)


def block(p, mode):
    """The full token set for one mode, derived from the anchors.

    The opacities are lifted from the existing green theme rather than
    re-chosen per palette, so every candidate is the same design in a
    different hue and the comparison is about colour alone.
    """
    dark = mode == "dark"
    return {
        "--bg-body": p["body"],
        "--bg-surface": p["surface"],
        "--bg-glass": rgba(p["surface"], "0.85"),

        "--border-subtle": rgba(p["accent"], "0.15" if dark else "0.25"),
        "--border-glow": rgba(p["accent"], "0.5" if dark else "0.4"),

        "--accent-primary": p["accent"],
        "--accent-glow": rgba(p["accent"], "0.25" if dark else "0.2"),

        "--text-main": p["text"],
        "--text-muted": p["muted"],
        "--text-placeholder": p["accent"],
        "--text-inverse": p["inverse"],

        "--card-bg": p["surface"],
        "--card-icon-bg": rgba(p["accent"], "0.05"),
        "--input-bg": rgba(p["accent"], "0.03" if dark else "0.04"),
        "--input-focus-bg": rgba(p["accent"], "0.08"),

        "--scrollbar-track": p["body"],
        "--scrollbar-thumb": p["thumb"],

        "--grid-color": rgba(p["accent"], "0.05" if dark else "0.06"),
        "--vignette-color": p["body"] if dark else "transparent",
    }


def css(theme):
    def rules(sel, mode):
        toks = block(theme[mode], mode)
        body = "\n".join("      %s: %s;" % (k, v) for k, v in toks.items())
        return "    %s {\n%s\n    }" % (sel, body)

    return "%s\n\n%s" % (rules(":root", "dark"), rules("body.light-mode", "light"))
