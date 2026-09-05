# -*- coding: utf-8 -*-
"""Runnable sections for the generated Python modules.

Every article on the site carries an editor that runs real CPython in the
browser through Pyodide; prose.py turns a ```python-run fence into one for
any track with an entry in runnable_specs. The thirty-four topics in
python_topics.TOPICS have their .txt regenerated at the start of every
build, so a fence added to the file is erased before anything reads it --
these sections are appended by slug instead, the same way python_extra.py
adds its prose.

Each snippet was run in Pyodide and its output read against the words
around it, so the numbers in the comments are the numbers the reader sees.

The other twelve python articles are ordinary prose files and carry their
fence directly.
"""

RUNNABLE = {}
