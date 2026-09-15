# What the reader's Python can and cannot do

Measured, not remembered. Regenerate after any Pyodide upgrade:

```bash
node .claude/skills/rewrite/probe.mjs
```

**Runtime: CPython 3.12.1 on wasm32** (Pyodide 0.26.4, loaded from
`cdn.jsdelivr.net` by `assets/vizlearn-python.js`, executed in a Web Worker).

The build machine is **CPython 3.9.6**. That divergence is real and has bitten:
`JUMP_BACKWARD` does not exist in 3.9, so a comprehension article that printed
opcode names worked in the editor and failed on the build. Local success proves
nothing about what the reader sees — always verify with `verify.mjs`.

## Raises — never write an example that depends on these

| Call | What you get |
|---|---|
| `threading.Thread(...).start()` | `RuntimeError: can't start new thread` |
| `ThreadPoolExecutor(...).submit(...)` | `RuntimeError: can't start new thread` |
| `os.fork()` | `OSError [Errno 52] Function not implemented` |
| `multiprocessing.Process(...).start()` | `OSError [Errno 52] Function not implemented` |
| `subprocess.run(...)` | `OSError [Errno 138] emscripten does not support processes` |
| `socket.create_connection(...)` | `TimeoutError` |
| `urllib.request.urlopen(...)` | `URLError: unknown url type: https` |
| `asyncio.run(...)` | `RuntimeError: cannot be called from a running event loop` |
| `import resource` | `ModuleNotFoundError` |

Two consequences worth designing around:

- **The concurrency and async tracks cannot demonstrate parallelism by running
  it.** They demonstrate it by *measuring the machinery* — the switch interval,
  the bytecode count, lock and queue protocol, a hand-driven `Future` — and by
  saying plainly that the sandbox is single-threaded. An article whose code
  silently no-ops here is worse than one that says so.
- **The runner is already inside an event loop**, so async examples use
  top-level `await`, never `asyncio.run(...)`.

## Works

| Call | Note |
|---|---|
| `time.perf_counter()` | the one to time with |
| `threading.Lock` / `Event` / `Semaphore` / `Condition` | the *protocol* works; only `start()` fails |
| `queue.Queue` put/get | full API |
| `sys.getswitchinterval()` | `0.005` |
| `dis.get_instructions` | works, but opcode *names* differ from 3.9 — describe what instructions do, not what they're called |
| `pickle` | round-trips |
| `open()` for read and write | in-memory FS |
| `sys.getsizeof` | real numbers |

## Silently useless

- **`time.process_time()` returns `0.0`.** Any cpu-versus-wall-clock
  demonstration is dead on arrival — it will print `0.0` and appear to prove
  whatever you claimed. One article now carries a labelled static block
  explaining why instead of a fake measurement.

## Packages

Per-track, from `tools/runnable_specs.py` — `numpy`, `pandas`,
`scikit-learn`, `matplotlib` (AGG backend, no DOM), `pydantic`. Wheels load from
the CDN on first use and cache into `node_modules`, so the first `verify.mjs`
run for a track is slow and the rest are not.

The `python` track has **no** `runnable_specs` entry: a `*-run` fence there
renders as static code. Its editors live in committed HTML.

## Counter-intuitive results this runtime has produced

Keep these in mind before writing "X is faster than Y" — each was measured here
and each contradicted the article that originally claimed otherwise:

- A **generator expression was slower** than the list comprehension it was
  supposed to beat. The real win is memory: 812,028 bytes versus 104.
- **`array("q")` pickled 1.84× larger** than a list of small ints.
- **`heapq.merge` is ~3× slower** than concatenate-and-sort for full
  materialisation; its win is the first value (0.3 ms versus 140 ms).
- **`nlargest` lost to a full sort** on data with few distinct values, and won
  155.9 ms → 11.9 ms on data with many.
