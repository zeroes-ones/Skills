/* Skill Chain Explorer v2 — dependency-free (no frameworks, no CDN).
 * Reads the embedded graph from <script type="application/json" id="graph-data">
 * (emitted by scripts/emit-skill-graph.py) so the page works from file:// and
 * GitHub Pages alike.
 *
 * v2 changes: directional arrowheads + incoming/outgoing edge coloring (feeds vs
 * consumes), domain chips (click to zoom into a field), a pathfinder (shortest
 * chain between two skills along feed direction, undirected fallback), hub
 * quick-jump, neighbor labels on hover, and a calmer dark diagram look.
 */
"use strict";

(function () {
  const DATA = document.getElementById("graph-data");
  const GRAPH = DATA && DATA.textContent.trim()
    ? JSON.parse(DATA.textContent)
    : null;
  if (!GRAPH || !GRAPH.nodes || !GRAPH.nodes.length) {
    document.body.innerHTML =
      '<div style="padding:20px;color:#8b98b4">' +
      "Graph data missing — run <code>python3 scripts/emit-skill-graph.py</code> to regenerate.</div>";
    return;
  }

  const W = 1600, H = 1150;
  const svg = document.getElementById("graph");
  const tooltip = document.getElementById("tooltip");
  const panel = document.getElementById("panel");
  const pathResult = document.getElementById("pathResult");
  const NS = "http://www.w3.org/2000/svg";

  /* ---------- data prep ---------- */
  const nodes = GRAPH.nodes;
  const links = GRAPH.links;              // {s, b, dir: out|in|both}
  const stats = GRAPH.stats || {};
  const byId = {};
  nodes.forEach((n) => (byId[n.id] = n));

  const arrows = [];                       // directed [from, to]
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
  links.forEach((l) => {
    adj[l.s].add(l.b);
    adj[l.b].add(l.s);
  });

  const domainOrder = Object.keys(stats.domains || {}).sort();
  const domainColor = {};
  domainOrder.forEach((d, i) => {
    domainColor[d] = "hsl(" + ((i * 137.508) % 360) + ",62%,58%)";
  });
  const colorOf = (n) => domainColor[n.label] || "#58a6ff";
  const radiusOf = (n) => {
    const deg = (adj[n.id] ? adj[n.id].size : 0);
    return Math.max(6, Math.min(13, 6 + deg * 0.6));
  };

  /* ---------- layers ---------- */
  const world = document.createElementNS(NS, "g");
  world.setAttribute("id", "world");
  svg.appendChild(world);
  const edgeLayer = document.createElementNS(NS, "g");
  const arrowLayer = document.createElementNS(NS, "g");
  const pathLayer = document.createElementNS(NS, "g");
  const nodeLayer = document.createElementNS(NS, "g");
  const labelLayer = document.createElementNS(NS, "g");
  world.appendChild(edgeLayer);
  world.appendChild(arrowLayer);
  world.appendChild(pathLayer);
  world.appendChild(nodeLayer);
  world.appendChild(labelLayer);

  /* ---------- edges + directional arrows ---------- */
  const edgeData = []; // {line, arrows:[{g, src, tgt}]}
  function addPolygon(pts) {
    const p = document.createElementNS(NS, "polygon");
    p.setAttribute("points", pts);
    arrowLayer.appendChild(p);
    return p;
  }
  function arrowGeometry(src, tgt) {
    const a = byId[src], b = byId[tgt];
    let dx = b.x - a.x, dy = b.y - a.y;
    const len = Math.hypot(dx, dy) || 1;
    dx /= len; dy /= len;
    const px = -dy, py = dx;
    const tipX = b.x - dx * (radiusOf(b) + 2);
    const tipY = b.y - dy * (radiusOf(b) + 2);
    const bx = tipX - dx * 10, by = tipY - dy * 10;
    const w = 4.2;
    return tipX + "," + tipY + " " +
      (bx + px * w) + "," + (by + py * w) + " " +
      (bx - px * w) + "," + (by - py * w);
  }
  links.forEach((l) => {
    const line = document.createElementNS(NS, "line");
    line.setAttribute("stroke", "#39445e");
    line.setAttribute("stroke-width", 1);
    line.setAttribute("stroke-linecap", "round");
    edgeLayer.appendChild(line);
    const rec = { line, s: l.s, b: l.b, arrows: [] };
    const dirs = l.dir === "out" ? [[l.s, l.b]]
      : l.dir === "in" ? [[l.b, l.s]]
      : [[l.s, l.b], [l.b, l.s]];
    dirs.forEach(([src, tgt]) => {
      const g = addPolygon(arrowGeometry(src, tgt));
      g.setAttribute("fill", "#5b6b8f");
      rec.arrows.push({ g, src, tgt });
    });
    edgeData.push(rec);
  });

  /* ---------- nodes ---------- */
  const nodeEls = {};
  nodes.forEach((n) => {
    const g = document.createElementNS(NS, "g");
    g.setAttribute("class", "node");
    g.dataset.id = n.id;
    const r = radiusOf(n);
    const circle = document.createElementNS(NS, "circle");
    circle.setAttribute("r", r);
    circle.setAttribute("fill", colorOf(n));
    circle.setAttribute("stroke", "#0b0f17");
    circle.setAttribute("stroke-width", 1.4);
    g.appendChild(circle);
    if (r >= 11) { // hub glow
      const ring = document.createElementNS(NS, "circle");
      ring.setAttribute("class", "hub-ring");
      ring.setAttribute("r", r + 4);
      ring.setAttribute("fill", "none");
      ring.setAttribute("stroke", "rgba(88,166,255,.35)");
      ring.setAttribute("stroke-width", 1);
      g.appendChild(ring);
    }
    nodeLayer.appendChild(g);
    nodeEls[n.id] = { g, r };
  });

  function positionAll() {
    nodes.forEach((n) => {
      nodeEls[n.id].g.setAttribute("transform", "translate(" + n.x + "," + n.y + ")");
    });
    edgeData.forEach((e) => {
      const a = byId[e.s], b = byId[e.b];
      e.line.setAttribute("x1", a.x);
      e.line.setAttribute("y1", a.y);
      e.line.setAttribute("x2", b.x);
      e.line.setAttribute("y2", b.y);
    });
  }

  /* ---------- view ---------- */
  let view = { x: 0, y: 0, k: 1 };
  function setTransform() {
    world.setAttribute(
      "transform", "translate(" + view.x + "," + view.y + ") scale(" + view.k + ")");
  }
  function fit() {
    const r = svg.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const k = Math.min(r.width / (W + 120), r.height / (H + 120));
    view = { x: (r.width - W * k) / 2, y: (r.height - H * k) / 2, k: Math.max(k, 0.02) };
    setTransform();
  }
  function zoomAt(cx, cy, factor) {
    const k2 = Math.min(8, Math.max(0.02, view.k * factor));
    view.x = cx - ((cx - view.x) * k2) / view.k;
    view.y = cy - ((cy - view.y) * k2) / view.k;
    view.k = k2;
    setTransform();
  }
  function zoomToIds(ids, pad) {
    const r = svg.getBoundingClientRect();
    if (!ids.length || !r.width) return;
    const xs = [], ys = [];
    ids.forEach((id) => { xs.push(byId[id].x); ys.push(byId[id].y); });
    const minx = Math.min.apply(null, xs), maxx = Math.max.apply(null, xs);
    const miny = Math.min.apply(null, ys), maxy = Math.max.apply(null, ys);
    const wpx = maxx - minx + pad * 2, hpx = maxy - miny + pad * 2;
    const k = Math.min(8, Math.max(0.05, Math.min(r.width / (wpx || 1), r.height / (hpx || 1))));
    view = {
      x: r.width / 2 - ((minx + maxx) / 2) * k,
      y: r.height / 2 - ((miny + maxy) / 2) * k,
      k,
    };
    setTransform();
  }
  function flyTo(id) {
    const n = byId[id];
    const r = svg.getBoundingClientRect();
    view = { x: r.width / 2 - n.x * 0.9, y: r.height / 2 - n.y * 0.9, k: 0.9 };
    setTransform();
  }

  /* ---------- view state + render ---------- */
  const S = { node: null, sel: null, domain: null, path: null };
  let hovered = null;
  let panning = null;

  const C_IN = "#58a6ff", C_OUT = "#e3b341", C_BASE = "#39445e",
    C_NEUTRAL = "#5b6b8f", C_PATH = "#e3b341";

  function pathSet() {
    return S.path ? new Set(S.path) : null;
  }
  function inMode() {
    return S.path || S.domain;
  }

  function render() {
    const pset = pathSet();
    const domSet = S.domain
      ? new Set(nodes.filter((n) => n.label === S.domain).map((n) => n.id))
      : null;
    const vis = pset || domSet || null;
    const active = S.node;

    // nodes
    Object.keys(nodeEls).forEach((id) => {
      let o;
      if (vis) o = vis.has(id) ? 1 : 0.06;
      else if (active) o = (active === id || adj[active].has(id)) ? 1 : 0.12;
      else o = 0.92;
      nodeEls[id].g.style.opacity = o;
    });

    // edges + arrows
    const amber = new Set(), blue = new Set(), pathEdges = S.path ? new Set() : null;
    if (S.path) {
      for (let i = 0; i < S.path.length - 1; i++) {
        pathEdges.add(S.path[i] + "\u0001" + S.path[i + 1]);
        pathEdges.add(S.path[i + 1] + "\u0001" + S.path[i]);
      }
    }
    edgeData.forEach((e) => {
      const key1 = e.s + "\u0001" + e.b, key2 = e.b + "\u0001" + e.s;
      const onPath = pathEdges && (pathEdges.has(key1) || pathEdges.has(key2));
      let on = false;
      if (vis) on = vis.has(e.s) && vis.has(e.b);
      else if (active) on = (e.s === active && adj[active].has(e.b)) ||
                            (e.b === active && adj[active].has(e.s));
      else on = true;

      if (onPath) { amber.add(e.s + "\u0001" + e.b); blue.delete(e.s + "\u0001" + e.b); }
      else if (active) {
        let isAmber = false, isBlue = false;
        e.arrows.forEach((a) => {
          if (a.src === active) isAmber = true;
          if (a.tgt === active) isBlue = true;
        });
        if (isAmber) amber.add(key1);
        else if (isBlue) blue.add(key1);
      }
      e.line.style.opacity = on ? (vis ? 0.55 : 0.9) : 0.05;
      e.line.setAttribute("stroke-width", onPath ? 2.6 : 1);
      e.line.style.stroke = onPath ? C_PATH : active ? (amber.has(key1) ? C_OUT : blue.has(key1) ? C_IN : C_BASE) : C_BASE;
      e.arrows.forEach((a) => {
        const kk = a.src + "\u0001" + a.tgt;
        a.g.style.opacity = e.line.style.opacity;
        a.g.setAttribute("fill", onPath ? C_PATH
          : active ? (a.src === active ? C_OUT : a.tgt === active ? C_IN : C_NEUTRAL)
          : C_NEUTRAL);
        void kk;
      });
    });

    // labels
    labelLayer.innerHTML = "";
    const labelIds = [];
    if (active) labelIds.push(active);
    if (S.domain) {
      // small labels for the domain's nodes when zoomed close enough
      if (view.k >= 1.4) domSet.forEach((id) => labelIds.push(id));
    }
    if (hovered && !S.domain && !S.path) {
      const neigh = (adj[hovered] || []);
      if (neigh.length <= 14) neigh.forEach((id) => labelIds.push(id));
    }
    labelIds.forEach((id, i) => {
      const n = byId[id];
      const t = document.createElementNS(NS, "text");
      t.setAttribute("x", n.x);
      t.setAttribute("y", n.y - radiusOf(n) - 6);
      t.setAttribute("text-anchor", "middle");
      t.setAttribute("fill", "#e6edf3");
      t.setAttribute("font-size", i === 0 ? 26 : 15);
      t.setAttribute("stroke", "#0b0f17");
      t.setAttribute("stroke-width", i === 0 ? 5 : 3);
      t.setAttribute("paint-order", "stroke");
      t.textContent = n.id;
      labelLayer.appendChild(t);
    });
  }

  /* ---------- pathfinder: BFS along feed direction ---------- */
  function bfsDirected(from, to) {
    if (from === to) return [from];
    const prev = {};
    const seen = new Set([from]);
    const queue = [from];
    while (queue.length) {
      const cur = queue.shift();
      for (const nxt of (outOf[cur] || [])) {
        if (seen.has(nxt)) continue;
        seen.add(nxt);
        prev[nxt] = cur;
        if (nxt === to) {
          const route = [to];
          let p = to;
          while (p !== from) { p = prev[p]; route.unshift(p); }
          return route;
        }
        queue.push(nxt);
      }
    }
    return null;
  }
  function bfsUndirected(from, to) {
    if (from === to) return [from];
    const prev = {};
    const seen = new Set([from]);
    const queue = [from];
    while (queue.length) {
      const cur = queue.shift();
      adj[cur].forEach((nxt) => {
        if (seen.has(nxt)) return;
        seen.add(nxt);
        prev[nxt] = cur;
        queue.push(nxt);
      });
    }
    if (!(to in prev)) return null;
    const route = [to];
    let p = to;
    while (p !== from) { p = prev[p]; route.unshift(p); }
    return route;
  }
  function resolveSkill(q) {
    q = (q || "").trim().toLowerCase();
    if (!q) return null;
    const hit = nodes.find((n) => n.id.toLowerCase() === q);
    if (hit) return hit.id;
    const pre = nodes.find((n) => n.id.toLowerCase().startsWith(q));
    if (pre) return pre.id;
    return nodes.find((n) => n.id.toLowerCase().includes(q))?.id || null;
  }
  function findPath() {
    const a = resolveSkill(document.getElementById("pathFrom").value);
    const b = resolveSkill(document.getElementById("pathTo").value);
    if (!a) { showPathError("Unknown start skill — check the name."); return; }
    if (!b) { showPathError("Unknown target skill — check the name."); return; }
    let route = bfsDirected(a, b);
    const directed = !!route;
    if (!route) route = bfsUndirected(a, b);
    if (!route) { showPathError("No path found between " + a + " and " + b + "."); return; }
    S.path = route;
    S.domain = null;
    S.sel = null;
    pathResult.className = "";
    pathResult.innerHTML = "<b>" + a + "</b> → " + route.slice(1, -1).map(esc).join(" → ") +
      (route.length > 1 ? " → <b>" + b + "</b>" : "") +
      " &nbsp;<span style='color:#8b98b4'>(" + (route.length - 1) + " hop" +
      (route.length > 2 ? "s" : "") + (directed ? ", along feed direction" : ", reverse/shortest") + ")</span>";
    setChipState(null);
    render();
    zoomToIds(route, 120);
  }
  function showPathError(msg) {
    pathResult.className = "err";
    pathResult.textContent = msg;
    void hovered;
  }

  /* ---------- domain chips ---------- */
  const chipsEl = document.getElementById("chips");
  const chipEls = {};
  function buildChips() {
    function mk(label, count) {
      const c = document.createElement("button");
      c.className = "chip-btn";
      c.innerHTML = esc(label) + (count != null ? "<span class='n'>" + count + "</span>" : "");
      c.addEventListener("click", () => {
        if (label === "All") {
          clearDomain();
          S.path = null;
          if (!S.sel) fit();
          render();
          return;
        }
        if (S.domain === label) { clearDomain(); return; }
        S.domain = label;
        S.path = null;
        S.sel = null;
        setChipState(label);
        render();
        const ids = nodes.filter((n) => n.label === label).map((n) => n.id);
        zoomToIds(ids, 90);
        showDomainPanel(label);
      });
      return c;
    }
    const all = mk("All", stats.nodes);
    chipsEl.appendChild(all);
    chipEls["__all__"] = all;
    domainOrder.forEach((d) => {
      const c = mk(d, stats.domains[d]);
      chipsEl.appendChild(c);
      chipEls[d] = c;
    });
  }
  function setChipState(label) {
    Object.keys(chipEls).forEach((k) => {
      chipEls[k].classList.toggle("active", k === label);
    });
  }
  function clearDomain() {
    S.domain = null;
    setChipState(null);
    render();
    if (!S.sel && !S.path) fit();
  }
  function showDomainPanel(label) {
    const ids = nodes.filter((n) => n.label === label).map((n) => n.id);
    panel.innerHTML = "";
    const h = document.createElement("h2");
    h.textContent = label + " domain";
    panel.appendChild(h);
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.textContent = ids.length + " skills";
    panel.appendChild(meta);
    const ls = document.createElement("div");
    ls.className = "neighbors";
    ls.style.cssText = "display:flex;flex-direction:column;gap:4px";
    ids.sort().forEach((id) => ls.appendChild(chipFor(id)));
    panel.appendChild(ls);
    void stats;
  }

  /* ---------- selection / panel ---------- */
  function esc(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }
  function chipFor(id) {
    const n = byId[id];
    const el = document.createElement("div");
    el.className = "chip";
    const dot = document.createElement("span");
    dot.className = "dot";
    dot.style.background = colorOf(n);
    el.appendChild(dot);
    const txt = document.createElement("span");
    txt.textContent = id + "  ·  " + n.label;
    el.appendChild(txt);
    el.addEventListener("click", () => {
      selectNode(id);
      flyTo(id);
    });
    return el;
  }
  function selectNode(id) {
    S.sel = id;
    S.node = id;
    S.path = null;
    setChipState(null);
    render();
    const n = byId[id];
    panel.innerHTML = "";
    const h = document.createElement("h2");
    h.textContent = n.id;
    panel.appendChild(h);
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.textContent = "domain: " + n.label +
      (n.type ? "  ·  type: " + n.type : "") +
      "  ·  " + adj[id].size + " connections";
    panel.appendChild(meta);
    const code = document.createElement("code");
    code.className = "path";
    code.textContent = n.path + "/SKILL.md";
    panel.appendChild(code);
    if (n.desc) {
      const d = document.createElement("p");
      d.className = "desc";
      d.textContent = n.desc;
      panel.appendChild(d);
    }
    const linksBox = document.createElement("div");
    linksBox.className = "links";
    const gh = document.createElement("a");
    gh.href = "https://github.com/zeroes-ones/Skills/blob/main/" + n.path + "/SKILL.md";
    gh.target = "_blank"; gh.rel = "noopener"; gh.textContent = "view on GitHub ↗";
    const ss = document.createElement("a");
    ss.href = "https://skills.sh/zeroes-ones/Skills/" + n.id;
    ss.target = "_blank"; ss.rel = "noopener"; ss.textContent = "skills.sh ↗";
    linksBox.appendChild(gh);
    linksBox.appendChild(ss);
    panel.appendChild(linksBox);

    const cons = (into[n.id] || []).slice();
    const feeds = (outOf[n.id] || []).slice();
    const sec = (label) => {
      const t = document.createElement("div");
      t.className = "section-label";
      t.textContent = label;
      panel.appendChild(t);
      const box = document.createElement("div");
      box.style.cssText = "display:flex;flex-direction:column;gap:4px";
      return box;
    };
    if (cons.length) {
      const box = sec("consumes from (" + cons.length + ")");
      cons.sort().forEach((c) => box.appendChild(chipFor(c)));
      panel.appendChild(box);
    }
    if (feeds.length) {
      const box = sec("feeds into (" + feeds.length + ")");
      feeds.sort().forEach((f) => box.appendChild(chipFor(f)));
      panel.appendChild(box);
    }
  }

  /* ---------- events ---------- */
  svg.addEventListener("pointerdown", (e) => {
    if (e.target.closest(".node")) return;
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
  svg.addEventListener("pointerup", () => {
    panning = null;
    svg.classList.remove("panning");
  });
  svg.addEventListener("wheel", (e) => {
    e.preventDefault();
    const r = svg.getBoundingClientRect();
    zoomAt(e.clientX - r.left, e.clientY - r.top, e.deltaY < 0 ? 1.14 : 0.88);
    render();
  }, { passive: false });

  function onOver(e) {
    const g = e.target.closest(".node");
    if (!g) { return; }
    hovered = g.dataset.id;
    if (!S.domain && !S.path) S.node = hovered;
    render();
    const n = byId[hovered];
    const r = svg.getBoundingClientRect();
    tooltip.style.display = "block";
    tooltip.style.left = e.clientX - r.left + 14 + "px";
    tooltip.style.top = e.clientY - r.top + 14 + "px";
    tooltip.innerHTML = "<b>" + esc(n.id) + "</b><br><span style='color:#8b98b4'>" +
      esc(n.label) + (n.type ? " · " + esc(n.type) : "") + "</span><br>" +
      (adj[n.id] ? adj[n.id].size : 0) + " connections" +
      "<br><span style='color:#58a6ff'>← " + (into[n.id] ? into[n.id].length : 0) + "</span>" +
      " <span style='color:#e3b341'>→ " + (outOf[n.id] ? outOf[n.id].length : 0) + "</span>";
  }
  function onOut(e) {
    const g = e.target.closest(".node");
    if (g && g.dataset.id === hovered) return; // moving within same node group
    hovered = null;
    if (!S.domain && !S.path) S.node = S.sel;
    tooltip.style.display = "none";
    render();
  }
  svg.addEventListener("pointerover", onOver);
  svg.addEventListener("pointerout", onOut);
  nodeLayer.addEventListener("click", (e) => {
    const g = e.target.closest(".node");
    if (!g) return;
    hovered = g.dataset.id;
    selectNode(g.dataset.id);
    if (S.domain) {
      // stay zoomed in domain, just select
      render();
    } else {
      flyTo(g.dataset.id);
    }
  });

  /* ---------- search ---------- */
  const search = document.getElementById("search");
  search.addEventListener("input", () => {
    const q = search.value.trim().toLowerCase();
    const activeSel = S.sel;
    if (!q) {
      if (S.domain || S.path) { S.node = activeSel; render(); }
      else { S.node = activeSel; render(); }
      return;
    }
    const hits = nodes.filter(
      (n) => n.id.toLowerCase().includes(q) ||
        n.label.toLowerCase().includes(q) ||
        (n.desc || "").toLowerCase().includes(q));
    const ids = new Set(hits.map((n) => n.id));
    Object.keys(nodeEls).forEach((id) => {
      nodeEls[id].g.style.opacity = ids.has(id) ? 1 : 0.05;
    });
    if (hits.length === 1) flyTo(hits[0].id);
    if (hits.length === 0) { S.sel = null; }
  });
  search.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;
    const q = search.value.trim().toLowerCase();
    const hit = nodes.find((n) => n.id.toLowerCase() === q) ||
      nodes.find((n) => n.id.toLowerCase().startsWith(q)) ||
      nodes.find((n) => n.id.toLowerCase().includes(q));
    if (hit) {
      selectNode(hit.id);
      flyTo(hit.id);
    }
    e.preventDefault();
  });

  /* ---------- pathfinder wiring ---------- */
  document.getElementById("pathBtn").addEventListener("click", findPath);
  [["pathFrom", 0], ["pathTo", 1]].forEach(([id]) => {
    document.getElementById(id).addEventListener("keydown", (e) => {
      if (e.key === "Enter") { findPath(); e.preventDefault(); }
    });
  });

  /* ---------- stats ---------- */
  const statsEl = document.getElementById("stats");
  if (statsEl && stats.nodes) {
    statsEl.innerHTML =
      "<span><b>" + stats.nodes + "</b> skills</span>" +
      "<span><b>" + stats.directed_edges + "</b> chain edges</span>" +
      "<span><b>" + stats.undirected_edges + "</b> connections</span>" +
      "<span><b>" + (stats.domains ? Object.keys(stats.domains).length : 0) + "</b> domains</span>";
  }

  /* ---------- boot ---------- */
  buildChips();
  window.addEventListener("resize", () => {
    if (!S.domain && !S.path) fit();
  });
  positionAll();
  render();
  fit();
  const first = (stats.hubs && stats.hubs[0] && stats.hubs[0].id) || nodes[0].id;
  selectNode(first);
  flyTo(first);
})();
