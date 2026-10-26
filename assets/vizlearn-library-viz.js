/* Small, dependency-free interactive explainers for the Python library tracks. */
(() => {
  const rootSelector = '[data-vz-library-viz]';
  const esc = (value) => String(value).replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[c]);
  const shell = (title, intro, controls, stage) => `
    <section class="vz-libviz" aria-label="Interactive visualization">
      <div class="vz-libviz-head"><div><span class="vz-libviz-kicker">Interactive visualization</span>
        <h2>${title}</h2><p>${intro}</p></div><span class="vz-libviz-live" data-live>Ready</span></div>
      <div class="vz-libviz-layout"><div class="vz-libviz-controls">${controls}</div>
        <div class="vz-libviz-stage">${stage}</div></div>
    </section>`;
  const button = (label, action = 'update') => `<button class="vz-libviz-button" type="button" data-action="${action}">${label}</button>`;
  const field = (label, html, extra = '') => `<label class="vz-libviz-field">${label}${html}${extra}</label>`;
  const select = (name, options) => `<select data-control="${name}">${options.map(([v, t]) => `<option value="${v}">${t}</option>`).join('')}</select>`;
  const range = (name, min, max, value, step = 1) => `<input type="range" data-control="${name}" min="${min}" max="${max}" value="${value}" step="${step}"><output data-output="${name}">${value}</output>`;
  const input = (name, value) => `<input type="text" data-control="${name}" value="${esc(value)}" spellcheck="false">`;
  const readout = (html = '') => `<div class="vz-libviz-readout" data-readout aria-live="polite">${html}</div>`;
  const svgOpen = '<svg class="vz-libviz-svg" viewBox="0 0 640 270" role="img" aria-label="Interactive data visualization">';
  const line = (x1, y1, x2, y2, cls = '') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}"></line>`;

  function initPydantic(root) {
    root.innerHTML = shell('What happens at validation?', 'Edit the incoming JSON, then validate it against a small typed model.',
      field('Incoming JSON', '<textarea data-control="json" rows="5">{\n  "name": "Ada",\n  "modules_done": 12\n}</textarea>') + button('Validate'),
      `<div class="vz-libviz-flow" data-flow><span class="vz-flow-node">JSON input</span><b>→</b><span class="vz-flow-node">Pydantic</span><b>→</b><span class="vz-flow-node">Typed model</span></div>${readout('<strong>Ready to validate</strong><span>Required: name (text), modules_done (integer)</span>')}`);
    const update = () => {
      const out = root.querySelector('[data-readout]');
      const flow = root.querySelector('[data-flow]');
      try {
        const value = JSON.parse(root.querySelector('[data-control="json"]').value);
        const errors = [];
        if (!value || typeof value !== 'object' || Array.isArray(value)) errors.push('Expected a JSON object.');
        else {
          if (typeof value.name !== 'string' || !value.name.trim()) errors.push('name: expected a non-empty string');
          if (!Number.isInteger(value.modules_done)) errors.push('modules_done: expected an integer');
        }
        if (errors.length) {
          out.innerHTML = `<strong>ValidationError</strong><span>${errors.map(esc).join('<br>')}</span>`;
          flow.classList.add('is-error'); root.querySelector('[data-live]').textContent = 'Rejected';
        } else {
          out.innerHTML = `<strong>Validated model</strong><span>name = ${esc(value.name)} · modules_done = ${value.modules_done}</span>`;
          flow.classList.remove('is-error'); root.querySelector('[data-live]').textContent = 'Validated';
        }
      } catch (error) {
        out.innerHTML = `<strong>Invalid JSON</strong><span>${esc(error.message)}</span>`;
        flow.classList.add('is-error'); root.querySelector('[data-live]').textContent = 'Invalid JSON';
      }
    };
    root.querySelector('[data-action]').addEventListener('click', update);
  }

  function initNumpy(root) {
    root.innerHTML = shell('One operation, every element', 'Change the operation and compare the input arrays with the computed result.',
      field('Operation', select('op', [['add', 'Add'], ['multiply', 'Multiply'], ['subtract', 'Subtract']])) +
      field('Array A', input('a', '2, 4, 6')) + field('Array B', input('b', '1, 3, 5')) + button('Apply operation'),
      `<div data-chart></div>${readout()}`);
    const update = () => {
      const parse = (n) => root.querySelector(`[data-control="${n}"]`).value.split(',').map(Number);
      const a = parse('a'), b = parse('b'), op = root.querySelector('[data-control="op"]').value;
      const out = root.querySelector('[data-readout]');
      if (!a.length || a.length !== b.length || [...a, ...b].some((n) => !Number.isFinite(n))) {
        out.textContent = 'Enter two comma-separated arrays of equal length.';
        root.querySelector('[data-chart]').innerHTML = ''; return;
      }
      const fn = { add: (x,y) => x+y, multiply: (x,y) => x*y, subtract: (x,y) => x-y }[op];
      const result = a.map((n,i) => fn(n,b[i]));
      const max = Math.max(1, ...a.map(Math.abs), ...b.map(Math.abs), ...result.map(Math.abs));
      const rows = [['A', a], ['B', b], ['Result', result]];
      root.querySelector('[data-chart]').innerHTML = `${svgOpen}${rows.map(([label, values], ri) =>
        `<text x="18" y="${58+ri*68}" class="vz-svg-label">${label}</text>${values.map((n,i) => {
          const x=112+i*165, width=Math.max(3,Math.abs(n)/max*115), y=36+ri*68;
          return `<rect x="${x}" y="${y}" width="${width}" height="34" rx="5" class="${ri===2?'vz-svg-accent':'vz-svg-bar'}"></rect><text x="${x+width+7}" y="${y+22}" class="vz-svg-value">${Number(n.toFixed(2))}</text>`;
        }).join('')}`).join('')}${line(104,24,104,238,'vz-svg-axis')}</svg>`;
      out.innerHTML = `<strong>${esc(op)} applied elementwise</strong><span>[${result.map(n=>Number(n.toFixed(3))).join(', ')}]</span>`;
      root.querySelector('[data-live]').textContent = 'Computed';
    };
    root.querySelector('[data-action]').addEventListener('click', update); update();
  }

  function initFastapi(root) {
    root.innerHTML = shell('Trace one request through the app', 'Change the payload type. Invalid request data is rejected before the endpoint runs.',
      field('modules_done', select('value', [['12','12 · integer'], ['twelve','"twelve" · text'], ['-1','-1 · integer']])) + button('Send request'),
      `<div class="vz-libviz-flow" data-flow><span class="vz-flow-node">Request</span><b>→</b><span class="vz-flow-node">Pydantic</span><b>→</b><span class="vz-flow-node">Endpoint</span><b>→</b><span class="vz-flow-node">Response</span></div>${readout()}`);
    const update = () => {
      const invalid = root.querySelector('[data-control="value"]').value === 'twelve';
      const nodes = [...root.querySelectorAll('.vz-flow-node')];
      nodes.forEach((node,i) => node.classList.toggle('is-active', i < (invalid ? 2 : 4)));
      nodes[2].classList.toggle('is-skipped', invalid);
      root.querySelector('[data-readout]').innerHTML = invalid
        ? '<strong>422 · Request validation failed</strong><span>The endpoint did not run. FastAPI returned the Pydantic error.</span>'
        : '<strong>200 · Endpoint returned</strong><span>The payload passed validation and the endpoint ran.</span>';
      root.querySelector('[data-live]').textContent = invalid ? '422 response' : '200 response';
    };
    root.querySelector('[data-action]').addEventListener('click', update); update();
  }

  function initPandas(root) {
    const data = [
      ['Ada','Python','Done'], ['Lin','NumPy','In progress'], ['Sam','pandas','Done'],
      ['Mira','FastAPI','In progress'], ['Noah','sklearn','Done'], ['Ivy','Matplotlib','In progress']
    ];
    root.innerHTML = shell('Filter rows, then inspect the result', 'Choose a status to see how a boolean mask keeps matching rows in a DataFrame.',
      field('Status', select('status', [['All','All rows'], ['Done','Done'], ['In progress','In progress']])) + button('Apply filter'),
      `<div class="vz-libviz-table-wrap"><table class="vz-libviz-table"><thead><tr><th>Name</th><th>Module</th><th>Status</th></tr></thead><tbody data-rows></tbody></table></div>${readout()}`);
    const update = () => {
      const status = root.querySelector('[data-control="status"]').value;
      const rows = data.filter((r) => status === 'All' || r[2] === status);
      root.querySelector('[data-rows]').innerHTML = rows.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`).join('');
      root.querySelector('[data-readout]').innerHTML = `<strong>${rows.length} of ${data.length} rows</strong><span>Equivalent to df[df["status"] ${status === 'All' ? 'notna()' : `== "${status}"`}].</span>`;
      root.querySelector('[data-live]').textContent = `${rows.length} rows shown`;
    };
    root.querySelector('[data-action]').addEventListener('click', update); update();
  }

  function initMatplotlib(root) {
    root.innerHTML = shell('The chart type changes the visual encoding', 'Switch chart types to see the same small dataset represented in different ways.',
      field('Chart', select('chart', [['line','Line'], ['bar','Bar'], ['scatter','Scatter'], ['hist','Histogram']])) +
      field('Number of points', range('count', 3, 8, 5)) + button('Redraw'),
      `<div data-chart></div>${readout()}`);
    const update = () => {
      const count = Number(root.querySelector('[data-control="count"]').value), type = root.querySelector('[data-control="chart"]').value;
      root.querySelector('[data-output="count"]').value = count;
      const vals = Array.from({length: count}, (_,i) => 3 + ((i*7+2)%9));
      const pts = vals.map((v,i) => [72+i*(496/Math.max(1,count-1)), 218-v*15]);
      let mark = '';
      if (type === 'bar') mark = pts.map(([x,y],i)=>`<rect x="${x-18}" y="${y}" width="36" height="${218-y}" class="vz-svg-accent"></rect>`).join('');
      else if (type === 'scatter') mark = pts.map(([x,y])=>`<circle cx="${x}" cy="${y}" r="7" class="vz-svg-accent"></circle>`).join('');
      else if (type === 'hist') {
        const bins=[0,0,0,0]; vals.forEach(v=>bins[Math.min(3,Math.floor((v-3)/3))]++);
        mark=bins.map((v,i)=>`<rect x="${94+i*120}" y="${218-v*34}" width="88" height="${v*34}" class="vz-svg-accent"></rect>`).join('');
      } else mark = `<polyline points="${pts.map(p=>p.join(',')).join(' ')}" class="vz-svg-line"></polyline>`+pts.map(([x,y])=>`<circle cx="${x}" cy="${y}" r="5" class="vz-svg-accent"></circle>`).join('');
      root.querySelector('[data-chart]').innerHTML = `${svgOpen}${line(54,218,600,218,'vz-svg-axis')}${line(54,28,54,218,'vz-svg-axis')}${mark}<text x="320" y="254" class="vz-svg-label" text-anchor="middle">observation</text></svg>`;
      root.querySelector('[data-readout]').innerHTML = `<strong>${type === 'hist' ? 'Distribution across bins' : `${count} ${type} marks`}</strong><span>Rendered from the same values: ${vals.join(', ')}.</span>`;
      root.querySelector('[data-live]').textContent = 'Chart redrawn';
    };
    root.querySelector('[data-action]').addEventListener('click', update);
    root.querySelector('[data-control="chart"]').addEventListener('change', update);
    root.querySelector('[data-control="count"]').addEventListener('input', update); update();
  }

  function initSklearn(root) {
    const points = [0.08,0.14,0.2,0.27,0.33,0.39,0.46,0.51,0.58,0.64,0.7,0.77,0.84,0.91];
    const labels = [0,0,0,0,1,0,1,0,1,1,0,1,1,1];
    root.innerHTML = shell('Move the decision threshold', 'A higher threshold predicts fewer positives. Compare predictions with the known labels.',
      field('Threshold', range('threshold', 0.1, 0.9, 0.5, 0.05)) + button('Update predictions'),
      `<div data-chart></div>${readout()}`);
    const update = () => {
      const threshold = Number(root.querySelector('[data-control="threshold"]').value);
      root.querySelector('[data-output="threshold"]').value = threshold.toFixed(2);
      let tp=0,fp=0,tn=0,fn=0;
      const circles=points.map((p,i)=>{
        const pred=p>=threshold?1:0, actual=labels[i];
        if(pred&&actual)tp++; else if(pred&&!actual)fp++; else if(!pred&&!actual)tn++; else fn++;
        const x=58+p*520, y=actual?72:164;
        return `<circle cx="${x}" cy="${y}" r="8" class="${pred?'vz-svg-accent':'vz-svg-muted'}"><title>score ${p.toFixed(2)}, actual ${actual}, predicted ${pred}</title></circle>`;
      }).join('');
      const x=58+threshold*520;
      root.querySelector('[data-chart]').innerHTML = `${svgOpen}<text x="15" y="76" class="vz-svg-label">positive</text><text x="15" y="168" class="vz-svg-label">negative</text>${line(58,118,578,118,'vz-svg-axis')}${line(x,34,x,204,'vz-svg-threshold')}${circles}<text x="${Math.min(560,x+5)}" y="28" class="vz-svg-label">${threshold.toFixed(2)}</text></svg>`;
      root.querySelector('[data-readout]').innerHTML = `<strong>Confusion counts</strong><span>TP ${tp} · FP ${fp} · TN ${tn} · FN ${fn}</span>`;
      root.querySelector('[data-live]').textContent = `Threshold ${threshold.toFixed(2)}`;
    };
    root.querySelector('[data-action]').addEventListener('click', update);
    root.querySelector('[data-control="threshold"]').addEventListener('input', update); update();
  }

  const initializers = { pydantic: initPydantic, numpy: initNumpy, fastapi: initFastapi, pandas: initPandas, matplotlib: initMatplotlib, sklearn: initSklearn };
  document.querySelectorAll(rootSelector).forEach((root) => initializers[root.dataset.vzLibraryViz]?.(root));
})();
