#!/usr/bin/env python3
"""Render /sql-lab/ - a SQL scratchpad backed by a real database.

The database track visualises what each clause does, but every one of those
pages simulates the engine. There was nowhere on the site to type
`CREATE TABLE` and have it mean anything.

This page runs actual SQLite (sql.js, compiled to WebAssembly) in the tab, via
assets/vizlearn-sql.js. The schema panel beside the editor is read back out of
`sqlite_master` after every statement, so it is the database's own account of
itself rather than a picture that has to be kept in sync.

Written whole on every build; no hand-edited regions.
"""

import sys

import lib_tool_page as tool

KEY = "sql-lab"

CSS = """
        .vz-sql-grid { display: grid; gap: 1.25rem; grid-template-columns: 1fr; }
        @media (min-width: 1024px) {
            /* Stretch, not start: the sidebar is much taller than the editor,
               and aligning to the top left a 451px void beside it. The editor
               column now fills the row and the result panel takes the slack,
               which is also where extra rows want to go. */
            .vz-sql-grid { grid-template-columns: minmax(0, 1fr) 18rem; align-items: stretch; }
            .vz-sql-editor-col { display: flex; flex-direction: column; }
            .vz-sql-editor-col .vz-console { flex: 1 1 auto; display: flex; flex-direction: column; }
            .vz-sql-editor-col .vz-console-body { flex: 1 1 auto; max-height: none; }
        }


        .sql-controls {
            display: flex; align-items: center; gap: 0.6rem;
            flex-wrap: wrap; margin: 0.75rem 0;
        }
        .sql-btn {
            font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;
            font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;
            padding: 0.7rem 1.1rem; border-radius: 9px; cursor: pointer;
            border: 1px solid var(--border-subtle);
            background: var(--input-bg); color: var(--text-main);
            min-height: 44px;
        }
        .sql-btn:hover { border-color: var(--accent-primary); }
        .sql-btn-primary {
            background: var(--accent-primary); color: var(--text-inverse);
            border-color: var(--accent-primary);
        }
        .sql-status {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem; color: var(--text-muted);
        }

        .sql-tablewrap { overflow-x: auto; border-radius: 8px; }
        .sql-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
        .sql-table th, .sql-table td {
            border: 1px solid var(--border-subtle);
            padding: 0.4rem 0.6rem; text-align: left; white-space: nowrap;
        }
        .sql-table th {
            background: var(--input-bg); color: var(--accent-primary);
            font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
            text-transform: uppercase; letter-spacing: 0.08em;
        }
        .sql-table td { color: var(--text-main); font-family: 'JetBrains Mono', monospace; }
        .sql-table td.is-null { color: var(--text-muted); font-style: italic; }

        .sql-count, .sql-ok {
            font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
            color: var(--text-muted); margin: 0.4rem 0 1rem;
        }
        .sql-error {
            font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
            color: #b91c1c; background: rgba(185, 28, 28, 0.07);
            border: 1px solid rgba(185, 28, 28, 0.3); border-left-width: 3px;
            border-radius: 8px; padding: 0.7rem 0.9rem; white-space: pre-wrap;
        }

        .vz-sql-side {
            border: 1px solid var(--border-subtle); border-radius: 12px;
            background: var(--card-bg); padding: 1rem 1.1rem;
        }
        .vz-sql-side + .vz-sql-side { margin-top: 1rem; }
        .vz-sql-side h2 {
            font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
            font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase;
            color: var(--accent-primary); margin-bottom: 0.6rem;
        }
        .vz-sql-side p, .vz-sql-side li { font-size: 0.85rem; line-height: 1.6; color: var(--text-muted); }
        .vz-sql-side ul { list-style: disc; padding-left: 1.15rem; display: grid; gap: 0.35rem; }
        .vz-sql-side a { color: var(--accent-primary); text-decoration: none; }
        .vz-sql-side a:hover { text-decoration: underline; }
        .vz-sql-side code {
            font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
            background: var(--input-bg); border: 1px solid var(--border-subtle);
            border-radius: 4px; padding: 0.05em 0.3em; color: var(--text-main);
        }

        .sql-tbl { margin-bottom: 0.9rem; }
        .sql-tbl-head {
            display: flex; justify-content: space-between; align-items: baseline;
            gap: 0.5rem; margin-bottom: 0.25rem;
        }
        .sql-tbl-name {
            font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
            font-weight: 700; color: var(--text-main);
        }
        .sql-tbl-rows { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: var(--text-muted); }
        .sql-cols { list-style: none; padding-left: 0.6rem; display: grid; gap: 0.15rem; }
        .sql-cols li { display: flex; justify-content: space-between; gap: 0.5rem; font-size: 0.76rem; }
        .sql-col { font-family: 'JetBrains Mono', monospace; color: var(--text-main); }
        .sql-type { font-family: 'JetBrains Mono', monospace; color: var(--text-muted); font-size: 0.7rem; }
        .sql-empty { font-size: 0.82rem; color: var(--text-muted); }
"""

# Two related tables, so a JOIN has something to join. Small enough to read in
# full, which matters when the point is seeing what the query did.
SEED = """CREATE TABLE artists (
  id      INTEGER PRIMARY KEY,
  name    TEXT NOT NULL,
  country TEXT
);

CREATE TABLE albums (
  id        INTEGER PRIMARY KEY,
  artist_id INTEGER REFERENCES artists(id),
  title     TEXT NOT NULL,
  year      INTEGER,
  sales     INTEGER
);

INSERT INTO artists (id, name, country) VALUES
  (1, 'Kate Bush',      'UK'),
  (2, 'Miles Davis',    'US'),
  (3, 'Fela Kuti',      'NG'),
  (4, 'Bjork',          'IS'),
  (5, 'Nina Simone',    NULL);

INSERT INTO albums (id, artist_id, title, year, sales) VALUES
  (1, 1, 'Hounds of Love',      1985, 1100000),
  (2, 1, 'The Dreaming',        1982,  320000),
  (3, 2, 'Kind of Blue',        1959, 5000000),
  (4, 2, 'Bitches Brew',        1970,  900000),
  (5, 3, 'Zombie',              1976,  450000),
  (6, 4, 'Homogenic',           1997,  980000),
  (7, 4, 'Vespertine',          2001,  760000),
  (8, 5, 'Pastel Blues',        1965,  210000);
"""

STARTER = """-- A real SQLite database, running in this tab.
-- CREATE and INSERT persist until you reload or press Reset.

SELECT a.name,
       COUNT(*)        AS albums,
       SUM(al.sales)   AS total_sales
FROM   artists a
JOIN   albums  al ON al.artist_id = a.id
GROUP  BY a.name
HAVING SUM(al.sales) > 500000
ORDER  BY total_sales DESC;
"""


def body():
    return """
        <div class="vz-sql-grid" data-vz-sql>
            <div class="vz-sql-editor-col">
                <script type="text/plain" class="sql-seed">%(seed)s</script>
                <div class="vz-code-bar">
                    <span class="vz-code-dot"></span><span>query.sql</span>
                    <span class="vz-code-lang">SQLite</span>
                </div>
                <!-- .sql-editor stays: assets/vizlearn-sql.js reads .value off it. -->
                <div class="vz-code" data-vz-code="sql">
                    <div class="vz-code-gutter" aria-hidden="true"></div>
                    <div class="vz-code-scroll">
                        <pre class="vz-code-hl" aria-hidden="true"></pre>
                        <textarea class="vz-code-input sql-editor" aria-label="SQL editor"
                                  spellcheck="false" autocapitalize="off"
                                  autocomplete="off">%(starter)s</textarea>
                    </div>
                </div>
                <div class="sql-controls">
                    <button type="button" class="sql-btn sql-btn-primary sql-run-btn"
                            aria-label="Run the SQL in the editor">Run</button>
                    <button type="button" class="sql-btn sql-reset-btn"
                            aria-label="Reset the database to the sample tables">Reset database</button>
                    <span class="sql-status" aria-live="polite"></span>
                </div>
                <div class="vz-console">
                    <div class="vz-console-bar">Result</div>
                    <div class="vz-console-body sql-result" aria-live="polite"
                         data-empty="Run a query to see rows here."></div>
                </div>
            </div>

            <div>
                <section class="vz-sql-side">
                    <h2>Tables</h2>
                    <div class="sql-schema"></div>
                </section>

                <section class="vz-sql-side">
                    <h2>Try</h2>
                    <ul>
                        <li><code>CREATE TABLE</code> your own, then insert into it &mdash; it
                            stays until you reload.</li>
                        <li>A <code>LEFT JOIN</code> from artists: Nina Simone has a NULL
                            country, so you can see how NULL behaves.</li>
                        <li><code>SELECT * FROM albums ORDER BY sales DESC LIMIT 3</code></li>
                        <li>A window function &mdash; <code>RANK() OVER (ORDER BY sales DESC)</code>.</li>
                    </ul>
                </section>

                <section class="vz-sql-side">
                    <h2>How it works</h2>
                    <p>This is SQLite compiled to WebAssembly. The database lives in memory
                    in this tab &mdash; nothing is uploaded, and a reload starts clean.</p>
                    <p><code>Ctrl</code>/<code>Cmd</code> + <code>Enter</code> runs.</p>
                </section>

                <section class="vz-sql-side">
                    <h2>Learning SQL?</h2>
                    <p>The <a href="%(p)sdatabase/">Databases &amp; SQL track</a> works through
                    the clauses in the order the engine actually applies them &mdash; which
                    explains most of the errors people hit. Start with
                    <a href="%(p)sdatabase/query_execution_order.html">query execution order</a>.</p>
                </section>
            </div>
        </div>

        <script src="%(p)sassets/vizlearn-sql.js" defer></script>
""" % {"seed": SEED.strip(), "starter": STARTER.strip(), "p": "%(p)s"}


def main():
    rel = tool.write(KEY, tool.render(KEY, CSS, body(), wide=True))
    print("sql lab page              : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
