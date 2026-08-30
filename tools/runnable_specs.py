# -*- coding: utf-8 -*-
"""How a ```lang-run fence renders, per track.

The Pydantic and FastAPI articles carry their examples inline: the reader
meets a program at the point the prose introduces it, and can run it there.
That needs three things the article file cannot know on its own - which
Pyodide packages to load, which wheels to install, and whether any setup code
has to run first - so they live here, keyed by the track's directory.

prose.py reads this at import. Adding a track is one entry.
"""


def _fastapi_prelude():
    """The FastAPI lab's test client, imported rather than copied.

    /fastapi-lab/, the /fastapi/ track and these inline editors all need the
    same client, and three copies of it would drift.
    """
    from build_fastapi_lab import PRELUDE
    return PRELUDE + "\n\ndrive = _drive\n"


SPECS = {
    "numpy": {
        # numpy ships with Pyodide, so this is a CDN fetch rather than a wheel.
        "packages": "numpy",
        "label": "NumPy",
        "filename": "example_%02d.py",
    },
    "pydantic": {
        "packages": "pydantic,ssl",
        "label": "Pydantic",
        "filename": "example_%02d.py",
    },
    "interview": {
        # Plain Python: no third-party imports anywhere in the track, so
        # there is nothing to load and the first Run only waits for the
        # interpreter.
        "packages": "",
        "label": "Python",
        "filename": "%s",
    },
    "fastapi": {
        "packages": "pydantic,ssl",
        "wheels": ",".join("../assets/wheels/" + w for w in [
            "sniffio-1.3.1-py3-none-any.whl",
            "anyio-4.6.2.post1-py3-none-any.whl",
            "starlette-0.41.3-py3-none-any.whl",
            "fastapi-0.115.6-py3-none-any.whl",
            # Form and file endpoints refuse to start without it, and the
            # error names the package rather than the endpoint, so it is
            # loaded for the whole track rather than one module.
            "python_multipart-0.0.32-py3-none-any.whl",
        ]),
        "label": "FastAPI",
        "filename": "example_%02d.py",
        "prelude": _fastapi_prelude,
    },
}


def resolve():
    """SPECS with any callable prelude evaluated."""
    out = {}
    for track, spec in SPECS.items():
        spec = dict(spec)
        if callable(spec.get("prelude")):
            spec["prelude"] = spec["prelude"]()
        out[track] = spec
    return out
