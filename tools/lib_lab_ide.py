# -*- coding: utf-8 -*-
"""Split-pane markup shared by the four labs.

Each lab already emitted an editor and an output element as siblings inside
one container that its JavaScript binds to. This wraps them in two panes with
a separator between, without moving either out of that container - so
vizlearn-python.js and friends still find their editor and their console
exactly where they left them.

The separator carries the ARIA a real one needs. assets/vizlearn-ide.js gives
it drag, arrow keys, double-click-to-centre, and per-lab persistence.
"""

SPLIT = (
    '</div>\n'
    '                <div class="vz-ide-split" role="separator" tabindex="0"\n'
    '                     aria-orientation="vertical" aria-label="Resize editor and output"\n'
    '                     aria-valuemin="20" aria-valuemax="80" aria-valuenow="50"></div>\n'
    '                <div class="vz-ide-pane vz-ide-out">'
)

CODE_PANE = '<div class="vz-ide-pane vz-ide-code">'
CLOSE_PANE = '</div>'


def head(title, lead, prefix="../"):
    """The compact bar that replaces the usual hero block."""
    return (
        '        <div class="vz-lab-head">\n'
        '            <h1>%s</h1>\n'
        '            <p>%s</p>\n'
        '            <a class="vz-lab-home" href="%sindex.html">&larr; VizLearn</a>\n'
        '        </div>\n' % (title, lead, prefix)
    )
