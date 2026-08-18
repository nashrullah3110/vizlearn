# -*- coding: utf-8 -*-
"""The finalised Ash theme for the hub.

Ash was chosen, then Minimal out of the five arrangements, so what is left
here is one theme rather than a set. The other four layouts are gone; the
constants they used (BRIEF, SPLIT, CONSOLE, LEDGER) are kept below because
they are the record of what was tried, and re-adding one is a single line in
VARIANTS.

**Two accent roles.** One colour was doing two jobs. `--accent-primary` has to
clear 4.5:1 against the page for links and labels, which in light mode forces
it down to a dark brown - and `.vz-cta-primary` then *filled* with it and put
near-black text on top, so the most prominent control on the page carried its
label at about 2.5:1. Now `--accent-primary` is only ever text on the page
background, and `--accent-fill` is what the accent fills, which stays a bright
amber because its contrast comes from the dark `--on-accent` text on it.
Measured at 6.46:1 light and 8.19:1 dark. The blurred halo under the button
goes with it: coloured blur under a saturated fill is a steady cost to read.

**The opening.** The three-card intro band and the "New here?" note are
removed - the whole `<section class="vz-intro-band">`, since its heading only
existed to introduce those cards.

**The order.** Four blocks of prose used to sit between the hero and the
modules, so the page opened with reading and kept the interactive part for
the end. Only the six start-here cards are above the rails now; the chart,
the three steps and the questions follow them. That leaves about seventy
words before the first thing you can click, and spreads the reading down the
page instead of stacking it at the top.
"""

from phosphor_variants import FIXES_CSS as PHOSPHOR_FIXES, MONO  # noqa: F401

# --------------------------------------------------------------------------
# Shared: the colour-role fix, plus the calmer treatments it enables.
# --------------------------------------------------------------------------
ASH_FIXES = """
    /* ---- Two accent roles ------------------------------------------------
     * Text-on-page needs 4.5:1 and therefore a dark accent; a filled control
     * needs contrast against its own fill, not against the page, so it can
     * stay bright. Filling with the text colour was what produced the brown
     * slab. */
    .vz-cta-primary,
    .vzx-btn-solid,
    .bg-brand-400, .bg-green-400, .bg-green-500 {
      background: var(--accent-fill) !important;
      color: var(--on-accent) !important;
      box-shadow: none !important;      /* the halo made it harder to read */
      border-color: var(--accent-fill) !important;
    }
    .vz-cta-primary:hover, .vzx-btn-solid:hover {
      background: var(--accent-fill-hi) !important;
      box-shadow: none !important;
    }
    .vz-cta-primary svg, .vzx-btn-solid svg { color: var(--on-accent); }

    /* The step tile and the radar dot are fills too, not text. */
    .vzx-step-n {
      background: color-mix(in srgb, var(--accent-fill) 20%, transparent);
      border-color: color-mix(in srgb, var(--accent-fill) 55%, transparent);
      color: var(--accent-primary);
    }
    .vzx-r-area { fill: color-mix(in srgb, var(--accent-fill) 26%, transparent);
                  stroke: var(--accent-fill); }
    .vzx-r-dot  { fill: var(--accent-fill); }

    /* Nothing on the page glows. Coloured blur under text or a control is a
     * steady low-level cost to read past. */
    [class*="shadow-[0_0_"], .vz-cta, .vz-tool-link, .vz-chip { box-shadow: none !important; }

    /* Links carry the readable accent, never the fill. */
    a { color: inherit; }
    .vz-tool-link:hover, .vzx-r-table a:hover { color: var(--accent-primary); }

    /* The hero band the intro cards used to sit under is gone; close the gap
     * it leaves rather than leaving a hole above the first section. */
    #hero-intro { padding-bottom: 1.5rem; }
    nav[aria-label="Study tools"] { padding-top: 1.25rem; padding-bottom: 2.5rem; }

    /* Stats strip: quieter by default in every variant.
     * Selected on border-brand-400/10, which appears exactly once on the
     * page. The obvious choice, bg-brand-400/5, is also on the "Welcome to
     * VizLearn" badge, and using it put the badge in the wrong grid column
     * and straight through the stats panel. */
    #hero-intro [class*="border-brand-400/10"] {
      background: transparent !important;
      border-color: var(--border-subtle) !important;
    }
"""


# --------------------------------------------------------------------------
# Per-variant: how the opening is arranged.
# --------------------------------------------------------------------------
BRIEF = """
    #hero-intro { padding-top: 2.75rem; padding-bottom: 1rem; }
    #hero-intro h1 { font-size: clamp(1.6rem, 3.4vw, 2.5rem); margin-bottom: .6rem; }
    #hero-intro p { font-size: .95rem; margin-bottom: 1.5rem; }
    /* The stats stop being a boxed panel and become one line of text. */
    #hero-intro [class*="border-brand-400/10"] {
      border: 0 !important; padding: 0 !important; gap: 1.25rem !important;
      font-size: .78rem; opacity: .8;
    }
    nav[aria-label="Study tools"] { padding-top: .75rem; padding-bottom: 2rem; }
    .vz-tool-link { font-size: .78rem; padding: .35rem .7rem; }
"""

SPLIT = """
    @media (min-width: 1024px) {
      /* The hero is a centred flex column in the markup. Turning it into a
       * grid is not enough on its own: its children are block-level and will
       * stretch to fill their cell, which is what ballooned the badge and the
       * stats panel on the first attempt. Each child has to be told to size
       * to its content and sit at the start of the column. */
      #hero-intro {
        display: grid !important;
        grid-template-columns: minmax(0, 1.4fr) minmax(18rem, 1fr);
        column-gap: 3.5rem;
        row-gap: 1rem;
        align-content: center;
        justify-items: start;
        text-align: left;
        padding-top: 3.5rem;
        padding-bottom: 2rem;
      }
      #hero-intro > * {
        justify-self: start;
        width: auto;
        max-width: 100%;
        margin-left: 0 !important;
        margin-right: 0 !important;
        text-align: left;
      }
      /* Auto-placement fills row by row, so without this the headline lands
       * in the second column and collides with the stats panel spanning it.
       * Everything except the stats belongs in column one. */
      #hero-intro > *:not([class*="border-brand-400/10"]) { grid-column: 1; }
      #hero-intro h1 { font-size: clamp(2rem, 3.2vw, 2.9rem); }
      #hero-intro p { max-width: 46ch; }
      /* The buttons row is centred in the markup too. */
      #hero-intro > div:has(.vz-cta) { justify-content: flex-start !important; }
      /* The numbers take the second column and sit alongside everything
       * else rather than adding another full-width row. */
      #hero-intro [class*="border-brand-400/10"] {
        grid-column: 2;
        grid-row: 1 / -1;
        align-self: center;
        justify-self: stretch;
        flex-direction: column;
        align-items: flex-start !important;
        justify-content: center !important;
        gap: 1rem !important;
        padding: 1.5rem !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 4px;
      }
    }
"""


CONSOLE = """
    /* The hero reads as a window: one bordered surface with the numbers
     * along its foot, which is the terminal idiom the type already implies. */
    #hero-intro {
      max-width: min(var(--vz-page, 1600px), 68rem);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      background: var(--bg-surface);
      padding: 3rem 2rem 0;
      margin-top: 2.5rem;
      position: relative;
      overflow: hidden;
    }
    #hero-intro::after {
      content: "vizlearn — 309 modules";
      position: absolute; top: 0; left: 0; right: 0;
      padding: .45rem .9rem;
      font-size: .68rem; letter-spacing: .14em; text-transform: uppercase;
      color: var(--text-muted);
      background: var(--vz-raise);
      border-bottom: 1px solid var(--border-subtle);
      text-align: left;
    }
    #hero-intro > :first-child { margin-top: 1.25rem; }
    #hero-intro [class*="border-brand-400/10"] {
      margin: 2rem -2rem 0 !important;
      border: 0 !important;
      border-top: 1px solid var(--border-subtle) !important;
      border-radius: 0 !important;
      padding: .9rem 1rem !important;
      background: var(--vz-band) !important;
      font-size: .8rem;
    }
"""

MINIMAL = """
    #hero-intro { padding-top: 5rem; padding-bottom: 2rem; }
    #hero-intro h1 { font-size: clamp(1.9rem, 4.4vw, 3.2rem); margin-bottom: 1rem; }
    #hero-intro p { font-size: 1rem; margin-bottom: 2rem; }
    /* The secondary button and the stats panel step back: one obvious action,
     * with the rest available but not competing for the same attention. */
    #hero-intro .vz-cta-ghost { border: 0; background: none; text-decoration: underline;
                                text-underline-offset: 4px; }
    #hero-intro [class*="border-brand-400/10"] {
      border: 0 !important; padding: 0 !important;
      font-size: .76rem; opacity: .7; gap: 1rem !important;
    }
    nav[aria-label="Study tools"] { padding-top: .5rem; padding-bottom: 3rem; opacity: .85; }
    .vz-tool-link { border: 0; font-size: .78rem; text-decoration: underline;
                    text-underline-offset: 3px; padding: .25rem .45rem; }
"""

LEDGER = """
    #hero-intro { padding-top: 3rem; padding-bottom: 1rem; }
    /* The four numbers become a real four-up, ruled like the rest of the
     * page, rather than a soft pill. */
    #hero-intro [class*="border-brand-400/10"] {
      display: grid !important;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 11rem), 1fr));
      gap: 0 !important;
      border: 1px solid var(--border-subtle) !important;
      border-radius: 4px !important;
      padding: 0 !important;
      overflow: hidden;
      max-width: 52rem;
      margin-left: auto; margin-right: auto;
    }
    #hero-intro [class*="border-brand-400/10"] > * {
      padding: .95rem 1rem;
      border-right: 1px solid var(--border-subtle);
      justify-content: center;
    }
    #hero-intro [class*="border-brand-400/10"] > *:last-child { border-right: 0; }
    .vz-tool-link { border-radius: 3px; font-size: .8rem; }
"""


VARIANTS = [
    {"slug": "minimal", "name": "Minimal",
     "blurb": "Headline, lede, one button, then straight into the modules. "
              "The explanatory sections sit below the rails rather than in "
              "front of them.",
     "layout": MINIMAL},
]


# One palette - Ash - across all five.
PALETTE = {
    "dark": {
        # Readable on the page (links, labels, headings).
        "accent": "#eaa94a",
        # Filled controls. Bright, with dark text on top.
        "fill": "#eaa94a", "fill_hi": "#f2b661", "on_fill": "#1c1e1f",
        "body": "#1c1e1f", "surface": "#242728", "raise": "#2c3031", "band": "#202324",
        "text": "#eceef0", "muted": "#b0b6ba", "inverse": "#1c1e1f", "thumb": "#454b4e",
    },
    "light": {
        "accent": "#8f5410",
        "fill": "#e0982f", "fill_hi": "#cf8a26", "on_fill": "#20242a",
        "body": "#f3f5f6", "surface": "#fcfdfd", "raise": "#e9ecee", "band": "#eef1f2",
        "text": "#22262a", "muted": "#4e565c", "inverse": "#fcfdfd", "thumb": "#ced4d7",
    },
}


def tokens(mode):
    p = PALETTE[mode]
    dark = mode == "dark"
    a = p["accent"]
    return {
        "--vz-mono": MONO,
        "--vz-raise": p["raise"],
        "--vz-band": p["band"],

        "--bg-body": p["body"],
        "--bg-surface": p["surface"],
        "--bg-glass": p["surface"],

        "--border-subtle": "color-mix(in srgb, %s %s, transparent)" % (a, "26%" if dark else "34%"),
        "--border-glow": "color-mix(in srgb, %s 50%%, transparent)" % a,

        "--accent-primary": a,
        "--accent-fill": p["fill"],
        "--accent-fill-hi": p["fill_hi"],
        "--on-accent": p["on_fill"],
        "--accent-glow": "transparent",

        "--text-main": p["text"],
        "--text-muted": p["muted"],
        "--text-placeholder": p["muted"],
        "--text-inverse": p["on_fill"],

        "--card-bg": p["surface"],
        "--card-icon-bg": "color-mix(in srgb, %s 10%%, transparent)" % a,
        "--input-bg": p["raise"],
        "--input-focus-bg": "color-mix(in srgb, %s 12%%, transparent)" % a,

        "--scrollbar-track": p["body"],
        "--scrollbar-thumb": p["thumb"],

        "--grid-color": "color-mix(in srgb, %s %s, transparent)" % (a, "6%" if dark else "8%"),
        "--vignette-color": "transparent",
    }


def css(_variant=None):
    def rules(sel, mode):
        return "    %s {\n%s\n    }" % (
            sel, "\n".join("      %s: %s;" % kv for kv in tokens(mode).items()))
    return "%s\n\n%s" % (rules(":root", "dark"), rules("body.light-mode", "light"))
