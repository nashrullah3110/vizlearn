/* Parse every inline <script> in the site.
 *
 * Counting <script> vs </script> tags is not enough: an edit can leave a page
 * with balanced tags but unbalanced braces, which silently kills the whole
 * script. That is exactly how hard_vs_soft_labelling.html lost its
 * visualisation - the closing `});` of a DOMContentLoaded handler was removed
 * along with a block above it, and nothing noticed.
 *
 * Exits non-zero on any syntax error.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.join(__dirname, '..');
const SKIP_DIRS = new Set(['tools', 'assets', 'node_modules']);

function htmlFiles() {
  const dirs = fs.readdirSync(ROOT, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !d.name.startsWith('.') && !SKIP_DIRS.has(d.name))
    .map((d) => d.name);
  const out = dirs.flatMap((d) =>
    fs.readdirSync(path.join(ROOT, d))
      .filter((f) => f.endsWith('.html'))
      .map((f) => path.join(d, f)));
  out.push('index.html');
  return out.sort();
}

let parsed = 0;
let skipped = 0;
const errors = [];

for (const rel of htmlFiles()) {
  const src = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/g;
  let m;
  let n = 0;
  while ((m = re.exec(src))) {
    n++;
    const [, attrs, code] = m;
    if (/\bsrc=/.test(attrs)) continue;      // external file
    if (!code.trim()) continue;
    const type = (attrs.match(/type\s*=\s*"([^"]*)"/) || [])[1] || '';
    if (/json|importmap/i.test(type)) { skipped++; continue; }   // data, not code

    const isModule = /module/i.test(type);
    try {
      // vm.Script accepts module-level syntax that `new Function` rejects.
      if (isModule) new vm.Script(code);
      else new Function(code);
      parsed++;
    } catch (e) {
      // ES module syntax is legal there but not in a plain Function body.
      if (isModule && /import|export/.test(e.message)) { skipped++; continue; }
      errors.push(`${rel} [script ${n}]: ${e.message}`);
    }
  }
}

console.log(`inline scripts parsed: ${parsed}  (skipped ${skipped} json/importmap/module)`);
if (errors.length) {
  console.log(`\n${errors.length} SYNTAX ERROR(S):`);
  errors.forEach((e) => console.log('  - ' + e));
  process.exit(1);
}
console.log('no inline script syntax errors');
