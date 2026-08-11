"""Hand-written entries for /whats-new/.

Module additions are *not* listed here. Those are derived from git in
build_whats_new.py, from the same first_published() the article dates already
use, so a new module appears on the page the moment it is committed and can
never drift from what actually shipped.

What cannot be derived is everything that is not a module: the features, the
site-wide fixes, the infrastructure. Those go here, newest first.

Each entry is (date, title, [lines]).
"""

CHANGES = [
    ("2026-08-11", "JavaScript and HTML labs", [
        "A JavaScript compiler at /js-lab/ runs on your browser's own engine, "
        "in a worker thread, with the console mirrored back into the page.",
        "An HTML playground at /html-lab/ renders your markup and inline "
        "scripts in a sandboxed preview, with console output shown below it.",
        "Both run entirely offline - no interpreter to download, nothing "
        "uploaded - joining the Python compiler and SQL playground.",
    ]),
    ("2026-08-05", "Bookmarks, notes, a glossary and a print stylesheet", [
        "Bookmark any module from its header, with a note if you want one, and "
        "read them all back on /saved/. Stored in your browser only.",
        "A glossary of 49 terms at /glossary/, and a definition card on the "
        "first mention of each term in any article.",
        "Printing a module now gives you a clean study sheet instead of a "
        "near-black page: no header, no rail, no dead widgets, and the check "
        "answers unfolded.",
        "Keyboard access finished. 52 modules had no keyboard route at all - "
        "the ones driven by buttons, checkboxes or number fields rather than "
        "sliders. Now 223 of 225 do.",
        "Fixed: the arrow-key hint was invisible on every canvas-driven "
        "module, because it was being appended inside the <canvas>.",
    ]),
    ("2026-08-03", "Practice mode, shareable state, and an installable app", [
        "Practice at /practice/ draws questions from the modules you have "
        "opened, weighted by what you got wrong and how long ago.",
        "Every module's controls are now in its URL, so you can link someone "
        "to exactly the state you are looking at.",
        "VizLearn is installable and works offline.",
        "The visualisations became keyboard-operable.",
    ]),
    ("2026-08-01", "Topic landing pages and the lab layer", [
        "Each track got its own page at /<track>/ instead of only existing as "
        "a fragment of the hub.",
        "Every module gained a runnable experiment, a predict-then-reveal "
        "step, and a check at the end.",
        "about, contact, privacy and terms.",
    ]),
]
