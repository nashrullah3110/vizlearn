# -*- coding: utf-8 -*-
"""Frames for the /interview/ step player.

assets/vizlearn-interview.js draws whatever frames it is given; this is where
they come from. The rule the whole track depends on is that a frame set is
produced by *running* the algorithm and recording its state, never by writing
out what the algorithm is supposed to do. A page whose picture disagreed with
the interpreter underneath it would be worse than a page with no picture.

Content modules import the three primitives - `cell`, `row`, `frame` - and
write a short loop that mirrors the program in the editor. The patterns below
are the ones that came up often enough to be worth sharing.

Cell states, and the only ones the stylesheet knows:

    lo, hi   being looked at now
    hit      the answer, or a match
    done     settled: finished, correct, no longer changing
    dim      ruled out, or outside the current window
    bad      wrong, or about to be discarded
"""


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------

def cell(v, k=None, tag=None):
    out = {"v": v}
    if k:
        out["k"] = k
    if tag:
        out["tag"] = tag
    return out


def row(items, label=None, kind="cells", index=True):
    out = {"items": items}
    if label:
        out["label"] = label
    if kind != "cells":
        out["kind"] = kind
    if not index:
        out["index"] = False
    return out


def frame(rows, note, read=None):
    out = {"rows": rows if isinstance(rows, list) else [rows], "note": note}
    if read:
        out["read"] = {k: str(v) for k, v in read.items()}
    return out


def viz(frames, title=None, readouts=None):
    out = {"frames": frames}
    if title:
        out["title"] = title
    if readouts:
        out["readouts"] = readouts
    return out


def marked(values, marks=None, tags=None, kind="cells", label=None, index=True):
    """A row of `values` with `marks` = {position: state} applied."""
    marks = marks or {}
    tags = tags or {}
    items = [cell(v, marks.get(i), tags.get(i)) for i, v in enumerate(values)]
    return row(items, label=label, kind=kind, index=index)


def pairs(items, marks=None, label=None):
    """A key/value column - dictionaries, counters, tables."""
    marks = marks or {}
    cells = [cell("%s : %s" % (k, v), marks.get(k)) for k, v in items]
    return row(cells, label=label, kind="pairs", index=False)


# --------------------------------------------------------------------------
# Shared patterns
# --------------------------------------------------------------------------

def two_pointer_sum(values, target, label="sorted"):
    """Converging pointers on a sorted list, looking for a pair."""
    frames = []
    lo, hi = 0, len(values) - 1
    while lo < hi:
        total = values[lo] + values[hi]
        marks = {i: "dim" for i in range(len(values)) if i < lo or i > hi}
        marks[lo] = "lo"
        marks[hi] = "hi"
        tags = {lo: "lo", hi: "hi"}
        if total == target:
            marks[lo] = marks[hi] = "hit"
            frames.append(frame(
                marked(values, marks, tags, label=label),
                "%d + %d = %d. That is the target - done in %d step(s)."
                % (values[lo], values[hi], total, len(frames) + 1),
                {"lo": lo, "hi": hi, "sum": total}))
            return frames
        verdict = ("too small, so move lo right" if total < target
                   else "too big, so move hi left")
        frames.append(frame(
            marked(values, marks, tags, label=label),
            "%d + %d = %d, %s." % (values[lo], values[hi], total, verdict),
            {"lo": lo, "hi": hi, "sum": total}))
        if total < target:
            lo += 1
        else:
            hi -= 1
    frames.append(frame(marked(values, {i: "dim" for i in range(len(values))}, label=label),
                        "The pointers met with nothing found - no such pair exists.",
                        {"lo": lo, "hi": hi, "sum": 0}))
    return frames


def linear_scan(values, target, label="list"):
    """One comparison per item, left to right."""
    frames = []
    for i, v in enumerate(values):
        marks = {j: "dim" for j in range(i + 1, len(values))}
        for j in range(i):
            marks[j] = "bad"
        hit = v == target
        marks[i] = "hit" if hit else "lo"
        frames.append(frame(
            marked(values, marks, {i: "i"}, label=label),
            "Compare %s with %s - %s."
            % (v, target, "match, stop here" if hit else "no, keep going"),
            {"index": i, "comparisons": i + 1}))
        if hit:
            return frames
    frames.append(frame(
        marked(values, {i: "bad" for i in range(len(values))}, label=label),
        "Every item ruled out. A miss costs the full n - the worst case and the "
        "not-found case are the same case.",
        {"index": -1, "comparisons": len(values)}))
    return frames


def growing_window(text, label="text"):
    """The variable-size window: longest run with no repeated character."""
    frames = []
    seen = {}
    start = best = 0
    best_text = ""
    for i, ch in enumerate(text):
        jumped = ch in seen and seen[ch] >= start
        if jumped:
            start = seen[ch] + 1
        seen[ch] = i
        marks = {j: ("dim" if j < start or j > i else "lo") for j in range(len(text))}
        marks[i] = "hit"
        window = text[start:i + 1]
        if len(window) > best:
            best, best_text = len(window), window
        frames.append(frame(
            marked(list(text), marks, {start: "start", i: "i"},
                   kind="text", label=label),
            ("Repeat of %r inside the window, so the left edge jumps to %d. "
             "Window is now %r." % (ch, start, window)) if jumped else
            ("%r is new, so the window grows to %r." % (ch, window)),
            {"start": start, "i": i, "length": len(window), "best": best}))
    frames.append(frame(
        marked(list(text),
               {j: ("hit" if text[j:j + best] == best_text and j == text.find(best_text)
                    else "dim") for j in range(len(text))},
               kind="text", label=label),
        "Longest run with no repeat: %r, length %d. Every character was looked "
        "at once." % (best_text, best),
        {"start": start, "i": len(text) - 1, "length": best, "best": best}))
    return frames


def counter_fill(items, label="counts"):
    """A dictionary filling up as a sequence is walked."""
    frames = []
    counts = {}
    for i, item in enumerate(items):
        first = item not in counts
        counts[item] = counts.get(item, 0) + 1
        marks = {j: ("dim" if j > i else "done") for j in range(len(items))}
        marks[i] = "hit"
        frames.append(frame(
            [marked(items, marks, {i: "reading"}, label="input"),
             pairs(sorted(counts.items()), {item: "hit"}, label=label)],
            "%r is %s - one lookup and one write, whatever the dictionary "
            "already holds." % (item, "new, so add it" if first else
                                "already there, so bump it to %d" % counts[item]),
            {"seen": i + 1, "distinct": len(counts)}))
    return frames


def cost_table(rows, note, label="cost"):
    """A static comparison - two or three measured columns side by side.

    Used by the conceptual questions, where there is no pointer to move but
    there is still a number worth showing.
    """
    return [frame(pairs(rows, label=label), note)]
