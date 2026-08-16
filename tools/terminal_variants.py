# -*- coding: utf-8 -*-
"""Five terminal palettes, chosen for how they read over long sessions.

The brief was a terminal look whose dark mode is not a black hole and whose
light mode is not a page of white paper, comfortable enough to sit in for
years. That is not a new problem - it is the problem every serious terminal
theme has already solved - so these are built on the palettes that solved it
rather than on colours picked by eye:

  Phosphor    amber CRT, the Ember direction in terminal form
  Solarized   Ethan Schoonover's, designed around uniform perceived lightness
  Gruvbox     warm retro, low saturation, the most forgiving of the five
  Nord        cool arctic, the lowest contrast that still passes AA
  Catppuccin  soft pastel, the modern favourite for long sessions

None of them use #000 or #fff anywhere. Every dark base sits between #1a and
#2f luminance and every light base is tinted off-white, because pure black
behind bright text causes halation - the text appears to bleed - and pure
white at full screen brightness is what actually tires eyes.

Body-text contrast is verified against WCAG AA by tools/check_terminal_contrast.py;
do not hand-edit these without re-running it.

`mono_body` is a per-variant call, not an oversight. A terminal look wants
monospace, but monospace at paragraph length is measurably slower to read, so
three variants stay fully mono for authenticity and two use mono only for
chrome and headings. That is also part of what makes the five feel different.
"""

# --------------------------------------------------------------------------
# Shared terminal chrome. Every variant is this, wearing a different palette.
# --------------------------------------------------------------------------
TERMINAL_BASE = """
    /* Chrome, labels and headings are monospace in every variant. */
    #hero-intro h1, .vzx-h, .vzx-kicker, .vz-intro-title,
    .vzx-track-name, .vzx-track-count, .vzx-step-n, .vzx-start-track,
    .vzx-btn, .vz-chip, input, select, button {
      font-family: var(--vz-mono);
    }

    body { font-family: var(--vz-body); }

    /* Terminals do not round their corners. */
    .vz-card, .vzx-panel, .vzx-cta, .vzx-btn, .vz-chip, .vz-btn, button, input, select {
      border-radius: 3px !important;
    }

    #hero-intro { padding-top: 3.5rem; padding-bottom: 2.75rem; }
    #hero-intro h1 {
      font-weight: 700;
      letter-spacing: -0.02em;
      font-size: clamp(1.75rem, 4vw, 2.9rem);
      line-height: 1.15;
    }
    #hero-intro h1::before { content: "> "; color: var(--accent-primary); opacity: .55; }
    /* 66ch keeps the lede at a comfortable measure whatever the viewport. */
    #hero-intro p { max-width: 66ch; line-height: 1.7; }

    .vz-card, .vzx-panel {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      box-shadow: none;
      transition: border-color .18s ease, background .18s ease, transform .18s ease;
    }
    .vz-card:hover, .vzx-panel:hover {
      border-color: var(--accent-primary);
      background: var(--vz-raise);
    }
    .vz-card:hover { transform: translateY(-2px); }

    /* Sections breathe differently as you go down the page, so a long scroll
     * does not read as the same block repeated. */
    .vzx-sec { padding: 4.5rem 0; border-top: 1px solid var(--border-subtle); }
    .vzx-sec:nth-of-type(even) { background: var(--vz-band); }

    .vzx-kicker {
      font-size: .68rem; letter-spacing: .2em; text-transform: uppercase;
      color: var(--accent-primary); font-weight: 600;
    }
    .vzx-kicker::before { content: "// "; opacity: .5; }
    .vzx-h {
      font-size: clamp(1.4rem, 2.7vw, 2.05rem); font-weight: 700;
      letter-spacing: -0.015em; margin: .55rem 0 .6rem; color: var(--text-main);
    }
    /* 68ch for mono, which sets wider per character than the sans. */
    .vzx-sub { color: var(--text-muted); max-width: 68ch; line-height: 1.75; font-size: .95rem; }

    .vzx-step-p, .vzx-faq-a { line-height: 1.75; }

    .vzx-step-n {
      width: 2.25rem; height: 2.25rem; display: grid; place-items: center;
      border: 1px solid var(--accent-primary); color: var(--accent-primary);
      background: var(--vz-raise); font-weight: 700; font-size: .95rem;
    }

    .vzx-start-card:hover .vzx-start-go { color: var(--accent-primary); }
    .vzx-start-track::before { content: "["; opacity: .5; }
    .vzx-start-track::after  { content: "]"; opacity: .5; }

    .vzx-btn-solid { background: var(--accent-primary); color: var(--text-inverse); }
    .vzx-btn-ghost { border: 1px solid var(--border-subtle); color: var(--text-main); }
    .vzx-btn-ghost:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
    .vzx-cta { border: 1px solid var(--border-subtle); background: var(--bg-surface); }

    /* Motion stays small on purpose: a page you sit in for years should not
     * perform every time it is scrolled. */
    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; transition: none !important; }
    }
"""


VARIANTS = [
    {
        "slug": "phosphor",
        "name": "Phosphor",
        "blurb": "Amber CRT. The Ember direction rendered as a terminal - warm "
                 "charcoal rather than black, so the glow reads without halation.",
        "mono_body": True,
        "dark": {
            "accent": "#e8a33d", "body": "#221e1b", "surface": "#2a2523",
            "raise": "#2d2827", "band": "#201c1a",
            "text": "#f2e8dc", "muted": "#c4b5a4", "inverse": "#1c1917",
            "thumb": "#57534e", "grid": "#e8a33d",
        },
        "light": {
            "accent": "#a35a12", "body": "#faf6ef", "surface": "#fffdf9",
            "raise": "#f5ede0", "band": "#f6f1e8",
            "text": "#2e2622", "muted": "#5c5048", "inverse": "#fffdf9",
            "thumb": "#d6ccbc", "grid": "#a35a12",
        },
    },
    {
        "slug": "solarized",
        "name": "Solarized",
        "blurb": "Schoonover's palette, built so every colour holds the same "
                 "perceived lightness. The most restful of the five, and the "
                 "one that keeps a sans for body text.",
        "mono_body": False,
        "dark": {
            "accent": "#d59526", "body": "#002b36", "surface": "#073642",
            "raise": "#0b4553", "band": "#00323d",
            "text": "#eee8d5", "muted": "#93a1a1", "inverse": "#002b36",
            "thumb": "#586e75", "grid": "#cb8b19",
        },
        "light": {
            "accent": "#a55708", "body": "#fdf6e3", "surface": "#fffbf0",
            "raise": "#f4ecd8", "band": "#f7f0dd",
            "text": "#073642", "muted": "#586e75", "inverse": "#fdf6e3",
            "thumb": "#d9d2c0", "grid": "#a55708",
        },
    },
    {
        "slug": "gruvbox",
        "name": "Gruvbox",
        "blurb": "Warm retro, deliberately low saturation. Forgiving at high "
                 "screen brightness and the friendliest to read at night.",
        "mono_body": True,
        "dark": {
            "accent": "#d79921", "body": "#282828", "surface": "#32302f",
            "raise": "#3c3836", "band": "#2d2b2a",
            "text": "#f2e5bc", "muted": "#c8b899", "inverse": "#282828",
            "thumb": "#665c54", "grid": "#d79921",
        },
        "light": {
            "accent": "#8a5600", "body": "#fbf1c7", "surface": "#fdf8e3",
            "raise": "#f2e5bc", "band": "#f7edcf",
            "text": "#3c3836", "muted": "#5f5750", "inverse": "#fbf1c7",
            "thumb": "#d5c4a1", "grid": "#9d6404",
        },
    },
    {
        "slug": "nord",
        "name": "Nord",
        "blurb": "Cool arctic. The lowest-contrast option that still clears AA, "
                 "for anyone who finds warm palettes tiring. Sans body text.",
        "mono_body": False,
        "dark": {
            "accent": "#8fbcbb", "body": "#2e3440", "surface": "#3b4252",
            "raise": "#434c5e", "band": "#333a47",
            "text": "#eceff4", "muted": "#c3ccd9", "inverse": "#2e3440",
            "thumb": "#4c566a", "grid": "#88c0d0",
        },
        "light": {
            "accent": "#3f6f76", "body": "#eceff4", "surface": "#f7f9fb",
            "raise": "#e1e6ee", "band": "#e7ebf1",
            "text": "#2e3440", "muted": "#4c566a", "inverse": "#f7f9fb",
            "thumb": "#c7cedb", "grid": "#3f6f76",
        },
    },
    {
        "slug": "catppuccin",
        "name": "Catppuccin",
        "blurb": "Soft pastel on a muted plum base. The modern long-session "
                 "favourite: nothing in it is saturated enough to fatigue.",
        "mono_body": True,
        "dark": {
            "accent": "#f0b080", "body": "#1e1e2e", "surface": "#282839",
            "raise": "#313244", "band": "#232334",
            "text": "#e8e6f0", "muted": "#b8b5cc", "inverse": "#1e1e2e",
            "thumb": "#45475a", "grid": "#f0b080",
        },
        "light": {
            "accent": "#a05a2c", "body": "#eff1f5", "surface": "#fbfcfe",
            "raise": "#e6e9ef", "band": "#e9ecf1",
            "text": "#3c3f52", "muted": "#5c5f70", "inverse": "#fbfcfe",
            "thumb": "#ccd0da", "grid": "#a05a2c",
        },
    },
]


MONO_STACK = ('ui-monospace, SFMono-Regular, "JetBrains Mono", Menlo, '
              'Consolas, "Liberation Mono", monospace')
SANS_STACK = ('Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", '
              'Helvetica, Arial, sans-serif')


def tokens(p, mode, mono_body):
    """The full token set for one mode of one variant."""
    dark = mode == "dark"
    a = p["accent"]
    return {
        "--vz-mono": MONO_STACK,
        "--vz-body": MONO_STACK if mono_body else SANS_STACK,
        "--vz-raise": p["raise"],
        "--vz-band": p["band"],
        "--vz-grid-ink": p["grid"],

        "--bg-body": p["body"],
        "--bg-surface": p["surface"],
        "--bg-glass": p["surface"],

        "--border-subtle": "color-mix(in srgb, %s 22%%, transparent)" % a,
        "--border-glow": "color-mix(in srgb, %s 45%%, transparent)" % a,

        "--accent-primary": a,
        "--accent-glow": "color-mix(in srgb, %s 22%%, transparent)" % a,

        "--text-main": p["text"],
        "--text-muted": p["muted"],
        "--text-placeholder": p["muted"],
        "--text-inverse": p["inverse"],

        "--card-bg": p["surface"],
        "--card-icon-bg": "color-mix(in srgb, %s 10%%, transparent)" % a,
        "--input-bg": p["raise"],
        "--input-focus-bg": "color-mix(in srgb, %s 12%%, transparent)" % a,

        "--scrollbar-track": p["body"],
        "--scrollbar-thumb": p["thumb"],

        # The background grid is the one thing that reads as "terminal" at a
        # glance, so it stays - but faint enough not to sit under the text.
        "--grid-color": "color-mix(in srgb, %s %s, transparent)" % (a, "7%" if dark else "9%"),
        "--vignette-color": "transparent",
    }


def css(v):
    def rules(sel, mode):
        t = tokens(v[mode], mode, v["mono_body"])
        return "    %s {\n%s\n    }" % (
            sel, "\n".join("      %s: %s;" % kv for kv in t.items()))
    return "%s\n\n%s" % (rules(":root", "dark"), rules("body.light-mode", "light"))
