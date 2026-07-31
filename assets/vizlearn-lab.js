/* VizLearn - the lab layer.
 *
 * Three things sit on top of every module's visualisation:
 *
 *   1. Executable guided experiments. The written experiments always said
 *      things like 'set the "Neighbors (K)" slider to 1' and then left you to
 *      go and do it. Each one that the build could resolve to real control
 *      values now has a button that performs it.
 *
 *   2. Predict-then-reveal. Before an experiment runs, you commit to what a
 *      named readout on the page will do. The verdict is not scripted: the
 *      runtime reads that readout, applies the preset to the actual
 *      visualisation, reads it again, and compares. If the module changes, the
 *      answer changes with it, because there is no stored answer.
 *
 *   3. End-of-module check. Multiple choice where the module has authored
 *      questions, retrieval flashcards built from its own key takeaways
 *      otherwise. Results go to localStorage next to the progress store.
 *
 * The visualisations are 166 independent hand-written pages with no shared
 * component layer, so nothing here may assume a page structure. Everything is
 * driven by the JSON the build emits into #vz-lab-data, and every step checks
 * that what it is about to touch actually exists.
 */
(function () {
  'use strict';

  var CHECK_KEY = 'vizlearn_checks';
  /* How long to let a visualisation settle before reading a value back. Most
   * pages re-render synchronously on 'input'; the ones that animate need a
   * beat, and reading too early would score a correct prediction as wrong. */
  var SETTLE_MS = 700;

  // --- storage -------------------------------------------------------------

  function readChecks() {
    try {
      return JSON.parse(localStorage.getItem(CHECK_KEY)) || {};
    } catch (e) {
      return {};
    }
  }

  function writeChecks(store) {
    try {
      localStorage.setItem(CHECK_KEY, JSON.stringify(store));
    } catch (e) {
      /* private browsing or quota - the check still works, it just forgets */
    }
  }

  function pagePath() {
    var link = document.querySelector('link[rel="canonical"]');
    if (!link || !link.href) return location.pathname;
    return link.href.replace(/^https?:\/\/[^/]+\//, '');
  }

  function recordCheck(patch) {
    var store = readChecks();
    var path = pagePath();
    var prev = store[path] || {};
    for (var k in patch) if (patch.hasOwnProperty(k)) prev[k] = patch[k];
    prev.at = new Date().toISOString();
    store[path] = prev;
    writeChecks(store);
  }

  // --- helpers -------------------------------------------------------------

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function fire(el, type) {
    el.dispatchEvent(new Event(type, { bubbles: true }));
  }

  function num(text) {
    if (text == null) return null;
    var m = String(text).replace(/,/g, '').match(/-?\d+(\.\d+)?/);
    return m ? parseFloat(m[0]) : null;
  }

  function textOf(el) {
    return el ? (el.textContent || '').replace(/\s+/g, ' ').trim() : '';
  }

  /* Pick the <option> that matches a wanted value, by value first and then by
   * visible text. Several pages build their options in JavaScript after load,
   * so the build cannot know the real values and has to match on what the
   * prose said. */
  function selectOption(sel, want) {
    var wanted = String(want).toLowerCase().trim();
    var opts = sel.options || [];
    var i;
    for (i = 0; i < opts.length; i++) {
      if (String(opts[i].value).toLowerCase().trim() === wanted) return opts[i].value;
    }
    for (i = 0; i < opts.length; i++) {
      if (textOf(opts[i]).toLowerCase() === wanted) return opts[i].value;
    }
    for (i = 0; i < opts.length; i++) {
      var t = textOf(opts[i]).toLowerCase();
      if (t.indexOf(wanted) !== -1 || wanted.indexOf(t) !== -1) return opts[i].value;
    }
    return null;
  }

  // --- applying a preset ---------------------------------------------------

  /* Returns the number of controls actually changed, so a caller can tell the
   * difference between "ran" and "the page did not have those controls". */
  function applyPreset(preset) {
    if (!preset) return 0;
    var changed = 0;

    (preset.set || []).forEach(function (item) {
      var el = document.getElementById(item.id);

      if (!el && item.kind === 'radio') {
        var radios = $$('input[type="radio"][name="' + item.id + '"]');
        for (var i = 0; i < radios.length; i++) {
          var v = String(radios[i].value).toLowerCase();
          var lbl = textOf(radios[i].parentNode).toLowerCase();
          var want = String(item.value).toLowerCase();
          if (v === want || lbl.indexOf(want) !== -1) {
            radios[i].checked = true;
            fire(radios[i], 'input');
            fire(radios[i], 'change');
            changed++;
            break;
          }
        }
        return;
      }
      if (!el) return;

      if (el.tagName === 'SELECT') {
        var val = selectOption(el, item.value);
        if (val === null) return;
        el.value = val;
      } else if (el.type === 'checkbox') {
        el.checked = !!item.value;
      } else {
        if (el.disabled) return;
        el.value = item.value;
      }

      fire(el, 'input');
      fire(el, 'change');
      changed++;
    });

    (preset.click || []).forEach(function (id) {
      var el = document.getElementById(id);
      if (el && !el.disabled) { el.click(); changed++; }
    });

    return changed;
  }

  /* Bring the visualisation into view and flash it, so it is obvious that
   * something just happened somewhere else on the page. */
  function revealViz() {
    var target = LAB.viz && document.getElementById(LAB.viz);
    if (!target) {
      var svg = $('main svg[id], main canvas');
      target = svg && svg.closest ? (svg.closest('.card-container') || svg) : svg;
    }
    if (!target) return;

    var reduce = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    target.classList.add('vz-flash');
    setTimeout(function () { target.classList.remove('vz-flash'); }, 1200);
  }

  // --- readouts ------------------------------------------------------------

  /* The readout to ask about. Candidates come from the build, which cannot
   * know which of a page's outputs are populated at load and which only
   * appear after an interaction - so the choice is made here, against what is
   * actually on screen.
   *
   * A numeric readout is worth more than a categorical one: "does it go up or
   * down" is a sharper question than "does it change", so a number wins even
   * if it appears later in the list. */
  function liveReadout() {
    var list = LAB.readouts || [];
    var fallback = null;

    for (var i = 0; i < list.length; i++) {
      var el = document.getElementById(list[i].id);
      if (!el) continue;
      var t = textOf(el);
      if (!t || t === '--' || t === '-') continue;
      if (num(t) !== null) return { meta: list[i], el: el, numeric: true };
      if (!fallback) fallback = { meta: list[i], el: el, numeric: false };
    }
    return fallback;
  }

  /* Up/down/same only makes sense for a number. When the readout is a label -
   * a predicted class, a state name - offer the question that fits it. */
  function retargetOptions(box, live) {
    if (live.numeric) return $$('.vz-predict-opt', box);

    var wrap = $('.vz-predict-opts', box);
    wrap.innerHTML =
      '<button type="button" class="vz-predict-opt" data-vz-guess="changed">' +
      'It changes</button>' +
      '<button type="button" class="vz-predict-opt" data-vz-guess="same">' +
      'It stays the same</button>';
    return $$('.vz-predict-opt', box);
  }

  // --- guided experiments --------------------------------------------------

  function initExperiments() {
    $$('[data-vz-run]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var preset = (LAB.presets || [])[parseInt(btn.dataset.vzRun, 10)];
        var n = applyPreset(preset);

        if (!n) {
          if (window.VizLearn) VizLearn.toast('That control is not on this page');
          return;
        }
        btn.classList.add('is-done');
        setTimeout(function () { btn.classList.remove('is-done'); }, 1600);
        revealViz();

        if (typeof gtag === 'function') {
          gtag('event', 'lab_experiment', { item_id: pagePath(), index: btn.dataset.vzRun });
        }
      });
    });
  }

  // --- predict, then reveal ------------------------------------------------

  function initPredict() {
    var box = $('.vz-predict');
    if (!box) return;

    var preset = (LAB.presets || [])[parseInt(box.dataset.vzPreset || '0', 10)];
    var result = $('.vz-predict-result', box);
    var readoutName = $('.vz-predict-readout', box);

    var live = liveReadout();
    if (!preset || !live) {
      // Nothing honest to ask about; leave the page as it was.
      box.remove();
      return;
    }
    if (readoutName) readoutName.textContent = live.meta.label;

    var options = retargetOptions(box, live);

    var answered = false;

    options.forEach(function (opt) {
      opt.addEventListener('click', function () {
        if (answered) return;
        answered = true;

        var guess = opt.dataset.vzGuess;
        var beforeText = textOf(live.el);
        var beforeNum = num(beforeText);

        options.forEach(function (o) {
          o.disabled = true;
          o.classList.toggle('is-picked', o === opt);
        });

        box.classList.add('is-running');
        applyPreset(preset);
        revealViz();

        setTimeout(function () {
          var afterText = textOf(live.el);
          var afterNum = num(afterText);

          var actual;
          if (beforeNum !== null && afterNum !== null) {
            var d = afterNum - beforeNum;
            // A hair of tolerance, so a rounding wobble is not "it went up".
            var eps = Math.max(Math.abs(beforeNum), 1) * 0.001;
            actual = d > eps ? 'up' : (d < -eps ? 'down' : 'same');
          } else {
            actual = beforeText === afterText ? 'same' : 'changed';
          }

          // "It changes" is satisfied by a move in either direction, which
          // matters when a numeric readout is being judged against the
          // categorical wording.
          var right = guess === actual ||
            (guess === 'changed' && (actual === 'up' || actual === 'down'));

          box.classList.remove('is-running');
          box.classList.add(right ? 'is-right' : 'is-wrong');

          options.forEach(function (o) {
            if (o.dataset.vzGuess === actual) o.classList.add('is-actual');
          });

          result.hidden = false;
          result.innerHTML =
            '<p class="vz-predict-verdict">' +
            (right ? 'Correct.' : 'Not quite.') + '</p>' +
            '<p><strong>' + escapeHtml(live.meta.label) + '</strong> went from <span ' +
            'class="mono-font">' + escapeHtml(beforeText) + '</span> to <span ' +
            'class="mono-font">' + escapeHtml(afterText) + '</span>.</p>' +
            '<p class="vz-predict-note">The visualisation above is now in that ' +
            'state &mdash; keep changing the controls to see how far it holds.</p>';

          recordCheck({ predicted: right });
          if (typeof gtag === 'function') {
            gtag('event', 'lab_predict', { item_id: pagePath(), correct: right });
          }
        }, SETTLE_MS);
      });
    });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // --- end-of-module check -------------------------------------------------

  function initCheck() {
    var box = $('.vz-check');
    if (!box) return;

    var questions = $$('.vz-q', box);
    var scoreEl = $('.vz-check-score', box);
    var total = questions.length;
    var correct = 0;
    var answered = 0;

    questions.forEach(function (q) {
      // Flashcard: no options, just a hidden answer to reveal.
      var reveal = $('[data-vz-reveal]', q);
      if (reveal) {
        var answer = $('.vz-q-answer', q);
        reveal.addEventListener('click', function () {
          var open = answer.hidden;
          answer.hidden = !open;
          reveal.textContent = open ? 'Hide answer' : 'Show answer';
          if (open && !q.dataset.vzSeen) {
            q.dataset.vzSeen = '1';
            answered++;
            updateScore();
          }
        });
        return;
      }

      // Multiple choice.
      var opts = $$('.vz-q-opt', q);
      opts.forEach(function (opt) {
        opt.addEventListener('click', function () {
          if (q.dataset.vzDone) return;
          q.dataset.vzDone = '1';
          answered++;

          var right = opt.dataset.vzCorrect === '1';
          if (right) correct++;

          opts.forEach(function (o) {
            o.disabled = true;
            if (o.dataset.vzCorrect === '1') o.classList.add('is-correct');
          });
          if (!right) opt.classList.add('is-wrong');

          var why = $('.vz-q-why', q);
          if (why) why.hidden = false;
          updateScore();
        });
      });
    });

    function updateScore() {
      if (!scoreEl) return;
      if (answered < total) {
        scoreEl.textContent = answered + ' of ' + total;
        return;
      }
      var hasMcq = questions.some(function (q) { return !$('[data-vz-reveal]', q); });
      scoreEl.textContent = hasMcq ? correct + ' / ' + total + ' correct' : 'All reviewed';
      box.classList.add('is-complete');
      recordCheck({ score: correct, total: total });
      if (typeof gtag === 'function') {
        gtag('event', 'lab_check_complete', {
          item_id: pagePath(), score: correct, total: total
        });
      }
    }

    // Show what this reader scored last time, if anything.
    var prev = readChecks()[pagePath()];
    if (prev && typeof prev.score === 'number' && scoreEl) {
      var note = document.createElement('p');
      note.className = 'vz-check-prev';
      note.textContent = 'Last time you scored ' + prev.score + ' / ' + prev.total + '.';
      box.insertBefore(note, box.firstChild.nextSibling);
    }
  }

  // --- boot ----------------------------------------------------------------

  var LAB = {};

  function boot() {
    var data = document.getElementById('vz-lab-data');
    if (data) {
      try { LAB = JSON.parse(data.textContent) || {}; } catch (e) { LAB = {}; }
    }
    initExperiments();
    initPredict();
    initCheck();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
