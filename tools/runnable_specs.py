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


def _matplotlib_prelude():
    """Pick a backend that works in a worker, and pay the import up front.

    Pyodide ships a matplotlib backend that draws into the page, which cannot
    work here: the runner executes in a Web Worker with no DOM. AGG renders to
    an in-memory buffer instead, which is what the runner then encodes as a
    PNG.

    Importing pyplot here rather than in the reader's code moves its cost -
    seconds, the first time - into the load budget rather than the run one,
    which is the same reason the FastAPI track imports its app in a prelude.
    """
    return (
        "import matplotlib\n\n"
        "matplotlib.use(\"AGG\")\n\n"
        "import matplotlib.pyplot as plt\n"
    )


def _pandas_prelude():
    """Silence the pyarrow DeprecationWarning pandas raises on import.

    Under Pyodide, "import pandas" warns that pyarrow will be required in
    pandas 3.0. It is accurate, irrelevant here, and written to stderr - so
    without this it is the first thing, in red, in every editor's output on
    the track.

    The filter matches that one message and is left installed, rather than
    wrapping the import in catch_warnings: exiting that context invalidates
    the per-module registry that stops a warning being shown twice, so the
    warning came back the moment the reader imported pandas themselves.

    Matching one message rather than ignoring DeprecationWarning wholesale
    keeps the reader's own warnings visible, which several modules rely on.
    """
    return (
        "import warnings\n\n"
        "warnings.filterwarnings(\n"
        "    \"ignore\", message=\"(?s).*Pyarrow will become a required.*\")\n\n"
        "import pandas\n"
    )


def _sklearn_prelude():
    """Pay scikit-learn's import cost during page load rather than on Run.

    Measured in a Pyodide worker on this runner: the interpreter takes ~6s, the
    wheels ~8s cold and almost nothing warm, and importing numpy and sklearn a
    further ~12s. Fitting a model, once all of that has happened, takes 47
    milliseconds - so the whole cost is startup, and the runner already shows a
    loading state while a prelude runs, which makes the prelude the right place
    for it.

    Two things are deliberately left out. The estimators: `from
    sklearn.linear_model import LinearRegression` belongs in the reader's editor
    where they can see it, and costs ~1.5s once per page.

    And pandas. It is in the packages list, so it is downloaded and importable,
    but importing it here measured at another ~7s on every page in the track -
    on top of 33s - when only the preprocessing modules use it. Left out, those
    modules pay it on their own first Run and the rest of the track does not pay
    it at all. The pyarrow filter still has to be installed here, before any
    import of pandas anywhere, which is why it stays even though pandas does
    not: warning filters are global and outlive this prelude.
    """
    return (
        "import warnings\n\n"
        "warnings.filterwarnings(\n"
        "    \"ignore\", message=\"(?s).*Pyarrow will become a required.*\")\n\n"
        "import numpy\n"
        "import sklearn\n"
    )


SPECS = {
    "sklearn": {
        # scikit-learn ships with Pyodide, so this is a CDN fetch rather than a
        # wheel - and scikit-learn brings numpy, scipy, joblib and openblas
        # with it. See _sklearn_prelude for what that costs and why pandas is here.
        "packages": "scikit-learn,pandas",
        "label": "scikit-learn",
        "filename": "example_%02d.py",
        "prelude": _sklearn_prelude,
    },
    "matplotlib": {
        # matplotlib ships with Pyodide, so this is a CDN fetch rather than a
        # wheel. numpy comes with it and is used throughout the track.
        #
        # pandas is here for one module - df.plot and where it stops being
        # enough. That is a whole extra package on every page of the track,
        # which I refused for the numpy track's pandas tangent; the
        # difference is that df.plot is how most people actually reach
        # matplotlib, so the module is core rather than an aside.
        "packages": "matplotlib,numpy,pandas",
        "label": "matplotlib",
        "filename": "example_%02d.py",
        "prelude": _matplotlib_prelude,
    },
    "pandas": {
        # pandas ships with Pyodide, so this is a CDN fetch rather than a wheel.
        "packages": "pandas",
        "label": "pandas",
        "filename": "example_%02d.py",
        "prelude": _pandas_prelude,
    },
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
