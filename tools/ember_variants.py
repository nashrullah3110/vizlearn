# -*- coding: utf-8 -*-
"""Five designs on the Ember palette.

Ember was picked from the palette round, so the question is no longer which
hue but what to do with it. Each variant here keeps the amber family and
changes the things a palette preview deliberately held constant: type, shape,
density, the weight of the hero, and how the new sections below it read.

Every variant gets the same new sections with the same words - the design is
what varies, so the comparison is about design. The numbers in those sections
are derived from the catalog rather than written down, for the same reason the
rest of the site's counts are.

A variant is:
  dark/light : the anchor colours, as in theme_previews
  css        : everything else - it restyles the existing hub and the new
               sections together, so a variant is one coherent look rather
               than a palette with sections bolted under it
"""

# ---------------------------------------------------------------------------
# 1. FORGE - dark, molten, glass. The accent is a light source.
# ---------------------------------------------------------------------------
FORGE_CSS = """
    body { background-attachment: fixed; }

    /* The hero sits in a pool of heat rather than on a flat field. */
    #hero-intro {
      position: relative;
      padding-top: 5rem;
      padding-bottom: 3.5rem;
    }
    #hero-intro::before {
      content: "";
      position: absolute;
      inset: -20% -10% auto -10%;
      height: 130%;
      background:
        radial-gradient(60% 55% at 50% 0%, color-mix(in srgb, var(--accent-primary) 22%, transparent) 0%, transparent 70%),
        radial-gradient(40% 40% at 15% 30%, color-mix(in srgb, var(--accent-primary) 10%, transparent) 0%, transparent 70%);
      pointer-events: none;
      z-index: 0;
      filter: blur(6px);
    }
    #hero-intro > * { position: relative; z-index: 1; }
    #hero-intro h1 { letter-spacing: -0.045em; }

    .vz-card,
    .vzx-panel {
      background: linear-gradient(160deg,
        color-mix(in srgb, var(--accent-primary) 7%, var(--bg-surface)) 0%,
        var(--bg-surface) 55%);
      border: 1px solid color-mix(in srgb, var(--accent-primary) 18%, transparent);
      box-shadow: 0 1px 0 color-mix(in srgb, var(--accent-primary) 12%, transparent) inset;
      transition: transform .25s cubic-bezier(.2,.8,.2,1), box-shadow .25s, border-color .25s;
    }
    .vz-card:hover {
      transform: translateY(-4px);
      border-color: color-mix(in srgb, var(--accent-primary) 45%, transparent);
      box-shadow: 0 14px 40px -14px var(--accent-glow),
                  0 1px 0 color-mix(in srgb, var(--accent-primary) 25%, transparent) inset;
    }

    .vzx-sec { padding: 5rem 0; position: relative; }
    .vzx-sec + .vzx-sec { border-top: 1px solid var(--border-subtle); }
    .vzx-kicker {
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: .68rem; letter-spacing: .22em; text-transform: uppercase;
      color: var(--accent-primary); opacity: .9;
    }
    .vzx-h { font-size: clamp(1.7rem, 3.4vw, 2.6rem); font-weight: 800; letter-spacing: -0.03em;
             margin: .6rem 0 .5rem; color: var(--text-main); }
    .vzx-sub { color: var(--text-muted); max-width: 62ch; }

    .vzx-step-n {
      width: 2.6rem; height: 2.6rem; border-radius: 999px;
      display: grid; place-items: center; font-weight: 800;
      background: var(--accent-primary); color: var(--text-inverse);
      box-shadow: 0 0 0 6px color-mix(in srgb, var(--accent-primary) 14%, transparent);
    }
    .vzx-track-row:hover { background: color-mix(in srgb, var(--accent-primary) 8%, transparent); }
    .vzx-bar span { background: linear-gradient(90deg, var(--accent-primary), color-mix(in srgb, var(--accent-primary) 45%, transparent)); }
    .vzx-cta {
      background: linear-gradient(135deg,
        color-mix(in srgb, var(--accent-primary) 16%, var(--bg-surface)),
        var(--bg-surface));
      border: 1px solid color-mix(in srgb, var(--accent-primary) 30%, transparent);
      border-radius: 1.5rem;
    }
"""

# ---------------------------------------------------------------------------
# 2. ATLAS - editorial. Serif display, hairlines, numerals that carry weight.
# ---------------------------------------------------------------------------
ATLAS_CSS = """
    body { background-image: none; background-color: var(--bg-body); }

    #hero-intro { padding-top: 4.5rem; padding-bottom: 3rem; text-align: left; align-items: flex-start; }
    #hero-intro > * { text-align: left; }
    #hero-intro h1,
    .vzx-h,
    .vz-intro-title {
      font-family: Georgia, "Iowan Old Style", "Times New Roman", serif;
      font-weight: 600;
      letter-spacing: -0.015em;
      line-height: 1.08;
    }
    #hero-intro h1 { font-size: clamp(2.4rem, 5.6vw, 4.2rem); }
    #hero-intro p { max-width: 54ch; margin-left: 0; margin-right: 0; }

    /* Rules instead of boxes. */
    .vzx-sec { padding: 4.5rem 0; border-top: 1px solid var(--border-subtle); }
    .vzx-kicker {
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: .66rem; letter-spacing: .28em; text-transform: uppercase;
      color: var(--text-muted);
    }
    .vzx-h { font-size: clamp(1.6rem, 3vw, 2.3rem); margin: .5rem 0 .6rem; color: var(--text-main); }
    .vzx-sub { color: var(--text-muted); max-width: 58ch; }

    .vz-card,
    .vzx-panel {
      background: transparent;
      border: 0;
      border-top: 1px solid var(--border-subtle);
      border-radius: 0;
      box-shadow: none;
    }
    .vz-card:hover { background: color-mix(in srgb, var(--accent-primary) 6%, transparent); }

    .vzx-step-n {
      width: auto; height: auto; border-radius: 0; background: none;
      color: var(--accent-primary); font-weight: 400;
      font-family: Georgia, serif; font-size: 2.6rem; line-height: 1;
      border-bottom: 2px solid var(--accent-primary); padding-bottom: .1rem;
    }
    .vzx-track-row { border-bottom: 1px solid var(--border-subtle); }
    .vzx-track-n { font-family: Georgia, serif; font-size: 1.5rem; color: var(--accent-primary); }
    .vzx-bar { display: none; }
    .vzx-cta { border-top: 2px solid var(--accent-primary); border-radius: 0; padding-top: 2.5rem; }
"""

# ---------------------------------------------------------------------------
# 3. TERMINAL - mono, sharp, bracketed. The site as a tool.
# ---------------------------------------------------------------------------
TERMINAL_CSS = """
    body, button, input, select { font-family: ui-monospace, SFMono-Regular, Menlo, "JetBrains Mono", monospace; }

    #hero-intro { padding-top: 3.5rem; padding-bottom: 2.5rem; }
    #hero-intro h1 {
      font-family: inherit; font-weight: 700; letter-spacing: -0.02em;
      font-size: clamp(1.9rem, 4.2vw, 3.1rem);
    }
    #hero-intro h1::before { content: "$ "; color: var(--accent-primary); opacity: .7; }

    /* Nothing rounds. Everything snaps to the grid. */
    .vz-card, .vzx-panel, .vzx-cta, #hero-intro a, .vz-btn, button, .vz-chip {
      border-radius: 2px !important;
    }
    .vz-card, .vzx-panel {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      box-shadow: none;
    }
    .vz-card:hover {
      border-color: var(--accent-primary);
      box-shadow: 4px 4px 0 0 color-mix(in srgb, var(--accent-primary) 25%, transparent);
    }

    .vzx-sec { padding: 4rem 0; border-top: 1px dashed var(--border-subtle); }
    .vzx-kicker { font-size: .68rem; letter-spacing: .16em; color: var(--accent-primary); }
    .vzx-kicker::before { content: "// "; opacity: .6; }
    .vzx-h {
      font-size: clamp(1.4rem, 2.6vw, 2rem); font-weight: 700;
      letter-spacing: -0.01em; margin: .5rem 0 .5rem; color: var(--text-main);
    }
    .vzx-sub { color: var(--text-muted); max-width: 70ch; font-size: .92rem; }

    .vzx-step-n {
      width: 2.2rem; height: 2.2rem; border-radius: 2px; display: grid; place-items: center;
      border: 1px solid var(--accent-primary); color: var(--accent-primary);
      background: color-mix(in srgb, var(--accent-primary) 10%, transparent); font-weight: 700;
    }
    .vzx-track-row { border-bottom: 1px dashed var(--border-subtle); }
    .vzx-track-row:hover { background: color-mix(in srgb, var(--accent-primary) 9%, transparent); }
    .vzx-track-name::before { content: "["; color: var(--accent-primary); opacity: .6; }
    .vzx-track-name::after  { content: "]"; color: var(--accent-primary); opacity: .6; }
    .vzx-bar { height: 6px; border-radius: 0; }
    .vzx-bar span { border-radius: 0; background: repeating-linear-gradient(90deg,
        var(--accent-primary) 0 6px, transparent 6px 9px); }
    .vzx-cta { border: 1px dashed var(--accent-primary); }
"""

# ---------------------------------------------------------------------------
# 4. KILN - warm paper, light-first, generous. The calm one.
# ---------------------------------------------------------------------------
KILN_CSS = """
    body {
      background-image:
        radial-gradient(circle at 20% 0%, color-mix(in srgb, var(--accent-primary) 7%, transparent) 0%, transparent 45%),
        radial-gradient(circle at 85% 12%, color-mix(in srgb, var(--accent-primary) 5%, transparent) 0%, transparent 40%);
      background-attachment: fixed;
    }

    #hero-intro { padding-top: 5.5rem; padding-bottom: 4rem; }
    #hero-intro h1 { letter-spacing: -0.03em; line-height: 1.05; }
    #hero-intro p { font-size: 1.06rem; line-height: 1.75; }

    .vz-card, .vzx-panel {
      background: var(--bg-surface);
      border: 1px solid color-mix(in srgb, var(--accent-primary) 14%, transparent);
      border-radius: 1.25rem;
      box-shadow: 0 1px 2px rgba(120, 70, 20, .04), 0 8px 24px -12px rgba(120, 70, 20, .10);
      transition: transform .3s cubic-bezier(.2,.8,.2,1), box-shadow .3s;
    }
    .vz-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 2px 4px rgba(120, 70, 20, .06), 0 18px 40px -16px rgba(120, 70, 20, .22);
    }

    .vzx-sec { padding: 6rem 0; }
    .vzx-kicker {
      display: inline-block;
      font-size: .68rem; letter-spacing: .18em; text-transform: uppercase; font-weight: 700;
      color: var(--accent-primary);
      background: color-mix(in srgb, var(--accent-primary) 12%, transparent);
      padding: .35rem .8rem; border-radius: 999px;
    }
    .vzx-h { font-size: clamp(1.7rem, 3.2vw, 2.5rem); font-weight: 700; letter-spacing: -0.025em;
             margin: .9rem 0 .6rem; color: var(--text-main); }
    .vzx-sub { color: var(--text-muted); max-width: 60ch; line-height: 1.75; }

    .vzx-step-n {
      width: 3rem; height: 3rem; border-radius: 1rem; display: grid; place-items: center;
      background: color-mix(in srgb, var(--accent-primary) 14%, transparent);
      color: var(--accent-primary); font-weight: 800; font-size: 1.05rem;
    }
    .vzx-track-row { border-radius: .9rem; }
    .vzx-track-row:hover { background: color-mix(in srgb, var(--accent-primary) 8%, transparent); }
    .vzx-bar { height: 8px; border-radius: 999px; }
    .vzx-bar span { border-radius: 999px; }
    .vzx-cta { border-radius: 2rem; padding: 3rem 2rem;
               background: color-mix(in srgb, var(--accent-primary) 9%, var(--bg-surface));
               border: 1px solid color-mix(in srgb, var(--accent-primary) 18%, transparent); }
"""

# ---------------------------------------------------------------------------
# 5. SIGNAL - high contrast, blocky, loud. Accent as a slab, not a tint.
# ---------------------------------------------------------------------------
SIGNAL_CSS = """
    body { background-image: none; }

    #hero-intro { padding-top: 4rem; padding-bottom: 3rem; }
    #hero-intro h1 {
      font-size: clamp(2.3rem, 6vw, 4.6rem);
      font-weight: 900; letter-spacing: -0.05em; line-height: .97; text-transform: none;
    }
    /* The second line of the headline gets the slab. */
    #hero-intro h1 span,
    #hero-intro h1 .text-brand-400 {
      background: var(--accent-primary);
      color: var(--text-inverse);
      padding: 0 .28em .06em;
      border-radius: .12em;
      box-decoration-break: clone;
      -webkit-box-decoration-break: clone;
    }

    .vz-card, .vzx-panel {
      background: var(--bg-surface);
      border: 2px solid var(--text-main);
      border-radius: .6rem;
      box-shadow: 4px 4px 0 0 var(--text-main);
      transition: transform .15s ease, box-shadow .15s ease;
    }
    .vz-card:hover {
      transform: translate(-2px, -2px);
      box-shadow: 7px 7px 0 0 var(--accent-primary);
    }

    .vzx-sec { padding: 4.5rem 0; }
    .vzx-sec + .vzx-sec { border-top: 3px solid var(--text-main); }
    .vzx-kicker {
      display: inline-block; font-weight: 900; font-size: .7rem;
      letter-spacing: .16em; text-transform: uppercase;
      background: var(--text-main); color: var(--bg-body);
      padding: .3rem .7rem; border-radius: .2rem;
    }
    .vzx-h { font-size: clamp(1.8rem, 3.8vw, 2.9rem); font-weight: 900; letter-spacing: -0.04em;
             margin: .8rem 0 .5rem; color: var(--text-main); }
    .vzx-sub { color: var(--text-muted); max-width: 58ch; font-weight: 500; }

    .vzx-step-n {
      width: 3rem; height: 3rem; border-radius: .5rem; display: grid; place-items: center;
      background: var(--accent-primary); color: var(--text-inverse);
      font-weight: 900; font-size: 1.15rem; border: 2px solid var(--text-main);
    }
    .vzx-track-row { border-bottom: 2px solid var(--border-subtle); }
    .vzx-track-row:hover { background: var(--accent-primary); }
    .vzx-track-row:hover .vzx-track-name,
    .vzx-track-row:hover .vzx-track-n,
    .vzx-track-row:hover .vzx-track-count { color: var(--text-inverse); }
    .vzx-bar { height: 10px; border-radius: 0; border: 2px solid var(--text-main); }
    .vzx-bar span { border-radius: 0; }
    .vzx-cta {
      border: 3px solid var(--text-main); border-radius: .8rem;
      box-shadow: 8px 8px 0 0 var(--accent-primary);
      background: var(--bg-surface);
    }
"""


VARIANTS = [
    {
        "slug": "forge",
        "name": "Forge",
        "blurb": "Dark and molten. The accent behaves like a light source: a "
                 "heat bloom behind the hero, glass cards that lift on hover.",
        "dark":  {"accent": "#fbbf24", "body": "#0b0805", "surface": "#17110a",
                  "text": "#fffbeb", "muted": "#fcd34d", "inverse": "#451a03",
                  "thumb": "#78350f"},
        "light": {"accent": "#b45309", "body": "#fffbeb", "surface": "#ffffff",
                  "text": "#451a03", "muted": "#57534e", "inverse": "#ffffff",
                  "thumb": "#fde68a"},
        "css": FORGE_CSS,
    },
    {
        "slug": "atlas",
        "name": "Atlas",
        "blurb": "Editorial. Serif headlines, hairline rules instead of boxes, "
                 "the track list set as an index. Quiet and confident.",
        "dark":  {"accent": "#f59e0b", "body": "#12100d", "surface": "#1a1712",
                  "text": "#faf7f0", "muted": "#c9bfae", "inverse": "#231a08",
                  "thumb": "#5b4420"},
        "light": {"accent": "#a16207", "body": "#faf7f0", "surface": "#fffdf8",
                  "text": "#1c1917", "muted": "#57534e", "inverse": "#ffffff",
                  "thumb": "#e7d9bd"},
        "css": ATLAS_CSS,
    },
    {
        "slug": "terminal",
        "name": "Terminal",
        "blurb": "Monospace throughout, square corners, bracketed labels. "
                 "Reads as a tool rather than a brochure.",
        "dark":  {"accent": "#f59e0b", "body": "#0a0a0a", "surface": "#111111",
                  "text": "#f5f5f4", "muted": "#a8a29e", "inverse": "#1c1917",
                  "thumb": "#44403c"},
        "light": {"accent": "#c2410c", "body": "#fafaf9", "surface": "#ffffff",
                  "text": "#1c1917", "muted": "#57534e", "inverse": "#ffffff",
                  "thumb": "#d6d3d1"},
        "css": TERMINAL_CSS,
    },
    {
        "slug": "kiln",
        "name": "Kiln",
        "blurb": "Warm paper, light first. Soft shapes, a lot of air, shadows "
                 "tinted brown rather than grey. The calm one.",
        "dark":  {"accent": "#f59e0b", "body": "#14100c", "surface": "#1d1811",
                  "text": "#fef6e7", "muted": "#d6c3a5", "inverse": "#2a1a05",
                  "thumb": "#6b4d22"},
        "light": {"accent": "#c2691a", "body": "#fdf8f1", "surface": "#ffffff",
                  "text": "#2a1a0d", "muted": "#6b5a4a", "inverse": "#ffffff",
                  "thumb": "#f2ddc2"},
        "css": KILN_CSS,
    },
    {
        "slug": "signal",
        "name": "Signal",
        "blurb": "High contrast and blocky. Hard borders, offset shadows, the "
                 "headline set in a solid amber slab. The loudest option.",
        "dark":  {"accent": "#f59e0b", "body": "#0c0a09", "surface": "#1c1917",
                  "text": "#fafaf9", "muted": "#d6d3d1", "inverse": "#1c1917",
                  "thumb": "#57534e"},
        "light": {"accent": "#ea8f0b", "body": "#fffdf7", "surface": "#ffffff",
                  "text": "#1c1917", "muted": "#44403c", "inverse": "#1c1917",
                  "thumb": "#e7e5e4"},
        "css": SIGNAL_CSS,
    },
]
