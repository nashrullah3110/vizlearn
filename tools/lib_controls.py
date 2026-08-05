"""Read a module page's interactive controls out of its markup.

The visualisations are 166 independent hand-written pages with no shared
component layer, so there is no registry of "what can be changed on this
page". There is, however, a very consistent shape to the markup: a <label>
holding the human name, then the <input>/<select> it names.

This walks that shape and returns a normalised list, which is what lets the
lab features (executable experiments, predict-then-reveal) drive any page
without a per-page adapter.

Nothing here guesses. A control with no discoverable label is returned with an
empty label and the callers skip it, rather than inventing a name for it.
"""

import html
import re

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")

# How far back to look for the label that names a control.
LOOKBACK = 900

ATTR = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*"([^"]*)"')


def attrs(tag_text):
    return {k.lower(): v for k, v in ATTR.findall(tag_text)}


def text_of(fragment):
    """Visible text of a markup fragment: tags out, entities resolved."""
    # Drop inline SVG wholesale - every button on the site leads with one and
    # its <path d="..."> content is not text.
    fragment = re.sub(r"<svg\b.*?</svg>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    return WS.sub(" ", html.unescape(TAG.sub(" ", fragment))).strip()


# Every element that plausibly captions a control or a readout.
_LABEL_PATS = [
    re.compile(r"<label\b[^>]*>(.*?)</label>", re.S | re.I),
    re.compile(r"<h[2-6]\b[^>]*>([^<]*)</h[2-6]>", re.I),
    re.compile(r"<span\b[^>]*>([^<]*)</span>", re.I),
    re.compile(r"<div\b[^>]*>([^<]*)</div>", re.I),
    re.compile(r"<p\b[^>]*>([^<]*)</p>", re.I),
    re.compile(r"<strong\b[^>]*>([^<]*)</strong>", re.I),
    re.compile(r"<td\b[^>]*>([^<]*)</td>", re.I),
]


# The site's convention for a span that mirrors a control's current value:
# <span id="k-value">5</span> sitting between the label and the input. Those
# are the *value*, never the name, and being nearest they would otherwise win.
VALUE_MIRROR = re.compile(
    r'<(\w+)\b[^>]*\bid="[^"]*(?:-value|-val)"[^>]*>.*?</\1>', re.S | re.I)


def _label_before(src, pos):
    """The caption nearest to `pos`, searching backwards.

    Proximity decides, not tag type. An earlier version tried each tag kind in
    turn - labels, then headings, then spans - and returned the first kind it
    found anywhere in the window. That let a card's <h3> half a panel away beat
    the <span> sitting immediately beside the value, so a readout called
    "Accuracy" came back named "Fit Quality" after the section it lived in.

    The one exception is a span that mirrors the control's own value, which is
    nearer still and is never a name: "Cloud Tilt" would come back as "30" or
    "1.5x". Those are removed before proximity is judged.
    """
    window = VALUE_MIRROR.sub(" ", src[max(0, pos - LOOKBACK):pos])

    best = None   # (end offset within window, text)
    for pat in _LABEL_PATS:
        for m in pat.finditer(window):
            raw = m.group(1)
            # A <label> wrapping a radio or checkbox names that option rather
            # than the group it belongs to.
            if "<input" in raw.lower():
                continue
            t = text_of(raw)
            if not t or len(t) > 60:
                continue
            # Digits alone are a value being mirrored, not a name for one.
            if re.fullmatch(r"[\d.,%+\-/]+", t):
                continue
            if not _usable_label(t):
                continue
            if best is None or m.end() > best[0]:
                best = (m.end(), t)

    return best[1] if best else ""


def _clean_label(t):
    """Strip the leading numbering the SQL pages use ("1. Group By Column")."""
    return re.sub(r"^\s*\d+[.)]\s*", "", t).strip()


# Markup that is really source code caught mid-template, or a bare axis
# figure. Both slip past the length and digit filters and end up printed at
# the reader as a control name - one page offered the arrow keys a slider
# called "${inputs[i].toFixed(2)}", another one called "80k".
_NOT_A_NAME = re.compile(r"\$\{|\{\{|=>|function\s*\(|^\d+(\.\d+)?[kKmMxX%]?$")


def _usable_label(t):
    return bool(t) and not _NOT_A_NAME.search(t)


def _real_id(cid):
    """False for an id that is really a template still waiting to be filled.

    Five controls across four pages are rendered from a JS template literal
    whose placeholder survives into the static markup - `in-slider-${i}`,
    `w-${i}-${j}`. There is no element with that id at runtime, so anything
    built on one (a lab preset, an arrow-key target) silently does nothing.
    """
    return bool(cid) and "${" not in cid and "{{" not in cid


def controls(src):
    """Every addressable control on the page.

    Each entry is a dict with at least `id`, `kind` and `label`. Ranges also
    carry min/max/step/value; selects and radios carry `options` as a list of
    {value, label}; buttons carry their visible text.
    """
    out = []
    seen = set()

    # --- range / number / checkbox --------------------------------------
    for m in re.finditer(r"<input\b[^>]*>", src, re.I):
        a = attrs(m.group(0))
        kind = (a.get("type") or "text").lower()
        cid = a.get("id")

        if kind == "radio":
            continue  # handled as a group below
        if kind not in ("range", "checkbox", "number"):
            continue
        if not _real_id(cid) or cid in seen:
            continue
        seen.add(cid)

        entry = {"id": cid, "kind": kind,
                 "label": _clean_label(_label_before(src, m.start()))}
        if kind in ("range", "number"):
            entry.update({
                "min": a.get("min", ""),
                "max": a.get("max", ""),
                "step": a.get("step", "1"),
                "value": a.get("value", ""),
            })
        else:
            entry["value"] = "checked" in m.group(0).lower()
        out.append(entry)

    # --- select ----------------------------------------------------------
    for m in re.finditer(r"<select\b[^>]*>(.*?)</select>", src, re.S | re.I):
        a = attrs(m.group(0)[:m.group(0).find(">") + 1])
        cid = a.get("id")
        if not _real_id(cid) or cid in seen:
            continue
        seen.add(cid)

        options = []
        for om in re.finditer(r"<option\b([^>]*)>(.*?)</option>", m.group(1), re.S | re.I):
            oa = attrs("<option" + om.group(1) + ">")
            label = text_of(om.group(2))
            options.append({"value": oa.get("value", label), "label": label})
        out.append({
            "id": cid, "kind": "select",
            "label": _clean_label(_label_before(src, m.start())),
            "options": options,
        })

    # --- radio groups ----------------------------------------------------
    groups = {}
    for m in re.finditer(r'<input\b[^>]*type="radio"[^>]*>', src, re.I):
        a = attrs(m.group(0))
        name = a.get("name")
        if not name:
            continue
        g = groups.setdefault(name, {"pos": m.start(), "options": []})
        # The visible text sits in the <label> that wraps the radio.
        tail = src[m.end():m.end() + 300]
        stop = tail.lower().find("</label>")
        label = text_of(tail[:stop] if stop != -1 else tail[:120])
        g["options"].append({"value": a.get("value", ""), "label": label})

    for name, g in groups.items():
        key = "radio:" + name
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "id": name, "kind": "radio",
            "label": _clean_label(_label_before(src, g["pos"])),
            "options": g["options"],
        })

    # --- buttons ---------------------------------------------------------
    for m in re.finditer(r"<button\b([^>]*)>(.*?)</button>", src, re.S | re.I):
        a = attrs("<button" + m.group(1) + ">")
        cid = a.get("id")
        if not _real_id(cid) or cid in seen:
            continue
        # Site furniture, not part of the visualisation.
        if cid in ("themeToggle",) or "vz-" in (a.get("class") or ""):
            continue
        seen.add(cid)
        out.append({
            "id": cid, "kind": "button",
            "label": text_of(m.group(2)) or _clean_label(_label_before(src, m.start())),
        })

    return out


SITE_BUTTON_CLASSES = ("vz-", "vz-share", "vz-run")


def _viz_window(src):
    """The slice of a page between the site header and the site footer."""
    start = src.find("</header>")
    start = start + len("</header>") if start != -1 else src.find("<body")
    if start == -1:
        return ""

    end = src.find("<!-- VIZLEARN:FOOTER")
    if end == -1:
        end = src.find("<footer")
    if end == -1 or end <= start:
        end = len(src)
    return src[start:end]


def action_buttons(src):
    """The buttons that *drive* the visualisation, addressable by selector.

    `controls()` deliberately only returns buttons carrying an id, because the
    lab layer clicks them by id and an entry with `id: None` would break it.
    Eleven pages drive themselves off buttons that only ever had a class -
    `.viz-btn`, `.chip`, `.mode-btn` - and those pages ended up with no
    keyboard route in at all.

    This returns both kinds in document order as {label, sel, i}, where `sel`
    plus `i` resolve to exactly one element via querySelectorAll. An id
    becomes `#id` with i=0, so the runtime has a single code path.

    The window is everything between the header and the footer, not the
    contents of <main>: six pages close <main> before their interactive
    section starts (and one never closes it at all), so anchoring on <main>
    silently dropped them. Anchoring on the header/footer instead still
    excludes the site furniture - the theme toggle and share button live in
    the header - which is the only thing the narrower window was buying.
    """
    body = _viz_window(src)
    if not body:
        return []

    seen_class = {}
    out = []
    for m in re.finditer(r"<button\b([^>]*)>(.*?)</button>", body, re.S | re.I):
        a = attrs("<button" + m.group(1) + ">")
        cls = a.get("class") or ""
        if any(tok in cls for tok in SITE_BUTTON_CLASSES):
            continue
        if a.get("disabled") is not None and "disabled" in m.group(1).lower():
            continue

        label = text_of(m.group(2)) or a.get("aria-label") or ""
        label = _clean_label(label)
        if not label or len(label) > 40:
            continue

        cid = a.get("id")
        if cid:
            out.append({"label": label, "sel": "#" + cid, "i": 0})
            continue

        first = cls.split()[0] if cls.split() else ""
        if not first:
            continue
        # Index within its own class, which is how querySelectorAll will see it.
        i = seen_class.get(first, 0)
        seen_class[first] = i + 1
        out.append({"label": label, "sel": "." + first, "i": i})

    return out


def index_by_label(ctrls):
    """{normalised label: control} for the controls that have a usable name."""
    idx = {}
    for c in ctrls:
        if not c.get("label"):
            continue
        idx.setdefault(normalise(c["label"]), c)
    return idx


def normalise(s):
    """Lowercase, punctuation-free form used to match prose against labels."""
    s = html.unescape(s or "").lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return WS.sub(" ", s).strip()
