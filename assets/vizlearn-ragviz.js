/* The interactive visualisation on the generated gen_ai/ pages.
 *
 * The hand-written modules in this track share a shape: a Parameters panel on
 * the left, a visualisation in the middle, a readout on the right, and a small
 * script that recomputes everything whenever a control moves. That shape is
 * the point of the track - you change a number and watch the ranking change -
 * and it is what the generated pages have to match.
 *
 * Rather than emit a bespoke script per page, each page declares its controls
 * and names a model. The model is a pure function of the control values, so
 * the numbers on screen are computed here in the browser rather than baked in
 * at build time - the same guarantee the hand-written pages give.
 *
 * Markup the page supplies:
 *
 *   <div class="vz-rv" data-vz-rv data-model="tfidf">
 *     <script type="application/json" class="vz-rv-data">{ ...spec... }</script>
 *     <div class="vz-rv-controls"></div>     (left column)
 *     <div class="vz-rv-bars"></div>         (centre)
 *     <div class="vz-rv-stats"></div>        (right)
 *     <p class="vz-rv-note"></p>
 *   </div>
 *
 * The spec is { controls: [...], data: {...} }. A model returns
 * { bars: [{label, value, max, tag, state}], stats: [[k, v], ...], note, badge }.
 */
(function () {
  'use strict';

  // ---------------------------------------------------------------- helpers

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function round(x, places) {
    var f = Math.pow(10, places == null ? 2 : places);
    return Math.round(x * f) / f;
  }

  // ----------------------------------------------------------------- models
  //
  // Each takes the current control values and the page's data, and returns
  // what to draw. They are deliberately small: the point is that the reader
  // can move a slider and see the consequence, not that this is a production
  // implementation.

  var MODELS = {};

  // Lexical scoring: idf x damped tf, with the damping exposed.
  MODELS.tfidf = function (p, data) {
    var docs = data.docs, query = data.queries[p.query];
    var N = docs.length;
    var df = {};
    docs.forEach(function (d) {
      var seen = {};
      d.text.toLowerCase().split(/\s+/).forEach(function (w) {
        if (!seen[w]) { seen[w] = 1; df[w] = (df[w] || 0) + 1; }
      });
    });

    var scored = docs.map(function (d) {
      var words = d.text.toLowerCase().split(/\s+/);
      var counts = {};
      words.forEach(function (w) { counts[w] = (counts[w] || 0) + 1; });
      var total = 0, parts = [];
      query.split(/\s+/).forEach(function (t) {
        if (!counts[t]) return;
        var idf = p.useIdf ? Math.log(N / df[t]) : 1;
        var tf = p.dampTf ? 1 + Math.log(counts[t]) : counts[t];
        var w = idf * tf;
        if (w > 0) parts.push(t + ' ' + round(w));
        total += w;
      });
      return { label: d.text, value: total, tag: parts.join('  ') };
    }).sort(function (a, b) { return b.value - a.value; });

    var max = Math.max.apply(null, scored.map(function (s) { return s.value; }).concat([0.001]));
    var stopword = query.split(/\s+/).filter(function (t) { return df[t] === N; });

    return {
      bars: scored.map(function (s, i) {
        return { label: s.label, value: round(s.value), max: max, tag: s.tag,
                 state: i === 0 && s.value > 0 ? 'hit' : (s.value === 0 ? 'dim' : '') };
      }),
      stats: [['documents', N], ['query terms', query.split(/\s+/).length],
              ['idf', p.useIdf ? 'on' : 'off'], ['tf damping', p.dampTf ? 'on' : 'off']],
      badge: scored[0].value > 0 ? 'top score ' + round(scored[0].value) : 'no match',
      note: !p.useIdf && stopword.length
        ? 'With idf off, "' + stopword[0] + '" contributes to every document and the '
          + 'ranking is driven by a word that distinguishes nothing.'
        : (stopword.length
            ? '"' + stopword[0] + '" is in every document, so its idf is 0 and it '
              + 'contributes nothing. No stopword list was needed.'
            : 'Every query term is rare enough to carry weight here.')
    };
  };

  // Grade retrieved evidence, then decide whether to answer at all.
  MODELS.crag = function (p, data) {
    var results = data.queries[p.query].results;
    var best = results[0].score;
    var verdict = best >= p.good ? 'correct' : (best >= p.poor ? 'ambiguous' : 'incorrect');
    var action = { correct: 'generate from the kept documents',
                   ambiguous: 'combine with an external source, flag low confidence',
                   incorrect: 'rewrite the query, then fall back, then decline' }[verdict];
    return {
      bars: results.map(function (r) {
        return { label: r.text, value: round(r.score), max: 1,
                 tag: r.score >= p.good ? 'kept' : 'dropped',
                 state: r.score >= p.good ? 'hit' : 'dim' };
      }),
      stats: [['best score', round(best)], ['verdict', verdict],
              ['kept', results.filter(function (r) { return r.score >= p.good; }).length],
              ['naive RAG would', 'answer from ' + results[0].text.slice(0, 18) + '...']],
      badge: verdict,
      note: verdict === 'incorrect'
        ? 'Nothing clears the bar. Naive RAG would still answer from the top result; '
          + 'this pipeline declines, which is the correct output.'
        : 'Documents below the threshold are dropped before generation - irrelevant '
          + 'context measurably degrades the answer.'
    };
  };

  // Attention: one query against every key, then softmax.
  MODELS.attention = function (p, data) {
    var tokens = data.tokens, focus = p.focus;
    var row = data.affinity[focus] || data.affinity[tokens[0]];
    var scores = tokens.map(function (t) {
      var s = row[t] * p.sharpness;
      return { token: t, raw: s };
    });
    var top = Math.max.apply(null, scores.map(function (s) { return s.raw; }));
    var exps = scores.map(function (s) { return Math.exp(s.raw - top); });
    var sum = exps.reduce(function (a, b) { return a + b; }, 0);
    var weights = exps.map(function (e) { return e / sum; });
    var biggest = weights.indexOf(Math.max.apply(null, weights));

    return {
      bars: tokens.map(function (t, i) {
        return { label: t, value: round(weights[i], 3), max: 1,
                 tag: 'Q.K ' + round(scores[i].raw, 2),
                 state: i === biggest ? 'hit' : '' };
      }),
      stats: [['attending from', focus], ['weights sum to', round(weights.reduce(function (a, b) { return a + b; }, 0), 3)],
              ['sharpest weight', round(weights[biggest], 3)],
              ['output', 'weighted sum of V, not K']],
      badge: focus + ' attends to ' + tokens[biggest],
      note: p.sharpness > 2.5
        ? 'A large scale saturates the softmax into nearly one-hot - which is what '
          + 'dividing by sqrt(d) exists to prevent.'
        : 'Scores come from Q dot K; the output is the weighted sum of the VALUES. '
          + 'Keys decide how much, values decide what.'
    };
  };

  // Three caches, three hit rates, one total.
  MODELS.caching = function (p, data) {
    var n = 100;
    var exactRepeats = Math.round(n * p.repeatRate / 100);
    var reworded = Math.round(n * p.rewordRate / 100);
    var cold = n - exactRepeats - reworded;
    if (cold < 0) { cold = 0; }

    var full = data.stages.reduce(function (a, s) { return a + s[1]; }, 0);
    var queryHitMs = 3;
    var promptSaving = p.promptCache ? 0.45 : 0;
    var rewordMs = full - data.stages[3][1] * promptSaving;
    var total = exactRepeats * queryHitMs + reworded * rewordMs + cold * full;
    var uncached = n * full;

    return {
      bars: [
        { label: 'exact repeat -> query cache', value: exactRepeats, max: n,
          tag: queryHitMs + ' ms each', state: 'hit' },
        { label: 'reworded -> prompt cache only', value: reworded, max: n,
          tag: Math.round(rewordMs) + ' ms each', state: p.promptCache ? '' : 'dim' },
        { label: 'cold -> full pipeline', value: cold, max: n,
          tag: full + ' ms each', state: 'dim' }
      ],
      stats: [['uncached', Math.round(uncached).toLocaleString() + ' ms'],
              ['with caches', Math.round(total).toLocaleString() + ' ms'],
              ['saved', Math.round(100 - total / uncached * 100) + '%'],
              ['prompt cache', p.promptCache ? 'on' : 'off']],
      badge: Math.round(uncached / Math.max(total, 1)) + 'x faster',
      note: p.repeatRate > 50
        ? 'A high exact-repeat rate makes the query cache dominate - and it is the '
          + 'cache that goes stale the moment a document changes.'
        : 'Reworded questions miss the exact caches entirely. Only the prompt cache, '
          + 'which keys on the shared prefix, still helps them.'
    };
  };

  // Split text on the largest separator that fits.
  MODELS.chunking = function (p, data) {
    var text = data.text;
    var ladders = { paragraph: ['\n\n', '\n', '. ', ' '], sentence: ['. ', ' '],
                    character: [''] };
    // An unknown strategy used to throw inside split() and take the whole
    // visualisation down with it; fall back to the widest ladder instead.
    var seps = ladders[p.strategy] || ladders.paragraph;

    function split(t, limit, list) {
      if (t.length <= limit) return [t];
      for (var i = 0; i < list.length; i++) {
        var sep = list[i];
        if (sep === '') {
          var out = [];
          for (var j = 0; j < t.length; j += limit) out.push(t.slice(j, j + limit));
          return out;
        }
        var parts = t.split(sep);
        if (parts.length === 1) continue;
        var chunks = [], buf = '';
        for (var k = 0; k < parts.length; k++) {
          var cand = buf ? buf + sep + parts[k] : parts[k];
          if (cand.length <= limit) { buf = cand; }
          else {
            if (buf) chunks.push(buf);
            buf = parts[k].length <= limit ? parts[k] : '';
            if (!buf) chunks = chunks.concat(split(parts[k], limit, list.slice(i + 1)));
          }
        }
        if (buf) chunks.push(buf);
        return chunks;
      }
      return [t];
    }

    var chunks = split(text, p.size, seps);
    var cut = chunks.filter(function (c) { return /[a-z],?$/.test(c.trim()); }).length;
    var max = Math.max.apply(null, chunks.map(function (c) { return c.length; }));

    return {
      bars: chunks.map(function (c, i) {
        var mid = /[a-z],?$/.test(c.trim());
        return { label: c.trim().replace(/\s+/g, ' ').slice(0, 64),
                 value: c.length, max: max, tag: c.length + ' chars',
                 state: mid ? 'bad' : 'done' };
      }),
      stats: [['chunks', chunks.length], ['limit', p.size + ' chars'],
              ['longest', max], ['cut mid-sentence', cut]],
      badge: chunks.length + ' chunks',
      note: cut
        ? cut + ' chunk(s) end mid-sentence. A retrieved fragment starting halfway '
          + 'through a thought is what this costs.'
        : 'Every chunk ends at a natural boundary. Recursive splitting spends the '
          + 'size budget on the best separator available.'
    };
  };

  // Cut where consecutive-sentence similarity drops.
  MODELS.semantic = function (p, data) {
    var gaps = data.gaps, sentences = data.sentences;
    var sorted = gaps.slice().sort(function (a, b) { return a - b; });
    var idx = Math.max(0, Math.round(sorted.length * p.percentile / 100) - 1);
    var threshold = sorted[idx];
    var boundaries = gaps.map(function (g) { return g <= threshold; });
    var chunks = 1 + boundaries.filter(Boolean).length;

    return {
      bars: gaps.map(function (g, i) {
        return { label: 's' + (i + 1) + ' -> s' + (i + 2), value: round(g, 2), max: 1,
                 tag: boundaries[i] ? 'SPLIT' : 'same topic',
                 state: boundaries[i] ? 'hit' : 'dim' };
      }),
      stats: [['sentences', sentences], ['threshold', round(threshold, 2)],
              ['percentile', p.percentile + '%'], ['chunks produced', chunks]],
      badge: chunks + ' chunks',
      note: p.percentile > 60
        ? 'A high percentile splits almost everywhere, producing chunks too small to '
          + 'carry an idea.'
        : 'The threshold is a percentile of THIS document, so it adapts to how varied '
          + 'the writing is. A fixed number would not.'
    };
  };

  // Enrich a chunk, and watch it become findable - then indistinguishable.
  MODELS.enrichment = function (p, data) {
    var base = data.chunk, q = data.queryTerms;
    var text = base.slice();
    if (p.title) text = text.concat(data.title);
    if (p.path) text = text.concat(data.path);
    if (p.resolve) text = data.resolved.concat(text.filter(function (w) {
      return data.resolved.indexOf(w) === -1; }));
    if (p.boilerplate) for (var i = 0; i < 3; i++) text = text.concat(data.boilerplate);

    function overlap(a, b) {
      var shared = a.filter(function (w) { return b.indexOf(w) !== -1; }).length;
      return shared / Math.sqrt(a.length * b.length);
    }
    var score = overlap(text, q);
    var sibling = data.sibling.concat(p.boilerplate ? data.boilerplate.concat(
      data.boilerplate, data.boilerplate) : []);
    var distinct = 1 - overlap(text, sibling);

    return {
      bars: [
        { label: 'similarity to the query', value: round(score, 3), max: 0.7,
          tag: score > 0.25 ? 'retrievable' : 'will not be retrieved',
          state: score > 0.25 ? 'hit' : 'bad' },
        { label: 'distinguishable from a sibling chunk', value: round(distinct, 3),
          max: 1, tag: distinct > 0.4 ? 'distinct' : 'too similar',
          state: distinct > 0.4 ? 'done' : 'bad' }
      ],
      stats: [['tokens embedded', text.length],
              ['title', p.title ? 'on' : 'off'], ['heading path', p.path ? 'on' : 'off'],
              ['pronouns resolved', p.resolve ? 'on' : 'off']],
      badge: score > 0.25 ? 'retrievable' : 'invisible to search',
      note: p.boilerplate
        ? 'Over-enriched: the shared boilerplate dominates the embedding, so two '
          + 'chunks on different subjects now look alike.'
        : (p.resolve
            ? 'Resolving the pronouns is what puts the searchable nouns into the text.'
            : 'The raw chunk is about refunds and never says so - only pronouns. '
              + 'Nothing in its vector matches the query.')
    };
  };

  // Cluster-and-probe: recall against comparisons.
  MODELS.ivf = function (p, data) {
    var n = data.corpus, clusters = p.clusters, probe = Math.min(p.probe, clusters);
    var compared = Math.round(n / clusters * probe);
    // Recall rises quickly with probes and saturates; finer clusters need more.
    var coverage = probe / clusters;
    var recall = Math.min(1, 1 - Math.pow(1 - coverage, 1 + 12 * coverage));
    var latency = 0.02 * compared + 0.4;

    return {
      bars: [
        { label: 'vectors compared', value: compared, max: n,
          tag: Math.round(compared / n * 100) + '% of the corpus',
          state: compared >= n ? 'bad' : 'hit' },
        { label: 'recall@10', value: round(recall, 2), max: 1,
          tag: recall > 0.9 ? 'good' : 'missing neighbours',
          state: recall > 0.9 ? 'hit' : 'bad' }
      ],
      stats: [['corpus', n.toLocaleString()], ['clusters', clusters],
              ['probes', probe], ['latency', round(latency, 1) + ' ms']],
      badge: 'recall ' + round(recall, 2),
      note: probe >= clusters
        ? 'Probing every cluster is an exact search with extra steps - recall 1.0, '
          + 'and none of the saving.'
        : 'More probes: better recall, more comparisons, more latency. Every index '
          + 'type exposes this same trade under a different name.'
    };
  };

  // HNSW: efSearch against recall and work.
  MODELS.hnsw = function (p, data) {
    var ef = p.ef, M = p.M, n = data.corpus;
    var visited = Math.round(ef * Math.log2(n) * (M / 8) * 1.4);
    var quality = Math.min(1, (M / 16) * 0.55 + 0.45);
    var recall = Math.min(quality, 1 - Math.exp(-ef / 40) * quality);
    var latency = round(visited * 0.004 + 0.3, 1);
    var memory = Math.round(n * (768 * 4 + M * 8) / 1e6);

    return {
      bars: [
        { label: 'nodes visited', value: visited, max: 4000,
          tag: Math.round(visited / n * 1000) / 10 + '% of the corpus', state: 'hit' },
        { label: 'recall@10', value: round(recall, 2), max: 1,
          tag: recall > 0.95 ? 'excellent' : (recall > 0.85 ? 'usable' : 'poor'),
          state: recall > 0.9 ? 'hit' : 'bad' }
      ],
      stats: [['efSearch', ef], ['M (edges/node)', M],
              ['latency', latency + ' ms'], ['index memory', memory + ' MB']],
      badge: 'recall ' + round(recall, 2),
      note: M <= 6
        ? 'A poorly connected graph caps recall no matter how large efSearch gets - '
          + 'build-time damage cannot be repaired at query time.'
        : 'efSearch is the runtime knob and can differ per query. M and '
          + 'efConstruction are fixed when the index is built.'
    };
  };

  // Pre- versus post-filtering, by how much of the corpus a user may see.
  MODELS.permissions = function (p, data) {
    var visible = p.visible / 100, k = p.k, fetch = p.fetch;
    var post = Math.round(k * visible);
    var postOver = Math.min(k, Math.round(fetch * visible));
    var pre = k;

    return {
      bars: [
        { label: 'post-filter (rank ' + k + ', then drop)', value: post, max: k,
          tag: post + ' of ' + k + ' returned', state: post < k ? 'bad' : 'done' },
        { label: 'post-filter, over-fetch ' + fetch, value: postOver, max: k,
          tag: postOver + ' of ' + k, state: postOver < k ? 'bad' : 'done' },
        { label: 'pre-filter (restrict, then rank)', value: pre, max: k,
          tag: pre + ' of ' + k, state: 'hit' }
      ],
      stats: [['user can see', p.visible + '% of the corpus'], ['k requested', k],
              ['over-fetch', fetch], ['post-filter shortfall', (k - post) + ' results']],
      badge: post < k ? 'post-filter returns ' + post : 'all strategies return ' + k,
      note: p.visible < 20
        ? 'The narrower the access, the worse post-filtering gets - which is the '
          + 'opposite of how a security control should behave.'
        : 'Over-fetching makes the shortfall less likely and never removes it. '
          + 'Pre-filtering restricts the candidate set before ranking.'
    };
  };

  // Scatter-gather: sharding strategy against recall, and tail latency.
  MODELS.sharding = function (p, data) {
    var shards = p.shards, perShard = p.perShard, k = 10;
    var recall = p.strategy === 'random'
      ? Math.min(1, 1 - Math.pow(0.35, perShard / k * shards / 2))
      : Math.min(1, perShard / k);
    var slowChance = 1 - Math.pow(1 - 0.02, shards);
    var p99 = Math.round(40 + slowChance * 180);

    return {
      bars: [
        { label: 'recall@' + k, value: round(recall, 2), max: 1,
          tag: p.strategy + ' sharding',
          state: recall > 0.9 ? 'hit' : 'bad' },
        { label: 'p99 latency', value: p99, max: 240,
          tag: p99 > 120 ? 'tail risk' : 'healthy',
          state: p99 > 120 ? 'bad' : 'done' }
      ],
      stats: [['shards', shards], ['per-shard k', perShard],
              ['strategy', p.strategy], ['chance a shard is slow',
              Math.round(slowChance * 100) + '%']],
      badge: 'recall ' + round(recall, 2) + ', p99 ' + p99 + ' ms',
      note: p.strategy === 'semantic'
        ? 'Semantic sharding concentrates the relevant documents in one shard, whose '
          + 'local top-k throws the rest away. Over-fetching recovers it, at the cost '
          + 'the routing was meant to save.'
        : 'Random sharding spreads relevant documents evenly, so a modest per-shard k '
          + 'captures nearly all of them. Note p99 climbing as shards are added.'
    };
  };


  // Ranking metrics, all four at once, over a result list the reader marks up.
  MODELS.ranking = function (p, data) {
    var on = p.__on || {};
    var results = data.results.map(function (r, i) {
      var key = 'r' + i;
      var relevant = on[key] ? !r.relevant : r.relevant;
      return { rank: i + 1, text: r.text, relevant: relevant, key: key };
    });

    var k = p.k;
    var topK = results.slice(0, k);
    var hitsAtK = topK.filter(function (r) { return r.relevant; }).length;
    var totalRelevant = results.filter(function (r) { return r.relevant; }).length;

    var precision = k ? hitsAtK / k : 0;
    var recall = totalRelevant ? hitsAtK / totalRelevant : 0;
    var hitRate = hitsAtK > 0 ? 1 : 0;
    var firstHit = 0;
    for (var i = 0; i < results.length; i++) {
      if (results[i].relevant) { firstHit = i + 1; break; }
    }
    var rr = firstHit ? 1 / firstHit : 0;
    var f1 = (precision + recall) ? 2 * precision * recall / (precision + recall) : 0;

    var focus = data.focus;
    var label = { precision: 'Precision@' + k, recall: 'Recall@' + k,
                  hit: 'Hit Rate@' + k, mrr: 'Reciprocal Rank' }[focus];
    var value = { precision: precision, recall: recall, hit: hitRate, mrr: rr }[focus];

    var notes = {
      precision: hitsAtK === k
        ? 'Every result in the top ' + k + ' is relevant, so precision is 1.0 - and it '
          + 'says nothing about the ' + (totalRelevant - hitsAtK) + ' relevant document(s) further down.'
        : 'Precision counts how much of what you returned was useful. Lower k and it '
          + 'usually rises, because the best results are at the top.',
      recall: recall === 1
        ? 'Every relevant document is inside the top ' + k + '. Recall is 1.0 and will '
          + 'stay there however much further you look.'
        : (totalRelevant - hitsAtK) + ' relevant document(s) sit below rank ' + k
          + '. Recall only rises by looking deeper - which is why it is the metric '
          + 'that matters for a RAG retriever.',
      hit: hitRate
        ? 'At least one relevant document made the top ' + k + ', so hit rate is 1. It '
          + 'does not care whether there was one or five, or where they landed.'
        : 'Nothing relevant in the top ' + k + '. Hit rate is 0 - the harshest and '
          + 'bluntest of the four.',
      mrr: firstHit
        ? 'The first relevant result is at rank ' + firstHit + ', so RR is 1/' + firstHit
          + ' = ' + round(rr, 3) + '. Only that one position matters; everything below it is ignored.'
        : 'No relevant result anywhere, so the reciprocal rank is 0.'
    };

    return {
      bars: results.map(function (r) {
        var inK = r.rank <= k;
        return { label: '#' + r.rank + '  ' + r.text,
                 value: r.relevant ? 1 : 0, max: 1,
                 tag: (inK ? 'in top ' + k : 'below k') +
                      (r.relevant ? '  ·  relevant' : '  ·  not relevant') +
                      (focus === 'mrr' && r.rank === firstHit ? '  ·  1/' + r.rank : ''),
                 click: r.key, on: r.relevant,
                 state: r.relevant ? (inK ? 'hit' : 'done') : (inK ? 'bad' : 'dim') };
      }),
      stats: [[label + ' \u2190 this page', round(value, 3)],
              ['Precision@' + k, round(precision, 3)],
              ['Recall@' + k, round(recall, 3)],
              ['Hit Rate@' + k, hitRate],
              ['Reciprocal Rank', round(rr, 3)],
              ['F1@' + k, round(f1, 3)],
              ['relevant in corpus', totalRelevant]],
      badge: label + ' = ' + round(value, 3),
      note: notes[focus] + '  Click any result to change whether it is relevant.'
    };
  };

  // Answer-quality judging: claims against the retrieved context.
  MODELS.judge = function (p, data) {
    var on = p.__on || {};
    var claims = data.claims.map(function (c, i) {
      var key = 'c' + i;
      var flipped = key in on ? on[key] : false;
      return { text: c.text, key: key,
               supported: flipped ? !c.supported : c.supported,
               correct: c.correct, onTopic: c.onTopic, required: c.required };
    });

    var total = claims.length;
    var supported = claims.filter(function (c) { return c.supported; }).length;
    var correct = claims.filter(function (c) { return c.correct; }).length;
    var onTopic = claims.filter(function (c) { return c.onTopic; }).length;
    var required = data.requiredPoints;
    var covered = claims.filter(function (c) { return c.required; }).length;

    var scores = {
      groundedness: total ? supported / total : 0,
      correctness: total ? correct / total : 0,
      relevance: total ? onTopic / total : 0,
      completeness: required ? covered / required : 0
    };
    var focus = data.focus;
    var value = scores[focus];
    var label = focus.charAt(0).toUpperCase() + focus.slice(1);

    var notes = {
      groundedness: supported === total
        ? 'Every claim traces to the retrieved context. Note that this says nothing '
          + 'about whether those claims are TRUE - only that the answer did not invent them.'
        : (total - supported) + ' claim(s) appear nowhere in the context. That is the '
          + 'definition of a hallucination in a RAG system, and it is measurable '
          + 'without a human.',
      correctness: correct === total
        ? 'Every claim matches the reference answer. Correctness needs a ground truth, '
          + 'which is why it is the expensive one to measure.'
        : (total - correct) + ' claim(s) disagree with the reference. A claim can be '
          + 'perfectly grounded in a retrieved document and still be wrong, if the '
          + 'document itself is out of date.',
      relevance: onTopic === total
        ? 'Every claim answers the question that was asked.'
        : (total - onTopic) + ' claim(s) are true, grounded, and not what was asked. '
          + 'Padding scores well on the other three dimensions and still fails the user.',
      completeness: covered === required
        ? 'Every point the reference answer requires is present.'
        : (required - covered) + ' required point(s) missing. Completeness is the '
          + 'dimension a confident, fluent, entirely correct answer can still fail.'
    };

    return {
      bars: claims.map(function (c) {
        var flags = [];
        flags.push(c.supported ? 'grounded' : 'NOT in context');
        if (!c.correct) flags.push('contradicts reference');
        if (!c.onTopic) flags.push('off topic');
        if (c.required) flags.push('required point');
        return { label: c.text, value: c.supported ? 1 : 0, max: 1,
                 tag: flags.join('  ·  '), click: c.key, on: c.supported,
                 state: focus === 'groundedness'
                   ? (c.supported ? 'hit' : 'bad')
                   : focus === 'correctness' ? (c.correct ? 'hit' : 'bad')
                   : focus === 'relevance' ? (c.onTopic ? 'hit' : 'bad')
                   : (c.required ? 'hit' : 'dim') };
      }),
      stats: [[label + ' \u2190 this page', round(value, 2)],
              ['Groundedness', round(scores.groundedness, 2)],
              ['Correctness', round(scores.correctness, 2)],
              ['Relevance', round(scores.relevance, 2)],
              ['Completeness', round(scores.completeness, 2)],
              ['claims in answer', total],
              ['points required', required]],
      badge: label + ' = ' + round(value, 2),
      note: notes[focus] + '  Click a claim to flip whether the context supports it.'
    };
  };

  // ---------------------------------------------------------------- drawing

  function drawBars(host, bars, onToggle) {
    host.textContent = '';
    bars.forEach(function (b) {
      var row = el(b.click ? 'button' : 'div',
                   'vz-rv-row' + (b.state ? ' is-' + b.state : '') +
                   (b.click ? ' is-clickable' : ''));
      if (b.click) {
        row.type = 'button';
        row.setAttribute('aria-pressed', b.on ? 'true' : 'false');
        row.addEventListener('click', function () { onToggle(b.click); });
      }
      var head = el('div', 'vz-rv-rowhead');
      head.appendChild(el('span', 'vz-rv-label', b.label));
      head.appendChild(el('span', 'vz-rv-value', String(b.value)));
      row.appendChild(head);
      var track = el('div', 'vz-rv-track');
      var fill = el('div', 'vz-rv-fill');
      var pct = b.max ? Math.max(0, Math.min(100, (b.value / b.max) * 100)) : 0;
      fill.style.width = pct + '%';
      track.appendChild(fill);
      row.appendChild(track);
      if (b.tag) row.appendChild(el('span', 'vz-rv-tag', b.tag));
      host.appendChild(row);
    });
  }

  function drawStats(host, stats) {
    host.textContent = '';
    stats.forEach(function (pair) {
      var row = el('div', 'vz-rv-stat');
      row.appendChild(el('span', 'vz-rv-stat-k', pair[0]));
      row.appendChild(el('span', 'vz-rv-stat-v', String(pair[1])));
      host.appendChild(row);
    });
  }

  // ----------------------------------------------------------------- wiring

  // What a select hands the model. Some models index an array with it
  // (tfidf and crag both do data.queries[p.query]), so the position is the
  // useful value there. Others need a name - a token, a separator strategy -
  // and got the raw index instead, which threw or silently took the wrong
  // branch. An option can now declare the value its model should see.
  function optionValue(c, i) {
    var o = c.options[i];
    return o && o.value !== undefined ? o.value : i;
  }

  function buildControls(host, controls, onChange) {
    var values = {};

    controls.forEach(function (c) {
      values[c.id] = c.kind === 'select' ? optionValue(c, c.value) : c.value;
      var wrap = el('div', 'vz-rv-control');

      if (c.kind === 'toggle') {
        var btn = el('button', 'vz-rv-toggle', c.label);
        btn.type = 'button';
        btn.setAttribute('aria-pressed', c.value ? 'true' : 'false');
        if (c.value) btn.classList.add('is-on');
        btn.addEventListener('click', function () {
          values[c.id] = !values[c.id];
          btn.classList.toggle('is-on', values[c.id]);
          btn.setAttribute('aria-pressed', values[c.id] ? 'true' : 'false');
          onChange(values);
        });
        wrap.appendChild(btn);
        host.appendChild(wrap);
        return;
      }

      var head = el('div', 'vz-rv-chead');
      // The id here is what tools/build_labs.py reads as a control, so the
      // predict-then-reveal panel can drive this page like any other.
      var label = el('label', 'vz-rv-clabel', c.label);
      label.setAttribute('for', c.id + '-input');
      head.appendChild(label);
      var readout = el('span', 'vz-rv-cvalue', c.kind === 'select'
        ? String(c.options[c.value].label || c.options[c.value])
        : String(c.value));
      readout.id = c.id + '-value';
      head.appendChild(readout);
      wrap.appendChild(head);

      var input;
      if (c.kind === 'select') {
        input = el('select', 'viz-input');
        c.options.forEach(function (o, i) {
          var opt = el('option', null, o.label || o);
          opt.value = String(i);
          input.appendChild(opt);
        });
        input.value = String(c.value);
      } else {
        input = el('input', null);
        input.type = 'range';
        input.min = c.min;
        input.max = c.max;
        input.step = c.step || 1;
        input.value = c.value;
      }
      input.id = c.id + '-input';
      input.addEventListener('input', function () {
        var v = Number(input.value);
        values[c.id] = c.kind === 'select' ? optionValue(c, v) : v;
        readout.textContent = c.kind === 'select'
          ? (c.options[v].label || c.options[v]) : String(v);
        onChange(values);
      });
      wrap.appendChild(input);
      host.appendChild(wrap);
    });

    return values;
  }

  function wire(block) {
    var tag = block.querySelector('.vz-rv-data');
    var model = MODELS[block.getAttribute('data-model')];
    if (!tag || !model) return;

    var spec;
    try {
      spec = JSON.parse(tag.textContent);
    } catch (err) {
      if (window.console) console.error('vz-rv: bad spec', err);
      return;
    }

    var controlHost = block.querySelector('.vz-rv-controls');
    var barHost = block.querySelector('.vz-rv-bars');
    var statHost = block.querySelector('.vz-rv-stats');
    var noteHost = block.querySelector('.vz-rv-note');
    var badgeHost = block.querySelector('.vz-rv-badge');

    // Rows a model marks clickable toggle a key in this set, which the model
    // reads back on the next render. It is how a reader marks which results
    // are relevant, rather than being told.
    var toggled = {};

    function render(values) {
      values.__on = toggled;
      var out;
      try {
        out = model(values, spec.data || {});
      } catch (err) {
        if (window.console) console.error('vz-rv: model failed', err);
        return;
      }
      if (barHost) drawBars(barHost, out.bars || [], function (key) {
        toggled[key] = !toggled[key];
        render(values);
      });
      if (statHost) drawStats(statHost, out.stats || []);
      if (noteHost) noteHost.textContent = out.note || '';
      if (badgeHost) badgeHost.textContent = out.badge || '';
    }

    var values = buildControls(controlHost, spec.controls || [], render);
    render(values);
  }

  function init() {
    var blocks = document.querySelectorAll('.vz-rv[data-vz-rv]');
    for (var i = 0; i < blocks.length; i++) wire(blocks[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
