// Run every ```*-run fence of an article in the runtime the site ships.
//
// The build machine is CPython 3.9.6; the reader's editor is Pyodide 0.26.4,
// which is CPython 3.12.1 on wasm32. Those disagree in ways that matter
// (JUMP_BACKWARD does not exist in 3.9; time.process_time returns 0 under
// Emscripten and not locally), so "it runs on my machine" proves nothing about
// what the reader sees. This loads the same Pyodide build headlessly.
//
//   node .claude/skills/rewrite/verify.mjs fences.json          # summary
//   SHOW=1 node .claude/skills/rewrite/verify.mjs fences.json   # full output
//
// Exit code is non-zero if any fence raised, so it can gate a rewrite.
// Reading the output against the prose is still a human step: a fence that
// runs and quietly proves nothing is the failure mode this cannot catch.

import { loadPyodide } from "pyodide";
import { readFileSync } from "node:fs";

const jobs = JSON.parse(readFileSync(process.argv[2] ?? "fences.json", "utf8"));
const py = await loadPyodide();

// Pyodide's `batched` stdout hands over ONE LINE PER CALL with the newline
// already stripped. Joining with "" welds the whole output onto one line, which
// makes a verifier lie about the very thing it exists to show.
let buf = [];
py.setStdout({ batched: (s) => buf.push(s) });
py.setStderr({ batched: (s) => buf.push(s) });

let failed = 0;
let total = 0;

for (const job of jobs) {
  if (job.packages?.length) await py.loadPackage(job.packages);
  console.log(`\n===== ${job.rel} — ${job.fences.length} fences =====`);

  for (let i = 0; i < job.fences.length; i++) {
    buf = [];
    total++;
    const t0 = Date.now();
    let status = "ok";

    // A fresh namespace per fence. The reader opens one editor and presses
    // Run; they do not inherit names from the fence above. Any fence that
    // only works because an earlier one defined something is broken for them,
    // and this is what surfaces it as a NameError.
    const ns = py.globals.get("dict")();
    try {
      await py.runPythonAsync((job.prelude ?? "") + "\n" + job.fences[i], {
        globals: ns,
      });
    } catch (e) {
      status = "RAISED";
      failed++;
      buf.push(String(e.message).trimEnd().split("\n").slice(-6).join("\n"));
    } finally {
      ns.destroy();
    }

    const out = buf.join("\n").trimEnd();
    const lines = out ? out.split("\n").length : 0;
    console.log(
      `-- fence ${i + 1}: ${status} (${Date.now() - t0}ms, ${lines} output lines)`
    );
    if (status === "RAISED" || process.env.SHOW) {
      console.log(out.split("\n").map((l) => "     " + l).join("\n"));
    }
    if (status === "ok" && lines === 0) {
      console.log("     WARNING: printed nothing. A runnable example the reader");
      console.log("     presses Run on must show them something.");
    }
  }
}

console.log(`\n${total - failed}/${total} fences ran clean.`);
if (failed) console.log(`${failed} RAISED — the rewrite is not done.`);
process.exit(failed ? 1 : 0);
