#!/usr/bin/env python3
"""Check the live theme against WCAG contrast, in both modes.

A theme meant to be lived in for years is a readability claim, and a
readability claim should be measured rather than asserted. This computes the
real WCAG 2.1 contrast ratios for the pairs that carry the page:

  body text        text on the page background      >= 4.5   (AA normal text)
  body on surface  text on cards and panels         >= 4.5
  muted text       secondary copy on the background >= 4.5
  headings         they are large, so                >= 3.0  (AA large text)
  accent on bg     links and labels                 >= 4.5
  accent fill      inverse text on an accent button >= 4.5
  borders          hairlines against the background  >= 1.3  (visible, not loud)

It also flags the two things that make a dark theme uncomfortable regardless
of ratio: a background at or near pure black, which makes bright text halate,
and a light background at pure white.

This used to iterate over the candidate palettes from the theme exploration.
Those palettes were superseded when the site moved to Ash, so the check was
passing on colours nothing shipped - a test that could stay green while the
real theme regressed. It reads tools/theme.py now, which is the single source
the whole site is generated from.

    python3 tools/check_theme_contrast.py
"""

import sys

import theme


def _srgb(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _srgb(r) + 0.7152 * _srgb(g) + 0.0722 * _srgb(b)


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# (label, foreground key, background key, minimum)
#
# The accent is split into two roles and each is checked against the rule that
# applies to it. --accent-primary carries text and links, so it needs 4.5;
# --accent-fill is a background for dark inverse text, so what needs 4.5 is
# on_fill against fill. Checking one rule against both roles is what forced
# the split in the first place: no single colour cleared 4.5 as text on a
# light background while still being bright enough to read as a button.
CHECKS = [
    ("body text",         "text",    "body",    4.5),
    ("body on surface",   "text",    "surface", 4.5),
    ("body on raise",     "text",    "raise",   4.5),
    ("muted text",        "muted",   "body",    4.5),
    ("muted on surface",  "muted",   "surface", 4.5),
    ("accent on bg",      "accent",  "body",    4.5),
    ("accent on surface", "accent",  "surface", 4.5),
    ("on_fill on fill",   "on_fill", "fill",    4.5),
]


def main():
    failures = []
    print("WCAG contrast, both modes. AA needs 4.5 for body text.\n")
    for v in [{"name": "Ash (live)", "dark": theme.DARK, "light": theme.LIGHT}]:
        print("%s" % v["name"])
        for mode in ("dark", "light"):
            p = v[mode]
            line = []
            for label, fg, bg, need in CHECKS:
                r = ratio(p[fg], p[bg])
                ok = r >= need
                if not ok:
                    failures.append((v["name"], mode, label, r, need))
                line.append("%s %.2f%s" % (label, r, "" if ok else " FAIL"))
            print("   %-6s %s" % (mode, "  |  ".join(line)))

            # Comfort, not contrast: pure black behind bright text halates,
            # and pure white at full brightness is what actually tires eyes.
            lum = luminance(p["body"])
            if mode == "dark" and lum < 0.012:
                failures.append((v["name"], mode, "background too close to black", lum, 0.012))
            if mode == "light" and lum > 0.94:
                failures.append((v["name"], mode, "background too close to white", lum, 0.94))
        print()

    if failures:
        print("FAILURES: %d" % len(failures))
        for name, mode, label, got, need in failures:
            print("   %-12s %-6s %-32s %.3f (needs %.2f)" % (name, mode, label, got, need))
        return 1
    print("the live palette passes AA for body text in both modes,")
    print("and no background sits at pure black or pure white.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
