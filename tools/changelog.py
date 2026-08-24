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
    ("2026-08-24", "Sixty modules across Computer Vision, Databases and machine learning", [
        "Computer Vision gained the classical floor it never had - convolution "
        "kernels you edit by hand, thresholding, histograms, the "
        "Gaussian/median/bilateral comparison, morphology, colour spaces, "
        "interpolation and affine transforms - and then the modern half: "
        "separable and dilated convolutions, anchor boxes, mAP, template "
        "matching, Harris corners, ViT patching, Grad-CAM and the "
        "semantic/instance/panoptic distinction.",
        "The database track picked up schema design and concurrency - keys, "
        "constraints, EXISTS against IN against JOIN, recursive CTEs, query "
        "plans, covering indexes, isolation levels and deadlocks - then scale "
        "and safety: MVCC, partitioning, sharding, replication lag, CAP, the "
        "document and graph models, columnar storage, star schemas and "
        "parameterised queries.",
        "Machine learning gained the workflow around the algorithms it already "
        "had: scaling, leakage, missing values, outliers, pipelines, the "
        "precision/recall family, threshold tuning and learning curves, then "
        "DBSCAN, hierarchical clustering, choosing k, Gaussian mixtures, "
        "embeddings, permutation importance, SHAP, calibration, isolation "
        "forests and ensembles.",
        "Every number on those pages is computed in your browser from data "
        "generated in your browser. The leakage module really does fit a "
        "scaler on the whole dataset and really does report the inflated score "
        "that follows; the calibration slider really does leave AUC untouched "
        "while wrecking the probabilities.",
    ]),
    ("2026-08-21", "Longer articles everywhere, and the labs documented", [
        "Every article on the site now runs to full length. The interview "
        "track had been quietly losing its written answers on every build - "
        "the generator ran after the article writer and overwrote it - which "
        "is fixed, and the 34 generated Python modules were expanded to match "
        "the hand-written ones.",
        "The four labs - Python, SQL, JavaScript and HTML - now explain how "
        "each runtime works, what it supports, the errors you will actually "
        "hit and what is worth trying, rather than being an editor with a "
        "sentence above it.",
        "Article prose is set in a proportional face at a comfortable reading "
        "measure, code inside articles sits in real code blocks, and the "
        "column widths were rebalanced so the text is not swimming in space.",
    ]),
    ("2026-08-18", "A new theme, and split-pane labs", [
        "The whole site moved to the Ash palette, chosen for long reading "
        "sessions in either mode: no yellow cast in light mode, nothing "
        "pure-black in dark, and a single accent split into two roles so text "
        "and fills can each meet contrast on their own terms.",
        "The four labs became genuine split-pane editors - code on one side, "
        "output on the other, with a divider you can drag, nudge with the "
        "arrow keys or reset with a double-click. The position is remembered "
        "per lab.",
        "The Python track grew from twelve modules to forty-six, covering the "
        "things a beginner meets in the first week and the generator gaps "
        "above them.",
    ]),
    ("2026-08-14", "An interview track, and runnable code inside the articles", [
        "A tenth track at /interview/ answers one interview question per page. "
        "Each has a step-through visualiser you drive yourself, the full "
        "solution in an editor you can run and edit, and questions at the end.",
        "Algorithm modules now carry a working Python program alongside the "
        "animation, annotated line by line, so the thing you just watched and "
        "the thing you can run are on the same page.",
        "The retrieval and evaluation articles in Gen AI got interactive "
        "panels of their own - chunkers, indexes, rankers and the metrics that "
        "score them, each with parameters you can move and a readout that "
        "explains what moved.",
        "Reader-facing counts are derived from the catalog now rather than "
        "typed in, so the site stops claiming a module total it outgrew.",
    ]),
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
