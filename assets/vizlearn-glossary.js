/* Glossary hover cards on article prose.
 *
 * Every module defines the terms it introduces and then every later module
 * uses them bare, so a reader arriving from search meets "nDCG" or "logit"
 * with nowhere to go. This marks the first mention of each known term in the
 * article and attaches a definition card on hover or focus, with a link to
 * the module that teaches it properly.
 *
 * Deliberately narrow about what it will touch:
 *
 *   - only inside .vz-article, which is the hand-written prose. Never the
 *     visualisation, the controls, the readouts or the check questions.
 *   - only text nodes, so markup is never re-parsed and no attribute, URL or
 *     script can be corrupted by a replacement.
 *   - never inside a, code, pre, kbd, h1-h3, or an existing term, so it
 *     cannot nest a tooltip in a link or rewrite a code sample.
 *   - once per term per page. A card on every occurrence would be noise.
 *
 * The page it is describing is skipped: linking "IoU" back to the IoU module
 * from inside the IoU module is a loop, not a help.
 */
(function () {
  'use strict';

  var SKIP = /^(A|CODE|PRE|KBD|SCRIPT|STYLE|H1|H2|H3|BUTTON|TEXTAREA|INPUT)$/;

  function currentPath() {
    var link = document.querySelector('link[rel="canonical"]');
    if (!link || !link.href) return '';
    return link.href.replace(/^https?:\/\/[^/]+\//, '');
  }

  function escapeRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  /* One regex per term, matching the term or any of its aliases on a word
   * boundary. Longest first so "cross-entropy" is not eaten by "entropy",
   * and "cosine similarity" wins over a bare "cosine". */
  function build(terms) {
    var out = [];
    terms.forEach(function (t) {
      var forms = (t.match || []).slice();
      if (!forms.length) return;
      forms.sort(function (a, b) { return b.length - a.length; });
      var alt = forms.map(escapeRe).join('|');
      // \b does not work against a leading "@" or a trailing "25", so the
      // boundaries are spelled out as "not a word character or hyphen".
      out.push({
        t: t,
        // Ranked by the longest form it can match, not by its display name:
        // "attention" is short but only ever matches "attention mechanism".
        len: forms[0].length,
        re: new RegExp('(^|[^\\w-])(' + alt + ')(?![\\w-])', 'i')
      });
    });
    // Longest term first, so a page mentioning both "recall" and "recall@k"
    // marks the more specific one.
    out.sort(function (a, b) { return b.len - a.len; });
    return out;
  }

  function textNodes(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var p = node.parentElement;
        while (p && p !== root) {
          if (SKIP.test(p.tagName) || p.classList.contains('vz-term')) {
            return NodeFilter.FILTER_REJECT;
          }
          p = p.parentElement;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var out = [], n;
    while ((n = walker.nextNode())) out.push(n);
    return out;
  }

  function mark(node, match, entry, prefix) {
    var value = node.nodeValue;
    var lead = match.index + match[1].length;
    var word = match[2];

    var after = node.splitText(lead);
    after.nodeValue = after.nodeValue.slice(word.length);

    var cardId = 'vz-term-card-' + entry.t.slug;

    var span = document.createElement('span');
    span.className = 'vz-term';
    span.tabIndex = 0;
    span.setAttribute('role', 'button');
    span.setAttribute('aria-label', word + ' - show definition');
    // The card is the term's description rather than a second unrelated
    // label, so a screen reader announces the definition when the term takes
    // focus instead of reading it inline as part of the sentence.
    span.setAttribute('aria-describedby', cardId);
    span.textContent = word;
    span.dataset.slug = entry.t.slug;

    var card = document.createElement('span');
    card.className = 'vz-term-card';
    card.id = cardId;
    card.setAttribute('role', 'tooltip');
    var body = '<b>' + entry.t.term + '</b>' + entry.t.def;
    if (entry.t.where && entry.t.where !== prefix.path) {
      body += '<a href="' + prefix.up + entry.t.where + '">Open the module &rarr;</a>';
    }
    card.innerHTML = body;
    span.appendChild(card);

    node.parentNode.insertBefore(span, after);
    return true;
  }

  function init() {
    var terms = window.VIZLEARN_GLOSSARY;
    var article = document.querySelector('.vz-article');
    if (!terms || !terms.length || !article) return;

    var path = currentPath();
    var prefix = { path: path, up: '../' };

    var pending = build(terms);
    var done = {};

    // One pass over the prose per term, stopping at its first hit. The node
    // list is re-read for each term because marking one splits the text node
    // it was in, which would invalidate a cached list.
    pending.forEach(function (entry) {
      if (done[entry.t.slug]) return;
      // Do not link a page to itself.
      if (entry.t.where && entry.t.where === path) return;

      var nodes = textNodes(article);
      for (var i = 0; i < nodes.length; i++) {
        var m = entry.re.exec(nodes[i].nodeValue);
        if (!m) continue;
        mark(nodes[i], m, entry, prefix);
        done[entry.t.slug] = true;
        break;
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
