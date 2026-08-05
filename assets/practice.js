/* Practice mode.
 *
 * Every module ends with a check, and the answers have been accumulating in
 * localStorage for as long as the lab layer has existed - but only ever on the
 * page they came from. This turns those isolated checks into a study system:
 * questions are drawn from the modules you have actually opened, weighted by
 * what you got wrong and how long ago you saw it.
 *
 * The question bank is generated at build time into practice-bank.js, from the
 * same authored questions and page-derived recall cards the modules carry, so
 * a question here can never drift from the module it belongs to.
 *
 * Nothing leaves the browser. No account, no backend.
 */
(function () {
  'use strict';

  var BANK = window.VIZLEARN_PRACTICE || [];
  var PROGRESS_KEY = 'vizlearn_progress';
  var CHECK_KEY = 'vizlearn_checks';
  var PRACTICE_KEY = 'vizlearn_practice';
  var DAY = 24 * 60 * 60 * 1000;

  // --- storage -------------------------------------------------------------

  function read(key) {
    try { return JSON.parse(localStorage.getItem(key)) || {}; }
    catch (e) { return {}; }
  }
  function write(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); }
    catch (e) { /* private browsing - the session still works, it just forgets */ }
  }

  function daysSince(iso) {
    if (!iso) return null;
    var t = Date.parse(iso);
    if (isNaN(t)) return null;
    return (Date.now() - t) / DAY;
  }

  // --- selection -----------------------------------------------------------

  /* One weight per module. Higher means more likely to be asked.
   *
   * Everything here is deliberately additive rather than multiplicative: a
   * module you got wrong once should come back sooner, not dominate the deck
   * forever, and a module you have never been asked about should not be
   * unreachable just because it is fresh in memory. */
  function weightFor(mod, checks, practice) {
    var w = 1;

    var c = checks[mod.path];
    if (c && c.total) {
      var missed = 1 - (c.score || 0) / c.total;
      w += missed * 2.5;                       // what you got wrong on the page
    }

    var p = practice[mod.path];
    if (p && p.asked) {
      var rate = 1 - (p.right || 0) / p.asked;
      w += rate * 2.5;                         // what you have got wrong here
      var d = daysSince(p.at);
      if (d !== null) w += Math.min(1, d / 14) * 1.5;   // and how long ago
    } else {
      w += 1.2;                                // never practised: worth asking
    }

    var seen = daysSince(mod.visitedAt);
    if (seen !== null) w += Math.min(1, seen / 30) * 0.8;

    return w;
  }

  function pickWeighted(pool, n) {
    var chosen = [];
    var rest = pool.slice();
    while (chosen.length < n && rest.length) {
      var total = rest.reduce(function (a, m) { return a + m.weight; }, 0);
      var r = Math.random() * total;
      var idx = 0;
      for (; idx < rest.length; idx++) {
        r -= rest[idx].weight;
        if (r <= 0) break;
      }
      if (idx >= rest.length) idx = rest.length - 1;
      chosen.push(rest[idx]);
      rest.splice(idx, 1);                     // no module asked twice in one round
    }
    return chosen;
  }

  /* "track:Deep Learning" -> "Deep Learning", else null. The track name is
   * the same `cat` the build writes into every bank entry, so this filter
   * cannot disagree with the option list that offered it. */
  function trackOf(scope) {
    return scope.indexOf('track:') === 0 ? scope.slice(6) : null;
  }

  function buildPool(scope) {
    var progress = read(PROGRESS_KEY);
    var checks = read(CHECK_KEY);
    var practice = read(PRACTICE_KEY);
    var track = trackOf(scope);

    var pool = [];
    BANK.forEach(function (mod) {
      if (!mod.q || !mod.q.length) return;
      var visited = progress[mod.path];
      if (scope === 'visited' && !visited) return;
      if (track && mod.cat !== track) return;
      var entry = {
        mod: mod, path: mod.path, title: mod.title, cat: mod.cat,
        visitedAt: visited && visited.at
      };
      entry.weight = weightFor(entry, checks, practice);
      pool.push(entry);
    });
    return pool;
  }

  /* Within a module, prefer a question this reader has not answered here yet,
   * then one they got wrong, then anything. */
  function pickQuestion(entry, practice) {
    var p = practice[entry.path] || {};
    var per = p.q || {};
    var qs = entry.mod.q.map(function (q, i) { return { q: q, i: i, s: per[i] }; });

    var unseen = qs.filter(function (x) { return !x.s; });
    if (unseen.length) return unseen[Math.floor(Math.random() * unseen.length)];

    var wrong = qs.filter(function (x) { return x.s && x.s.wrong; });
    if (wrong.length) return wrong[Math.floor(Math.random() * wrong.length)];

    return qs[Math.floor(Math.random() * qs.length)];
  }

  function record(path, qi, right) {
    var store = read(PRACTICE_KEY);
    var p = store[path] || { asked: 0, right: 0, q: {} };
    p.asked = (p.asked || 0) + 1;
    if (right) p.right = (p.right || 0) + 1;
    p.q = p.q || {};
    p.q[qi] = { wrong: !right, at: new Date().toISOString() };
    p.at = new Date().toISOString();
    store[path] = p;
    write(PRACTICE_KEY, store);
  }

  // --- rendering -----------------------------------------------------------

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function prefixed(path) { return '../' + path; }

  var state = null;

  function startSession() {
    var scope = document.getElementById('scope-select').value;
    var count = parseInt(document.getElementById('length-select').value, 10) || 10;
    var practice = read(PRACTICE_KEY);

    var pool = buildPool(scope);
    if (!pool.length) {
      showEmpty(scope);
      return;
    }

    var picked = pickWeighted(pool, Math.min(count, pool.length));
    if (!picked.length) {
        showEmpty(scope);
        return;
    }
    state = {
      items: picked.map(function (entry) {
        var chosen = pickQuestion(entry, practice);
        return { entry: entry, q: chosen.q, qi: chosen.i, answered: false, right: false };
      }),
      at: 0, right: 0
    };

    document.getElementById('practice-intro').hidden = true;
    document.getElementById('practice-summary').hidden = true;
    document.getElementById('practice-run').hidden = false;
    renderQuestion();
  }

  function showEmpty(scope) {
    var box = document.getElementById('practice-empty');
    var track = trackOf(scope);
    box.hidden = false;
    if (scope === 'visited') {
      box.innerHTML = '<p>No modules opened yet on this device, so there is nothing ' +
        'personal to practise. Open a module or two, or switch the scope to ' +
        '<strong>every module</strong> to draw from the whole site.</p>';
    } else if (track) {
      box.innerHTML = '<p>No questions in the ' + track + ' track yet.</p>';
    } else {
      box.innerHTML = '<p>The question bank is empty, which should not happen &mdash; ' +
        'it is generated at build time. Try a hard refresh.</p>';
    }
  }

  function renderQuestion() {
    var item = state.items[state.at];
    var host = document.getElementById('practice-card');
    host.innerHTML = '';

    document.getElementById('practice-count').textContent =
      (state.at + 1) + ' / ' + state.items.length;
    document.getElementById('practice-score').textContent =
      state.right + ' right';
    var bar = document.getElementById('practice-bar');
    bar.style.width = (state.at / state.items.length * 100) + '%';

    host.appendChild(el('p', 'vz-p-source',
      '<a href="' + prefixed(item.entry.path) + '">' + esc(item.entry.title) + '</a>' +
      '<span class="vz-p-cat">' + esc(item.entry.cat) + '</span>'));
    host.appendChild(el('h2', 'vz-p-question', esc(item.q.t)));

    if (item.q.o) {
      var opts = el('div', 'vz-p-opts');
      item.q.o.forEach(function (opt, i) {
        var b = el('button', 'vz-p-opt', esc(opt));
        b.type = 'button';
        b.addEventListener('click', function () { answerMcq(item, i, opts); });
        opts.appendChild(b);
      });
      host.appendChild(opts);
    } else {
      var reveal = el('button', 'vz-p-reveal', 'Show answer');
      reveal.type = 'button';
      var answer = el('p', 'vz-p-answer', esc(item.q.ans));
      answer.hidden = true;
      var grade = el('div', 'vz-p-grade');
      grade.hidden = true;
      [['I knew it', true], ['Not quite', false]].forEach(function (g) {
        var b = el('button', 'vz-p-opt', g[0]);
        b.type = 'button';
        b.addEventListener('click', function () { answerCard(item, g[1]); });
        grade.appendChild(b);
      });
      reveal.addEventListener('click', function () {
        answer.hidden = false;
        grade.hidden = false;
        reveal.hidden = true;
      });
      host.appendChild(reveal);
      host.appendChild(answer);
      host.appendChild(grade);
    }
  }

  function afterAnswer(item, right) {
    if (item.answered) return;
    item.answered = true;
    item.right = right;
    if (right) state.right++;
    record(item.entry.path, item.qi, right);
    document.getElementById('practice-score').textContent = state.right + ' right';

    var next = document.getElementById('practice-next');
    next.hidden = false;
    next.textContent = state.at === state.items.length - 1 ? 'See results' : 'Next question';
    next.focus();
  }

  function answerMcq(item, i, optsEl) {
    if (item.answered) return;
    var right = i === item.q.a;
    Array.prototype.forEach.call(optsEl.children, function (b, k) {
      b.disabled = true;
      if (k === item.q.a) b.classList.add('is-right');
      if (k === i && !right) b.classList.add('is-wrong');
    });
    if (item.q.w) {
      var why = el('p', 'vz-p-why', esc(item.q.w));
      document.getElementById('practice-card').appendChild(why);
    }
    afterAnswer(item, right);
  }

  function answerCard(item, right) {
    if (item.answered) return;
    var buttons = document.querySelectorAll('.vz-p-grade .vz-p-opt');
    Array.prototype.forEach.call(buttons, function (b, i) {
      b.disabled = true;
      // 0 is "I knew it", 1 is "Not quite" - mark the one that was pressed so
      // the card reads as answered rather than merely greyed out.
      if ((i === 0) === right) b.classList.add(right ? 'is-right' : 'is-wrong');
    });
    afterAnswer(item, right);
  }

  function nextQuestion() {
    document.getElementById('practice-next').hidden = true;
    if (state.at < state.items.length - 1) {
      state.at++;
      renderQuestion();
      return;
    }
    finish();
  }

  function finish() {
    document.getElementById('practice-run').hidden = true;
    var box = document.getElementById('practice-summary');
    box.hidden = false;

    var missed = state.items.filter(function (i) { return !i.right; });
    var pct = Math.round(state.right / state.items.length * 100);

    var html = '<div class="vz-p-result"><div class="vz-p-big">' + state.right + ' / ' +
      state.items.length + '</div><p>' + pct + '% this round</p></div>';

    if (missed.length) {
      html += '<h2 class="vz-p-h">Worth another look</h2><ul class="vz-p-list">';
      var seen = {};
      missed.forEach(function (i) {
        if (seen[i.entry.path]) return;
        seen[i.entry.path] = 1;
        html += '<li><a href="' + prefixed(i.entry.path) + '">' +
          esc(i.entry.title) + '</a> <span class="vz-p-cat">' +
          esc(i.entry.cat) + '</span></li>';
      });
      html += '</ul><p class="vz-p-note">These are now weighted to come back sooner.</p>';
    } else {
      html += '<p class="vz-p-note">Everything right. The modules you struggled with ' +
        'before are still weighted to reappear, so come back tomorrow.</p>';
    }

    html += '<button type="button" class="vz-p-start" id="practice-again">Another round</button>';
    box.innerHTML = html;
    document.getElementById('practice-again').addEventListener('click', startSession);
  }

  // --- stats on the intro screen ------------------------------------------

  function paintStats() {
    var progress = read(PROGRESS_KEY);
    var checks = read(CHECK_KEY);
    var practice = read(PRACTICE_KEY);

    var visited = 0, withQuestions = 0, questions = 0;
    BANK.forEach(function (m) {
      if (!m.q || !m.q.length) return;
      withQuestions++;
      questions += m.q.length;
      if (progress[m.path]) visited++;
    });

    var asked = 0, right = 0;
    Object.keys(practice).forEach(function (k) {
      asked += practice[k].asked || 0;
      right += practice[k].right || 0;
    });

    var scored = 0, scoreTotal = 0;
    Object.keys(checks).forEach(function (k) {
      if (checks[k].total) { scored += checks[k].score || 0; scoreTotal += checks[k].total; }
    });

    var set = function (id, v) {
      var e = document.getElementById(id);
      if (e) e.textContent = v;
    };
    set('stat-visited', visited);
    set('stat-bank', questions);
    set('stat-asked', asked);
    set('stat-accuracy', asked ? Math.round(right / asked * 100) + '%' : '—');

    var scope = document.getElementById('scope-select');
    if (scope && !visited) scope.value = 'all';

    // Recomputed on every scope change, so the description always matches
    // what Start would actually draw from.
    function describe() {
      var note = document.getElementById('practice-note');
      if (!note) return;
      var chosen = scope ? scope.value : 'visited';
      var track = trackOf(chosen);
      var text;

      if (track) {
        var n = buildPool(chosen).length;
        text = 'Drawing from the ' + n + ' ' + track + ' module' +
          (n === 1 ? '' : 's') + ' that have questions, whether or not you have ' +
          'opened them. Still weighted by what you got wrong and how long ago.';
      } else if (chosen === 'all') {
        text = 'Drawing from every module on the site, weighted by what you got ' +
          'wrong and how long ago you saw it.';
      } else if (visited) {
        text = 'Drawing from the ' + visited + ' module' + (visited === 1 ? '' : 's') +
          ' you have opened on this device, weighted by what you got wrong and how ' +
          'long ago you saw it.';
      } else {
        text = 'Nothing opened on this device yet, so the scope has been set to every ' +
          'module. Visit a few and this page will start following you rather than the catalog.';
      }

      if (scoreTotal) {
        text += ' Your end-of-module checks so far: ' + scored + ' of ' +
          scoreTotal + ' correct.';
      }
      note.textContent = text;
    }

    describe();
    if (scope && !scope.dataset.wired) {
      scope.dataset.wired = '1';
      scope.addEventListener('change', describe);
    }
  }

  function init() {
    if (!document.getElementById('practice-run')) return;
    paintStats();
    document.getElementById('practice-start').addEventListener('click', startSession);
    document.getElementById('practice-next').addEventListener('click', nextQuestion);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
