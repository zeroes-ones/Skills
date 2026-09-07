/* Skill Chain Explorer v3 — cinematic, Apple-HIG-flavored, dependency-free.
 * Data embedded from scripts/emit-skill-graph.py (<script id="graph-data">).
 *
 * Two visual scenes:
 *   OVERVIEW ("constellations") — domain clusters + aggregated inter-field arcs,
 *     no edge spaghetti until you go deeper.
 *   FIELD / SKILL / PATH — the actual force graph of skills, zoomed and focused.
 *
 * Apple HIG principles applied: hierarchy first (overview -> field -> skill),
 * purposeful motion (eased camera flights, entrance), glass surfaces, generous
 * spacing, SF-style type, and prefers-reduced-motion respected.
 */
"use strict";

(function () {
  const DATA = document.getElementById("graph-data");
  const GRAPH = DATA && DATA.textContent.trim() ? JSON.parse(DATA.textContent) : null;
  if (!GRAPH || !GRAPH.nodes || !GRAPH.nodes.length) {
    document.body.innerHTML =
      '<div style="padding:30px;color:#9aa7bf">Graph data missing — run ' +
      '<code>python3 scripts/emit-skill-graph.py</code>.</div>';
    return;
  }

  const REDUCED = typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const W = 1600, H = 1150;
  const svg = document.getElementById("graph");
  const tooltip = document.getElementById("tooltip");
  const panel = document.getElementById("panel");
  const pathResult = document.getElementById("pathResult");
  const crumbRoot = document.getElementById("crumbRoot");
  const crumbCurrent = document.getElementById("crumbCurrent");
  const browse = document.getElementById("browse");
  const NS = "http://www.w3.org/2000/svg";

  /* ---------- data ---------- */
  const nodes = GRAPH.nodes;
  const links = GRAPH.links;
  const stats = GRAPH.stats || {};
  const byId = {};
  nodes.forEach((n) => (byId[n.id] = n));

  const arrows = [];
  links.forEach((l) => {
    if (l.dir === "out" || l.dir === "both") arrows.push([l.s, l.b]);
    if (l.dir === "in" || l.dir === "both") arrows.push([l.b, l.s]);
  });
  const outOf = {}, into = {};
  arrows.forEach(([f, t]) => {
    (outOf[f] = outOf[f] || []).push(t);
    (into[t] = into[t] || []).push(f);
  });
  const adj = {};
  nodes.forEach((n) => (adj[n.id] = new Set()));
  links.forEach((l) => { adj[l.s].add(l.b); adj[l.b].add(l.s); });

  const domainOrder = Object.keys(stats.domains || {}).sort();
  const domainColor = {};
  domainOrder.forEach((d, i) => { domainColor[d] = "hsl(" + ((i * 137.508) % 360) + ",70%,64%)"; });
  const colorOf = (n) => domainColor[n.label] || "#4da3ff";
  const radiusOf = (n) => Math.max(6, Math.min(13, 6 + (adj[n.id] ? adj[n.id].size : 0) * 0.6));

  /* ---------- layers ---------- */
  const world = document.createElementNS(NS, "g");
  world.setAttribute("id", "world");
  svg.appendChild(world);
  const clusterLayer = document.createElementNS(NS, "g");
  const arcLayer = document.createElementNS(NS, "g");
  const edgeLayer = document.createElementNS(NS, "g");
  const arrowLayer = document.createElementNS(NS, "g");
  const pathLayer = document.createElementNS(NS, "g");
  const nodeLayer = document.createElementNS(NS, "g");
  const labelLayer = document.createElementNS(NS, "g");
  world.appendChild(arcLayer);
  world.appendChild(clusterLayer);
  world.appendChild(edgeLayer);
  world.appendChild(arrowLayer);
  world.appendChild(pathLayer);
  world.appendChild(nodeLayer);
  world.appendChild(labelLayer);

  /* ---------- domain clusters & arcs ---------- */
  const domainNodes = {};
  domainOrder.forEach((d) => { domainNodes[d] = nodes.filter((n) => n.label === d).map((n) => n.id); });
  const centroid = (ids) => {
    let x = 0, y = 0;
    ids.forEach((id) => { x += byId[id].x; y += byId[id].y; });
    return { x: x / ids.length, y: y / ids.length };
  };
  const clusterPos = {};
  domainOrder.forEach((d) => { clusterPos[d] = centroid(domainNodes[d]); });
  const clusterR = {};
  domainOrder.forEach((d) => { clusterR[d] = 13 + 2.2 * Math.sqrt(domainNodes[d].length); });

  const clusterEls = {};
  domainOrder.forEach((d) => {
    const g = document.createElementNS(NS, "g");
    g.setAttribute("class", "cluster");
    g.dataset.domain = d;
    const halo = document.createElementNS(NS, "circle");
    halo.setAttribute("class", "halo");
    halo.setAttribute("r", clusterR[d] + 10);
    halo.setAttribute("stroke", domainColor[d]);
    const body = document.createElementNS(NS, "circle");
    body.setAttribute("r", clusterR[d]);
    body.setAttribute("fill", domainColor[d]);
    body.setAttribute("fill-opacity", 0.16);
    body.setAttribute("stroke", domainColor[d]);
    body.setAttribute("stroke-width", 1.5);
    g.appendChild(halo);
    g.appendChild(body);
    const t = document.createElementNS(NS, "text");
    t.setAttribute("text-anchor", "middle");
    t.setAttribute("y", -clusterR[d] - 12);
    t.setAttribute("fill", "#e8edf7");
    t.setAttribute("font-size", 17);
    t.setAttribute("stroke", "#05070f");
    t.setAttribute("stroke-width", 4);
    t.setAttribute("paint-order", "stroke");
    t.textContent = d;
    const c = document.createElementNS(NS, "text");
    c.setAttribute("text-anchor", "middle");
    c.setAttribute("y", 4);
    c.setAttribute("font-size", 12);
    c.setAttribute("fill", "rgba(255,255,255,.75)");
    c.textContent = domainNodes[d].length;
    g.appendChild(t);
    g.appendChild(c);
    clusterLayer.appendChild(g);
    clusterEls[d] = { g, pos: clusterPos[d], r: clusterR[d] };
  });

  // aggregated inter-field arcs
  const arcCount = {};
  links.forEach((l) => {
    const a = byId[l.s], b = byId[l.b];
    if (!a || !b || a.label === b.label) return;
    const k = a.label < b.label ? a.label + "\u0001" + b.label : b.label + "\u0001" + a.label;
    arcCount[k] = (arcCount[k] || 0) + 1;
  });
  const arcEls = {};
  Object.keys(arcCount).forEach((k) => {
    const [d1, d2] = k.split("\u0001");
    const p = document.createElementNS(NS, "path");
    p.setAttribute("class", "arc");
    p.setAttribute("stroke", "#7f8db0");
    p.setAttribute("stroke-width", Math.min(3, 0.5 + Math.sqrt(arcCount[k]) * 0.35));
    p.setAttribute("opacity", Math.min(0.5, 0.08 + arcCount[k] * 0.012));
    arcLayer.appendChild(p);
    arcEls[k] = { p, d1, d2, n: arcCount[k] };
  });
  function layoutArcs() {
    Object.keys(arcEls).forEach((k) => {
      const a = clusterEls[arcEls[k].d1], b = clusterEls[arcEls[k].d2];
      if (!a || !b) return;
      const mx = (a.pos.x + b.pos.x) / 2, my = (a.pos.y + b.pos.y) / 2;
      const dx = b.pos.x - a.pos.x, dy = b.pos.y - a.pos.y;
      const len = Math.hypot(dx, dy) || 1;
      const lift = Math.min(120, len * 0.16);
      const cx = mx - (dy / len) * lift, cy = my + (dx / len) * lift;
      arcEls[k].p.setAttribute("d",
        "M" + a.pos.x + "," + a.pos.y + " Q" + cx + "," + cy + " " + b.pos.x + "," + b.pos.y);
    });
  }

  /* ---------- skill edges + arrows ---------- */
  const edgeData = [];
  function arrowPts(src, tgt) {
    const a = byId[src], b = byId[tgt];
    let dx = b.x - a.x, dy = b.y - a.y;
    const len = Math.hypot(dx, dy) || 1; dx /= len; dy /= len;
    const px = -dy, py = dx;
    const tipX = b.x - dx * (radiusOf(b) + 2), tipY = b.y - dy * (radiusOf(b) + 2);
    const bx = tipX - dx * 10, by = tipY - dy * 10, w = 4.2;
    return tipX + "," + tipY + " " + (bx + px * w) + "," + (by + py * w) + " " +
      (bx - px * w) + "," + (by - py * w);
  }
  links.forEach((l) => {
    const line = document.createElementNS(NS, "line");
    line.setAttribute("stroke", "#39445e");
    line.setAttribute("stroke-width", 1);
    edgeLayer.appendChild(line);
    const rec = { line, s: l.s, b: l.b, arrows: [] };
    const dirs = l.dir === "out" ? [[l.s, l.b]] : l.dir === "in" ? [[l.b, l.s]]
      : [[l.s, l.b], [l.b, l.s]];
    dirs.forEach(([src, tgt]) => {
      const p = document.createElementNS(NS, "polygon");
      p.setAttribute("points", arrowPts(src, tgt));
      p.setAttribute("fill", "#5b6b8f");
      arrowLayer.appendChild(p);
      rec.arrows.push({ p, src, tgt });
    });
    edgeData.push(rec);
  });
  function positionSkills() {
    nodes.forEach((n) => {
      const g = nodeEls[n.id].g;
      g.setAttribute("transform", "translate(" + n.x + "," + n.y + ")");
    });
    edgeData.forEach((e) => {
      const a = byId[e.s], b = byId[e.b];
      e.line.setAttribute("x1", a.x); e.line.setAttribute("y1", a.y);
      e.line.setAttribute("x2", b.x); e.line.setAttribute("y2", b.y);
    });
  }

  /* ---------- nodes ---------- */
  const nodeEls = {};
  nodes.forEach((n) => {
    const g = document.createElementNS(NS, "g");
    g.setAttribute("class", "node");
    g.dataset.id = n.id;
    const r = radiusOf(n);
    const c = document.createElementNS(NS, "circle");
    c.setAttribute("r", r);
    c.setAttribute("fill", colorOf(n));
    c.setAttribute("stroke", "#0a0f1e");
    c.setAttribute("stroke-width", 1.4);
    g.appendChild(c);
    if (r >= 11) {
      const ring = document.createElementNS(NS, "circle");
      ring.setAttribute("r", r + 4);
      ring.setAttribute("fill", "none");
      ring.setAttribute("stroke", "rgba(120,170,255,.4)");
      ring.setAttribute("stroke-width", 1);
      g.appendChild(ring);
    }
    nodeLayer.appendChild(g);
    nodeEls[n.id] = { g, r };
  });

  /* ---------- view ---------- */
  let view = { x: 0, y: 0, k: 1 };
  function setTransform() {
    world.setAttribute("transform", "translate(" + view.x + "," + view.y + ") scale(" + view.k + ")");
  }
  function fitAll() {
    const r = svg.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const k = Math.min(r.width / (W + 160), r.height / (H + 160));
    view = { x: (r.width - W * k) / 2, y: (r.height - H * k) / 2, k: Math.max(k, 0.03) };
    setTransform();
  }
  function zoomAt(cx, cy, f) {
    const k2 = Math.min(9, Math.max(0.02, view.k * f));
    view.x = cx - ((cx - view.x) * k2) / view.k;
    view.y = cy - ((cy - view.y) * k2) / view.k;
    view.k = k2;
    setTransform();
  }
  function zoomToBox(x0, y0, x1, y1, pad, minK) {
    const r = svg.getBoundingClientRect();
    if (!r.width) return;
    const w = (x1 - x0) + pad * 2, h = (y1 - y0) + pad * 2;
    let k = Math.min(9, Math.max(0.03, Math.min(r.width / (w || 1), r.height / (h || 1))));
    if (minK) k = Math.max(k, minK);
    view = {
      x: r.width / 2 - ((x0 + x1) / 2) * k,
      y: r.height / 2 - ((y0 + y1) / 2) * k,
      k,
    };
    setTransform();
  }
  function zoomToNodes(ids, pad, minK) {
    const xs = [], ys = [];
    ids.forEach((id) => { const n = byId[id]; n && (xs.push(n.x), ys.push(n.y)); });
    if (!xs.length) return;
    zoomToBox(Math.min.apply(null, xs), Math.min.apply(null, ys),
      Math.max.apply(null, xs), Math.max.apply(null, ys), pad || 90, minK);
  }
  function flyTo(id) {
    const n = byId[id], r = svg.getBoundingClientRect();
    view = { x: r.width / 2 - n.x * 1.1, y: r.height / 2 - n.y * 1.1, k: 1.1 };
    setTransform();
  }
  function kick() {
    world.classList.remove("world-enter");
    if (!REDUCED) {
      void world.getBoundingClientRect();
      world.classList.add("world-enter");
    }
  }

  /* ---------- mode & state ---------- */
  const MODE = { kind: "overview", domain: null, path: null };
  let sel = null, hover = null, panning = null;

  function layerVisibility() {
    const skillsVisible = MODE.kind !== "overview";
    const setVis = (el, v) => { el.style.display = v ? "" : "none"; };
    setVis(clusterLayer, MODE.kind === "overview");
    setVis(arcLayer, MODE.kind === "overview");
    setVis(nodeLayer, skillsVisible);
    setVis(edgeLayer, skillsVisible);
    setVis(arrowLayer, skillsVisible);
    setVis(pathLayer, skillsVisible);
    setVis(labelLayer, skillsVisible);
  }

  function crumbs() {
    crumbRoot.textContent = MODE.kind === "overview" ? "All Fields" : "All Fields";
    if (MODE.kind === "overview") crumbCurrent.textContent = "constellations";
    else if (MODE.kind === "domain") crumbCurrent.textContent = MODE.domain;
    else if (MODE.kind === "path") crumbCurrent.textContent = "chain path";
    else crumbCurrent.textContent = (sel && byId[sel] ? sel : "skill");
  }
  crumbRoot.addEventListener("click", goOverview);

  function goOverview() {
    MODE.kind = "overview"; MODE.domain = null; MODE.path = null; sel = null; hover = null;
    layerVisibility(); crumbs(); renderOverview();
    panelEmpty();
    fitAll(); kick();
  }

  function enterDomain(label) {
    MODE.kind = "domain"; MODE.domain = label; MODE.path = null; sel = null;
    layerVisibility(); crumbs();
    renderDomain();
    zoomToNodes(domainNodes[label], 110, 0.55);
    renderDomain();   // re-run after zoom so inline labels respect the level of detail
    showDomainPanel(label);
    kick();
  }

  function panelEmpty() {
    panel.innerHTML = '<div id="empty">Click a field to explore it, a skill to inspect it, or trace a chain between two skills.</div>';
  }
  function browseDomains() {
    browse.innerHTML = "";
    domainOrder.forEach((d) => {
      const el = document.createElement("div");
      el.className = "browse-item";
      const dot = document.createElement("span");
      dot.className = "dot";
      dot.style.background = domainColor[d];
      el.appendChild(dot);
      const nm = document.createElement("span");
      nm.textContent = d;
      el.appendChild(nm);
      const n = document.createElement("span");
      n.className = "n";
      n.textContent = domainNodes[d].length;
      el.appendChild(n);
      el.addEventListener("click", () => enterDomain(d));
      browse.appendChild(el);
    });
  }

  /* ---------- rendering ---------- */
  const C_IN = "#4da3ff", C_OUT = "#e9b44c", C_BASE = "#39445e", C_PATH = "#e9b44c";

  function setDomainClusterFocus(domain) {
    Object.keys(clusterEls).forEach((d) => {
      const el = clusterEls[d].g;
      const on = !domain || d === domain;
      el.style.opacity = on ? 1 : 0.25;
      el.firstChild.setAttribute("stroke-width", on ? 1 : 0.5);
    });
    Object.keys(arcEls).forEach((k) => {
      const a = arcEls[k];
      const on = !domain || a.d1 === domain || a.d2 === domain;
      arcEls[k].p.style.opacity = on ? Math.min(0.5, 0.08 + a.n * 0.012) : 0.03;
    });
  }
  function renderOverview() {
    Object.keys(clusterEls).forEach((d) => {
      clusterEls[d].g.setAttribute("transform",
        "translate(" + clusterEls[d].pos.x + "," + clusterEls[d].pos.y + ")");
    });
    layoutArcs();
    setDomainClusterFocus(null);
  }
  function neighborsOf(id) { const s = new Set(adj[id] || []); s.add(id); return s; }

  function renderDomain() {
    const keep = new Set(domainNodes[MODE.domain] || []);
    Object.keys(nodeEls).forEach((id) => {
      nodeEls[id].g.style.opacity = keep.has(id) ? 0.96 : 0.05;
    });
    edgeData.forEach((e) => {
      const on = keep.has(e.s) && keep.has(e.b);
      e.line.style.opacity = on ? 0.6 : 0.02;
      e.line.style.stroke = C_BASE;
      e.line.setAttribute("stroke-width", 1);
      e.arrows.forEach((a) => { a.p.style.opacity = on ? 0.7 : 0.02; a.p.setAttribute("fill", "#6b7ba0"); });
    });
    labelLayer.innerHTML = "";
    if (view.k >= 1.05) {
      keep.forEach((id) => {
        const n = byId[id], t = document.createElementNS(NS, "text");
        t.setAttribute("x", n.x); t.setAttribute("y", n.y - radiusOf(n) - 5);
        t.setAttribute("text-anchor", "middle"); t.setAttribute("font-size", 14);
        t.setAttribute("fill", "#dfe6f2"); t.setAttribute("stroke", "#05070f");
        t.setAttribute("stroke-width", 3); t.setAttribute("paint-order", "stroke");
        t.textContent = n.id;
        labelLayer.appendChild(t);
      });
    }
  }

  function renderNodeMode() {
    const active = hover || sel;
    const neigh = active ? neighborsOf(active) : null;
    Object.keys(nodeEls).forEach((id) => {
      let o;
      if (MODE.kind === "domain" && !(domainNodes[MODE.domain] || []).includes(id)) o = 0.04;
      else if (active) o = neigh.has(id) ? 1 : 0.1;
      else o = 0.9;
      nodeEls[id].g.style.opacity = o;
    });
    edgeData.forEach((e) => {
      let on;
      if (MODE.kind === "domain") on = (domainNodes[MODE.domain] || []).includes(e.s) &&
        (domainNodes[MODE.domain] || []).includes(e.b);
      else if (active) on = neigh.has(e.s) && neigh.has(e.b);
      else on = true;
      e.line.style.opacity = on ? (active ? 0.9 : 0.5) : 0.03;
      let col = C_BASE;
      if (active) {
        let amber = false, blue = false;
        e.arrows.forEach((a) => { if (a.src === active) amber = true; if (a.tgt === active) blue = true; });
        col = amber ? C_OUT : blue ? C_IN : C_BASE;
      }
      e.line.style.stroke = col;
      e.line.setAttribute("stroke-width", 1);
      e.arrows.forEach((a) => {
        a.p.style.opacity = e.line.style.opacity;
        a.p.setAttribute("fill", active ? (a.src === active ? C_OUT : a.tgt === active ? C_IN : "#6b7ba0") : "#6b7ba0");
      });
    });
    renderLabels(active);
  }

  function renderPath() {
    if (!MODE.path) return;
    const set = new Set(MODE.path);
    Object.keys(nodeEls).forEach((id) => {
      nodeEls[id].g.style.opacity = set.has(id) ? 1 : 0.07;
    });
    const pathEdges = new Set();
    for (let i = 0; i < MODE.path.length - 1; i++) {
      pathEdges.add(MODE.path[i] + "\u0001" + MODE.path[i + 1]);
      pathEdges.add(MODE.path[i + 1] + "\u0001" + MODE.path[i]);
    }
    edgeData.forEach((e) => {
      const k1 = e.s + "\u0001" + e.b, k2 = e.b + "\u0001" + e.s;
      const on = pathEdges.has(k1) || pathEdges.has(k2);
      e.line.style.opacity = on ? 1 : 0.04;
      e.line.style.stroke = on ? C_PATH : C_BASE;
      e.line.setAttribute("stroke-width", on ? 3 : 1);
      e.arrows.forEach((a) => {
        a.p.style.opacity = on ? 1 : 0.03;
        a.p.setAttribute("fill", on ? C_PATH : "#6b7ba0");
      });
    });
    labelLayer.innerHTML = "";
    MODE.path.forEach((id, i) => {
      const n = byId[id];
      const t = document.createElementNS(NS, "text");
      t.setAttribute("x", n.x); t.setAttribute("y", n.y - radiusOf(n) - 7);
      t.setAttribute("text-anchor", "middle");
      t.setAttribute("font-size", i === 0 || i === MODE.path.length - 1 ? 26 : 17);
      t.setAttribute("fill", "#fff"); t.setAttribute("stroke", "#05070f");
      t.setAttribute("stroke-width", i === 0 || i === MODE.path.length - 1 ? 5 : 3);
      t.setAttribute("paint-order", "stroke");
      t.textContent = n.id;
      labelLayer.appendChild(t);
    });
  }

  function renderLabels(active) {
    labelLayer.innerHTML = "";
    const ids = [];
    if (active) ids.push(active);
    if (hover && !MODE.path) {
      const nz = adj[hover] || [];
      if (nz.size <= 14) nz.forEach((x) => ids.push(x));
    }
    ids.forEach((id, i) => {
      const n = byId[id];
      const t = document.createElementNS(NS, "text");
      t.setAttribute("x", n.x); t.setAttribute("y", n.y - radiusOf(n) - 6);
      t.setAttribute("text-anchor", "middle");
      t.setAttribute("font-size", i === 0 ? 26 : 15);
      t.setAttribute("fill", "#f1f4fa"); t.setAttribute("stroke", "#05070f");
      t.setAttribute("stroke-width", i === 0 ? 5 : 3); t.setAttribute("paint-order", "stroke");
      t.textContent = n.id;
      labelLayer.appendChild(t);
    });
  }

  function renderAll() {
    crumbs();
    if (MODE.kind === "overview") { renderOverview(); return; }
    if (MODE.kind === "path") { renderPath(); return; }
    if (MODE.kind === "domain" && !hover && !sel && !view) renderDomain();
    renderNodeMode();
  }

  /* ---------- panels ---------- */
  function esc(s) { return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
  function chipFor(id) {
    const n = byId[id];
    const el = document.createElement("div");
    el.className = "chip";
    const dot = document.createElement("span");
    dot.className = "dot"; dot.style.background = colorOf(n);
    el.appendChild(dot);
    const tx = document.createElement("span");
    tx.textContent = id + "  ·  " + n.label;
    el.appendChild(tx);
    el.addEventListener("click", () => { selectNode(id); });
    return el;
  }
  function showDomainPanel(label) {
    panel.innerHTML = "";
    const h = document.createElement("h2");
    h.textContent = label;
    panel.appendChild(h);
    const tagRow = document.createElement("div");
    tagRow.className = "tag-row";
    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = domainNodes[label].length + " skills";
    tagRow.appendChild(tag);
    panel.appendChild(tagRow);
    const sec = document.createElement("div");
    sec.className = "section-label";
    sec.textContent = "Skills in this field";
    panel.appendChild(sec);
    domainNodes[label].sort().forEach((id) => panel.appendChild(chipFor(id)));
  }
  function selectNode(id) {
    sel = id;
    const n = byId[id];
    if (MODE.kind === "path") MODE.kind = "node";   // clicking out of a path returns to a focused node view
    if (MODE.kind === "overview") { enterDomain(n.label); }
    MODE.path = null;
    hover = id;
    layerVisibility();
    crumbs();
    renderNodeMode();
    if (MODE.kind === "domain" && n.label !== MODE.domain) {
      // neighboring skill from another field: focus its field
      MODE.domain = n.label;
      layerVisibility(); crumbs(); renderNodeMode();
      zoomToNodes(domainNodes[n.label], 110, 0.55);
    } else if (MODE.kind === "node") {
      flyTo(id);
    } else if (MODE.kind === "domain") {
      zoomToNodes(domainNodes[MODE.domain], 110, 0.9);
    }
    showSkillPanel(n);
    kick();
  }
  function showSkillPanel(n) {
    panel.innerHTML = "";
    const h = document.createElement("h2");
    h.textContent = n.id;
    panel.appendChild(h);
    const tagRow = document.createElement("div");
    tagRow.className = "tag-row";
    ["domain: " + n.label, "type: " + (n.type || "—"), (adj[n.id] ? adj[n.id].size : 0) + " connections"]
      .forEach((t) => { const s = document.createElement("span"); s.className = "tag"; s.textContent = t; tagRow.appendChild(s); });
    panel.appendChild(tagRow);
    const code = document.createElement("code");
    code.className = "path";
    code.textContent = n.path + "/SKILL.md";
    panel.appendChild(code);
    if (n.desc) { const d = document.createElement("p"); d.className = "desc"; d.textContent = n.desc; panel.appendChild(d); }
    const linksBox = document.createElement("div");
    linksBox.className = "links";
    [["view on GitHub ↗", "https://github.com/zeroes-ones/Skills/blob/main/" + n.path + "/SKILL.md"],
     ["skills.sh ↗", "https://skills.sh/zeroes-ones/Skills/" + n.id]]
      .forEach(([t, u]) => {
        const a = document.createElement("a");
        a.href = u; a.target = "_blank"; a.rel = "noopener"; a.textContent = t;
        linksBox.appendChild(a);
      });
    panel.appendChild(linksBox);
    const cons = (into[n.id] || []).slice().sort();
    const feeds = (outOf[n.id] || []).slice().sort();
    const block = (label, arr) => {
      if (!arr.length) return;
      const s = document.createElement("div");
      s.className = "section-label";
      s.textContent = label + " (" + arr.length + ")";
      panel.appendChild(s);
      arr.forEach((x) => panel.appendChild(chipFor(x)));
    };
    block("Consumes from", cons);
    block("Feeds into", feeds);
  }

  /* ---------- events ---------- */
  svg.addEventListener("pointerdown", (e) => {
    if (e.target.closest(".node") || e.target.closest(".cluster")) return;
    panning = { px: e.clientX, py: e.clientY, ox: view.x, oy: view.y };
    svg.classList.add("panning");
    svg.setPointerCapture(e.pointerId);
  });
  svg.addEventListener("pointermove", (e) => {
    if (panning) {
      view.x = panning.ox + (e.clientX - panning.px);
      view.y = panning.oy + (e.clientY - panning.py);
      setTransform();
    }
  });
  svg.addEventListener("pointerup", () => { panning = null; svg.classList.remove("panning"); });
  svg.addEventListener("wheel", (e) => {
    e.preventDefault();
    const r = svg.getBoundingClientRect();
    zoomAt(e.clientX - r.left, e.clientY - r.top, e.deltaY < 0 ? 1.14 : 0.88);
    if (MODE.kind === "overview") { renderOverview(); } else { renderAll(); }
  }, { passive: false });

  function tipNode(id, cx, cy) {
    const n = byId[id];
    const r = svg.getBoundingClientRect();
    tooltip.style.display = "block";
    tooltip.style.left = cx - r.left + 16 + "px";
    tooltip.style.top = cy - r.top + 16 + "px";
    tooltip.innerHTML = "<b>" + esc(n.id) + "</b><br><span style='color:#9aa7bf'>" +
      esc(n.label) + (n.type ? " · " + esc(n.type) : "") + "</span><br>" +
      (adj[n.id] ? adj[n.id].size : 0) + " connections · <span style='color:#4da3ff'>← " +
      (into[n.id] ? into[n.id].length : 0) + "</span> <span style='color:#e9b44c'>→ " +
      (outOf[n.id] ? outOf[n.id].length : 0) + "</span>";
  }
  function hideTip() { tooltip.style.display = "none"; }

  clusterLayer.addEventListener("pointerover", (e) => {
    const c = e.target.closest(".cluster");
    if (!c) return;
    setDomainClusterFocus(c.dataset.domain);
    const r = svg.getBoundingClientRect();
    tooltip.style.display = "block";
    tooltip.style.left = e.clientX - r.left + 16 + "px";
    tooltip.style.top = e.clientY - r.top + 16 + "px";
    tooltip.innerHTML = "<b>" + esc(c.dataset.domain) + "</b><br><span style='color:#9aa7bf'>" +
      domainNodes[c.dataset.domain].length + " skills — click to explore</span>";
  });
  clusterLayer.addEventListener("pointerout", () => {
    if (MODE.kind === "overview") setDomainClusterFocus(null);
    hideTip();
  });
  clusterLayer.addEventListener("click", (e) => {
    const c = e.target.closest(".cluster");
    if (!c) return;
    enterDomain(c.dataset.domain);
  });

  function onOver(e) {
    const n = e.target.closest(".node");
    if (!n) return;
    hover = n.dataset.id;
    if (MODE.kind === "domain" || MODE.kind === "node") { renderNodeMode(); tipNode(hover, e.clientX, e.clientY); }
  }
  function onOut(e) {
    const n = e.target.closest(".node");
    if (n && n.dataset.id === hover) return;
    hover = null;
    hideTip();
    if (MODE.kind === "domain" || MODE.kind === "node") renderNodeMode();
  }
  svg.addEventListener("pointerover", onOver);
  svg.addEventListener("pointerout", onOut);
  nodeLayer.addEventListener("click", (e) => {
    const n = e.target.closest(".node");
    if (!n) return;
    selectNode(n.dataset.id);
  });

  /* ---------- search ---------- */
  const search = document.getElementById("search");
  search.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;
    const q = search.value.trim().toLowerCase();
    const hit = nodes.find((x) => x.id.toLowerCase() === q) ||
      nodes.find((x) => x.id.toLowerCase().startsWith(q)) ||
      nodes.find((x) => x.id.toLowerCase().includes(q));
    if (hit) {
      if (MODE.kind === "overview") MODE.kind = "node";
      layerVisibility();
      selectNode(hit.id);
      flyTo(hit.id);
    }
    e.preventDefault();
  });

  /* ---------- pathfinder ---------- */
  function bfsDirected(from, to) {
    if (from === to) return [from];
    const prev = {}, seen = new Set([from]);
    const q = [from];
    while (q.length) {
      const cur = q.shift();
      for (const nx of (outOf[cur] || [])) {
        if (seen.has(nx)) continue;
        seen.add(nx); prev[nx] = cur;
        if (nx === to) { const r = [to]; let p = to; while (p !== from) { p = prev[p]; r.unshift(p); } return r; }
        q.push(nx);
      }
    }
    return null;
  }
  function bfsUndirected(from, to) {
    if (from === to) return [from];
    const prev = {}, seen = new Set([from]);
    const q = [from];
    while (q.length) {
      const cur = q.shift();
      adj[cur].forEach((nx) => {
        if (seen.has(nx)) return;
        seen.add(nx); prev[nx] = cur; q.push(nx);
      });
    }
    if (!(to in prev)) return null;
    const r = [to]; let p = to;
    while (p !== from) { p = prev[p]; r.unshift(p); }
    return r;
  }
  function resolve(q) {
    q = (q || "").trim().toLowerCase();
    if (!q) return null;
    return (nodes.find((x) => x.id.toLowerCase() === q) ||
      nodes.find((x) => x.id.toLowerCase().startsWith(q)) ||
      nodes.find((x) => x.id.toLowerCase().includes(q)) || null)?.id || null;
  }
  function tracePath() {
    const a = resolve(document.getElementById("pathFrom").value);
    const b = resolve(document.getElementById("pathTo").value);
    if (!a || !b) {
      pathResult.className = "err";
      pathResult.textContent = !a && !b ? "Unknown skills — check names." : "Unknown " + (!a ? "from" : "to") + " skill.";
      return;
    }
    let route = bfsDirected(a, b);
    const directed = !!route;
    if (!route) route = bfsUndirected(a, b);
    if (!route) {
      pathResult.className = "err";
      pathResult.textContent = "No chain found between " + a + " and " + b + ".";
      return;
    }
    MODE.kind = "path"; MODE.path = route; MODE.domain = null; sel = null;
    layerVisibility(); crumbs(); renderPath();
    zoomToNodes(route, 130, 0.55);
    pathResult.className = "";
    pathResult.innerHTML = "<b>" + esc(a) + "</b>" +
      (route.length > 2 ? " → … (" + (route.length - 1) + " hops) → " : " → ") + "<b>" + esc(b) + "</b>" +
      " <span style='color:#9aa7bf'>(" + (directed ? "feed direction" : "reverse/shortest") + ")</span>";
    kick();
  }
  document.getElementById("pathBtn").addEventListener("click", tracePath);
  ["pathFrom", "pathTo"].forEach((id) => {
    document.getElementById(id).addEventListener("keydown", (e) => {
      if (e.key === "Enter") { tracePath(); e.preventDefault(); }
    });
  });

  /* ---------- stats ---------- */
  const statsEl = document.getElementById("stats");
  if (statsEl && stats.nodes) {
    const stat = (n, v) => "<span class='stat'><b>" + v + "</b>" + n + "</span>";
    statsEl.innerHTML = stat("skills", stats.nodes) + stat("chain edges", stats.directed_edges) +
      stat("connections", stats.undirected_edges) +
      stat("fields", stats.domains ? Object.keys(stats.domains).length : 0);
  }

  /* ---------- boot ---------- */
  window.addEventListener("resize", () => { if (MODE.kind === "overview") fitAll(); });
  browseDomains();
  positionSkills();
  MODE.kind = "overview";
  layerVisibility();
  crumbs();
  fitAll();
  renderOverview();
  kick();
  panelEmpty();
})();
