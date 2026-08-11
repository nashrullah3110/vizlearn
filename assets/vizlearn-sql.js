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

    var root = document.querySelector('[data-vz-sql]');
    if (!root) return;

    var editor = root.querySelector('.sql-editor');
    var runBtn = root.querySelector('.sql-run-btn');
    var resetBtn = root.querySelector('.sql-reset-btn');
    var status = root.querySelector('.sql-status');
    var result = root.querySelector('.sql-result');
    var schema = root.querySelector('.sql-schema');
    var seed = root.querySelector('.sql-seed');

    var SQL = null;      // the sql.js module
    var db = null;       // the live database
    var loading = null;  // in-flight load, so two clicks share one download

    function say(msg) { if (status) status.textContent = msg || ''; }

    function esc(s) {
        return String(s).replace(/[&<>"]/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
        });
    }

    function load() {
        if (SQL) return Promise.resolve(SQL);
        if (loading) return loading;
        say('Loading SQLite…');
        loading = new Promise(function (resolve, reject) {
            var tag = document.createElement('script');
            tag.src = SQL_URL + 'sql-wasm.js';
            tag.onload = resolve;
            tag.onerror = function () { reject(new Error('could not load sql.js')); };
            document.head.appendChild(tag);
        }).then(function () {
            return window.initSqlJs({ locateFile: function (f) { return SQL_URL + f; } });
        }).then(function (mod) {
            SQL = mod;
            return SQL;
        });
        return loading;
    }

    function fresh() {
        db = new SQL.Database();
        if (seed && seed.textContent.trim()) {
            try { db.run(seed.textContent); } catch (e) { /* seed is ours; ignore */ }
        }
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

    function drawSchema() {
        if (!schema || !db) return;
        var out = '';
        try {
            var res = db.exec(
                "SELECT name FROM sqlite_master WHERE type='table' " +
                "AND name NOT LIKE 'sqlite_%' ORDER BY name");
            var names = res.length ? res[0].values.map(function (r) { return r[0]; }) : [];
            if (!names.length) {
                schema.innerHTML = '<p class="sql-empty">No tables yet. ' +
                                   'Run a <code>CREATE TABLE</code> to make one.</p>';
                return;
            }
            names.forEach(function (n) {
                var info = db.exec('PRAGMA table_info(' + JSON.stringify(n) + ')');
                var count = db.exec('SELECT COUNT(*) FROM ' + JSON.stringify(n));
                var rows = count.length ? count[0].values[0][0] : 0;
                var cols = info.length ? info[0].values.map(function (c) {
                    return '<li><span class="sql-col">' + esc(c[1]) + '</span>' +
                           '<span class="sql-type">' + esc(c[2] || '') + '</span></li>';
                }).join('') : '';
                out += '<div class="sql-tbl">' +
                       '<div class="sql-tbl-head"><span class="sql-tbl-name">' + esc(n) + '</span>' +
                       '<span class="sql-tbl-rows">' + rows + (rows === 1 ? ' row' : ' rows') + '</span></div>' +
                       '<ul class="sql-cols">' + cols + '</ul></div>';
            });
            schema.innerHTML = out;
        } catch (e) {
            schema.innerHTML = '<p class="sql-empty">' + esc(e.message) + '</p>';
        }
    }

    // ------------------------------------------------------------------- run

    function run() {
        var sql = (editor.value || '').trim();
        if (!sql) { say('Nothing to run.'); return; }

        load().then(function () {
            if (!db) fresh();
            say('Running…');
            var t0 = performance.now();
            var out = '';
            try {
                // exec returns one result set per statement that produced rows.
                var sets = db.exec(sql);
                if (!sets.length) {
                    // DDL/DML: report what changed instead of an empty table.
                    var n = db.getRowsModified();
                    out = '<p class="sql-ok">Statement ran. ' +
                          (n ? n + (n === 1 ? ' row' : ' rows') + ' affected.' : 'No rows returned.') +
                          '</p>';
                } else {
                    out = sets.map(function (s) {
                        return table(s.columns, s.values) +
                               '<p class="sql-count">' + s.values.length +
                               (s.values.length === 1 ? ' row' : ' rows') + '</p>';
                    }).join('');
                }
                say('Ran in ' + Math.max(1, Math.round(performance.now() - t0)) + ' ms');
            } catch (e) {
                out = '<pre class="sql-error">' + esc(e.message) + '</pre>';
                say('Error');
            }
            result.innerHTML = out;
            drawSchema();
        }).catch(function (e) {
            result.innerHTML = '<pre class="sql-error">' + esc(e.message) + '</pre>';
            say('Could not start SQLite');
        });
    }

    runBtn.addEventListener('click', run);

    // Ctrl/Cmd+Enter runs, which is what every SQL client does.
    editor.addEventListener('keydown', function (e) {
        if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') { run(); e.preventDefault(); }
    });

    resetBtn.addEventListener('click', function () {
        load().then(function () {
            fresh();
            result.innerHTML = '';
            say('Database reset to the sample tables.');
            drawSchema();
        });
    });

    // Show the starting schema without making anyone press Run first.
    load().then(function () {
        fresh();
        say('Ready. Ctrl+Enter runs.');
        drawSchema();
    }).catch(function () {
        if (schema) {
            schema.innerHTML = '<p class="sql-empty">SQLite could not be loaded. ' +
                               'Check your connection and reload.</p>';
        }
    });
})();
