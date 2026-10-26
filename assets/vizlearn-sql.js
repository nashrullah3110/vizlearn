/* In-browser SQL for /sql-lab/.
 *
 * Real SQLite (sql.js, the C library compiled to WebAssembly) running in the
 * page. The database lives in memory for the length of the visit: CREATE and
 * INSERT persist between runs, so a session builds up the way it would against
 * a real connection, and a reload starts clean.
 *
 * Unlike the Python runner this does not use a Web Worker. SQLite has no way
 * to spin forever on a well-formed statement the way a Python `while True`
 * can, so the timeout a worker buys is not worth the message-passing.
 *
 * A page may hold several blocks. The lesson's visualizer blocks share one
 * database; runnable prose examples opt into isolated databases so each
 * sample has a clean schema and does not disturb the visualization.
 *
 * Markup the page supplies:
 *
 *   <div data-vz-sql>
 *     <textarea class="sql-editor"></textarea>
 *     <button class="sql-run-btn">Run</button>
 *     <button class="sql-reset-btn">Reset</button>
 *     <span class="sql-status"></span>
 *     <div class="sql-result"></div>      results / errors land here
 *     <div class="sql-schema"></div>      live table list, redrawn after each run
 *   </div>
 *
 * The loader is lazy: nothing is fetched until the first Run, so the 1.2MB
 * wasm payload is not charged to anyone who does not use the page.
 */
(function () {
    'use strict';

    var SQL_URL = 'https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/';

    var roots = [].slice.call(document.querySelectorAll('[data-vz-sql]'));
    if (!roots.length) return;

    // The main lesson runner uses one shared seed. Runnable prose examples opt
    // into a separate seeded database so schemas cannot collide.
    var seed = document.querySelector('.sql-seed');

    var SQL = null;      // the sql.js module
    var db = null;       // the live database
    var loading = null;  // in-flight load, so two clicks share one download

    function esc(s) {
        return String(s).replace(/[&<>"]/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
        });
    }

    function load() {
        if (SQL) return Promise.resolve(SQL);
        if (loading) return loading;
        loading = new Promise(function (resolve, reject) {
            var tag = document.createElement('script');
            tag.src = SQL_URL + 'sql-wasm.js';
            tag.onload = resolve;
            tag.onerror = function () { reject(new Error('could not load sql.js')); };
            document.head.appendChild(tag);
        }).then(function () {
            return window.initSqlJs({ locateFile: function (f) { return SQL_URL + f; } });
        }).then(function (mod) { SQL = mod; return SQL; });
        return loading;
    }

    function fresh(root) {
        var isolated = root && root.hasAttribute('data-vz-sql-isolated');
        var activeDb = new SQL.Database();
        var activeSeed = isolated ? root.querySelector('.sql-seed') : seed;
        if (activeSeed && activeSeed.textContent.trim()) {
            try { activeDb.run(activeSeed.textContent); } catch (e) { /* seed is ours */ }
        }
        if (isolated) root.__vzSqlDb = activeDb;
        else db = activeDb;
        return activeDb;
    }

    function databaseFor(root) {
        if (root.hasAttribute('data-vz-sql-isolated')) {
            return root.__vzSqlDb || fresh(root);
        }
        return db || fresh();
    }

    function bindParameters(root) {
        var fields = root.querySelectorAll('.sql-param-input');
        if (!fields.length) return undefined;
        var positional = [], named = {};
        [].forEach.call(fields, function (field) {
            var name = field.getAttribute('data-sql-param');
            if (name === '?') positional.push(field.value);
            else named[name] = field.value;
        });
        return positional.length ? positional : named;
    }

    // ---------------------------------------------------------------- render

    function table(cols, rows) {
        var head = cols.map(function (c) { return '<th>' + esc(c) + '</th>'; }).join('');
        var body = rows.map(function (r) {
            return '<tr>' + r.map(function (v) {
                var isNull = v === null || v === undefined;
                return '<td' + (isNull ? ' class="is-null"' : '') + '>' +
                       (isNull ? 'NULL' : esc(v)) + '</td>';
            }).join('') + '</tr>';
        }).join('');
        return '<div class="sql-tablewrap"><table class="sql-table">' +
               '<thead><tr>' + head + '</tr></thead><tbody>' + body + '</tbody></table></div>';
    }

    // Shared lesson runners redraw every panel. Isolated prose examples only
    // redraw the schema panel inside their own editor.
    function drawSchema(root, activeDb) {
        var isolated = root && root.hasAttribute('data-vz-sql-isolated');
        var panels = isolated ? [root.querySelector('.sql-schema')] :
            [].filter.call(document.querySelectorAll('.sql-schema'), function (panel) {
                return !panel.closest('[data-vz-sql-isolated]');
            });
        panels = [].filter.call(panels, Boolean);
        if (!panels.length || !activeDb) return;
        var out = '';
        try {
            var res = activeDb.exec("SELECT name FROM sqlite_master WHERE type='table' " +
                              "AND name NOT LIKE 'sqlite_%' ORDER BY name");
            var names = res.length ? res[0].values.map(function (r) { return r[0]; }) : [];
            if (!names.length) {
                out = '<p class="sql-empty">No tables yet. Run a <code>CREATE TABLE</code> to make one.</p>';
            } else {
                names.forEach(function (n) {
                    var info = activeDb.exec('PRAGMA table_info(' + JSON.stringify(n) + ')');
                    var count = activeDb.exec('SELECT COUNT(*) FROM ' + JSON.stringify(n));
                    var rows = count.length ? count[0].values[0][0] : 0;
                    var cols = info.length ? info[0].values.map(function (c) {
                        return '<li><span class="sql-col">' + esc(c[1]) + '</span>' +
                               '<span class="sql-type">' + esc(c[2] || '') + '</span></li>';
                    }).join('') : '';
                    out += '<div class="sql-tbl">' +
                           '<div class="sql-tbl-head"><span class="sql-tbl-name">' + esc(n) + '</span>' +
                           '<span class="sql-tbl-rows">' + rows + (rows === 1 ? ' row' : ' rows') +
                           '</span></div><ul class="sql-cols">' + cols + '</ul></div>';
                });
            }
        } catch (e) {
            out = '<p class="sql-empty">' + esc(e.message) + '</p>';
        }
        [].forEach.call(panels, function (el) { el.innerHTML = out; });
    }


    /* Does the last statement in this script read rather than write?
     *
     * Comments and string literals both contain semicolons and keywords, so
     * they are skipped rather than matched against - a comment reading
     * "-- then DELETE the row" must not make this look like a write.
     */
    var QUERY_HEAD = /^(SELECT|WITH|VALUES|PRAGMA|EXPLAIN)\b/i;

    function lastIsQuery(sql) {
        var out = '', i = 0, ch, next;
        while (i < sql.length) {
            ch = sql[i]; next = sql[i + 1];
            if (ch === '-' && next === '-') {
                while (i < sql.length && sql[i] !== '\n') i++;
            } else if (ch === '/' && next === '*') {
                i += 2;
                while (i < sql.length && !(sql[i] === '*' && sql[i + 1] === '/')) i++;
                i += 2;
            } else if (ch === "'" || ch === '"') {
                var quote = ch;
                out += ' ';
                i++;
                while (i < sql.length) {
                    if (sql[i] === quote && sql[i + 1] === quote) { i += 2; continue; }
                    if (sql[i] === quote) { i++; break; }
                    i++;
                }
            } else {
                out += ch;
                i++;
            }
        }
        var parts = out.split(';').map(function (x) { return x.trim(); })
                       .filter(function (x) { return x.length; });
        if (!parts.length) return false;
        return QUERY_HEAD.test(parts[parts.length - 1]);
    }

    // ----------------------------------------------------------- one block

    function attach(root) {
        var editor = root.querySelector('.sql-editor');
        var runBtn = root.querySelector('.sql-run-btn');
        var resetBtn = root.querySelector('.sql-reset-btn');
        var status = root.querySelector('.sql-status');
        var result = root.querySelector('.sql-result');
        if (!editor || !runBtn || !result) return;

        function say(msg) { if (status) status.textContent = msg || ''; }

        function run() {
            var sql = (editor.value || '').trim();
            if (!sql) { say('Nothing to run.'); return; }
            say('Running…');
            load().then(function () {
                var activeDb = databaseFor(root);
                var t0 = performance.now(), out = '';
                try {
                    var sets = activeDb.exec(sql, bindParameters(root));
                    if (!sets.length) {
                        /* exec() returns no result sets both for a statement
                         * that changed rows and for a SELECT that matched
                         * none. getRowsModified() is sqlite3_changes, which
                         * reports the last MODIFYING statement - so on a
                         * no-match SELECT it happily reported rows affected
                         * by an INSERT from the seed script. A query that
                         * finds nothing has to say so. */
                        if (lastIsQuery(sql)) {
                            out = '<p class="sql-ok">0 rows.</p>';
                        } else {
                            var n = activeDb.getRowsModified();
                            out = '<p class="sql-ok">Statement ran. ' +
                                  (n ? n + (n === 1 ? ' row' : ' rows') + ' affected.' : 'No rows returned.') +
                                  '</p>';
                        }
                    } else {
                        out = sets.map(function (r) {
                            return table(r.columns, r.values) +
                                   '<p class="sql-count">' + r.values.length +
                                   (r.values.length === 1 ? ' row' : ' rows') + '</p>';
                        }).join('');
                    }
                    say('Ran in ' + Math.max(1, Math.round(performance.now() - t0)) + ' ms');
                } catch (e) {
                    out = '<pre class="sql-error">' + esc(e.message) + '</pre>';
                    say('Error');
                }
                result.innerHTML = out;
                drawSchema(root, activeDb);
            }).catch(function (e) {
                result.innerHTML = '<pre class="sql-error">' + esc(e.message) + '</pre>';
                say('Could not start SQLite');
            });
        }

        runBtn.addEventListener('click', run);
        // Shift+Enter and Cmd/Ctrl+Enter come from assets/vizlearn-code.js,
        // which owns the editor and dispatches vz-run. Handling the key here
        // as well meant two listeners on one textarea.
        root.addEventListener('vz-run', run);

        if (resetBtn) {
            resetBtn.addEventListener('click', function () {
                load().then(function () {
                    var activeDb = fresh(root);
                    result.innerHTML = '';
                    say('Database reset to the sample tables.');
                    drawSchema(root, activeDb);
                });
            });
        }

        return say;
    }

    var says = roots.map(attach).filter(Boolean);

    // Show the starting schema without making anyone press Run first.
    load().then(function () {
        fresh();
        roots.forEach(function (root) {
            if (root.hasAttribute('data-vz-sql-isolated')) fresh(root);
        });
        says.forEach(function (say) { say('Ready. Ctrl+Enter runs.'); });
        drawSchema(null, db);
        roots.forEach(function (root) {
            if (root.hasAttribute('data-vz-sql-isolated')) {
                drawSchema(root, root.__vzSqlDb);
            }
        });
    }).catch(function () {
        says.forEach(function (say) { say('SQLite could not be loaded.'); });
    });
})();
