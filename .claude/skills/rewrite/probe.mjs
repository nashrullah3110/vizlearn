import { loadPyodide } from "pyodide";
const py = await loadPyodide();
let buf = [];
py.setStdout({ batched: s => buf.push(s) });
py.setStderr({ batched: s => buf.push(s) });
const CODE = `
import sys, platform
print("VERSION|python %s on %s" % (sys.version.split()[0], platform.machine()))

def probe(label, fn):
    try:
        r = fn()
        print("OK|%s|%s" % (label, "" if r is None else str(r)[:54]))
    except Exception as e:
        print("NO|%s|%s: %s" % (label, type(e).__name__, str(e)[:52]))

import threading, time, os, queue, pickle, dis, socket
probe("threading.Thread().start()", lambda: threading.Thread(target=lambda: None).start())
probe("ThreadPoolExecutor.submit", lambda: __import__("concurrent.futures", fromlist=["x"]).ThreadPoolExecutor(2).submit(len, "ab").result())
probe("os.fork()", lambda: os.fork())
probe("multiprocessing.Process", lambda: __import__("multiprocessing").Process(target=len).start())
probe("socket.create_connection", lambda: socket.create_connection(("example.com", 80), 2))
probe("urllib.request.urlopen", lambda: __import__("urllib.request", fromlist=["x"]).urlopen("https://example.com", timeout=3))
probe("time.process_time()", lambda: time.process_time())
probe("time.perf_counter()", lambda: round(time.perf_counter(), 3))
probe("threading.Lock acquire/release", lambda: (threading.Lock().acquire(), "acquired")[1])
probe("threading.Event().set()", lambda: threading.Event().set())
probe("queue.Queue put/get", lambda: (lambda q: (q.put(1), q.get())[1])(queue.Queue()))
probe("sys.getswitchinterval()", lambda: sys.getswitchinterval())
probe("dis.get_instructions", lambda: len(list(dis.get_instructions("a=1"))))
probe("pickle round trip", lambda: pickle.loads(pickle.dumps({"a": 1})))
probe("open() write to /tmp", lambda: (open("/tmp/x.txt","w").write("hi"), "wrote")[1])
probe("subprocess.run", lambda: __import__("subprocess").run(["echo","hi"]))
probe("asyncio.run + sleep", lambda: __import__("asyncio").run(__import__("asyncio").sleep(0)))
probe("random / numpy-free math", lambda: round(__import__("random").Random(0).random(), 4))
probe("sys.getsizeof", lambda: sys.getsizeof([1,2,3]))
probe("resource.getrusage", lambda: __import__("resource").getrusage(0).ru_maxrss)
`;
await py.runPythonAsync(CODE);
console.log(buf.join("\n"));
