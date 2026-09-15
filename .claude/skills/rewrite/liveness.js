// Does this page's interactive visualisation actually work?
//
// Paste the WHOLE of this file as the `text` of one
// mcp__Claude_Browser__javascript_tool call, on a page already loaded in the
// Browser pane. It returns JSON: {verdict, checks:[...], notes:[...]}.
// `verdict` is "PASS", "FAIL" or "NO-WIDGET". Nothing to interpret — if it
// says FAIL, the reason is in `checks`.
//
// Why it does not look at pixels: the Browser pane reports
// document.visibilityState === "hidden", and browsers do not run
// requestAnimationFrame callbacks on a hidden page. Every canvas widget here
// draws in a rAF callback, so a screenshot or a getImageData() check comes
// back blank on a perfectly healthy widget. This shims rAF to run callbacks
// immediately, re-dispatches a change on the controls to force a redraw, and
// then measures. Do not replace this with a screenshot.

(async () => {
  // A freshly navigated page in the pane may not have laid out yet, and
  // every geometric check below would then read zeros.
  await new Promise((r) => setTimeout(r, 250));
  const notes = [];
  const checks = [];
  const add = (name, pass, detail) => checks.push({ name, pass, detail });

  // ---- 1. make rAF actually run -----------------------------------------
  // The widgets capture requestAnimationFrame at call time, not at load, so
  // patching it now is enough for any redraw we trigger below.
  let rafCalls = 0;
  const realRaf = window.requestAnimationFrame;
  window.requestAnimationFrame = (cb) => {
    rafCalls++;
    const id = setTimeout(() => cb(performance.now()), 0);
    return id;
  };
  notes.push("rAF shimmed (page is " + document.visibilityState + ")");

  // ---- 2. find the widget ------------------------------------------------
  const HOOKS = [
    "data-vz-arch", "data-vz-async", "data-vz-con", "data-vz-rv",
    "data-vz-iv", "data-vz-ml", "data-vz-math", "data-vz-cv",
    "data-vz-db", "data-vz-dl", "data-vz-sql",
  ];
  let host = null, hook = null;
  for (const h of HOOKS) {
    const el = document.querySelector("[" + h + "]");
    if (el) { host = el; hook = h; break; }
  }
  if (!host) {
    const generic = document.querySelector("[data-vz-viz]");
    if (generic) { host = generic; hook = "data-vz-viz (bespoke/inline)"; }
  }
  if (!host) {
    return JSON.stringify({ verdict: "NO-WIDGET", checks, notes,
      hint: "This page has no visualisation hook. That is allowed for some " +
            "pages, but most module pages have one." }, null, 1);
  }
  add("widget host found", true, hook);

  // ---- 3. did it mount? --------------------------------------------------
  // An unmounted widget leaves only its <script type=application/json> config
  // and the JavaScript-required fallback paragraph behind.
  const svgs = host.querySelectorAll("svg").length;
  const canvases = host.querySelectorAll("canvas").length;
  const inputs = host.querySelectorAll(
    "input, select, button, [role=slider], [role=button]").length;
  const fallbackOnly =
    host.children.length > 0 &&
    [...host.children].every(
      (c) => c.tagName === "SCRIPT" || /fallback/i.test(c.className || ""));

  add("mounted (not just config + fallback)", !fallbackOnly,
      "children=" + host.children.length + " svg=" + svgs +
      " canvas=" + canvases + " controls=" + inputs);
  // Not every widget draws into an svg or a canvas: the RAG/vector-index
  // explorer (data-vz-rv) renders its bars as plain divs, and it is perfectly
  // healthy. So a "surface" is svg, canvas, or a rendered subtree.
  const painted = host.querySelectorAll("*").length;
  add("has something rendered", svgs + canvases > 0 || painted >= 6,
      "svg=" + svgs + " canvas=" + canvases + " elements=" + painted);

  // An SVG that mounted but drew nothing has no shapes in it.
  let shapes = 0;
  host.querySelectorAll("svg").forEach((s) => {
    shapes += s.querySelectorAll(
      "rect, circle, path, line, text, polyline, polygon, g > *").length;
  });
  if (svgs) add("svg has shapes", shapes > 0, "shapes=" + shapes);

  // ---- 4. controls above the stage, not below it -------------------------
  // The fix in assets/vizlearn-arch.js: sliders used to sit under a canvas
  // thousands of pixels tall, so the reader could not see what they changed.
  const firstControl = host.querySelector("input, select, button");
  const surface = host.querySelector("canvas, svg");
  if (firstControl && surface) {
    const c = firstControl.getBoundingClientRect();
    const s = surface.getBoundingClientRect();
    const gap = Math.round(c.top - s.top);
    // The defect this guards against was sliders sitting under a canvas
    // 3,800px tall (9,984px on the autoencoders page) - you had to scroll
    // past the thing you were controlling to reach the control. Controls a
    // few hundred pixels below a short chart are fine: both are on screen at
    // once. So the test is "within about one screen", not "above".
    const budget = Math.round(window.innerHeight * 0.9);
    add("controls reachable without scrolling past the stage",
        gap <= budget,
        "control sits " + gap + "px below the top of the stage " +
        "(budget " + budget + "px, one screen)");
  }

  // ---- 5. does it respond? ----------------------------------------------
  // Nudge the first range/select/button and see whether the DOM changes.
  const before = host.innerHTML.length;
  const beforeText = host.textContent.replace(/\s+/g, " ").slice(0, 4000);
  let driven = null;
  const range = host.querySelector('input[type=range]');
  const select = host.querySelector("select");
  const button = host.querySelector("button:not([disabled])");
  try {
    if (range) {
      const min = +range.min || 0, max = +range.max || 100;
      const cur = +range.value;
      range.value = String(cur === max ? min : max);
      range.dispatchEvent(new Event("input", { bubbles: true }));
      range.dispatchEvent(new Event("change", { bubbles: true }));
      driven = "range " + cur + " -> " + range.value;
    } else if (select && select.options.length > 1) {
      const i = select.selectedIndex;
      select.selectedIndex = i === 0 ? 1 : 0;
      select.dispatchEvent(new Event("change", { bubbles: true }));
      driven = "select index " + i + " -> " + select.selectedIndex;
    } else if (button) {
      button.click();
      driven = "clicked " + (button.textContent || "").trim().slice(0, 24);
    }
  } catch (e) {
    notes.push("driving a control threw: " + e.message);
  }

  await new Promise((r) => setTimeout(r, 400));

  if (driven) {
    const after = host.innerHTML.length;
    const afterText = host.textContent.replace(/\s+/g, " ").slice(0, 4000);
    const changed = after !== before || afterText !== beforeText || rafCalls > 0;
    add("responds to input", changed,
        driven + "; html " + before + "->" + after +
        ", text " + (afterText !== beforeText ? "changed" : "same") +
        ", rAF calls " + rafCalls);
  } else {
    notes.push("no range/select/button to drive - static visualisation");
  }

  // ---- 6. the inline editor, if the page has one ------------------------
  const ed = document.querySelector(".vz-py-inline");
  if (ed) {
    const cs = getComputedStyle(ed);
    add("inline editor has its frame",
        cs.borderTopStyle === "solid" && parseFloat(cs.borderTopWidth) > 0,
        "border " + cs.borderTopWidth + " " + cs.borderTopStyle +
        ", radius " + cs.borderRadius);
  }

  // ---- 7. widths line up ------------------------------------------------
  const w = (s) => {
    const e = document.querySelector(s);
    if (!e) return null;
    const r = e.getBoundingClientRect();
    return { left: Math.round(r.left), width: Math.round(r.width) };
  };
  const prose = w("[data-vz-prose]"), lab = w(".vz-lab");
  // `.vz-lab:empty { display: none }`, so a page with no check block reports
  // 0x0 for it - comparing that to the prose column is a false failure. Only
  // compare when both bands are actually laid out.
  if (prose && lab && prose.width > 0 && lab.width > 0) {
    add("reading bands share one column",
        prose.left === lab.left && prose.width === lab.width,
        "prose " + prose.left + "/" + prose.width +
        " vs lab " + lab.left + "/" + lab.width);
  } else if (prose && prose.width === 0) {
    notes.push("layout not measurable (width 0) - the pane needs " +
               "resize_window to a real size before width checks mean anything");
  }

  window.requestAnimationFrame = realRaf;
  const failed = checks.filter((c) => !c.pass);
  return JSON.stringify({
    verdict: failed.length ? "FAIL" : "PASS",
    failedCount: failed.length,
    checks,
    notes,
  }, null, 1);
})()
