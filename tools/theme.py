# -*- coding: utf-8 -*-
"""The site's theme, in one place.

Ash: a cool grey-white page over graphite, with amber as the only colour.
Chosen after a palette round and a layout round; see git history for the
alternatives.

Two things here are worth knowing before editing.

**The accent has two roles.** `--accent-primary` is only ever text on the page
background, so it has to clear 4.5:1 and is therefore dark in light mode.
`--accent-fill` is what the accent *fills* - buttons, badges, the chart's area
- and stays bright, because its contrast comes from the dark `--on-accent`
text sitting on top of it. Using one colour for both is what produced a muddy
brown button carrying its label at about 2.5:1.

**Nothing is pure black or pure white.** Pure black behind bright text
halates; a full-brightness white page is the other half of the eye strain.
The dark base is a raised graphite and the light base sits just under white.

tools/check_theme_contrast.py measures both modes and fails on a regression.
"""

MONO = ('ui-monospace, SFMono-Regular, "JetBrains Mono", "Cascadia Mono", '
        'Menlo, Consolas, "Liberation Mono", monospace')

DARK = {
    "accent": "#eaa94a",
    "fill": "#eaa94a", "fill_hi": "#f2b661", "on_fill": "#1c1e1f",
    "body": "#1c1e1f", "surface": "#242728", "raise": "#2c3031", "band": "#202324",
    "text": "#eceef0", "muted": "#b0b6ba", "inverse": "#1c1e1f", "thumb": "#454b4e",
}

LIGHT = {
    "accent": "#8f5410",
    "fill": "#e0982f", "fill_hi": "#cf8a26", "on_fill": "#20242a",
    "body": "#f3f5f6", "surface": "#fcfdfd", "raise": "#e9ecee", "band": "#eef1f2",
    "text": "#22262a", "muted": "#4e565c", "inverse": "#fcfdfd", "thumb": "#ced4d7",
}


def tokens(mode):
    """Every custom property the theme owns, for one mode."""
    p = DARK if mode == "dark" else LIGHT
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

        # Page-local surfaces some modules declare. Kept here so a module that
        # sets its own canvas does not fall back to the old green scheme.
        "--canvas-bg": p["body"] if dark else p["surface"],
        "--code-bg": p["raise"],
        "--stat-bg": p["raise"],
        "--stat-border": "color-mix(in srgb, %s 26%%, transparent)" % a,
    }


# Literal colours from the old green theme, and what each becomes. Applied to
# every inline <style> so no page keeps a green that the tokens no longer
# explain. Ordered longest-first so a prefix never eats a longer match.
GREEN_MAP = [
    ("rgba(74, 222, 128,", "rgba(234, 169, 74,"),
    ("rgba(74,222,128,", "rgba(234,169,74,"),
    ("rgba(34, 197, 94,", "rgba(217, 154, 60,"),
    ("rgba(34,197,94,", "rgba(217,154,60,"),
    ("rgba(22, 163, 74,", "rgba(143, 84, 16,"),
    ("rgba(22,163,74,", "rgba(143,84,16,"),
    ("rgba(21, 128, 61,", "rgba(143, 84, 16,"),
    ("rgba(240, 253, 244,", "rgba(243, 245, 246,"),
    ("#4ade80", "#eaa94a"),
    ("#22c55e", "#d99a3c"),
    ("#16a34a", "#b0762a"),
    ("#15803d", "#8f5410"),
    ("#14532d", "#454b4e"),
    ("#bbf7d0", "#ced4d7"),
    ("#dcfce7", "#e9ecee"),
    ("#86efac", "#b0b6ba"),
    ("#f0fdf4", "#f3f5f6"),
    ("#052e16", "#1c1e1f"),
    ("#04140a", "#20242a"),
]
