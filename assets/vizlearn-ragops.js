/* The interactive models for the RAG operations pages in gen_ai/.
 *
 * These are the pages about running a retrieval pipeline rather than scoring
 * one: gating, abstention, de-duplication, chunk-size sweeps, capacity,
 * latency, failure handling, ingestion and migration. Each registers one model
 * into window.VizRagViz.MODELS, the same harness the other generated gen_ai/
 * pages use, so the layout, controls and readout are shared.
 *
 * Every number on screen is computed here from the control values. Where a
 * model needs a measured curve (chunk size against recall, say) the points are
 * stored in the page's own data and interpolated, so the reader can see what
 * the curve is built from. None of these are benchmarks of a real system; they
 * are small worked models whose arithmetic matches the page's text.
 *
 * Loaded only on pages that carry data-vz-ops. It must come after
 * vizlearn-ragviz.js, which creates window.VizRagViz.
 */
(function () {
  'use strict';

  var V = window.VizRagViz;
  if (!V) return;
  var M = V.MODELS;
  var round = V.round;

  function clamp(x, lo, hi) { return Math.max(lo, Math.min(hi, x)); }
  function pct(x) { return Math.round(x * 100) + '%'; }
  function fmt(n) { return Math.round(n).toLocaleString(); }

  // Linear interpolation over [[x, y], ...] sorted by x.
  function interp(points, x) {
    if (x <= points[0][0]) return points[0][1];
    for (var i = 1; i < points.length; i++) {
      if (x <= points[i][0]) {
        var a = points[i - 1], b = points[i];
        return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]);
      }
    }
    return points[points.length - 1][1];
  }

  // ------------------------------------------------- similarity threshold gate
  M.gate = function (p, d) {
    var scores = d.chunks.map(function (c) { return c.score; });
    var floor = 0.25;
    var absT = p.threshold / 100;

    // Score-drop: cut at the largest gap that is at least minDrop.
    var minDrop = p.minDrop / 100, cut = scores.length, best = 0;
    for (var i = 1; i < scores.length; i++) {
      var gap = scores[i - 1] - scores[i];
      if (gap >= minDrop && gap > best) { best = gap; cut = i; }
    }

    // Calibrated: the score that keeps `target` of known-relevant chunks.
    var rel = d.calibration.slice().sort(function (a, b) { return a - b; });
    var calT = rel[Math.max(0, Math.floor((1 - p.target / 100) * rel.length))];

    var pass = scores.map(function (s, i) {
      if (p.strategy === 'absolute') return s >= absT;
      if (p.strategy === 'drop') return i < cut;
      if (p.strategy === 'calibrated') return s >= calT;
      return s >= floor && i < cut && s >= calT;       // layered
    });
    if (!pass.some(Boolean)) pass[0] = p.strategy !== 'layered';  // layered may pass nothing

    var kept = 0, keptRel = 0, totRel = 0;
    d.chunks.forEach(function (c, i) {
      if (c.relevant) totRel++;
      if (pass[i]) { kept++; if (c.relevant) keptRel++; }
    });
    var precision = kept ? keptRel / kept : 0;
    var recall = totRel ? keptRel / totRel : 0;

    return {
      bars: d.chunks.map(function (c, i) {
        return { label: '#' + (i + 1) + ' ' + c.text, value: c.score, max: 1,
                 tag: (c.relevant ? 'relevant' : 'noise') + (pass[i] ? ' - passes' : ' - gated'),
                 state: pass[i] ? (c.relevant ? 'hit' : 'bad') : 'dim' };
      }),
      stats: [['kept', kept + ' of ' + d.chunks.length],
              ['precision', pct(precision)], ['recall', pct(recall)],
              ['absolute cut-off', absT.toFixed(2)],
              ['calibrated cut-off', calT.toFixed(2)],
              ['largest drop', best ? best.toFixed(2) + ' after #' + cut : 'none']],
      badge: kept ? kept + ' chunks reach the model' : 'nothing passes - abstain',
      note: kept === 0
        ? 'Every chunk was gated out. Say so to the user rather than letting the model answer from nothing.'
        : (p.strategy === 'absolute'
          ? 'A fixed cut-off ignores the shape of this result set: raise it and good chunks vanish, lower it and noise walks in.'
          : (p.strategy === 'drop'
            ? 'The drop finds the natural boundary in this query without knowing the score scale.'
            : (p.strategy === 'calibrated'
              ? 'The cut-off comes from known-relevant scores, so raising the target recall lowers it and lets more noise through.'
              : 'A chunk has to clear the floor, sit above the drop and beat the calibrated line.')))
    };
  };

  // ---------------------------------------------------------- abstention gates
  M.abstain = function (p, d) {
    var answerable = p.coverage >= 50;
    var g1 = p.top1 >= p.minTop1;
    var g2 = !p.selfAbstain;
    var g3 = p.unsupported <= p.limit;
    var stop = !g1 ? 1 : (!g2 ? 2 : (!g3 ? 3 : 0));
    var answered = stop === 0;
    var outcome = answered
      ? (answerable ? 'correct answer' : 'hallucinated answer')
      : (answerable ? 'false abstention' : 'correct abstention');
    var bad = outcome === 'hallucinated answer' || outcome === 'false abstention';

    function row(n, label, ok, value, max, tag) {
      return { label: 'Gate ' + n + ': ' + label, value: value, max: max,
               tag: stop && stop < n ? 'not reached' : tag,
               state: stop && stop < n ? 'dim' : (ok ? 'hit' : 'bad') };
    }
    return {
      bars: [
        row(1, 'retrieval confidence', g1, p.top1, 100,
            g1 ? 'top score clears ' + p.minTop1 : 'below ' + p.minTop1 + ' - abstain, no model call'),
        row(2, 'model may say "I do not know"', g2, g2 ? 0 : 100, 100,
            g2 ? 'model answered' : 'model abstained'),
        row(3, 'faithfulness check', g3, p.unsupported, 100,
            g3 ? p.unsupported + '% unsupported, limit ' + p.limit + '%'
               : p.unsupported + '% unsupported - rejected')
      ],
      stats: [['question is', answerable ? 'answerable' : 'not in the corpus'],
              ['stopped at', stop ? 'gate ' + stop : 'none - answered'],
              ['outcome', outcome],
              ['model calls', stop === 1 ? '0' : (stop === 2 ? '1' : '3 to 5')]],
      badge: outcome,
      note: bad
        ? (outcome === 'hallucinated answer'
          ? 'The corpus cannot answer this, and every gate let it through. Tighten the gate that is nearest to failing.'
          : 'The corpus could answer this and a gate refused it. This is the cost of an over-strict threshold.')
        : 'Cheap gates run first so the expensive faithfulness check only sees what is left.'
    };
  };

  // ------------------------------------------------------- chunk de-duplication
  M.dedup = function (p, d) {
    var threshold = p.strategy === 'exact' ? 1.0 : p.threshold / 100;
    var keptClusters = {}, kept = [], tokens = 0, total = 0;
    d.chunks.forEach(function (c, i) {
      total += c.tokens;
      var dup = false;
      if (p.strategy !== 'none') {
        var rep = keptClusters[c.cluster];
        dup = rep !== undefined && c.sim >= threshold;
      }
      if (!dup) { keptClusters[c.cluster] = keptClusters[c.cluster] === undefined ? i : keptClusters[c.cluster]; }
      kept.push(!dup);
      if (!dup) tokens += c.tokens;
    });
    var removed = kept.filter(function (k) { return !k; }).length;
    var lost = d.chunks.filter(function (c, i) { return !kept[i] && c.distinct; }).length;
    return {
      bars: d.chunks.map(function (c, i) {
        return { label: c.text, value: c.sim, max: 1,
                 tag: (kept[i] ? 'kept' : 'removed') + ' - ' + c.tokens + ' tokens' +
                      (c.sim === 1 ? ', exact copy' : ''),
                 state: kept[i] ? 'hit' : (c.distinct ? 'bad' : 'dim') };
      }),
      stats: [['chunks kept', (d.chunks.length - removed) + ' of ' + d.chunks.length],
              ['tokens saved', pct(1 - tokens / total)],
              ['distinct chunks lost', String(lost)],
              ['threshold', p.strategy === 'none' ? 'off' : threshold.toFixed(2)]],
      badge: removed + ' removed, ' + lost + ' lost',
      note: lost
        ? 'Too low a threshold treats a different fact as a copy. A distinct chunk was removed - raise the threshold.'
        : (p.strategy === 'exact'
          ? 'Exact hashing removes byte-identical copies and nothing else. Near-copies, such as the same text with a new date, all survive.'
          : 'Near-duplicates are gone and every distinct chunk survived.')
    };
  };

  // ------------------------------------------------------- chunk-size sweep
  // The grid is the one the page's own code prints: every figure here was
  // measured on the toy corpus in the article, not fitted.
  M.sweep = function (p, d) {
    var i = d.sizes.indexOf(p.size);
    var overlapped = p.overlap === 25;
    var recall = (overlapped ? d.recall25 : d.recall0)[i];
    var chunks = (overlapped ? d.chunks25 : d.chunks0)[i];
    var tokens = d.k * p.size;

    // Beaten: another configuration is at least as good on all three goals
    // and strictly better on one.
    var all = [];
    d.sizes.forEach(function (s, j) {
      all.push({ r: d.recall0[j], t: d.k * s, c: d.chunks0[j] });
      if (d.recall25[j] !== d.recall0[j] || d.chunks25[j] !== d.chunks0[j]) {
        all.push({ r: d.recall25[j], t: d.k * s, c: d.chunks25[j] });
      }
    });
    var me = { r: recall, t: tokens, c: chunks };
    var beaten = all.some(function (o) {
      var ge = o.r >= me.r && o.t <= me.t && o.c <= me.c;
      var gt = o.r > me.r || o.t < me.t || o.c < me.c;
      return ge && gt;
    });

    return {
      bars: [
        { label: 'recall@' + d.k, value: round(recall, 2), max: 1,
          tag: p.size + ' words, ' + p.overlap + '% overlap',
          state: recall >= 0.95 ? 'hit' : (recall < 0.6 ? 'bad' : '') },
        { label: 'tokens sent to the model per question', value: tokens, max: d.k * d.sizes[d.sizes.length - 1],
          tag: d.k + ' chunks x ' + p.size, state: 'dim' },
        { label: 'chunks to store', value: chunks, max: d.chunks25[0], tag: 'index size', state: 'dim' }
      ],
      stats: [['recall@' + d.k, pct(recall)], ['tokens per question', tokens],
              ['chunks', chunks], ['Pareto status', beaten ? 'beaten' : 'on the front']],
      badge: beaten ? 'another setting beats it' : 'on the Pareto front',
      note: recall < 0.6
        ? 'Chunks this small cut most facts in half, so neither piece matches the question.'
        : (recall >= 0.95 && tokens > 200
          ? 'Recall has levelled off, but every question still sends ' + tokens + ' tokens. A smaller chunk may match it for less.'
          : 'Overlap repeats words at each boundary. It rescues cut facts when chunks are small, and adds only storage once they are big.')
    };
  };

  // -------------------------------------------------------- capacity planning
  // The same arithmetic as the page's code: chunks from the average article
  // length, bytes per vector, an HNSW graph of 2*M links per vector, text and
  // metadata, and ten percent of bookkeeping. Sizes are decimal gigabytes.
  M.capacity = function (p, d) {
    var overlap = Math.round(p.chunk * p.overlap / 100);
    var stride = p.chunk - overlap;
    var perArticle = p.length <= p.chunk ? 1 : Math.ceil((p.length - overlap) / stride);
    var chunks = p.articles * 1000 * perArticle;
    var bytesPer = { float32: 4, float16: 2, int8: 1, binary: 0.125 }[p.precision];
    var emb = chunks * p.dims * bytesPer;
    var text = chunks * 2000, meta = chunks * 500;
    var index = p.index === 'hnsw' ? chunks * 2 * 16 * 4 * 1.07
              : (p.index === 'ivf' ? chunks * 8 + 4096 * p.dims * 4 : 0);
    var sub = emb + text + meta + index;
    var total = sub * 1.1, overhead = total - sub;
    var ram = (emb + index) * 1.3;
    var gb = function (b) { return round(b / 1e9, 2); };
    var big = Math.max(total, 1);
    return {
      bars: [
        { label: 'embeddings', value: gb(emb), max: gb(big), tag: p.dims + ' dims, ' + p.precision, state: 'hit' },
        { label: 'chunk text and metadata', value: gb(text + meta), max: gb(big), tag: 'kept on disk', state: '' },
        { label: 'index structure', value: gb(index), max: gb(big), tag: p.index === 'flat' ? 'no index' : p.index, state: 'dim' },
        { label: 'database overhead', value: gb(overhead), max: gb(big), tag: '10% of the rest', state: 'dim' }
      ],
      stats: [['chunks', fmt(chunks)], ['chunks per article', perArticle],
              ['total storage', gb(total) + ' GB'],
              ['RAM for vectors + index', round(ram / 1e9, 1) + ' GB'],
              ['vs float32 vectors', pct(bytesPer / 4)]],
      badge: gb(total) + ' GB total',
      note: ram / 1e9 > d.ramBudget
        ? 'The hot data needs more than the ' + d.ramBudget + ' GB RAM budget. Quantise, shorten the vectors or shard.'
        : 'The vectors and index fit in the ' + d.ramBudget + ' GB RAM budget. Overlap, chunk size and precision all move this figure.'
    };
  };

  // --------------------------------------------------------- latency budget
  // Stage times are assumptions the page states. The total p95 is not the sum
  // of the stage p95s: it is the median total plus the combined spread of the
  // stages, treating them as independent (the page's simulation checks this
  // against 2,000 simulated requests).
  M.latency = function (p, d) {
    var factor = { large: 1, medium: 0.6, small: 0.35 }[p.model];
    var S = {};
    d.stages.forEach(function (s) { S[s[0]] = { p50: s[1], p95: s[2] }; });
    var gen = { p50: S.generate.p50 * factor, p95: S.generate.p95 * factor };
    var rer = p.rerank ? S.rerank : { p50: 0, p95: 0 };

    function chain(list) {
      var p50 = 0, sq = 0;
      list.forEach(function (x) { p50 += x.p50; sq += Math.pow(x.p95 - x.p50, 2); });
      return { p50: p50, p95: p50 + Math.sqrt(sq) };
    }
    var vec = chain([S.embed, S.vector]);
    var kw = S.keyword;
    var retrieval = p.parallel
      ? (vec.p50 >= kw.p50 ? vec : { p50: kw.p50, p95: kw.p95 })
      : chain([S.embed, S.vector, S.keyword]);
    var all = chain([retrieval, rer, gen]);
    // chain() above treats `retrieval` as one stage whose spread is its own.
    all.p95 = all.p50 + Math.sqrt(Math.pow(retrieval.p95 - retrieval.p50, 2) +
      Math.pow(rer.p95 - rer.p50, 2) + Math.pow(gen.p95 - gen.p50, 2));
    var hit = p.cacheHit / 100;
    var average = hit * d.cacheMs + (1 - hit) * all.p50;
    var base = chain([S.embed, S.vector, S.keyword, S.rerank, S.generate]).p50;

    var rows = [
      { name: 'embed the query', v: S.embed.p50 },
      { name: 'vector search', v: S.vector.p50 },
      { name: 'keyword search', v: p.parallel ? 0 : S.keyword.p50, tag: p.parallel ? 'overlapped with the vector path' : '' },
      { name: 'rerank', v: rer.p50, tag: p.rerank ? '' : 'switched off' },
      { name: 'generate', v: gen.p50, tag: p.model + ' model' }
    ];
    var biggest = Math.max.apply(null, rows.map(function (r) { return r.v; }));
    return {
      bars: rows.map(function (r) {
        return { label: r.name, value: Math.round(r.v), max: S.generate.p50,
                 tag: r.tag || 'p50, ms', state: r.v === biggest ? 'bad' : (r.v ? '' : 'dim') };
      }),
      stats: [['p50, uncached', fmt(all.p50) + ' ms'], ['p95, uncached', fmt(all.p95) + ' ms'],
              ['average with cache', fmt(average) + ' ms'],
              ['vs the baseline p50', pct(1 - all.p50 / base) + ' faster']],
      badge: fmt(all.p50) + ' ms p50',
      note: 'The red row is the stage to fix. A cache lowers the average and leaves a miss exactly as slow as before, so the p95 of the requests that miss does not move.'
    };
  };

  // ------------------------------------------------ production design: failure
  M.subsystems = function (p, d) {
    var names = d.systems;
    var down = p.fail;           // index, or -1 for none
    var guard = p.guard;
    var served = true, quality = 100, note = d.healthy;
    if (down >= 0) {
      var s = names[down];
      served = guard ? s.guardServed : s.rawServed;
      quality = guard ? s.guardQuality : s.rawQuality;
      note = guard ? s.guardNote : s.rawNote;
    }
    return {
      bars: names.map(function (s, i) {
        return { label: s.name, value: i === down ? 0 : 100, max: 100,
                 tag: i === down ? (guard ? 'failed - ' + s.guard : 'failed - nothing catches it') : s.role,
                 state: i === down ? 'bad' : 'hit' };
      }),
      stats: [['answers served', served ? 'yes' : 'no'], ['answer quality', quality + '%'],
              ['safeguards', guard ? 'on' : 'off']],
      badge: served ? 'serving at ' + quality + '%' : 'outage',
      note: note
    };
  };

  // ------------------------------------------------------------ debugging trace
  M.trace = function (p, d) {
    var rank = p.rank;                       // 1..10, 11 = never retrieved
    var inContext = rank <= p.k;
    var retrievalOk = rank <= 10;
    var synthOk = inContext && p.faithful >= 60;
    var postOk = !p.truncate;
    var where, fix;
    if (!retrievalOk) { where = 'retrieval'; fix = 'The right chunk was never fetched. Look at chunking, the embedding and the query.'; }
    else if (!inContext) { where = 'context cut-off'; fix = 'It was retrieved at rank ' + rank + ' but k=' + p.k + ' dropped it. Raise k or rerank.'; }
    else if (!synthOk) { where = 'synthesis'; fix = 'The chunk was in the prompt and the model ignored it. Fix the prompt, not the retriever.'; }
    else if (!postOk) { where = 'post-processing'; fix = 'The model answered correctly and the output step cut it. Check truncation and formatting.'; }
    else { where = 'none'; fix = 'Every stage did its job. The answer should be correct.'; }
    function st(ok, active) { return ok ? 'hit' : (active ? 'bad' : 'dim'); }
    return {
      bars: [
        { label: '1 retrieve', value: retrievalOk ? 100 : 0, max: 100,
          tag: retrievalOk ? 'right chunk at rank ' + rank : 'right chunk not in the top 10', state: st(retrievalOk, true) },
        { label: '2 fit in context', value: inContext ? 100 : 0, max: 100,
          tag: 'k = ' + p.k, state: retrievalOk ? st(inContext, true) : 'dim' },
        { label: '3 synthesise', value: p.faithful, max: 100,
          tag: 'faithfulness ' + p.faithful + '%', state: inContext ? st(synthOk, true) : 'dim' },
        { label: '4 post-process', value: postOk ? 100 : 0, max: 100,
          tag: postOk ? 'untouched' : 'answer truncated', state: synthOk ? st(postOk, true) : 'dim' }
      ],
      stats: [['first failing stage', where], ['rank of gold chunk', rank > 10 ? 'missing' : rank]],
      badge: where === 'none' ? 'healthy' : 'fails at ' + where,
      note: fix
    };
  };

  // ------------------------------------------------------ query decomposition
  // The times are assumptions that the page states; the scheduling is real:
  // each sub-question starts when its prerequisites are done and a worker is
  // free.
  M.plan = function (p, d) {
    var qs = d.questions, finish = {}, lanes = [];
    for (var w = 0; w < p.workers; w++) lanes.push(0);
    qs.forEach(function (q, i) {
      var ready = Math.max.apply(null, [0].concat(q.needs.map(function (n) { return finish[n]; })));
      var lane = 0;
      for (var l = 1; l < lanes.length; l++) if (lanes[l] < lanes[lane]) lane = l;
      var start = Math.max(ready, lanes[lane]);
      finish[i] = start + q.ms;
      lanes[lane] = finish[i];
    });
    var longest = Math.max.apply(null, Object.keys(finish).map(function (k) { return finish[k]; }));
    var overhead = d.classifyMs + d.planMs + d.synthMs;
    var decomposed = longest + overhead;
    var oneByOne = qs.reduce(function (a, q) { return a + q.ms; }, 0) + overhead;
    var useDecomp = p.mode === 'decomposed';
    var total = useDecomp ? decomposed : d.singleMs;
    return {
      bars: useDecomp ? qs.map(function (q, i) {
        return { label: q.text, value: finish[i], max: decomposed,
                 tag: q.needs.length ? 'waits for #' + q.needs.map(function (n) { return n + 1; }).join(', #')
                                     : 'starts straight away',
                 state: '' };
      }) : [{ label: 'one retrieval for the whole question', value: d.singleMs, max: decomposed,
              tag: 'single pass', state: '' }],
      stats: [['mode', useDecomp ? 'decomposed' : 'single pass'],
              ['latency', fmt(total) + ' ms'],
              ['one by one', useDecomp ? fmt(oneByOne) + ' ms' : 'n/a'],
              ['model calls', useDecomp ? qs.length + 3 : 1]],
      badge: fmt(total) + ' ms',
      note: useDecomp
        ? 'Independent sub-questions run side by side; one that needs another has to wait. Past three workers the dependent chain is the limit.'
        : 'Single pass is fast and cheap, and it retrieves for the question as a whole. The second half of a compound question often goes unanswered.'
    };
  };

  // ------------------------------------------------------- embedding migration
  // In place: documents and queries meet in the same space only for the
  // matching share, and a cross-space comparison is no better than chance.
  // Blue-green: blue is untouched until the cutover, and green only holds the
  // documents re-embedded so far.
  M.migrate = function (p, d) {
    var f = p.reembedded / 100;
    var cut = !!p.cutover;
    var recall;
    if (p.strategy === 'inplace') {
      recall = cut ? d.newBase * f + d.chance * (1 - f)
                   : d.base * (1 - f) + d.chance * f;
    } else {
      recall = cut ? d.newBase * f : d.base;
    }
    recall = round(recall, 2);
    var healthy = recall >= d.base - 0.01;
    return {
      bars: [
        { label: 'documents in the new space', value: p.reembedded, max: 100,
          tag: 're-embedded so far', state: '' },
        { label: 'queries encoded by', value: cut ? 100 : 0, max: 100,
          tag: cut ? 'the new model' : 'the old model', state: 'dim' },
        { label: 'recall@5', value: recall, max: 1,
          tag: healthy ? 'at or above the old level' : 'below the old level',
          state: healthy ? 'hit' : 'bad' }
      ],
      stats: [['strategy', p.strategy === 'inplace' ? 'in place' : 'blue-green'],
              ['mixed spaces in one index', p.strategy === 'inplace' && f > 0 && f < 1 ? 'yes' : 'no'],
              ['old index serving', p.strategy === 'inplace' ? 'partly' : (cut ? 'no' : 'yes')]],
      badge: 'recall ' + recall,
      note: p.strategy === 'inplace'
        ? 'Vectors from two models are not comparable. In one index, part of every query is compared against the wrong space.'
        : (cut && f < 1
          ? 'Cut over too early: the green index is only ' + p.reembedded + '% built, so the rest of the corpus cannot be found.'
          : 'The old index keeps serving until the new one is complete and validated.')
    };
  };

  // --------------------------------------------------- resilience and retries
  M.retry = function (p, d) {
    var f = p.fail / 100;
    var r = p.retries;
    var gaveUp = Math.pow(f, r + 1);
    var attempts = f >= 1 ? r + 1 : (1 - Math.pow(f, r + 1)) / (1 - f);
    var wait = 0;
    for (var i = 0; i < r; i++) wait += p.base * Math.pow(2, i) * Math.pow(f, i + 1) * (p.jitter ? 1 : 1);
    var batches = d.batches;
    var perBatchSec = d.batchSec;
    var timeSec = batches * (attempts * perBatchSec + wait);
    var crashAt = 0.7 * batches;
    var redone = p.checkpoint ? 0 : crashAt;
    var lost = round(batches * gaveUp, 1);
    return {
      bars: [
        { label: 'batches abandoned for good', value: lost, max: batches, tag: pct(gaveUp) + ' per batch',
          state: gaveUp > 0.01 ? 'bad' : 'hit' },
        { label: 'average attempts per batch', value: round(attempts, 2), max: r + 1, tag: 'of up to ' + (r + 1), state: '' },
        { label: 'batches redone after a crash at 70%', value: redone, max: batches,
          tag: p.checkpoint ? 'checkpoint resumes at 70%' : 'starts again from 0', state: p.checkpoint ? 'hit' : 'bad' }
      ],
      stats: [['run time', round(timeSec / 60, 1) + ' min'],
              ['plus crash recovery', round((redone * (attempts * perBatchSec)) / 60, 1) + ' min'],
              ['backoff wait per batch', round(wait, 1) + ' s'],
              ['jitter', p.jitter ? 'on' : 'off']],
      badge: lost + ' lost, ' + round(timeSec / 60, 1) + ' min',
      note: p.jitter
        ? 'Jitter spreads retries so workers that failed together do not hit the API together again.'
        : 'Without jitter every worker retries at the same instant, which is how a brief limit becomes a long outage.'
    };
  };

  // -------------------------------------------------- distributed idempotency
  // Expected counts, not a simulation: a crash after the write and before the
  // acknowledgement causes one redelivery, which writes a second copy unless
  // the write is keyed on content. At-most-once acknowledges first, so a crash
  // loses the chunk instead.
  M.idempotency = function (p, d) {
    var n = d.chunks, crash = p.crash / 100;
    var atLeast = p.delivery === 'atleast';
    var dupes = (atLeast && p.layer === 0) ? Math.round(n * crash) : 0;
    var lost = atLeast ? 0 : Math.round(n * crash);
    var staleRaw = Math.round(n * d.edited * d.changed);
    var stale = p.layer === 2 ? 0 : staleRaw;
    var cap = Math.max(1, Math.round(n * 0.2));
    var names = ['random IDs, plain insert', 'content IDs and upsert',
                 'content IDs, upsert and cleanup'];
    var ok = !dupes && !lost && !stale;
    return {
      bars: [
        { label: 'duplicate chunks in the index', value: dupes, max: cap,
          tag: dupes ? 'every redelivery left a copy' : 'none', state: dupes ? 'bad' : 'hit' },
        { label: 'chunks never indexed', value: lost, max: cap,
          tag: lost ? 'silent data loss' : 'none', state: lost ? 'bad' : 'hit' },
        { label: 'stale chunks from edited articles', value: stale, max: cap,
          tag: stale ? 'old text still retrievable' : 'none', state: stale ? 'bad' : 'hit' }
      ],
      stats: [['chunks processed', fmt(n)], ['worker crash rate', p.crash + '%'],
              ['delivery', atLeast ? 'at least once' : 'at most once'],
              ['writes', names[p.layer]]],
      badge: ok ? 'clean index' : 'index is wrong',
      note: atLeast
        ? 'At-least-once delivery repeats work after a crash, so safety has to come from making the repeat harmless.'
        : 'At-most-once never repeats work, and it silently drops whatever a crashing worker held. For an index that is the worse failure.'
    };
  };

  // ------------------------------------------------------ ingestion funnel
  M.funnel = function (p, d) {
    var n = d.pdfs;
    var scanShare = p.scanned / 100;
    var steps = [
      { name: 'extract text', keep: 1 - scanShare * (p.ocr ? 0.05 : 0.9) - 0.01, secPer: scanShare * (p.ocr ? 4 : 0.2) + (1 - scanShare) * 0.4 },
      { name: 'clean', keep: 0.995, secPer: 0.05 },
      { name: 'chunk', keep: 0.999, secPer: 0.08 },
      { name: 'embed', keep: 1 - Math.pow(0.02, p.retry + 1), secPer: 0.6 },
      { name: 'store', keep: 0.999, secPer: 0.1 }
    ];
    var alive = n, rows = [], secs = 0, worst = 0, wi = 0;
    steps.forEach(function (s, i) {
      var out = Math.round(alive * s.keep);
      rows.push({ name: s.name, out: out, lost: alive - out, sec: s.secPer * n });
      secs += s.secPer * n;
      if (s.secPer > worst) { worst = s.secPer; wi = i; }
      alive = out;
    });
    var perWorker = secs / p.workers;
    return {
      bars: rows.map(function (r, i) {
        return { label: (i + 1) + '. ' + r.name, value: r.out, max: n,
                 tag: r.lost ? r.lost + ' lost - ' + round(r.sec / p.workers / 3600, 2) + ' h' : round(r.sec / p.workers / 3600, 2) + ' h',
                 state: i === wi ? 'bad' : (r.lost > n * 0.02 ? 'dim' : 'hit') };
      }),
      stats: [['documents searchable', fmt(alive) + ' of ' + fmt(n)],
              ['slowest stage', rows[wi].name], ['wall-clock time', round(perWorker / 3600, 1) + ' h'],
              ['workers', p.workers]],
      badge: fmt(alive) + ' of ' + fmt(n) + ' searchable',
      note: p.ocr
        ? 'OCR rescues scanned pages and is by far the slowest stage. Add workers there first.'
        : 'Without OCR a scanned PDF yields no text, so it silently drops out at stage one - and nothing downstream will ever tell you.'
    };
  };

  // ------------------------------------------------------- batch embedding
  // Text lengths come from a small seeded generator, so the padding figures
  // are counted over a real batching of a real length distribution rather
  // than quoted. Memory is a rough estimate (activations only) and is
  // labelled as one.
  function sampleLengths(n) {
    var x = 12345, out = [];
    for (var i = 0; i < n; i++) {
      x = (x * 1103515245 + 12345) % 2147483648;
      var u = (x + 1) / 2147483649;
      out.push(Math.min(120, 4 + Math.floor(-Math.log(u) * 10)));
    }
    return out;
  }

  M.batch = function (p, d) {
    var model = d.models[p.model];
    var lengths = sampleLengths(d.sample);
    if (p.sorted) lengths.sort(function (a, b) { return b - a; });
    var padded = 0, real = 0, peak = 0;
    for (var i = 0; i < lengths.length; i += p.batch) {
      var chunk = lengths.slice(i, i + p.batch), mx = 0;
      chunk.forEach(function (l) { if (l > mx) mx = l; real += l; });
      padded += mx * chunk.length;
      peak = Math.max(peak, mx * chunk.length);
    }
    var blank = 1 - real / padded;
    var memGB = model.gb + peak * model.hidden * model.layers * 4 * 8 / 1e9;
    var oom = memGB > p.gpu;
    var calls = Math.ceil(d.texts / p.batch);
    var work = padded / d.sample * d.texts;
    return {
      bars: [
        { label: 'GPU memory (estimate)', value: round(memGB, 1), max: Math.max(p.gpu, memGB),
          tag: oom ? 'out of memory on a ' + p.gpu + ' GB card' : 'fits in ' + p.gpu + ' GB',
          state: oom ? 'bad' : 'hit' },
        { label: 'blank (padding) tokens', value: Math.round(blank * 100), max: 100,
          tag: p.sorted ? 'texts sorted by length' : 'texts in arrival order',
          state: blank > 0.4 ? 'bad' : 'done' },
        { label: 'model calls for ' + fmt(d.texts) + ' texts', value: calls, max: d.texts,
          tag: 'batch of ' + p.batch, state: 'dim' }
      ],
      stats: [['model', model.name], ['vector size', model.hidden + ' dims'],
              ['padded tokens', fmt(work)], ['blank share', pct(blank)],
              ['peak batch', fmt(peak) + ' tokens']],
      badge: oom ? 'out of memory' : pct(blank) + ' blank, ' + fmt(calls) + ' calls',
      note: oom
        ? 'The biggest batch does not fit. Halve the batch size, or use a smaller model.'
        : (p.sorted
          ? 'Sorting cuts the blank tokens and the work. The longest batch is just as big, so peak memory barely moves.'
          : 'Each batch is padded to its longest text, so one long title makes the rest do work on blanks. Try sorting.')
    };
  };
})();
