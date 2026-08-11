/* Syntax highlighting and a line-number gutter for the editor on /python-lab/
 * and /sql-lab/.
 *
 * A <textarea> cannot style its own contents, so this is the standard overlay:
 * a <pre> of highlighted markup sits directly under a textarea whose text is
 * transparent. The caret, selection, scrolling and every keystroke stay with
 * the real textarea - which matters, because the Python and SQL runners read
 * `.value` off it and must keep working untouched.
 *
 * The two layers only line up if their font metrics are identical. Font,
 * size, line-height, padding, letter-spacing and tab-size are all set from one
 * place in the stylesheet for that reason; changing one on the textarea alone
 * makes the highlight drift a character further out on every line.
 *
 * Markup the page supplies:
 *
 *   <div class="vz-code" data-vz-code="python">     (or "sql")
 *     <div class="vz-code-gutter" aria-hidden="true"></div>
 *     <div class="vz-code-scroll">
 *       <pre class="vz-code-hl" aria-hidden="true"></pre>
 *       <textarea class="vz-code-input py-editor"></textarea>
 *     </div>
 *   </div>
 *
 * The textarea keeps whatever class its runner looks for; this file never
 * renames it.
 */
(function () {
    'use strict';

    function esc(s) {
        return s.replace(/[&<>]/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c];
        });
    }

    // ------------------------------------------------------------ tokenisers
    //
    // One regex per language with named alternatives, applied left to right so
    // the first match wins. Order is the whole design: strings and comments
    // have to be tried before keywords, or the word "for" inside a string gets
    // highlighted as a keyword.

    var PY_KEYWORDS = ('False|None|True|and|as|assert|async|await|break|class|continue|def|del|' +
        'elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|' +
        'raise|return|try|while|with|yield|match|case').split('|');

    var PY_BUILTINS = ('abs|all|any|bool|dict|dir|enumerate|filter|float|format|frozenset|' +
        'getattr|hasattr|hash|id|input|int|isinstance|issubclass|iter|len|list|map|max|min|next|' +
        'object|open|ord|chr|pow|print|range|repr|reversed|round|set|setattr|slice|sorted|str|' +
        'sum|tuple|type|zip|super|self').split('|');

    var SQL_KEYWORDS = ('SELECT|FROM|WHERE|GROUP|BY|HAVING|ORDER|LIMIT|OFFSET|INSERT|INTO|' +
        'VALUES|UPDATE|SET|DELETE|CREATE|TABLE|VIEW|INDEX|DROP|ALTER|ADD|COLUMN|PRIMARY|KEY|' +
        'FOREIGN|REFERENCES|UNIQUE|NOT|NULL|DEFAULT|CHECK|JOIN|INNER|LEFT|RIGHT|FULL|OUTER|' +
        'CROSS|ON|USING|AS|AND|OR|IN|IS|LIKE|BETWEEN|EXISTS|CASE|WHEN|THEN|ELSE|END|UNION|ALL|' +
        'INTERSECT|EXCEPT|DISTINCT|WITH|RECURSIVE|OVER|PARTITION|ASC|DESC|CAST|BEGIN|COMMIT|' +
        'ROLLBACK|TRANSACTION|PRAGMA|IF|AUTOINCREMENT|CONSTRAINT|COLLATE|GLOB').split('|');

    var SQL_TYPES = ('INTEGER|INT|REAL|TEXT|BLOB|NUMERIC|VARCHAR|CHAR|BOOLEAN|DATE|DATETIME|' +
        'TIMESTAMP|DECIMAL|FLOAT|DOUBLE').split('|');

    var SQL_FUNCS = ('COUNT|SUM|AVG|MIN|MAX|ROUND|ABS|COALESCE|IFNULL|NULLIF|LENGTH|LOWER|' +
        'UPPER|TRIM|SUBSTR|REPLACE|ROW_NUMBER|RANK|DENSE_RANK|NTILE|LAG|LEAD|FIRST_VALUE|' +
        'LAST_VALUE|GROUP_CONCAT|STRFTIME|DATE|TOTAL').split('|');

    function wordSet(list) {
        var m = {};
        list.forEach(function (w) { m[w.toLowerCase()] = 1; });
        return m;
    }

    var PY_KW = wordSet(PY_KEYWORDS), PY_BI = wordSet(PY_BUILTINS);
    var SQL_KW = wordSet(SQL_KEYWORDS), SQL_TY = wordSet(SQL_TYPES), SQL_FN = wordSet(SQL_FUNCS);

    // Comments and strings first, then numbers, then bare words.
    var PY_RE = new RegExp([
        '(#[^\\n]*)',                                        // 1 comment
        '("""[\\s\\S]*?"""|\'\'\'[\\s\\S]*?\'\'\')',         // 2 triple string
        '([frbu]?"(?:\\\\.|[^"\\\\\\n])*"|[frbu]?\'(?:\\\\.|[^\'\\\\\\n])*\')', // 3 string
        '(\\b\\d[\\d_]*\\.?\\d*(?:[eE][+-]?\\d+)?\\b)',      // 4 number
        '(@[A-Za-z_][\\w]*)',                                // 5 decorator
        '\\b([A-Za-z_][\\w]*)\\b'                            // 6 word
    ].join('|'), 'g');

    var SQL_RE = new RegExp([
        '(--[^\\n]*|/\\*[\\s\\S]*?\\*/)',                    // 1 comment
        '(\'(?:\'\'|[^\'])*\'|"(?:[^"])*")',                 // 2 string / quoted ident
        '(\\b\\d+\\.?\\d*\\b)',                              // 3 number
        '\\b([A-Za-z_][\\w]*)\\b'                            // 4 word
    ].join('|'), 'g');

    function tag(cls, text) {
        return '<span class="t-' + cls + '">' + esc(text) + '</span>';
    }

    function highlightPython(src) {
        var out = '', last = 0, m;
        PY_RE.lastIndex = 0;
        while ((m = PY_RE.exec(src)) !== null) {
            out += esc(src.slice(last, m.index));
            if (m[1]) out += tag('com', m[1]);
            else if (m[2]) out += tag('str', m[2]);
            else if (m[3]) out += tag('str', m[3]);
            else if (m[4]) out += tag('num', m[4]);
            else if (m[5]) out += tag('dec', m[5]);
            else if (m[6]) {
                var w = m[6];
                // `def name` / `class Name`: colour the name, not just the keyword.
                var after = src.slice(m.index + w.length).match(/^\s*\(/);
                if (PY_KW[w]) out += tag('kw', w);
                else if (PY_BI[w]) out += tag('bi', w);
                else if (after) out += tag('fn', w);
                else out += esc(w);
            } else {
                out += esc(m[0]);
            }
            last = m.index + m[0].length;
        }
        return out + esc(src.slice(last));
    }

    function highlightSql(src) {
        var out = '', last = 0, m;
        SQL_RE.lastIndex = 0;
        while ((m = SQL_RE.exec(src)) !== null) {
            out += esc(src.slice(last, m.index));
            if (m[1]) out += tag('com', m[1]);
            else if (m[2]) out += tag('str', m[2]);
            else if (m[3]) out += tag('num', m[3]);
            else if (m[4]) {
                var w = m[4], k = w.toLowerCase();
                if (SQL_KW[k]) out += tag('kw', w);
                else if (SQL_TY[k]) out += tag('ty', w);
                else if (SQL_FN[k]) out += tag('fn', w);
                else out += esc(w);
            } else {
                out += esc(m[0]);
            }
            last = m.index + m[0].length;
        }
        return out + esc(src.slice(last));
    }

    var HIGHLIGHT = { python: highlightPython, sql: highlightSql };

    // ----------------------------------------------------------------- wiring

    function attach(wrap) {
        var lang = wrap.dataset.vzCode;
        var paint = HIGHLIGHT[lang];
        if (!paint) return;

        var ta = wrap.querySelector('.vz-code-input');
        var hl = wrap.querySelector('.vz-code-hl');
        var gutter = wrap.querySelector('.vz-code-gutter');
        if (!ta || !hl) return;

        var lastValue = null;
        var lastLines = -1;

        function render() {
            var v = ta.value;
            if (v === lastValue) return;
            lastValue = v;

            // The trailing newline matters: without it the last line of a
            // document that ends in \n has nothing to give the <pre> height,
            // and the highlight sits one line short of the caret.
            hl.innerHTML = paint(v) + '\n';

            if (gutter) {
                var n = v.split('\n').length;
                if (n !== lastLines) {
                    lastLines = n;
                    var rows = '';
                    for (var i = 1; i <= n; i++) rows += i + '\n';
                    gutter.textContent = rows;
                }
            }
        }

        function sync() {
            hl.scrollTop = ta.scrollTop;
            hl.scrollLeft = ta.scrollLeft;
            if (gutter) gutter.scrollTop = ta.scrollTop;
        }

        ta.addEventListener('input', function () { render(); sync(); });
        ta.addEventListener('scroll', sync);

        // The editor's contents are also set programmatically, and assigning
        // .value fires no event: the Python runner injects the starter from
        // .py-src after this file has already run, and both Reset buttons
        // rewrite it later. A document-wide click listener covered Reset but
        // not the initial fill, which left the first paint blank.
        //
        // One interval, one string compare per tick. Cheap enough to be
        // uninteresting, and it catches every writer without either file
        // needing to know about the other.
        var timer = setInterval(function () {
            if (ta.value !== lastValue) { render(); sync(); }
        }, 250);
        window.addEventListener('pagehide', function () { clearInterval(timer); });

        // Tab should indent, not leave the editor - it is a code box.
        ta.addEventListener('keydown', function (e) {
            if (e.key !== 'Tab' || e.shiftKey) return;
            e.preventDefault();
            var s = ta.selectionStart, t = ta.selectionEnd;
            ta.value = ta.value.slice(0, s) + '    ' + ta.value.slice(t);
            ta.selectionStart = ta.selectionEnd = s + 4;
            render(); sync();
        });

        render();
        sync();
    }

    document.querySelectorAll('[data-vz-code]').forEach(attach);
})();
