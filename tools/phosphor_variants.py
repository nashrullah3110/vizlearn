# -*- coding: utf-8 -*-
"""Five Phosphor palettes, and the fixes that apply to all of them.

Phosphor was chosen, with six things to correct:

  1. the light mode's cream base was tiring over long sessions, so every
     light background here is a shade of white - neutral, warm or cool grey,
     no yellow cast anywhere
  2. the step numbers were undersized and sat off the heading baseline
  3. the page mixed three typefaces; it is now one
  4. the header looked soft, from a backdrop blur it did not need
  5. the radar was a picture; it is now something you can point at
  6. switching light/dark stuttered

On (6): index.html transitions background, border, colour and shadow on
`*, *::before, *::after` for 300ms. That is fine on a small page and not fine
on this one - toggling the theme starts a transition on every node in a
document holding 309 cards, and the browser has to interpolate all of them at
once. The fix is not a shorter duration; it is not transitioning the theme at
all. Colour changes are instant, and transitions are kept for the things a
pointer actually drives.

Light backgrounds sit between #f7 and #fc rather than at #fff: still white to
the eye, without the full-brightness page that causes the strain being avoided.
"""

MONO = ('ui-monospace, SFMono-Regular, "JetBrains Mono", "Cascadia Mono", '
        'Menlo, Consolas, "Liberation Mono", monospace')


# --------------------------------------------------------------------------
# Everything below applies to all five.
# --------------------------------------------------------------------------
FIXES_CSS = """
    /* ---- FIX 3: one typeface, everywhere -------------------------------
     * The hub set Space Grotesk on headings, Inter on body and a monospace
     * on chrome. A list of element selectors is not enough to replace them:
     * the typefaces are attached to classes - .brand-font, .nav-btn,
     * .viz-btn, .mono-font, Tailwind's .font-sans - and a class beats an
     * element, so the nav kept Space Grotesk on the first attempt. One rule
     * at full weight is the honest way to say "one typeface". Nothing here
     * depends on an icon font; every icon on the site is inline SVG, so
     * there is nothing for this to break. */
    *, *::before, *::after {
      font-family: var(--vz-mono) !important;
    }
    body {
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    /* ---- FIX 6: the theme switch is instant ----------------------------
     * Kill the blanket transition, then give it back only to the handful of
     * properties a pointer drives. Nothing animates on a theme change. */
    *, *::before, *::after {
      transition-property: none;
    }
    /* Only transform and opacity, deliberately. Colour and border-color are
     * exactly the properties a theme change alters, so transitioning them
     * means every card, link and button animates on the swap - 738 elements
     * on this page even after the blanket rule was removed. Hover colour
     * lands instantly instead, which suits the terminal look, and the swap
     * has nothing left to interpolate. */
    a, button, .vz-card, .vzx-panel, .vzx-btn, .vzx-r-node,
    .vz-chip, input, select, .vzx-track-row, .vzx-r-row {
      transition-property: transform, opacity;
      transition-duration: 140ms;
      transition-timing-function: cubic-bezier(.2, .8, .2, 1);
    }
    /* The hub attaches transitions to classes too - .card-title alone is 309
     * elements - and a class beats the universal selector above, so those
     * have to be named. a[class] outranks any single class, which covers the
     * anchors. */
    .card-title, .card-container, .course-wrapper, .nav-btn, .vz-rail-btn,
    .viz-btn, .vz-card-title, .theme-toggle, a[class] {
      transition-property: transform, opacity;
    }

    /* Belt and braces: the toggle adds this for one frame, so even a rule
     * added later cannot animate the swap. */
    html.vz-swapping *,
    html.vz-swapping *::before,
    html.vz-swapping *::after {
      transition: none !important;
      animation: none !important;
    }

    /* ---- FIX 4: the header is crisp ------------------------------------
     * backdrop-filter promotes the header to its own composited layer, which
     * on several GPUs drops subpixel antialiasing and softens every glyph in
     * it. The header sits on an opaque colour anyway, so the blur bought
     * nothing. The grey bar under the nav was its scrollbar. */
    .glass-header {
      backdrop-filter: none !important;
      -webkit-backdrop-filter: none !important;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-subtle);
    }
    #topic-nav { scrollbar-width: none; -ms-overflow-style: none; padding-bottom: .5rem; }
    #topic-nav::-webkit-scrollbar { display: none; height: 0; }
    .nav-scroll-fade { display: none !important; }
    /* Monospace sets wider than the sans it replaced, so twelve topics no
     * longer fit one row and the nav quietly scrolled - with the scrollbar
     * now hidden, "Featured" and "Interview" were simply cut off. From the
     * md breakpoint up it wraps instead, so nothing is ever off-screen;
     * below that it stays a swipe, which is the right gesture on a phone. */
    @media (min-width: 768px) {
      #topic-nav {
        flex-wrap: wrap;
        overflow-x: visible;
        justify-content: center;
        row-gap: .5rem;
      }
    }
    #topic-nav .nav-btn { font-size: .82rem; letter-spacing: -0.01em; }
    .glass-header, .glass-header * { text-rendering: optimizeLegibility; }

    /* The active topic pill: a flat, legible state rather than a glow. */
    #topic-nav .topic-btn.active,
    #topic-nav [aria-current="true"] {
      background: color-mix(in srgb, var(--accent-primary) 14%, transparent);
      border-color: var(--accent-primary);
      color: var(--accent-primary);
      box-shadow: none;
    }

    /* ---- Terminal chrome ------------------------------------------------ */
    .vz-card, .vzx-panel, .vzx-cta, .vzx-btn, .vz-chip, .vz-btn,
    button, input, select { border-radius: 4px !important; }

    #hero-intro { padding-top: 3.5rem; padding-bottom: 2.75rem; }
    #hero-intro h1 {
      font-weight: 700; letter-spacing: -0.02em;
      font-size: clamp(1.75rem, 4vw, 2.9rem); line-height: 1.18;
    }
    #hero-intro h1::before { content: "> "; color: var(--accent-primary); opacity: .55; }
    #hero-intro p { max-width: 66ch; line-height: 1.75; }

    .vz-card, .vzx-panel {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      box-shadow: none;
    }
    .vz-card:hover, .vzx-panel:hover {
      border-color: var(--accent-primary);
      background: var(--vz-raise);
    }
    .vz-card:hover { transform: translateY(-2px); }

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
    .vzx-sub { color: var(--text-muted); max-width: 68ch; line-height: 1.75; font-size: .95rem; }
    .vzx-step-p, .vzx-faq-a { line-height: 1.75; }

    /* ---- FIX 2: the step numbers ---------------------------------------
     * They were a 2.25rem outline box holding a small glyph, top-aligned
     * against a heading on a different baseline, so they read as stray
     * checkboxes. Now a filled tile whose height matches the heading's line
     * box, which puts the digit and the title on the same line. */
    .vzx-steps { gap: 2.25rem 2rem; }
    .vzx-step { gap: 1rem; align-items: flex-start; }
    .vzx-step-n {
      flex: 0 0 auto;
      width: 2rem; height: 2rem;
      display: inline-grid; place-items: center;
      background: color-mix(in srgb, var(--accent-primary) 16%, transparent);
      border: 1px solid color-mix(in srgb, var(--accent-primary) 42%, transparent);
      color: var(--accent-primary);
      font-weight: 700; font-size: .9rem; line-height: 1;
      font-variant-numeric: tabular-nums;
      border-radius: 4px;
    }
    .vzx-step-h {
      font-weight: 700; color: var(--text-main); font-size: 1rem;
      line-height: 2rem;      /* matches the tile, so both sit on one line */
      margin: 0 0 .3rem;
    }
    .vzx-step-p { color: var(--text-muted); font-size: .93rem; margin: 0; }

    .vzx-start-track::before { content: "["; opacity: .5; }
    .vzx-start-track::after  { content: "]"; opacity: .5; }
    .vzx-start-card:hover .vzx-start-go { color: var(--accent-primary); }

    .vzx-btn-solid { background: var(--accent-primary); color: var(--text-inverse); }
    .vzx-btn-ghost { border: 1px solid var(--border-subtle); color: var(--text-main); }
    .vzx-btn-ghost:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
    .vzx-cta { border: 1px solid var(--border-subtle); background: var(--bg-surface); }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { transition: none !important; animation: none !important; }
    }
"""


# accent / body / surface / raise / band / text / muted / inverse / thumb
VARIANTS = [
    {
        "slug": "bone",
        "name": "Bone",
        "blurb": "Neutral off-white and warm charcoal. The straight reading of "
                 "the brief: the amber is the only colour on the page.",
        "dark": {"accent": "#e8a33d", "body": "#1f1d1b", "surface": "#272423",
                 "raise": "#2f2b29", "band": "#232120", "text": "#f0ece6",
                 "muted": "#bab3a9", "inverse": "#1f1d1b", "thumb": "#4a4542"},
        "light": {"accent": "#9a5410", "body": "#f6f6f4", "surface": "#fdfdfc",
                  "raise": "#eeedea", "band": "#f2f1ef", "text": "#2b2926",
                  "muted": "#57534e", "inverse": "#ffffff", "thumb": "#d6d3d1"},
    },
    {
        "slug": "ash",
        "name": "Ash",
        "blurb": "Cool grey-white over graphite. The least warm of the five - "
                 "pick this if warm greys are what tire you.",
        "dark": {"accent": "#eaa94a", "body": "#1c1e1f", "surface": "#242728",
                 "raise": "#2c3031", "band": "#202324", "text": "#eceef0",
                 "muted": "#b0b6ba", "inverse": "#1c1e1f", "thumb": "#454b4e"},
        "light": {"accent": "#8f5410", "body": "#f3f5f6", "surface": "#fcfdfd",
                  "raise": "#e9ecee", "band": "#eef1f2", "text": "#22262a",
                  "muted": "#4e565c", "inverse": "#fdfdfd", "thumb": "#ced4d7"},
    },
    {
        "slug": "copper",
        "name": "Copper",
        "blurb": "Deeper, redder accent on a soft white. Reads as a warmer "
                 "terminal without the background carrying any of the warmth.",
        "dark": {"accent": "#dd8f4a", "body": "#201c1a", "surface": "#292422",
                 "raise": "#322c29", "band": "#241f1d", "text": "#f0e9e3",
                 "muted": "#bdb0a6", "inverse": "#201c1a", "thumb": "#4d4441"},
        "light": {"accent": "#a04b17", "body": "#f7f5f3", "surface": "#fdfcfb",
                  "raise": "#efece9", "band": "#f3f1ee", "text": "#2c2724",
                  "muted": "#5a524c", "inverse": "#ffffff", "thumb": "#d8d3ce"},
    },
    {
        "slug": "quartz",
        "name": "Quartz",
        "blurb": "Blue-tinted white over slate. The coolest background here, "
                 "which makes the amber sit forward more than in the others.",
        "dark": {"accent": "#e5a53f", "body": "#1b1e21", "surface": "#232629",
                 "raise": "#2b2f33", "band": "#1f2225", "text": "#e9edf1",
                 "muted": "#adb6bf", "inverse": "#1b1e21", "thumb": "#414a52"},
        "light": {"accent": "#8e5512", "body": "#f2f5f7", "surface": "#fcfdfe",
                  "raise": "#e7ebef", "band": "#edf1f4", "text": "#1f242a",
                  "muted": "#4b545d", "inverse": "#ffffff", "thumb": "#ccd3da"},
    },
    {
        "slug": "linen",
        "name": "Linen",
        "blurb": "The softest contrast of the five, for high screen "
                 "brightness. Still clears AA, with the edges dialled down.",
        "dark": {"accent": "#edaa4e", "body": "#222220", "surface": "#2b2a28",
                 "raise": "#333230", "band": "#262624", "text": "#eeeae4",
                 "muted": "#b7b2aa", "inverse": "#222220", "thumb": "#4e4c48"},
        "light": {"accent": "#96551a", "body": "#f8f7f5", "surface": "#fefdfc",
                  "raise": "#f0efec", "band": "#f4f3f1", "text": "#33302c",
                  "muted": "#5e5952", "inverse": "#ffffff", "thumb": "#dad7d3"},
    },
]


def tokens(p, mode):
    dark = mode == "dark"
    a = p["accent"]
    return {
        "--vz-mono": MONO,
        "--vz-raise": p["raise"],
        "--vz-band": p["band"],

        "--bg-body": p["body"],
        "--bg-surface": p["surface"],
        "--bg-glass": p["surface"],

        "--border-subtle": "color-mix(in srgb, %s %s, transparent)" % (a, "26%" if dark else "30%"),
        "--border-glow": "color-mix(in srgb, %s 50%%, transparent)" % a,

        "--accent-primary": a,
        "--accent-glow": "color-mix(in srgb, %s 20%%, transparent)" % a,

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

        "--grid-color": "color-mix(in srgb, %s %s, transparent)" % (a, "6%" if dark else "8%"),
        "--vignette-color": "transparent",
    }


def css(v):
    def rules(sel, mode):
        t = tokens(v[mode], mode)
        return "    %s {\n%s\n    }" % (
            sel, "\n".join("      %s: %s;" % kv for kv in t.items()))
    return "%s\n\n%s" % (rules(":root", "dark"), rules("body.light-mode", "light"))
