#!/usr/bin/env node
/* Render pages in Chromium and dump what a crawler that runs JavaScript sees.
 *
 * Called by tools/scan_quality.py, which serves the repo, decides which pages
 * to scan and does all the scoring. This file only collects raw facts per
 * page, so the thresholds live in one place (the Python side).
 *
 *   node tools/scan_render.js <base-url> <pages.json> <out.json>
 *
 * pages.json is a list of repo-relative paths. Playwright is not a project
 * dependency; it is resolved from the global install (NODE_PATH=$(npm root -g)).
 */
'use strict';

const fs = require('fs');
const { chromium } = require('playwright');

const [, , BASE, PAGES, OUT] = process.argv;
const CONCURRENCY = 6;

// Runs inside the page. Keep it self-contained: nothing from this file's
// scope is visible there.
function collect() {
  const words = (s) => (s.match(/[A-Za-z0-9][A-Za-z0-9'’.-]*/g) || []).length;
  const clean = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const q = (sel) => document.querySelector(sel);
  const qa = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  const article = q('.vz-article');
  const lede = q('.vz-lede-body');

  // Prose: the article with code, the code lab, figures and the glossary's
  // hidden cards taken out. innerText of a detached clone ignores layout, so
  // read textContent of the cleaned clone instead.
  let prose = '';
  let proseParas = [];
  if (article) {
    const c = article.cloneNode(true);
    qa('script,style,svg,pre,code,.vz-py,.vz-code,.vz-console,.vz-lab,.vz-term-card,button,table', c)
      .forEach((n) => n.remove());
    prose = clean(c.textContent);
    proseParas = qa('p,li,blockquote', c).map((n) => clean(n.textContent)).filter((t) => t);
  }

  // Glossary bleed: hidden definition cards sitting inside the prose. A
  // crawler reading textContent gets "overfitoverfittingLearning noise...".
  const cards = article ? qa('.vz-term-card', article) : [];
  const bleedSamples = cards.slice(0, 3).map((card) => {
    const term = card.parentElement ? clean(card.parentElement.textContent) : '';
    return term.slice(0, 160);
  });

  // Text a crawler meets before the article starts, line by line, so the
  // Python side can measure how much of it is control labels.
  const bodyText = document.body.innerText || '';
  let preArticle = bodyText;
  if (article) {
    // The article is one contiguous run of the body's text, so its opening
    // stretch locates it; a single first line can also match the TOC.
    const head = (article.innerText || '').trim().slice(0, 200);
    const at = head ? bodyText.indexOf(head) : -1;
    if (at > 0) preArticle = bodyText.slice(0, at);
  }

  const check = q('.vz-check');
  const checkAnswers = check
    ? qa('.vz-q-answer, .vz-q-why', check).map((n) => clean(n.textContent)).filter((t) => t)
    : [];
  const checkTitle = check ? clean((check.querySelector('h2') || {}).textContent) : '';
  const cheat = q('.vz-cheatsheet .vz-cheat-text');

  const jsonld = qa('script[type="application/ld+json"]').map((s) => s.textContent);
  const dates = [];
  jsonld.forEach((t) => {
    const re = /"(date(?:Published|Modified))"\s*:\s*"([^"]+)"/g;
    let m;
    while ((m = re.exec(t))) dates.push({ field: m[1], value: m[2] });
  });
  qa('time[datetime]').forEach((t) => dates.push({ field: 'time', value: t.getAttribute('datetime') }));
  qa('meta[property$="_time"]').forEach((t) => dates.push({ field: t.getAttribute('property'), value: t.content }));
  const ldTypes = [];
  jsonld.forEach((t) => {
    const re = /"@type"\s*:\s*"([^"]+)"/g;
    let m;
    while ((m = re.exec(t))) ldTypes.push(m[1]);
  });

  const links = qa('a[href]').map((a) => a.getAttribute('href'));
  const robots = q('meta[name="robots"]');
  const bodyParas = qa('main p, article p, section p, p').map((n) => clean(n.innerText || n.textContent));

  return {
    title: document.title,
    h1: qa('h1').map((n) => clean(n.textContent)),
    h2: qa('h2').map((n) => clean(n.textContent)),
    articleH2: article ? qa('h2,h3', article).map((n) => clean(n.textContent)) : [],
    hasArticle: !!article,
    lede: lede ? clean(lede.textContent) : '',
    prose,
    proseParas,
    proseWords: words(prose),
    hasTable: article ? qa('table', article).length : 0,
    hasCode: article ? qa('pre, .vz-code', article).length : 0,
    // MathJax cannot load during the scan, so raw TeX delimiters count too.
    hasMath: article
      ? (/\\\(|\\\[|\$\$/.test(article.textContent) ? 1 : 0) +
        qa('.katex, math, mjx-container, .vz-math, .math-block, .formula-box, p.mono-font, sup, sub', article).length
      : 0,
    glossaryCards: cards.length,
    glossaryHiddenChars: cards.reduce((n, c) => n + clean(c.textContent).length, 0),
    bleedSamples,
    bodyWords: words(bodyText),
    preArticle,
    checkTitle,
    checkAnswers,
    cheatText: cheat ? clean(cheat.textContent) : '',
    dates,
    ldTypes,
    links: links.length,
    uniqueLinks: new Set(links).size,
    longParas: bodyParas.filter((t) => words(t) >= 40 && (t.match(/[.!?](\s|$)/g) || []).length >= 2).length,
    robots: robots ? robots.content : '',
    adsense: !!q('script[src*="adsbygoogle"]'),
    canonical: (q('link[rel="canonical"]') || {}).href || '',
  };
}

async function scan(browser, path) {
  const ctx = await browser.newContext({ serviceWorkers: 'block' });
  const page = await ctx.newPage();
  // Third-party requests (fonts, analytics, ads) are irrelevant to the
  // page's own text and only slow the scan or hang it offline.
  // Library CDNs (Chart.js, three.js, MathJax) are recorded, so a script
  // error they cause can be told apart from a real one in the report.
  const blockedLibs = [];
  await page.route('**/*', (route) => {
    const u = route.request().url();
    if (u.startsWith(BASE)) return route.continue();
    if (/cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com|unpkg\.com/.test(u)) blockedLibs.push(u);
    return route.abort();
  });
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message || e).slice(0, 200)));
  try {
    const resp = await page.goto(BASE + path, { waitUntil: 'load', timeout: 45000 });
    await page.waitForTimeout(600); // let deferred enhancers (glossary, lede) run
    const data = await page.evaluate(collect);
    return { path, status: resp ? resp.status() : 0, errors, blockedLibs, ...data };
  } catch (e) {
    return { path, status: 0, errors: [String(e.message || e).slice(0, 200)], failed: true };
  } finally {
    await ctx.close();
  }
}

(async () => {
  const pages = JSON.parse(fs.readFileSync(PAGES, 'utf8'));
  const browser = await chromium.launch();
  const out = [];
  let next = 0;
  async function worker() {
    while (next < pages.length) {
      const p = pages[next++];
      out.push(await scan(browser, p));
      if (out.length % 50 === 0) process.stderr.write(`  rendered ${out.length}/${pages.length}\n`);
    }
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  await browser.close();
  fs.writeFileSync(OUT, JSON.stringify(out));
})();
