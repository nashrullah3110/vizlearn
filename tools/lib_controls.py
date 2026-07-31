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


def _label_before(src, pos):
    """The nearest <label> (or small heading) text that precedes `pos`."""
    window = src[max(0, pos - LOOKBACK):pos]

    # A <label> that closes before the control is the strongest signal.
    labels = re.findall(r"<label\b[^>]*>(.*?)</label>", window, re.S | re.I)
    for raw in reversed(labels):
        t = text_of(raw)
        # A label wrapping a radio/checkbox names the option, not the group.
        if t and "<input" not in raw.lower() and 1 <= len(t) <= 60:
            return t

    # Then any small text element that closes just before the control. Many
    # panels caption their readouts with a plain <div> or <p> rather than a
    # <label>, so leaving those out loses most of the good names.
    for pat in (r"<h[2-6]\b[^>]*>([^<]*)</h[2-6]>",
                r"<span\b[^>]*>([^<]*)</span>",
                r"<div\b[^>]*>([^<]*)</div>",
                r"<p\b[^>]*>([^<]*)</p>",
                r"<strong\b[^>]*>([^<]*)</strong>"):
        found = re.findall(pat, window, re.I)
        for raw in reversed(found):
            t = text_of(raw)
            # Digits alone are a value being mirrored, not a name for one.
            if t and 2 <= len(t) <= 60 and not re.fullmatch(r"[\d.,%+-]+", t):
                return t
    return ""


def _clean_label(t):
    """Strip the leading numbering the SQL pages use ("1. Group By Column")."""
    return re.sub(r"^\s*\d+[.)]\s*", "", t).strip()


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
        if not cid or cid in seen:
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
        if not cid or cid in seen:
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
        if not cid or cid in seen:
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
