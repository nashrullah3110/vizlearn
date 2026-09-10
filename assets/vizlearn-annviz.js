/* The vector-index explorers on the gen_ai/ indexing modules.
 *
 * Eight modules describe eight ways to avoid comparing a query against every
 * vector you have stored. The thing being explained in each is a *structure* -
 * a Voronoi partition, a navigable graph, a quantisation lattice, a forest of
 * random splits - and none of that fits in a bar chart, so these models return
 * a drawn scene as well as the numbers.
 *
 * The important commitment: nothing here is a fitted curve. The corpus is
 * real, the index is really built, the search really runs, and recall is
 * measured against a real exhaustive search over the same points. When the
 * page says "recall 0.83 after comparing 14% of the corpus", both figures were
 * counted during a search that just happened in the reader's browser. Move
 * nprobe by one and the number moves because a different set of points was
 * examined, not because a formula said it should.
 *
 * That matters more here than usual, because every one of these algorithms is
 * a claim about a trade-off, and a demonstration that assumes the trade-off
 * cannot be evidence for it.
 *
 * The corpus is two-dimensional so it can be drawn. Real embeddings are 768 or
 * 1536, every page says so, and the pages carry the arithmetic for those sizes
 * beside the picture - because the *cost* model is what changes with dimension
 * while the *structure* is what the picture is for.
 *
 * Registers into window.VizRagViz.MODELS; loads only on pages with data-vz-ann.
 */
(function () {
  'use strict';

  var RV = window.VizRagViz;
  if (!RV) return;

  var NS = 'http://www.w3.org/2000/svg';

  // ------------------------------------------------------------------ maths

  /* Mulberry32. Deterministic, so a slider changes the index and not the
   * data - a corpus that reshuffled on every redraw would make every
   * comparison on these pages meaningless. */
  function rng(seed) {
    var s = (seed || 1) >>> 0;
    return function () {
      s = (s + 0x6D2B79F5) >>> 0;
      var t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function gauss(r) {
    var u = 1 - r(), v = r();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  function d2(a, b) {
    var dx = a[0] - b[0], dy = a[1] - b[1];
    return dx * dx + dy * dy;
  }

  function fmt(n) {
    var a = Math.abs(n);
    if (a >= 1e9) return (n / 1e9).toFixed(a >= 1e10 ? 1 : 2) + ' G';
    if (a >= 1e6) return (n / 1e6).toFixed(a >= 1e7 ? 1 : 2) + ' M';
    if (a >= 1e3) return (n / 1e3).toFixed(a >= 1e4 ? 0 : 1) + ' K';
    return String(Math.round(n));
  }

  function commas(n) {
    return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  // ----------------------------------------------------------------- corpus

  /* One corpus, shared by all eight modules, so the recall and comparison
   * counts on different pages are directly comparable. Six dense clusters
   * plus a uniform scattering, which is roughly what a real embedding set
   * looks like projected to two dimensions: topics, and things between them. */
  var N = 600;
  var CORPUS = (function () {
    var r = rng(20260910), pts = [], i;
    var centres = [[0.22, 0.28], [0.72, 0.20], [0.50, 0.52],
                   [0.20, 0.76], [0.80, 0.68], [0.62, 0.86]];
    for (i = 0; i < N; i++) {
      if (i % 6 === 5) {
        pts.push([r(), r()]);                       // background
      } else {
        var c = centres[i % centres.length];
        pts.push([clamp(c[0] + gauss(r) * 0.075, 0.02, 0.98),
                  clamp(c[1] + gauss(r) * 0.075, 0.02, 0.98)]);
      }
    }
    return pts;
  })();

  function exactKNN(q, k, pts) {
    pts = pts || CORPUS;
    var scored = [], i;
    for (i = 0; i < pts.length; i++) scored.push([d2(q, pts[i]), i]);
    scored.sort(function (a, b) { return a[0] - b[0]; });
    return scored.slice(0, k).map(function (s) { return s[1]; });
  }

  /* A fixed set of probe queries, drawn from the same distribution as the
   * corpus - some inside clusters, some in the gaps between them.
   *
   * Reporting recall for the single query on screen turned out to be almost
   * useless: the default query sits inside a dense cluster, where every index
   * on these pages scores 1.0 and no slider appears to do anything. Recall is
   * a property of an index averaged over a query workload, not of one lookup,
   * and benchmarks measure it that way for exactly this reason. So each page
   * shows the average over these 48, and draws the one you are dragging. */
  var PROBES = (function () {
    var r = rng(31337), out = [], i;
    var centres = [[0.22, 0.28], [0.72, 0.20], [0.50, 0.52],
                   [0.20, 0.76], [0.80, 0.68], [0.62, 0.86]];
    for (i = 0; i < 48; i++) {
      if (i % 3 === 2) {
        out.push([0.08 + r() * 0.84, 0.08 + r() * 0.84]);
      } else {
        var c = centres[i % centres.length];
        out.push([clamp(c[0] + gauss(r) * 0.11, 0.03, 0.97),
                  clamp(c[1] + gauss(r) * 0.11, 0.03, 0.97)]);
      }
    }
    return out;
  })();

  /* Mean recall@k of `search` over the probe set. `search` is the index's own
   * query path, so this is measured, not modelled - and it is the same code
   * that produced the picture. */
  function avgRecall(search, k) {
    var total = 0, i;
    for (i = 0; i < PROBES.length; i++) {
      total += recall(search(PROBES[i]), exactKNN(PROBES[i], k));
    }
    return total / PROBES.length;
  }

  /* Mean number of vectors a search touched, over the same probes. */
  function avgCost(costOf) {
    var total = 0, i;
    for (i = 0; i < PROBES.length; i++) total += costOf(PROBES[i]);
    return total / PROBES.length;
  }

  function recall(got, truth) {
    var set = {}, hit = 0, i;
    for (i = 0; i < got.length; i++) set[got[i]] = 1;
    for (i = 0; i < truth.length; i++) if (set[truth[i]]) hit++;
    return truth.length ? hit / truth.length : 0;
  }

  /* Lloyd's algorithm, seeded deterministically. Used for IVF's cell centroids
   * and for every product-quantiser codebook on these pages. */
  function kmeans(points, k, iters, seed, dims) {
    dims = dims || 2;
    var r = rng(seed || 7), i, j, d, best, bd;
    var cent = [];
    for (i = 0; i < k; i++) cent.push(points[Math.floor(r() * points.length)].slice());
    var assign = new Int32Array(points.length);
    for (var it = 0; it < (iters || 12); it++) {
      for (i = 0; i < points.length; i++) {
        best = 0; bd = Infinity;
        for (j = 0; j < k; j++) {
          var s = 0;
          for (d = 0; d < dims; d++) {
            var df = points[i][d] - cent[j][d];
            s += df * df;
          }
          if (s < bd) { bd = s; best = j; }
        }
        assign[i] = best;
      }
      var sums = [], counts = new Int32Array(k);
      for (j = 0; j < k; j++) sums.push(new Float64Array(dims));
      for (i = 0; i < points.length; i++) {
        counts[assign[i]]++;
        for (d = 0; d < dims; d++) sums[assign[i]][d] += points[i][d];
      }
      for (j = 0; j < k; j++) {
        if (!counts[j]) continue;
        for (d = 0; d < dims; d++) cent[j][d] = sums[j][d] / counts[j];
      }
    }
    return { centroids: cent, assign: assign };
  }

  // ---------------------------------------------------------------- drawing

  var W = 460, H = 340, PAD = 10;

  function svgEl(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) if (attrs.hasOwnProperty(k)) {
      if (attrs[k] === null || attrs[k] === undefined) continue;
      n.setAttribute(k, attrs[k]);
    }
    return n;
  }

  function px(x) { return PAD + x * (W - 2 * PAD); }
  function py(y) { return PAD + y * (H - 2 * PAD); }

  function stage() {
    var s = svgEl('svg', {
      viewBox: '0 0 ' + W + ' ' + H,
      class: 'vz-ann-svg vz-touch-surface'
    });
    s.setAttribute('aria-hidden', 'true');
    s.appendChild(svgEl('rect', {
      x: 0.5, y: 0.5, width: W - 1, height: H - 1, rx: 8,
      fill: 'var(--bg-surface)', stroke: 'var(--border-subtle)'
    }));
    return s;
  }

  function dot(p, o) {
    o = o || {};
    return svgEl('circle', {
      cx: px(p[0]), cy: py(p[1]), r: o.r || 2,
      fill: o.fill || 'var(--text-muted)',
      'fill-opacity': o.fo === undefined ? 0.55 : o.fo,
      stroke: o.stroke || 'none',
      'stroke-width': o.sw || 0
    });
  }

  function seg(a, b, o) {
    o = o || {};
    return svgEl('line', {
      x1: px(a[0]), y1: py(a[1]), x2: px(b[0]), y2: py(b[1]),
      stroke: o.stroke || 'var(--border-subtle)',
      'stroke-width': o.sw === undefined ? 1 : o.sw,
      'stroke-dasharray': o.dash,
      opacity: o.opacity
    });
  }

  function label(x, y, str, o) {
    o = o || {};
    var t = svgEl('text', {
      x: x, y: y, fill: o.fill || 'var(--text-muted)',
      'font-size': o.size || 9.5,
      'font-family': 'var(--vz-mono)',
      'text-anchor': o.anchor || 'start'
    });
    t.textContent = str;
    return t;
  }

  /* The query marker: a ring plus crosshairs, so it reads as "the thing being
   * searched for" rather than as another corpus point. */
  function queryMark(q) {
    var g = svgEl('g', {});
    g.appendChild(svgEl('circle', {
      cx: px(q[0]), cy: py(q[1]), r: 6,
      fill: 'none', stroke: 'var(--accent-primary)', 'stroke-width': 2
    }));
    g.appendChild(svgEl('line', {
      x1: px(q[0]) - 10, y1: py(q[1]), x2: px(q[0]) + 10, y2: py(q[1]),
      stroke: 'var(--accent-primary)', 'stroke-width': 1
    }));
    g.appendChild(svgEl('line', {
      x1: px(q[0]), y1: py(q[1]) - 10, x2: px(q[0]), y2: py(q[1]) + 10,
      stroke: 'var(--accent-primary)', 'stroke-width': 1
    }));
    return g;
  }

  function legend(s, items) {
    var x = 12, y = H - 10;
    items.forEach(function (it) {
      s.appendChild(svgEl('circle', {
        cx: x + 3, cy: y - 3, r: 3, fill: it[1],
        'fill-opacity': it[2] === undefined ? 1 : it[2]
      }));
      var t = label(x + 10, y, it[0], { size: 8.5 });
      s.appendChild(t);
      x += 12 + it[0].length * 5.1;
    });
  }

  /* The query is draggable on every page, and the position is remembered per
   * model so moving between control changes does not reset it. */
  var QUERY = {};
  function queryFor(name) {
    if (!QUERY[name]) QUERY[name] = [0.46, 0.44];
    return QUERY[name];
  }

  /* The harness publishes its current render for the duration of a model
   * call, which is what a drag handler needs in order to redraw. Capturing it
   * at scene-construction time is correct because models are synchronous. */
  function makeDraggable(s, name) {
    var rerender = RV.rerender || function () {};
    function move(ev) {
      var r = s.getBoundingClientRect();
      QUERY[name] = [
        clamp((ev.clientX - r.left) / r.width * (W / (W - 2 * PAD))
              - PAD / (W - 2 * PAD), 0, 1),
        clamp((ev.clientY - r.top) / r.height * (H / (H - 2 * PAD))
              - PAD / (H - 2 * PAD), 0, 1)
      ];
      rerender();
      ev.preventDefault();
    }
    s.addEventListener('pointerdown', function (ev) {
      move(ev);
      function moved(e) { move(e); }
      function done() {
        window.removeEventListener('pointermove', moved);
        window.removeEventListener('pointerup', done);
        window.removeEventListener('pointercancel', done);
      }
      /* Listening on the window rather than capturing on the SVG: the scene
       * is replaced on every re-render, and removing a capturing element from
       * the document releases its capture, so a drag died on the first frame. */
      window.addEventListener('pointermove', moved, { passive: false });
      window.addEventListener('pointerup', done);
      window.addEventListener('pointercancel', done);
    });
  }

  // ------------------------------------------------------------ cost models
  //
  // The picture is two-dimensional; the arithmetic anybody cares about is not.
  // Every page carries the same cost model evaluated at a realistic corpus, so
  // "14% of the corpus" becomes a number of bytes and a number of milliseconds.

  var REAL = { n: 1000000, d: 768 };

  function flatBytes() { return REAL.n * REAL.d * 4; }

  function scaled(fraction) {
    /* One distance is d multiply-adds; a modern core does a few billion a
     * second with SIMD. The constant is deliberately round - it is there to
     * turn a ratio into something with units, not to predict your hardware. */
    var comparisons = REAL.n * fraction;
    return {
      comparisons: comparisons,
      ms: comparisons * REAL.d / 4e9 * 1000
    };
  }

  window.VizAnnViz = {
    CORPUS: CORPUS, exactKNN: exactKNN, recall: recall, kmeans: kmeans,
    rng: rng, gauss: gauss, clamp: clamp, d2: d2, fmt: fmt, commas: commas,
    stage: stage, dot: dot, seg: seg, label: label, queryMark: queryMark,
    legend: legend, px: px, py: py, svgEl: svgEl, W: W, H: H,
    queryFor: queryFor, makeDraggable: makeDraggable, REAL: REAL,
    flatBytes: flatBytes, scaled: scaled, N: N,
    PROBES: PROBES, avgRecall: avgRecall, avgCost: avgCost
  };
})();

/* ===========================================================================
 * Flat index - the exhaustive scan, and the baseline everything is measured
 * against.
 * ======================================================================== */
(function () {
  'use strict';
  var RV = window.VizRagViz, V = window.VizAnnViz;
  if (!RV || !V) return;

  RV.MODELS.ann_flat = function (p) {
    var q = V.queryFor('flat'), k = p.k;
    var n = Math.round(p.corpus);
    var pts = V.CORPUS.slice(0, n);
    var truth = V.exactKNN(q, k, pts);
    var inTop = {};
    truth.forEach(function (i) { inTop[i] = 1; });

    /* The "scanned" slider is what makes the point: a flat index has no way
     * to stop early, and stopping early is exactly what loses you neighbours. */
    var scanned = Math.max(1, Math.round(n * p.scanned / 100));
    function run(qq) { return V.exactKNN(qq, k, pts.slice(0, scanned)); }
    var got = run(q);
    var r = V.recall(got, truth);
    var avgR = V.avgRecall(run, k);

    var s = V.stage();
    var i;
    for (i = 0; i < n; i++) {
      s.appendChild(V.dot(pts[i], {
        r: inTop[i] ? 3.6 : 2,
        fill: inTop[i] ? 'var(--accent-primary)'
             : (i < scanned ? 'var(--text-muted)' : 'var(--border-subtle)'),
        fo: inTop[i] ? 1 : (i < scanned ? 0.6 : 0.9)
      }));
    }
    /* Lines to the k returned neighbours: the answer, drawn. */
    got.forEach(function (idx) {
      s.appendChild(V.seg(q, pts[idx], {
        stroke: 'var(--accent-primary)', sw: 1, opacity: 0.7
      }));
    });
    s.appendChild(V.queryMark(q));
    s.appendChild(V.label(12, 20, n + ' vectors  ·  ' + scanned +
      ' compared  ·  drag the query', { size: 9 }));
    V.legend(s, [['true top-' + k, 'var(--accent-primary)'],
                 ['compared', 'var(--text-muted)', 0.6],
                 ['not reached', 'var(--border-subtle)', 0.9]]);
    V.makeDraggable(s, 'flat');

    var real = V.scaled(p.scanned / 100);
    var full = V.scaled(1);

    return {
      scene: s,
      bars: [
        { label: 'vectors compared', value: scanned, max: n,
          tag: p.scanned + '% of the corpus - a flat index has no way to skip any',
          state: scanned >= n ? 'hit' : 'bad' },
        { label: 'recall@' + k + ' over 48 queries', value: RV.round(avgR, 3), max: 1,
          tag: avgR === 1 ? 'exact by construction - this is the ground truth'
                          : 'stopping early is the only way a flat index can be wrong',
          state: avgR === 1 ? 'hit' : 'bad' }
      ],
      stats: [
        ['corpus (drawn)', V.commas(n)],
        ['distance computations', V.commas(scanned)],
        ['at 1 M x 768 dims', V.fmt(real.comparisons * V.REAL.d * 2) + ' FLOPs'],
        ['full scan latency', full.ms.toFixed(0) + ' ms'],
        ['index memory', V.fmt(V.flatBytes()) + 'B'],
        ['index build time', 'none']
      ],
      badge: 'recall ' + RV.round(avgR, 3),
      note: scanned >= n
        ? 'This is the ground truth. Every approximate index on the following '
          + 'pages is scored by how much of this answer it recovers, and the '
          + 'only way to know that is to run this search on a sample.'
        : 'A flat index cannot prune, so the only way to make it cheaper is to '
          + 'stop early - and the neighbours you lose are wherever you stopped. '
          + 'That is why the approximate indexes organise the vectors instead.'
    };
  };
})();

/* ===========================================================================
 * IVF-Flat - partition into Voronoi cells, probe the nearest few.
 * ======================================================================== */
(function () {
  'use strict';
  var RV = window.VizRagViz, V = window.VizAnnViz;
  if (!RV || !V) return;

  var CACHE = {};
  function index(nlist) {
    if (CACHE[nlist]) return CACHE[nlist];
    var km = V.kmeans(V.CORPUS, nlist, 18, 4242);
    var lists = [], i;
    for (i = 0; i < nlist; i++) lists.push([]);
    for (i = 0; i < V.CORPUS.length; i++) lists[km.assign[i]].push(i);
    CACHE[nlist] = { centroids: km.centroids, lists: lists, assign: km.assign };
    return CACHE[nlist];
  }

  RV.MODELS.ann_ivfflat = function (p) {
    var q = V.queryFor('ivf'), k = p.k;
    var nlist = p.nlist, nprobe = Math.min(p.nprobe, nlist);
    var ix = index(nlist);

    /* The search, exactly as it runs: rank the centroids, open the nearest
     * nprobe lists, and compare against every vector inside those lists. */
    function run(qq) {
      var order = ix.centroids.map(function (c, i) { return [V.d2(qq, c), i]; })
                    .sort(function (a, b) { return a[0] - b[0]; });
      var probed = {}, candidates = [];
      order.slice(0, nprobe).forEach(function (o) {
        probed[o[1]] = 1;
        candidates = candidates.concat(ix.lists[o[1]]);
      });
      var got = candidates.map(function (i) { return [V.d2(qq, V.CORPUS[i]), i]; })
                  .sort(function (a, b) { return a[0] - b[0]; })
                  .slice(0, k).map(function (x) { return x[1]; });
      return { got: got, probed: probed, candidates: candidates };
    }
    var here = run(q);
    var probed = here.probed, candidates = here.candidates, got = here.got;
    var truth = V.exactKNN(q, k);
    var r = V.recall(got, truth);
    var avgR = V.avgRecall(function (qq) { return run(qq).got; }, k);
    var avgC = V.avgCost(function (qq) { return run(qq).candidates.length; });

    var gotSet = {}, truthSet = {};
    got.forEach(function (i) { gotSet[i] = 1; });
    truth.forEach(function (i) { truthSet[i] = 1; });

    var s = V.stage();
    var i;
    /* Cell boundaries, drawn as the assignment itself: every point tinted by
     * whether its cell was opened. A true Voronoi diagram would be prettier
     * and would say less - what matters is which points were reachable. */
    for (i = 0; i < V.CORPUS.length; i++) {
      var open = probed[ix.assign[i]];
      var missed = truthSet[i] && !gotSet[i];
      s.appendChild(V.dot(V.CORPUS[i], {
        r: missed ? 4 : (truthSet[i] ? 3.4 : 1.9),
        fill: missed ? 'var(--vz-series-warn)'
             : truthSet[i] ? 'var(--accent-primary)'
             : (open ? 'var(--text-muted)' : 'var(--border-subtle)'),
        fo: missed || truthSet[i] ? 1 : (open ? 0.6 : 0.85)
      }));
    }
    ix.centroids.forEach(function (c, j) {
      s.appendChild(V.svgEl('rect', {
        x: V.px(c[0]) - 3.5, y: V.py(c[1]) - 3.5, width: 7, height: 7,
        fill: probed[j] ? 'var(--accent-fill)' : 'none',
        'fill-opacity': 0.9,
        stroke: probed[j] ? 'var(--accent-primary)' : 'var(--text-muted)',
        'stroke-width': 1.2
      }));
      if (probed[j]) s.appendChild(V.seg(q, c, {
        stroke: 'var(--accent-primary)', sw: 0.8, dash: '3 3', opacity: 0.65
      }));
    });
    s.appendChild(V.queryMark(q));
    s.appendChild(V.label(12, 20, nlist + ' cells  ·  ' + nprobe +
      ' probed  ·  ' + candidates.length + ' vectors compared', { size: 9 }));
    V.legend(s, [['probed', 'var(--text-muted)', 0.6],
                 ['skipped', 'var(--border-subtle)', 0.85],
                 ['found', 'var(--accent-primary)'],
                 ['missed', 'var(--vz-series-warn)']]);
    V.makeDraggable(s, 'ivf');

    var frac = candidates.length / V.CORPUS.length;
    var missedCount = truth.filter(function (i) { return !gotSet[i]; }).length;

    return {
      scene: s,
      bars: [
        { label: 'vectors compared (mean)', value: Math.round(avgC),
          max: V.CORPUS.length,
          tag: (avgC / V.CORPUS.length * 100).toFixed(1) + '% of the corpus, plus ' +
               nlist + ' centroid comparisons',
          state: avgC / V.CORPUS.length > 0.6 ? 'bad' : 'hit' },
        { label: 'recall@' + k + ' over 48 queries', value: RV.round(avgR, 3), max: 1,
          tag: missedCount ? missedCount + ' true neighbour(s) missed on the drawn query'
                           : 'the drawn query found all ' + k,
          state: avgR >= 0.9 ? 'hit' : 'bad' }
      ],
      stats: [
        ['nlist (cells)', nlist],
        ['nprobe', nprobe],
        ['avg list length', Math.round(V.CORPUS.length / nlist)],
        ['corpus touched (mean)', (avgC / V.CORPUS.length * 100).toFixed(1) + '%'],
        ['this query', candidates.length + ' compared, recall ' + RV.round(r, 2)],
        ['at 1 M x 768', V.scaled(avgC / V.CORPUS.length).ms.toFixed(1) + ' ms vs ' +
          V.scaled(1).ms.toFixed(0) + ' ms flat'],
        ['index memory', V.fmt(V.flatBytes()) + 'B (vectors, uncompressed)']
      ],
      badge: 'recall ' + RV.round(avgR, 3),
      note: missedCount
        ? 'The red points are true neighbours sitting in a cell the search never '
          + 'opened. That is IVF’s entire failure mode - a hard boundary '
          + 'through a neighbourhood - and the fix is always more probes.'
        : (nprobe >= nlist
            ? 'Probing every cell is an exact search with extra steps: recall 1.0 '
              + 'and none of the saving.'
            : 'Every true neighbour landed in an opened cell. Drag the query onto '
              + 'a cell boundary and watch that stop being true.')
    };
  };
})();

/* ===========================================================================
 * Product quantization
 *
 * The idea is easier to see in two dimensions than in 768, and it is not a
 * simplification: split the vector into m subvectors, quantise each against
 * its own codebook of 2^nbits centroids, and store the m codes instead of the
 * vector. At d = 2 and m = 2 the subspaces are the two axes, so the set of
 * representable points is literally a grid - k centroids per axis giving k^2
 * reachable positions from 2k stored centroids. That combinatorial blow-up is
 * the whole reason PQ works, and here you can count the intersections.
 * ======================================================================== */
(function () {
  'use strict';
  var RV = window.VizRagViz, V = window.VizAnnViz;
  if (!RV || !V) return;

  var CACHE = {};

  /* Codebooks: one per subspace, trained by k-means on that subspace alone. */
  function train(m, bits) {
    var key = m + '|' + bits;
    if (CACHE[key]) return CACHE[key];
    var ks = Math.pow(2, bits), books = [], sub, i;
    if (m === 1) {
      books.push(V.kmeans(V.CORPUS, ks, 20, 91, 2).centroids);
    } else {
      for (var axis = 0; axis < 2; axis++) {
        sub = V.CORPUS.map(function (p) { return [p[axis]]; });
        books.push(V.kmeans(sub, ks, 20, 91 + axis, 1).centroids);
      }
    }
    /* Encode every corpus vector once, exactly as an index build would. */
    var codes = [];
    for (i = 0; i < V.CORPUS.length; i++) codes.push(encode(V.CORPUS[i], books, m));
    CACHE[key] = { books: books, codes: codes, m: m, ks: ks };
    return CACHE[key];
  }

  function encode(v, books, m) {
    var out = [], j, best, bd, s;
    if (m === 1) {
      best = 0; bd = Infinity;
      for (j = 0; j < books[0].length; j++) {
        s = V.d2(v, books[0][j]);
        if (s < bd) { bd = s; best = j; }
      }
      return [best];
    }
    for (var axis = 0; axis < 2; axis++) {
      best = 0; bd = Infinity;
      for (j = 0; j < books[axis].length; j++) {
        s = (v[axis] - books[axis][j][0]) * (v[axis] - books[axis][j][0]);
        if (s < bd) { bd = s; best = j; }
      }
      out.push(best);
    }
    return out;
  }

  function decode(code, books, m) {
    if (m === 1) return books[0][code[0]].slice();
    return [books[0][code[0]][0], books[1][code[1]][0]];
  }

  RV.MODELS.ann_pq = function (p) {
    var q = V.queryFor('pq'), k = p.k, m = p.m, bits = p.bits;
    var ix = train(m, bits);

    /* Asymmetric distance computation: the query stays exact, and the
     * distance to every code is read out of a table built once per query. */
    var table = [], axis, j;
    if (m === 1) {
      table.push(ix.books[0].map(function (c) { return V.d2(q, c); }));
    } else {
      for (axis = 0; axis < 2; axis++) {
        table.push(ix.books[axis].map(function (c) {
          var df = q[axis] - c[0];
          return df * df;
        }));
      }
    }
    var tableEntries = (m === 1 ? 1 : 2) * ix.ks;

    function run(qq) {
      var tb = [], ax;
      if (m === 1) {
        tb.push(ix.books[0].map(function (c) { return V.d2(qq, c); }));
      } else {
        for (ax = 0; ax < 2; ax++) {
          tb.push(ix.books[ax].map(function (c) {
            var df = qq[ax] - c[0];
            return df * df;
          }));
        }
      }
      return ix.codes.map(function (code, i) {
        return [m === 1 ? tb[0][code[0]] : tb[0][code[0]] + tb[1][code[1]], i];
      }).sort(function (a, b) { return a[0] - b[0]; })
        .slice(0, k).map(function (x) { return x[1]; });
    }
    var got = run(q);
    var truth = V.exactKNN(q, k);
    var r = V.recall(got, truth);
    var avgR = V.avgRecall(run, k);

    /* Reconstruction error, measured over the whole corpus. */
    var err = 0, i;
    for (i = 0; i < V.CORPUS.length; i++)
      err += Math.sqrt(V.d2(V.CORPUS[i], decode(ix.codes[i], ix.books, m)));
    err /= V.CORPUS.length;

    var s = V.stage();
    var gotSet = {}, truthSet = {};
    got.forEach(function (x) { gotSet[x] = 1; });
    truth.forEach(function (x) { truthSet[x] = 1; });

    /* The representable set: every point the index can possibly return a
     * position for. With m = 2 it is the grid; with m = 1 it is k dots. */
    if (m === 2) {
      ix.books[0].forEach(function (c) {
        s.appendChild(V.seg([c[0], 0], [c[0], 1],
          { stroke: 'var(--border-subtle)', sw: 0.5, opacity: 0.8 }));
      });
      ix.books[1].forEach(function (c) {
        s.appendChild(V.seg([0, c[0]], [1, c[0]],
          { stroke: 'var(--border-subtle)', sw: 0.5, opacity: 0.8 }));
      });
    }
    for (i = 0; i < V.CORPUS.length; i++) {
      s.appendChild(V.dot(V.CORPUS[i], {
        r: 1.6, fill: 'var(--text-muted)', fo: 0.3
      }));
    }
    /* Where each vector is actually stored: its reconstruction. Drawing the
     * displacement is the point - that arrow is the quantisation error. */
    for (i = 0; i < V.CORPUS.length; i += 4) {
      var rec = decode(ix.codes[i], ix.books, m);
      s.appendChild(V.seg(V.CORPUS[i], rec,
        { stroke: 'var(--vz-series-2)', sw: 0.6, opacity: 0.5 }));
    }
    truth.forEach(function (idx) {
      s.appendChild(V.dot(V.CORPUS[idx], {
        r: 3.4, fill: gotSet[idx] ? 'var(--accent-primary)' : 'var(--vz-series-warn)', fo: 1
      }));
      s.appendChild(V.dot(decode(ix.codes[idx], ix.books, m), {
        r: 2.6, fill: 'none', stroke: 'var(--accent-primary)', sw: 1.2, fo: 0
      }));
    });
    s.appendChild(V.queryMark(q));
    s.appendChild(V.label(12, 20,
      (m === 1 ? '1 codebook of ' : '2 codebooks of ') + ix.ks +
      ' -> ' + V.commas(m === 1 ? ix.ks : ix.ks * ix.ks) + ' representable points',
      { size: 9 }));
    V.legend(s, [['stored position', 'var(--vz-series-2)'],
                 ['true top-' + k, 'var(--accent-primary)'],
                 ['lost', 'var(--vz-series-warn)']]);
    V.makeDraggable(s, 'pq');

    /* The memory arithmetic, at a size anyone would actually run. */
    var codeBits = m * bits;
    var realM = p.m === 1 ? 1 : 96;   /* the usual choice at d = 768 */
    var realBytes = realM * bits / 8;
    var ratio = (V.REAL.d * 4) / realBytes;

    return {
      scene: s,
      bars: [
        { label: 'bytes per vector (at d=768, m=' + realM + ')',
          value: RV.round(realBytes, 1), max: V.REAL.d * 4,
          tag: 'against ' + (V.REAL.d * 4) + ' uncompressed - ' +
               Math.round(ratio) + 'x smaller',
          state: 'hit' },
        { label: 'recall@' + k + ' over 48 queries', value: RV.round(avgR, 3), max: 1,
          tag: 'against an exact search on the uncompressed vectors',
          state: avgR >= 0.8 ? 'hit' : 'bad' }
      ],
      stats: [
        ['subquantizers m', m],
        ['bits per code', bits],
        ['centroids per subspace', ix.ks],
        ['representable points', V.commas(m === 1 ? ix.ks : ix.ks * ix.ks)],
        ['code size (drawn, d=2)', codeBits + ' bits'],
        ['mean reconstruction error', RV.round(err, 4)],
        ['distance table per query', tableEntries + ' entries'],
        ['this query', 'recall ' + RV.round(r, 2)],
        ['index memory at 1 M', V.fmt(V.REAL.n * realBytes) + 'B']
      ],
      badge: 'recall ' + RV.round(avgR, 3),
      note: m === 1
        ? 'With one codebook this is plain vector quantisation: every vector is '
          + 'replaced by one of ' + ix.ks + ' centroids, and the index cannot '
          + 'distinguish two vectors that share one. Raise m to 2 and the same '
          + 'number of stored centroids describes ' + V.commas(ix.ks * ix.ks)
          + ' positions.'
        : 'Two codebooks of ' + ix.ks + ' centroids describe ' +
          V.commas(ix.ks * ix.ks) + ' positions - that multiplication is the '
          + 'whole trick. The blue lines are the quantisation error: what the '
          + 'index has forgotten about each vector.'
    };
  };
})();

/* ===========================================================================
 * IVF-PQ - the combination that actually ships.
 *
 * The one thing that is easy to miss: PQ is applied to the *residual* after
 * subtracting the cell centroid, not to the vector. So each cell gets the
 * codebook grid centred on itself, and the same number of bits buys much finer
 * resolution. Turning residuals off here shows exactly how much.
 * ======================================================================== */
(function () {
  'use strict';
  var RV = window.VizRagViz, V = window.VizAnnViz;
  if (!RV || !V) return;

  var CACHE = {};
  function build(nlist, bits, residual) {
    var key = nlist + '|' + bits + '|' + (residual ? 1 : 0);
    if (CACHE[key]) return CACHE[key];
    var km = V.kmeans(V.CORPUS, nlist, 18, 4242);
    var lists = [], i, axis;
    for (i = 0; i < nlist; i++) lists.push([]);
    for (i = 0; i < V.CORPUS.length; i++) lists[km.assign[i]].push(i);

    /* Train one pair of codebooks over all residuals (a single shared
     * codebook, which is what FAISS does - per-cell codebooks would be
     * nlist times the memory for very little gain). */
    var basis = V.CORPUS.map(function (p, idx) {
      var c = km.centroids[km.assign[idx]];
      return residual ? [p[0] - c[0], p[1] - c[1]] : [p[0], p[1]];
    });
    var ks = Math.pow(2, bits), books = [];
    for (axis = 0; axis < 2; axis++) {
      books.push(V.kmeans(basis.map(function (b) { return [b[axis]]; }),
                          ks, 20, 313 + axis, 1).centroids);
    }
    var codes = [];
    for (i = 0; i < V.CORPUS.length; i++) {
      var b = basis[i], code = [];
      for (axis = 0; axis < 2; axis++) {
        var best = 0, bd = Infinity;
        for (var j = 0; j < ks; j++) {
          var df = b[axis] - books[axis][j][0];
          if (df * df < bd) { bd = df * df; best = j; }
        }
        code.push(best);
      }
      codes.push(code);
    }
    CACHE[key] = { centroids: km.centroids, assign: km.assign, lists: lists,
                   books: books, codes: codes, ks: ks, residual: residual };
    return CACHE[key];
  }

  function reconstruct(ix, i) {
    var c = ix.centroids[ix.assign[i]];
    var rx = ix.books[0][ix.codes[i][0]][0], ry = ix.books[1][ix.codes[i][1]][0];
    return ix.residual ? [c[0] + rx, c[1] + ry] : [rx, ry];
  }

  RV.MODELS.ann_ivfpq = function (p) {
    var q = V.queryFor('ivfpq'), k = p.k;
    var nlist = p.nlist, nprobe = Math.min(p.nprobe, nlist);
    var ix = build(nlist, p.bits, !!p.residual);

    function run(qq) {
      var order = ix.centroids.map(function (c, i) { return [V.d2(qq, c), i]; })
                    .sort(function (a, b) { return a[0] - b[0]; });
      var probed = {}, candidates = [];
      order.slice(0, nprobe).forEach(function (o) {
        probed[o[1]] = 1;
        candidates = candidates.concat(ix.lists[o[1]]);
      });
      /* Scoring uses the reconstruction, never the stored vector - the index
       * does not have the stored vector in memory any more. */
      var scored = candidates.map(function (i) {
        return [V.d2(qq, reconstruct(ix, i)), i];
      }).sort(function (a, b) { return a[0] - b[0]; });
      var got;
      if (p.rerank > 0) {
        /* Rerank: re-read the full vectors for the shortlist and score them
         * exactly. This is what "refine" does in FAISS. */
        got = scored.slice(0, Math.max(k, p.rerank))
                .map(function (x) { return [V.d2(qq, V.CORPUS[x[1]]), x[1]]; })
                .sort(function (a, b) { return a[0] - b[0]; })
                .slice(0, k).map(function (x) { return x[1]; });
      } else {
        got = scored.slice(0, k).map(function (x) { return x[1]; });
      }
      return { got: got, probed: probed, candidates: candidates };
    }
    var here = run(q);
    var probed = here.probed, candidates = here.candidates, got = here.got;
    var truth = V.exactKNN(q, k);
    var r = V.recall(got, truth);
    var avgR = V.avgRecall(function (qq) { return run(qq).got; }, k);
    var avgC = V.avgCost(function (qq) { return run(qq).candidates.length; });
    var gotSet = {}, truthSet = {};
    got.forEach(function (i) { gotSet[i] = 1; });
    truth.forEach(function (i) { truthSet[i] = 1; });

    var s = V.stage();
    var i;
    for (i = 0; i < V.CORPUS.length; i++) {
      var open = probed[ix.assign[i]];
      s.appendChild(V.dot(V.CORPUS[i], {
        r: 1.5, fill: open ? 'var(--text-muted)' : 'var(--border-subtle)',
        fo: open ? 0.35 : 0.7
      }));
    }
    /* Where the index believes each probed vector is. */
    for (i = 0; i < V.CORPUS.length; i++) {
      if (!probed[ix.assign[i]]) continue;
      if (i % 2) continue;
      var rec = reconstruct(ix, i);
      s.appendChild(V.seg(V.CORPUS[i], rec,
        { stroke: 'var(--vz-series-2)', sw: 0.6, opacity: 0.55 }));
      s.appendChild(V.dot(rec, { r: 1.4, fill: 'var(--vz-series-2)', fo: 0.9 }));
    }
    ix.centroids.forEach(function (c, j) {
      s.appendChild(V.svgEl('rect', {
        x: V.px(c[0]) - 3.5, y: V.py(c[1]) - 3.5, width: 7, height: 7,
        fill: probed[j] ? 'var(--accent-fill)' : 'none', 'fill-opacity': 0.9,
        stroke: probed[j] ? 'var(--accent-primary)' : 'var(--text-muted)',
        'stroke-width': 1.2
      }));
    });
    truth.forEach(function (idx) {
      s.appendChild(V.dot(V.CORPUS[idx], {
        r: 3.4, fo: 1,
        fill: gotSet[idx] ? 'var(--accent-primary)' : 'var(--vz-series-warn)'
      }));
    });
    s.appendChild(V.queryMark(q));
    s.appendChild(V.label(12, 20, (ix.residual ? 'residual' : 'raw') +
      ' PQ  ·  ' + nprobe + '/' + nlist + ' cells  ·  ' +
      candidates.length + ' codes scanned', { size: 9 }));
    V.legend(s, [['stored (PQ code)', 'var(--vz-series-2)'],
                 ['found', 'var(--accent-primary)'],
                 ['lost', 'var(--vz-series-warn)']]);
    V.makeDraggable(s, 'ivfpq');

    var err = 0, cnt = 0;
    for (i = 0; i < V.CORPUS.length; i++) {
      err += Math.sqrt(V.d2(V.CORPUS[i], reconstruct(ix, i))); cnt++;
    }
    err /= cnt;

    var realM = 96, realBytes = realM * p.bits / 8;
    var ram = V.REAL.n * realBytes + nlist * V.REAL.d * 4;

    return {
      scene: s,
      bars: [
        { label: 'codes scanned (mean)', value: Math.round(avgC),
          max: V.CORPUS.length,
          tag: (avgC / V.CORPUS.length * 100).toFixed(1) + '% of the corpus, as ' +
               realBytes + '-byte codes rather than 3 KB vectors',
          state: 'hit' },
        { label: 'recall@' + k + ' over 48 queries', value: RV.round(avgR, 3), max: 1,
          tag: p.rerank > 0 ? 'after reranking the top ' + p.rerank + ' exactly'
                            : 'on the PQ approximation alone',
          state: avgR >= 0.85 ? 'hit' : 'bad' }
      ],
      stats: [
        ['nlist / nprobe', nlist + ' / ' + nprobe],
        ['bits per subquantizer', p.bits],
        ['quantise residuals', ix.residual ? 'yes' : 'no'],
        ['mean reconstruction error', RV.round(err, 4)],
        ['rerank shortlist', p.rerank || 'off'],
        ['this query', candidates.length + ' scanned, recall ' + RV.round(r, 2)],
        ['bytes/vector (d=768, m=96)', realBytes],
        ['RAM at 1 M vectors', V.fmt(ram) + 'B'],
        ['vs flat', V.fmt(V.flatBytes()) + 'B  (' +
          Math.round(V.flatBytes() / ram) + 'x)']
      ],
      badge: 'recall ' + RV.round(avgR, 3),
      note: !ix.residual
        ? 'With residuals off, one codebook has to describe the whole space, so '
          + 'the grid is coarse everywhere and the reconstruction error is large. '
          + 'Turn residuals on: the same bits now describe an offset from the '
          + 'cell centroid, and the error drops without a byte being added.'
        : (p.rerank > 0
            ? 'Reranking reads the full vectors for the shortlist and rescores '
              + 'them exactly. It costs ' + p.rerank + ' random reads and buys '
              + 'back most of the recall PQ gave away - which is why almost '
              + 'every production IVF-PQ setup does it.'
            : 'The PQ distance is an approximation, so the ordering near the top '
              + 'is unreliable even when the right vectors are in the candidate '
              + 'set. Turn on reranking and watch recall recover.')
    };
  };
})();

/* ===========================================================================
 * HNSW - a real layered proximity graph, really walked.
 *
 * The graph is built with the paper's insertion procedure (search the layers
 * above for entry points, collect efConstruction candidates, keep M by the
 * heuristic), and the search is the paper's greedy beam. The hop path drawn on
 * screen is the path the search actually took, which is why it changes shape
 * when you drag the query across a sparse region.
 * ======================================================================== */
(function () {
  'use strict';
  var RV = window.VizRagViz, V = window.VizAnnViz;
  if (!RV || !V) return;

  var CACHE = {};

  function build(M, efC) {
    var key = M + '|' + efC;
    if (CACHE[key]) return CACHE[key];
    var n = V.CORPUS.length, r = V.rng(555);
    var mL = 1 / Math.log(M > 1 ? M : 2);
    var level = new Int32Array(n), i;
    var maxLevel = 0, entry = 0;
    for (i = 0; i < n; i++) {
      level[i] = Math.floor(-Math.log(r() + 1e-12) * mL);
      if (level[i] > maxLevel) { maxLevel = level[i]; entry = i; }
    }
    /* links[l] is the adjacency for layer l. */
    var links = [];
    for (i = 0; i <= maxLevel; i++) links.push({});

    function neighbours(l, id) { return links[l][id] || (links[l][id] = []); }

    function searchLayer(q, entries, ef, l) {
      var visited = {}, cand = [], top = [], j;
      entries.forEach(function (e) {
        visited[e] = 1;
        var d = V.d2(q, V.CORPUS[e]);
        cand.push([d, e]); top.push([d, e]);
      });
      cand.sort(function (a, b) { return a[0] - b[0]; });
      top.sort(function (a, b) { return b[0] - a[0]; });
      while (cand.length) {
        var c = cand.shift();
        if (top.length >= ef && c[0] > top[0][0]) break;
        var ns = neighbours(l, c[1]);
        for (j = 0; j < ns.length; j++) {
          var e2 = ns[j];
          if (visited[e2]) continue;
          visited[e2] = 1;
          var d2v = V.d2(q, V.CORPUS[e2]);
          if (top.length < ef || d2v < top[0][0]) {
            cand.push([d2v, e2]);
            cand.sort(function (a, b) { return a[0] - b[0]; });
            top.push([d2v, e2]);
            top.sort(function (a, b) { return b[0] - a[0]; });
            if (top.length > ef) top.shift();
          }
        }
      }
      return top.slice().sort(function (a, b) { return a[0] - b[0]; });
    }

    /* The neighbour-selection heuristic: keep a candidate only if it is
     * closer to the new node than to any neighbour already kept. That is what
     * stops every edge pointing into the same dense blob and is why HNSW
     * stays navigable rather than collapsing into a clique. */
    function selectNeighbours(base, candidates, m) {
      var out = [];
      for (var i2 = 0; i2 < candidates.length && out.length < m; i2++) {
        var c = candidates[i2], keep = true;
        for (var j2 = 0; j2 < out.length; j2++) {
          if (V.d2(V.CORPUS[c[1]], V.CORPUS[out[j2][1]]) < c[0]) { keep = false; break; }
        }
        if (keep) out.push(c);
      }
      return out;
    }

    var inserted = [entry];
    for (i = 0; i < n; i++) {
      if (i === entry) continue;
      var q = V.CORPUS[i], ep = [entry], l;
      for (l = maxLevel; l > level[i]; l--) {
        var res = searchLayer(q, ep, 1, l);
        if (res.length) ep = [res[0][1]];
      }
      for (l = Math.min(level[i], maxLevel); l >= 0; l--) {
        var found = searchLayer(q, ep, efC, l);
        var chosen = selectNeighbours(i, found, l === 0 ? M * 2 : M);
        var mine = neighbours(l, i);
        chosen.forEach(function (c) {
          if (mine.indexOf(c[1]) === -1) mine.push(c[1]);
          var theirs = neighbours(l, c[1]);
          if (theirs.indexOf(i) === -1) theirs.push(i);
          var cap = l === 0 ? M * 2 : M;
          if (theirs.length > cap) {
            /* Prune with the same heuristic rather than dropping the last
             * arrival, which would make edge quality depend on insertion
             * order. */
            var re = theirs.map(function (t) {
              return [V.d2(V.CORPUS[c[1]], V.CORPUS[t]), t];
            }).sort(function (a, b) { return a[0] - b[0]; });
            var kept = selectNeighbours(c[1], re, cap);
            links[l][c[1]] = kept.map(function (x) { return x[1]; });
          }
        });
        ep = found.map(function (f) { return f[1]; });
      }
      inserted.push(i);
    }

    var edges = 0;
    for (i = 0; i <= maxLevel; i++)
      for (var kk in links[i]) if (links[i].hasOwnProperty(kk)) edges += links[i][kk].length;

    CACHE[key] = { links: links, level: level, entry: entry,
                   maxLevel: maxLevel, edges: edges / 2, searchLayer: searchLayer };
    return CACHE[key];
  }

  RV.MODELS.ann_hnsw = function (p) {
    var q = V.queryFor('hnsw'), k = p.k;
    var ix = build(p.M, p.efc);

    /* The query, run for real, recording the path so it can be drawn. */
    function run(qq, trace) {
      var seen = {}, hops = [], ep = [ix.entry], l;
      for (l = ix.maxLevel; l > 0; l--) {
        var res = ix.searchLayer(qq, ep, 1, l);
        res.forEach(function (x) { seen[x[1]] = 1; });
        if (res.length) {
          if (trace) hops.push([ep[0], res[0][1], l]);
          ep = [res[0][1]];
        }
      }
      /* efSearch is NOT clamped up to k. A candidate list narrower than k
       * cannot return k neighbours, and that is a real property of the
       * parameter rather than an edge case to paper over - an earlier version
       * clamped it and every efSearch below k behaved identically, which made
       * the page's most important control look broken. */
      var top = ix.searchLayer(qq, ep, p.ef, 0);
      top.forEach(function (x) { seen[x[1]] = 1; });
      return { got: top.slice(0, k).map(function (x) { return x[1]; }),
               seen: seen, hops: hops, visited: Object.keys(seen).length };
    }
    var here = run(q, true);
    var visited = here.seen, path = here.hops, got = here.got;
    var truth = V.exactKNN(q, k);
    var r = V.recall(got, truth);
    var nVisited = here.visited;
    var avgR = V.avgRecall(function (qq) { return run(qq).got; }, k);
    var avgV = V.avgCost(function (qq) { return run(qq).visited; });

    var gotSet = {}, truthSet = {};
    got.forEach(function (i) { gotSet[i] = 1; });
    truth.forEach(function (i) { truthSet[i] = 1; });

    var s = V.stage();
    var i, j;
    /* Layer-0 edges, faint, then the higher layers picked out - the long hops
     * are the whole reason the structure works. */
    var showLayer = Math.min(p.layer, ix.maxLevel);
    var lk = ix.links[showLayer] || {};
    for (var id in lk) if (lk.hasOwnProperty(id)) {
      for (j = 0; j < lk[id].length; j++) {
        if (+id > lk[id][j]) continue;
        s.appendChild(V.seg(V.CORPUS[+id], V.CORPUS[lk[id][j]], {
          stroke: 'var(--border-subtle)', sw: showLayer ? 0.9 : 0.4,
          opacity: showLayer ? 0.9 : 0.55
        }));
      }
    }
    for (i = 0; i < V.CORPUS.length; i++) {
      var onLayer = ix.level[i] >= showLayer;
      s.appendChild(V.dot(V.CORPUS[i], {
        r: truthSet[i] ? 3.4 : (visited[i] ? 2.4 : (onLayer ? 1.8 : 1.3)),
        fill: truthSet[i] ? (gotSet[i] ? 'var(--accent-primary)' : 'var(--vz-series-warn)')
             : visited[i] ? 'var(--vz-series-2)' : 'var(--text-muted)',
        fo: truthSet[i] || visited[i] ? 1 : (onLayer ? 0.45 : 0.18)
      }));
    }
    path.forEach(function (h) {
      s.appendChild(V.seg(V.CORPUS[h[0]], V.CORPUS[h[1]], {
        stroke: 'var(--accent-primary)', sw: 1.6, opacity: 0.85
      }));
    });
    s.appendChild(V.dot(V.CORPUS[ix.entry], {
      r: 4, fill: 'none', stroke: 'var(--accent-primary)', sw: 1.6, fo: 0
    }));
    s.appendChild(V.queryMark(q));
    s.appendChild(V.label(12, 20, 'layer ' + showLayer + ' of ' + ix.maxLevel +
      '  ·  ' + nVisited + ' nodes visited  ·  ' + path.length + ' descent hops',
      { size: 9 }));
    V.legend(s, [['visited', 'var(--vz-series-2)'],
                 ['found', 'var(--accent-primary)'],
                 ['missed', 'var(--vz-series-warn)']]);
    V.makeDraggable(s, 'hnsw');

    var frac = nVisited / V.CORPUS.length;
    var graphBytes = V.REAL.n * p.M * 2 * 4;
    var total = V.flatBytes() + graphBytes;

    return {
      scene: s,
      bars: [
        { label: 'nodes visited (mean)', value: Math.round(avgV),
          max: V.CORPUS.length,
          tag: (avgV / V.CORPUS.length * 100).toFixed(1) +
               '% of the corpus, reached by following edges',
          state: 'hit' },
        { label: 'recall@' + k + ' over 48 queries', value: RV.round(avgR, 3), max: 1,
          tag: r === 1 ? 'the drawn query reached the true neighbourhood'
                       : 'the drawn query settled somewhere good but not best',
          state: avgR >= 0.9 ? 'hit' : 'bad' }
      ],
      stats: [
        ['M (edges/node)', p.M],
        ['efConstruction', p.efc],
        ['efSearch', p.ef],
        ['layers', ix.maxLevel + 1],
        ['edges in graph', V.commas(Math.round(ix.edges))],
        ['corpus touched (mean)', (avgV / V.CORPUS.length * 100).toFixed(1) + '%'],
        ['this query', nVisited + ' visited, recall ' + RV.round(r, 2)],
        ['graph memory at 1 M', V.fmt(graphBytes) + 'B'],
        ['total vs flat', V.fmt(total) + 'B  (+' +
          Math.round(graphBytes / V.flatBytes() * 100) + '%)']
      ],
      badge: 'recall ' + RV.round(avgR, 3),
      note: p.M <= 4
        ? 'A poorly connected graph caps recall no matter how large efSearch '
          + 'gets: the walk simply has nowhere better to go. Build-time damage '
          + 'cannot be repaired at query time.'
        : (p.ef <= 4
            ? 'With efSearch this small the search keeps almost no alternatives, '
              + 'so one wrong greedy step is unrecoverable. Raise it and watch '
              + 'the visited count and the recall climb together.'
            : 'Set the layer control to 1 or 2 to see the long edges - a few '
              + 'hops up there cross most of the space, and the dense bottom '
              + 'layer does the precise work.')
    };
  };
})();

/* ===========================================================================
 * DiskANN / Vamana - one flat graph, built so that a beam search reaches
 * anything in a few hops, because every hop is an SSD read.
 *
 * The alpha-pruning rule is the whole paper and it is implemented here rather
 * than described: a candidate edge survives only if no already-kept neighbour
 * is more than alpha times closer to it. At alpha = 1 that is HNSW's
 * heuristic and the graph is all short edges; above 1 it deliberately keeps
 * some long ones, which is what collapses the hop count.
 * ======================================================================== */
(function () {
  'use strict';
  var RV = window.VizRagViz, V = window.VizAnnViz;
  if (!RV || !V) return;

  var CACHE = {};

  function build(R, alpha) {
    var key = R + '|' + alpha;
    if (CACHE[key]) return CACHE[key];
    var n = V.CORPUS.length, i, j;
    var r = V.rng(88);

    /* Medoid entry point: the vector closest to the centroid of everything.
     * A single fixed entry, unlike HNSW's random top layer. */
    var cx = 0, cy = 0;
    for (i = 0; i < n; i++) { cx += V.CORPUS[i][0] / n; cy += V.CORPUS[i][1] / n; }
    var medoid = 0, bd = Infinity;
    for (i = 0; i < n; i++) {
      var d = V.d2([cx, cy], V.CORPUS[i]);
      if (d < bd) { bd = d; medoid = i; }
    }

    /* Start from a random R-regular graph, then prune it twice - the two
     * passes are what Vamana specifies, and the second is what fixes the
     * damage the first one's ordering does. */
    var adj = [];
    for (i = 0; i < n; i++) {
      var set = {};
      while (Object.keys(set).length < Math.min(R, n - 1)) {
        var c = Math.floor(r() * n);
        if (c !== i) set[c] = 1;
      }
      adj.push(Object.keys(set).map(Number));
    }

    function robustPrune(node, candidates, a) {
      var pool = candidates.filter(function (c) { return c !== node; })
        .map(function (c) { return [V.d2(V.CORPUS[node], V.CORPUS[c]), c]; })
        .sort(function (x, y) { return x[0] - y[0]; });
      var out = [];
      while (pool.length && out.length < R) {
        var best = pool.shift();
        out.push(best[1]);
        pool = pool.filter(function (c) {
          /* Keep c only if the already-chosen neighbour is NOT much closer to
           * it than the node is - otherwise the edge to c is redundant, since
           * the search can reach c through the neighbour. The rule is stated
           * on distances, and everything here is squared, so the factor is
           * alpha squared. Getting that wrong prunes far too hard and the
           * average degree collapses to a third of R. */
          return a * a * V.d2(V.CORPUS[best[1]], V.CORPUS[c[1]]) > c[0];
        });
      }
      return out;
    }

    /* Beam search, as Vamana specifies it: keep a candidate list of size L,
     * repeatedly expand its closest *unvisited* member, and stop when every
     * member has been visited. L bounds the list, not the number of visits -
     * an earlier version stopped after L expansions, which made the read
     * count exactly equal to L on every query and the headline number
     * meaningless. The count varies now because a query landing in a
     * well-connected region genuinely converges sooner. */
    function greedy(qv, ep, L) {
      var visited = {}, seen = {}, out = [];
      var cand = [[V.d2(qv, V.CORPUS[ep]), ep]];
      seen[ep] = 1;
      var guard = 0;
      while (guard++ < 4000) {
        cand.sort(function (a2, b2) { return a2[0] - b2[0]; });
        if (cand.length > L) cand = cand.slice(0, L);
        var next = null, ci;
        for (ci = 0; ci < cand.length; ci++) {
          if (!visited[cand[ci][1]]) { next = cand[ci]; break; }
        }
        if (!next) break;                     /* every candidate expanded */
        visited[next[1]] = 1;
        out.push(next[1]);
        adj[next[1]].forEach(function (nb) {
          if (seen[nb]) return;
          seen[nb] = 1;
          cand.push([V.d2(qv, V.CORPUS[nb]), nb]);
        });
      }
      return { visited: out, pool: cand };
    }

    [1.0, alpha].forEach(function (a) {
      var order = [];
      for (i = 0; i < n; i++) order.push(i);
      for (i = n - 1; i > 0; i--) {
        j = Math.floor(r() * (i + 1));
        var t = order[i]; order[i] = order[j]; order[j] = t;
      }
      order.forEach(function (node) {
        var res = greedy(V.CORPUS[node], medoid, Math.max(R, 24));
        adj[node] = robustPrune(node, res.visited.concat(adj[node]), a);
        adj[node].forEach(function (nb) {
          if (adj[nb].indexOf(node) === -1) {
            adj[nb] = adj[nb].concat([node]);
            if (adj[nb].length > R) adj[nb] = robustPrune(nb, adj[nb], a);
          }
        });
      });
    });

    var deg = 0, longEdges = 0;
    for (i = 0; i < n; i++) {
      deg += adj[i].length;
      for (j = 0; j < adj[i].length; j++)
        if (Math.sqrt(V.d2(V.CORPUS[i], V.CORPUS[adj[i][j]])) > 0.25) longEdges++;
    }
    CACHE[key] = { adj: adj, medoid: medoid, greedy: greedy,
                   avgDeg: deg / n, longEdges: longEdges / 2 };
    return CACHE[key];
  }

  RV.MODELS.ann_diskann = function (p) {
    var q = V.queryFor('diskann'), k = p.k;
    var ix = build(p.R, p.alpha / 10);
    function run(qq) {
      var res = ix.greedy(qq, ix.medoid, p.L);
      return {
        visited: res.visited,
        got: res.visited.map(function (i) { return [V.d2(qq, V.CORPUS[i]), i]; })
               .sort(function (a, b) { return a[0] - b[0]; })
               .slice(0, k).map(function (x) { return x[1]; })
      };
    }
    var here = run(q);
    var visited = here.visited, got = here.got;
    var truth = V.exactKNN(q, k);
    var r = V.recall(got, truth);
    var avgR = V.avgRecall(function (qq) { return run(qq).got; }, k);
    var avgReads = V.avgCost(function (qq) { return run(qq).visited.length; });

    var vis = {}, gotSet = {}, truthSet = {};
    visited.forEach(function (i) { vis[i] = 1; });
    got.forEach(function (i) { gotSet[i] = 1; });
    truth.forEach(function (i) { truthSet[i] = 1; });

    var s = V.stage();
    var i, j;
    for (i = 0; i < V.CORPUS.length; i++) {
      if (!p.edges && !vis[i]) continue;
      for (j = 0; j < ix.adj[i].length; j++) {
        if (i > ix.adj[i][j]) continue;
        var isLong = Math.sqrt(V.d2(V.CORPUS[i], V.CORPUS[ix.adj[i][j]])) > 0.25;
        s.appendChild(V.seg(V.CORPUS[i], V.CORPUS[ix.adj[i][j]], {
          stroke: isLong ? 'var(--vz-series-2)' : 'var(--border-subtle)',
          sw: isLong ? 0.7 : 0.4, opacity: isLong ? 0.7 : 0.4
        }));
      }
    }
    for (i = 0; i < V.CORPUS.length; i++) {
      s.appendChild(V.dot(V.CORPUS[i], {
        r: truthSet[i] ? 3.4 : (vis[i] ? 2.3 : 1.3),
        fill: truthSet[i] ? (gotSet[i] ? 'var(--accent-primary)' : 'var(--vz-series-warn)')
             : vis[i] ? 'var(--vz-series-2)' : 'var(--text-muted)',
        fo: truthSet[i] || vis[i] ? 1 : 0.25
      }));
    }
    s.appendChild(V.dot(V.CORPUS[ix.medoid], {
      r: 5, fill: 'none', stroke: 'var(--accent-primary)', sw: 1.6, fo: 0
    }));
    s.appendChild(V.queryMark(q));
    s.appendChild(V.label(12, 20, 'alpha ' + (p.alpha / 10).toFixed(1) +
      '  ·  ' + Math.round(ix.longEdges) + ' long edges  ·  ' +
      visited.length + ' nodes read', { size: 9 }));
    V.legend(s, [['long edge', 'var(--vz-series-2)'],
                 ['read from SSD', 'var(--vz-series-2)'],
                 ['found', 'var(--accent-primary)']]);
    V.makeDraggable(s, 'diskann');

    /* The cost that matters is reads, not FLOPs: an NVMe random read is
     * about 100 microseconds, and a distance is nanoseconds. */
    var reads = visited.length;
    var readMs = avgReads * 0.1;
    var pqRam = V.REAL.n * 32;
    var disk = V.flatBytes() + V.REAL.n * p.R * 4;

    return {
      scene: s,
      bars: [
        { label: 'SSD reads per query (mean)', value: Math.round(avgReads), max: 300,
          tag: 'one page per node visited - this, not arithmetic, is the cost',
          state: avgReads > 150 ? 'bad' : 'hit' },
        { label: 'recall@' + k + ' over 48 queries', value: RV.round(avgR, 3), max: 1,
          tag: 'beam width L = ' + p.L,
          state: avgR >= 0.9 ? 'hit' : 'bad' }
      ],
      stats: [
        ['R (max degree)', p.R],
        ['alpha', (p.alpha / 10).toFixed(1)],
        ['L (beam width)', p.L],
        ['average degree', RV.round(ix.avgDeg, 1)],
        ['long edges kept', Math.round(ix.longEdges)],
        ['this query', reads + ' reads, recall ' + RV.round(r, 2)],
        ['estimated latency', readMs.toFixed(1) + ' ms of I/O'],
        ['RAM at 1 M (PQ codes)', V.fmt(pqRam) + 'B'],
        ['SSD at 1 M', V.fmt(disk) + 'B']
      ],
      badge: 'recall ' + RV.round(avgR, 3),
      note: p.alpha <= 10
        ? 'At alpha = 1.0 the pruning keeps only short edges, so the graph is a '
          + 'careful local mesh and the search has to crawl across it - many '
          + 'hops, and every hop is a disk read. Raise alpha.'
        : 'The blue edges are the long ones alpha kept. They are what lets a '
          + 'search starting at the medoid arrive in a handful of hops, which '
          + 'is the difference between a graph that lives in RAM and one that '
          + 'lives on an SSD.'
    };
  };
})();

/* ===========================================================================
 * Annoy - a forest of random projection trees.
 *
 * Each tree splits on the hyperplane bisecting two randomly chosen points,
 * recursively, until a node holds few enough vectors. One tree is a poor
 * index; the union of many is a good one, and the reason is visible - each
 * tree cuts the space differently, so a neighbour separated by one boundary
 * is usually together in another.
 * ======================================================================== */
(function () {
  'use strict';
  var RV = window.VizRagViz, V = window.VizAnnViz;
  if (!RV || !V) return;

  var CACHE = {};

  function buildTree(ids, r, leafSize, depth) {
    if (ids.length <= leafSize || depth > 12) return { leaf: ids };
    var a = ids[Math.floor(r() * ids.length)], b = ids[Math.floor(r() * ids.length)];
    var guard = 0;
    while (b === a && guard++ < 20) b = ids[Math.floor(r() * ids.length)];
    var pa = V.CORPUS[a], pb = V.CORPUS[b];
    /* The split plane: normal along pa->pb, through the midpoint. */
    var nx = pb[0] - pa[0], ny = pb[1] - pa[1];
    var mx = (pa[0] + pb[0]) / 2, my = (pa[1] + pb[1]) / 2;
    var off = nx * mx + ny * my;
    if (Math.abs(nx) + Math.abs(ny) < 1e-9) return { leaf: ids };
    var left = [], right = [];
    ids.forEach(function (i) {
      var side = nx * V.CORPUS[i][0] + ny * V.CORPUS[i][1] - off;
      (side <= 0 ? left : right).push(i);
    });
    if (!left.length || !right.length) return { leaf: ids };
    return {
      n: [nx, ny], off: off,
      left: buildTree(left, r, leafSize, depth + 1),
      right: buildTree(right, r, leafSize, depth + 1)
    };
  }

  function forest(nTrees, leafSize) {
    var key = nTrees + '|' + leafSize;
    if (CACHE[key]) return CACHE[key];
    var ids = [], i;
    for (i = 0; i < V.CORPUS.length; i++) ids.push(i);
    var trees = [];
    for (i = 0; i < nTrees; i++) trees.push(buildTree(ids, V.rng(1000 + i * 17), leafSize, 0));
    CACHE[key] = trees;
    return trees;
  }

  /* Annoy's actual search: one priority queue over the roots of *all* trees
   * at once, keyed by how far the query sits from each split plane. Pop the
   * most promising node, descend, and stop once search_k candidates have been
   * collected. Descending one tree fully and then the next would explore the
   * wrong nodes - the budget belongs to the forest, not to a tree. */
  function searchForest(trees, q, searchK, showIdx, planes) {
    var queue = [], cand = {}, count = 0, shown = [];
    trees.forEach(function (t, ti) {
      queue.push([Infinity, t, ti]);
    });
    while (queue.length && count < searchK) {
      queue.sort(function (a, b) { return b[0] - a[0]; });
      var top = queue.shift();
      var node = top[1], ti = top[2];
      if (node.leaf) {
        node.leaf.forEach(function (i) {
          if (!cand[i]) { cand[i] = 1; count++; }
        });
        if (ti === showIdx) shown.push(node.leaf);
        continue;
      }
      var margin = node.n[0] * q[0] + node.n[1] * q[1] - node.off;
      if (ti === showIdx && planes) planes.push(node);
      /* The near child inherits the parent's priority; the far child is
       * queued at the distance to the plane, so a query sitting close to a
       * boundary explores both sides and one deep inside a cell does not. */
      var near = margin <= 0 ? node.left : node.right;
      var far = margin <= 0 ? node.right : node.left;
      queue.push([top[0], near, ti]);
      queue.push([Math.min(top[0], Math.abs(margin)), far, ti]);
    }
    return { cand: cand, count: count, shown: shown };
  }

  RV.MODELS.ann_annoy = function (p) {
    var q = V.queryFor('annoy'), k = p.k;
    var trees = forest(p.trees, p.leaf);

    function run(qq, planesOut, showIdx) {
      var res = searchForest(trees, qq, p.searchk,
                             showIdx === undefined ? -1 : showIdx, planesOut);
      var ids = Object.keys(res.cand).map(Number);
      return {
        cand: res.cand, shown: res.shown, ids: ids,
        got: ids.map(function (i) { return [V.d2(qq, V.CORPUS[i]), i]; })
               .sort(function (a, b) { return a[0] - b[0]; })
               .slice(0, k).map(function (x) { return x[1]; })
      };
    }
    var planes = [];
    var here = run(q, planes, p.show);
    var cand = here.cand, leaves = here.shown, candidates = here.ids;
    var count = candidates.length;
    var got = here.got;
    var truth = V.exactKNN(q, k);
    var r = V.recall(got, truth);
    var avgR = V.avgRecall(function (qq) { return run(qq).got; }, k);
    var avgC = V.avgCost(function (qq) { return run(qq).ids.length; });
    var gotSet = {}, truthSet = {}, leafSet = {};
    got.forEach(function (i) { gotSet[i] = 1; });
    truth.forEach(function (i) { truthSet[i] = 1; });
    leaves.forEach(function (l) { l.forEach(function (i) { leafSet[i] = 1; }); });

    var s = V.stage();
    var i;
    /* The split planes of the tree being shown, clipped to the unit square. */
    planes.forEach(function (node) {
      var nx = node.n[0], ny = node.n[1], off = node.off, pts = [];
      [[0, null], [1, null], [null, 0], [null, 1]].forEach(function (edge) {
        if (edge[0] !== null && Math.abs(ny) > 1e-9) {
          var y = (off - nx * edge[0]) / ny;
          if (y >= 0 && y <= 1) pts.push([edge[0], y]);
        }
        if (edge[1] !== null && Math.abs(nx) > 1e-9) {
          var x = (off - ny * edge[1]) / nx;
          if (x >= 0 && x <= 1) pts.push([x, edge[1]]);
        }
      });
      if (pts.length >= 2) s.appendChild(V.seg(pts[0], pts[1], {
        stroke: 'var(--vz-series-2)', sw: 0.8, opacity: 0.7
      }));
    });
    for (i = 0; i < V.CORPUS.length; i++) {
      s.appendChild(V.dot(V.CORPUS[i], {
        r: truthSet[i] ? 3.4 : (cand[i] ? 2.1 : 1.3),
        fill: truthSet[i] ? (gotSet[i] ? 'var(--accent-primary)' : 'var(--vz-series-warn)')
             : leafSet[i] ? 'var(--vz-series-2)'
             : cand[i] ? 'var(--text-muted)' : 'var(--border-subtle)',
        fo: truthSet[i] ? 1 : (leafSet[i] ? 0.9 : (cand[i] ? 0.5 : 0.7))
      }));
    }
    s.appendChild(V.queryMark(q));
    s.appendChild(V.label(12, 20, p.trees + ' trees  ·  showing tree ' +
      (p.show + 1) + '  ·  ' + count + ' candidates from the union', { size: 9 }));
    V.legend(s, [['this tree’s leaves', 'var(--vz-series-2)'],
                 ['other trees', 'var(--text-muted)', 0.5],
                 ['found', 'var(--accent-primary)'],
                 ['missed', 'var(--vz-series-warn)']]);
    V.makeDraggable(s, 'annoy');

    var frac = count / V.CORPUS.length;
    var treeBytes = V.REAL.n * p.trees * 12;

    return {
      scene: s,
      bars: [
        { label: 'candidates, union of all trees (mean)', value: Math.round(avgC),
          max: V.CORPUS.length,
          tag: (avgC / V.CORPUS.length * 100).toFixed(1) +
               '% of the corpus, then rescored exactly',
          state: avgC / V.CORPUS.length > 0.5 ? 'bad' : 'hit' },
        { label: 'recall@' + k + ' over 48 queries', value: RV.round(avgR, 3), max: 1,
          tag: p.trees === 1 ? 'one tree - a bad split is unrecoverable'
                             : p.trees + ' independent partitions, unioned',
          state: avgR >= 0.9 ? 'hit' : 'bad' }
      ],
      stats: [
        ['n_trees', p.trees],
        ['leaf size', p.leaf],
        ['search_k budget', p.searchk],
        ['candidates (this query)', count],
        ['corpus touched (mean)', (avgC / V.CORPUS.length * 100).toFixed(1) + '%'],
        ['index at 1 M', V.fmt(V.flatBytes() + treeBytes) + 'B'],
        ['of which trees', V.fmt(treeBytes) + 'B'],
        ['updates', 'rebuild only']
      ],
      badge: 'recall ' + RV.round(avgR, 3),
      note: p.trees === 1
        ? 'One tree is a poor index: any neighbour on the far side of a split '
          + 'is invisible, and the splits are random. Add trees and watch the '
          + 'misses disappear - each new partition is a fresh chance to keep '
          + 'the query and its neighbours together.'
        : 'Every tree cuts the space differently, so a neighbour separated by a '
          + 'boundary in one tree is usually kept in another. That is the whole '
          + 'design: cheap independent partitions, and the union as the '
          + 'candidate set.'
    };
  };
})();

/* ===========================================================================
 * ScaNN - anisotropic vector quantization.
 *
 * Every other quantiser on these pages minimises plain squared reconstruction
 * error, which treats all error as equally bad. ScaNN's observation is that
 * for maximum inner product search it is not: the component of the error
 * *parallel* to the vector changes the inner product with any query that
 * scores the vector highly, while the perpendicular component largely cancels.
 * So weight the parallel part more.
 *
 * This page decomposes the error for a real assignment and lets you move the
 * weight, so you can watch a vector change which centroid it belongs to - and
 * watch the recall of the top results change with it.
 * ======================================================================== */
(function () {
  'use strict';
  var RV = window.VizRagViz, V = window.VizAnnViz;
  if (!RV || !V) return;

  var CACHE = {};

  /* The corpus, re-centred on the origin, because inner product only means
   * anything with respect to a direction from somewhere. */
  var CENTRED = V.CORPUS.map(function (p) { return [p[0] - 0.5, p[1] - 0.5]; });

  function codebook(ks) {
    if (CACHE[ks]) return CACHE[ks];
    CACHE[ks] = V.kmeans(CENTRED, ks, 25, 606, 2).centroids;
    return CACHE[ks];
  }

  /* The anisotropic loss: split the residual into the part along x and the
   * part across it, and weight them differently. eta = 1 is plain squared
   * error; larger eta says a parallel error is worse. */
  function anisoCost(x, c, eta) {
    var nx = Math.sqrt(x[0] * x[0] + x[1] * x[1]) || 1e-9;
    var ux = [x[0] / nx, x[1] / nx];
    var rx = c[0] - x[0], ry = c[1] - x[1];
    var par = rx * ux[0] + ry * ux[1];
    var perpX = rx - par * ux[0], perpY = ry - par * ux[1];
    var perp2 = perpX * perpX + perpY * perpY;
    return { total: eta * par * par + perp2, par: par * par, perp: perp2 };
  }

  function assign(ks, eta) {
    var book = codebook(ks), out = new Int32Array(CENTRED.length), i, j;
    for (i = 0; i < CENTRED.length; i++) {
      var best = 0, bd = Infinity;
      for (j = 0; j < ks; j++) {
        var c = anisoCost(CENTRED[i], book[j], eta).total;
        if (c < bd) { bd = c; best = j; }
      }
      out[i] = best;
    }
    return { book: book, code: out };
  }

  RV.MODELS.ann_scann = function (p) {
    var qRaw = V.queryFor('scann');
    var q = [qRaw[0] - 0.5, qRaw[1] - 0.5];
    var k = p.k, eta = p.eta / 10, ks = p.ks;

    var aniso = assign(ks, eta);
    var plain = assign(ks, 1);

    /* Maximum inner product, scored against the quantised vectors. */
    function search(a, qq) {
      var shortlist = CENTRED.map(function (x, i) {
        var c = a.book[a.code[i]];
        return [-(qq[0] * c[0] + qq[1] * c[1]), i];
      }).sort(function (u, v) { return u[0] - v[0]; })
        .slice(0, Math.max(k, p.rerank)).map(function (u) { return u[1]; });
      if (p.rerank > 0) {
        return shortlist.map(function (i) {
          return [-(qq[0] * CENTRED[i][0] + qq[1] * CENTRED[i][1]), i];
        }).sort(function (u, v) { return u[0] - v[0]; })
          .slice(0, k).map(function (u) { return u[1]; });
      }
      return shortlist.slice(0, k);
    }
    function exactIP(qq, kk) {
      return CENTRED.map(function (x, i) {
        return [-(qq[0] * x[0] + qq[1] * x[1]), i];
      }).sort(function (u, v) { return u[0] - v[0]; })
        .slice(0, kk).map(function (u) { return u[1]; });
    }

    var truth = exactIP(q, k);
    var gotA = search(aniso, q), gotP = search(plain, q);
    var rHereA = V.recall(gotA, truth), rHereP = V.recall(gotP, truth);

    /* The claim this page exists to test is about a *workload*, not a query:
     * for any single query the plain objective can easily win. Averaging over
     * the probe set - each recentred the same way, each scored against its own
     * exact MIPS answer - is the only measurement that can support it, and it
     * is cheap enough to redo on every slider move. */
    function meanRecall(a) {
      var tot = 0, i2;
      for (i2 = 0; i2 < V.PROBES.length; i2++) {
        var pq = [V.PROBES[i2][0] - 0.5, V.PROBES[i2][1] - 0.5];
        tot += V.recall(search(a, pq), exactIP(pq, k));
      }
      return tot / V.PROBES.length;
    }
    var rA = meanRecall(aniso), rP = meanRecall(plain);

    /* How many vectors the two objectives assign differently. */
    var moved = 0, i;
    for (i = 0; i < CENTRED.length; i++) if (aniso.code[i] !== plain.code[i]) moved++;

    var gotSet = {}, truthSet = {};
    gotA.forEach(function (x) { gotSet[x] = 1; });
    truth.forEach(function (x) { truthSet[x] = 1; });

    var s = V.stage();
    function back(x) { return [x[0] + 0.5, x[1] + 0.5]; }
    /* The query direction: everything on this page is about it. */
    var scale = 0.48 / (Math.sqrt(q[0] * q[0] + q[1] * q[1]) || 1e-9);
    s.appendChild(V.seg(back([0, 0]), back([q[0] * scale, q[1] * scale]), {
      stroke: 'var(--accent-primary)', sw: 1.2, dash: '5 4', opacity: 0.8
    }));
    for (i = 0; i < CENTRED.length; i++) {
      var changed = aniso.code[i] !== plain.code[i];
      s.appendChild(V.dot(back(CENTRED[i]), {
        r: truthSet[i] ? 3.4 : (changed ? 2.2 : 1.4),
        fill: truthSet[i] ? (gotSet[i] ? 'var(--accent-primary)' : 'var(--vz-series-warn)')
             : changed ? 'var(--vz-series-2)' : 'var(--text-muted)',
        fo: truthSet[i] ? 1 : (changed ? 0.85 : 0.25)
      }));
      if (changed && i % 3 === 0) {
        s.appendChild(V.seg(back(CENTRED[i]), back(aniso.book[aniso.code[i]]), {
          stroke: 'var(--vz-series-2)', sw: 0.5, opacity: 0.45
        }));
      }
    }
    aniso.book.forEach(function (c) {
      s.appendChild(V.svgEl('rect', {
        x: V.px(c[0] + 0.5) - 3, y: V.py(c[1] + 0.5) - 3, width: 6, height: 6,
        fill: 'var(--accent-fill)', 'fill-opacity': 0.85,
        stroke: 'var(--accent-primary)', 'stroke-width': 1
      }));
    });
    s.appendChild(V.queryMark(qRaw));
    s.appendChild(V.label(12, 20, 'eta ' + eta.toFixed(1) + '  ·  ' + moved +
      ' of ' + CENTRED.length + ' vectors assigned differently', { size: 9 }));
    V.legend(s, [['moved by anisotropy', 'var(--vz-series-2)'],
                 ['found', 'var(--accent-primary)'],
                 ['missed', 'var(--vz-series-warn)']]);
    V.makeDraggable(s, 'scann');

    /* The error decomposition for one vector - the argument, in numbers. */
    var sample = truth[0] === undefined ? 0 : truth[0];
    var ca = anisoCost(CENTRED[sample], aniso.book[aniso.code[sample]], eta);
    var cp = anisoCost(CENTRED[sample], plain.book[plain.code[sample]], eta);

    return {
      scene: s,
      bars: [
        { label: 'MIPS recall@' + k + ', anisotropic loss  (48 queries)',
          value: RV.round(rA, 3), max: 1,
          tag: 'eta = ' + eta.toFixed(1) + ', error along the vector weighted ' +
               eta.toFixed(1) + 'x',
          state: rA >= rP ? 'hit' : 'bad' },
        { label: 'MIPS recall@' + k + ', plain squared error  (48 queries)',
          value: RV.round(rP, 3), max: 1,
          tag: 'the objective every other quantiser on these pages uses',
          state: rP > rA ? 'hit' : 'dim' }
      ],
      stats: [
        ['eta (parallel weight)', eta.toFixed(1)],
        ['centroids', ks],
        ['assignments changed', moved],
        ['gain over plain loss', ((rA - rP) >= 0 ? '+' : '') +
          RV.round((rA - rP) * 100, 1) + ' points'],
        ['the drawn query', RV.round(rHereA, 2) + ' vs ' + RV.round(rHereP, 2)],
        ['top result: parallel err', RV.round(ca.par, 5)],
        ['top result: perpendicular', RV.round(ca.perp, 5)],
        ['plain-loss parallel err', RV.round(cp.par, 5)],
        ['rerank shortlist', p.rerank || 'off'],
        ['bytes/vector at d=768', '~' + Math.round(768 / 8 * 2) + ' (2-bit AVQ)']
      ],
      badge: 'aniso ' + RV.round(rA, 2) + ' vs plain ' + RV.round(rP, 2),
      note: eta <= 1.05
        ? 'At eta = 1 this is ordinary k-means: every direction of error costs '
          + 'the same, and the assignment is identical to the plain one. Raise '
          + 'eta and vectors start changing centroid - the blue ones.'
        : 'The blue vectors chose a different centroid once error along their '
          + 'own direction was made expensive. For the single drawn query the '
          + 'two can easily trade places - drag it and watch. The bars are the '
          + 'average over 48 queries, which is the only level at which the '
          + 'claim is either true or false, and where the paper makes it.'
    };
  };
})();
