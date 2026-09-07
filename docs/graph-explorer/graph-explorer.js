/* Skill Chain Explorer — dependency-free UI (no frameworks, no CDN).
 * Reads the embedded graph from <script type="application/json" id="graph-data">
 * (emitted by scripts/emit-skill-graph.py) so the page works from file:// and
 * GitHub Pages alike.
 *
 * View model: data coordinates live in a 1600x1150 space; the <g id="world">
 * transform maps them onto the viewport (pan + zoom).
 */
"use strict";

(function () {
  const DATA = document.getElementById("graph-data");
  const GRAPH = DATA && DATA.textContent.trim()
    ? JSON.parse(DATA.textContent)
    : null;
  if (!GRAPH || !GRAPH.nodes || !GRAPH.nodes.length) {
    document.body.innerHTML =
      '<div id="empty" style="padding:20px;color:#8b949e">' +
      "Graph data missing — run <code>python3 scripts/emit-skill-graph.py</code> to regenerate.</div>";
    return;
  }

  const W = 1600, H = 1150;
  const svg = document.getElementById("graph");
  const viewport = document.getElementById("viewport");
  const tooltip = document.getElementById("tooltip");
  const panel = document.getElementById("panel");
  const NS = "http://www.w3.org/2000/svg";

  /* ---------- data prep ---------- */
  const nodes = GRAPH.nodes;                 // {id, domain, label, desc, type, path, x, y}
  const links = GRAPH.links;                 // {s, b, dir: out|in|both}
  const stats = GRAPH.stats || {};
  const byId = {};
  nodes.forEach((n) => (byId[n.id] = n));

  // directed arrow list: [from, to]
  const arrows = [];
  links.forEach((l) => {
    if (l.dir === "out" || l.dir === "both") arrows.push([l.s, l.b]);
    if (l.dir === "in" || l.dir === "both") arrows.push([l.b, l.s]);
  });
  const outOf = {}; // id -> [ids]
  const into = {};  // id -> [ids]
  arrows.forEach(([f, t]) => {
    (outOf[f] = outOf[f] || []).push(t);
    (into[t] = into[t] || []).push(f);
  });
  const adj = {};   // undirected neighbor set
  nodes.forEach((n) => (adj[n.id] = new Set()));
  links.forEach((l) => {
    adj[l.s].add(l.b);
    adj[l.b].add(l.s);
  });

  // deterministic domain palette
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

  /* ---------- svg scaffolding ---------- */
  const world = document.createElementNS(NS, "g");
  world.setAttribute("id", "world");
  svg.appendChild(world);

  const edgeLayer = document.createElementNS(NS, "g");
  const nodeLayer = document.createElementNS(NS, "g");
  const labelLayer = document.createElementNS(NS, "g");
  world.appendChild(edgeLayer);
  world.appendChild(nodeLayer);
  world.appendChild(labelLayer);

  /* ---------- edges ---------- */
  const edgeEls = {};
  links.forEach((l) => {
    const line = document.createElementNS(NS, "line");
    line.setAttribute("stroke", "#2d3748");
    line.setAttribute("stroke-width", 1);
    line.dataset.s = l.s;
    line.dataset.b = l.b;
    edgeLayer.appendChild(line);
    edgeEls[l.s + "\u0001" + l.b] = line;
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
    circle.setAttribute("stroke", "#0d1117");
    circle.setAttribute("stroke-width", 1.5);
    g.appendChild(circle);
    nodeLayer.appendChild(g);
    nodeEls[n.id] = { g, r };
  });

  /* ---------- interaction state ---------- */
  let view = { x: 0, y: 0, k: 1 };
  let selected = null;
  let hovered = null;
  let panning = null; // {px, py, ox, oy}

  function setTransform() {
    world.setAttribute(
      "transform",
      "translate(" + view.x + "," + view.y + ") scale(" + view.k + ")"
    );
  }
  function dataPoint(clientX, clientY) {
    const r = svg.getBoundingClientRect();
    return {
      x: (clientX - r.left - view.x) / view.k,
      y: (clientY - r.top - view.y) / view.k,
    };
  }
  function fit() {
    const r = svg.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const k = Math.min(r.width / (W + 120), r.height / (H + 120));
    view = {
      x: (r.width - W * k) / 2,
      y: (r.height - H * k) / 2,
      k: Math.max(k, 0.02),
    };
    setTransform();
  }
  function zoomAt(cx, cy, factor) {
    const k2 = Math.min(6, Math.max(0.02, view.k * factor));
    view.x = cx - ((cx - view.x) * k2) / view.k;
    view.y = cy - ((cy - view.y) * k2) / view.k;
    view.k = k2;
    setTransform();
  }

  /* ---------- highlighting ---------- */
  function neighborSet(id) {
    const set = new Set(adj[id] || []);
    set.add(id);
    return set;
  }
  function updateHighlight() {
    const active = hovered || selected;
    const show = active ? neighborSet(active) : null;
    Object.keys(nodeEls).forEach((id) => {
      const el = nodeEls[id].g;
      const dim = show && !show.has(id);
      el.style.opacity = dim ? 0.08 : show ? 1 : 0.9;
      if (active) {
        el.firstChild.setAttribute(
          "stroke",
          id === active ? "#ffffff" : "#0d1117"
        );
      } else {
        el.firstChild.setAttribute("stroke", "#0d1117");
      }
    });
    Object.keys(edgeEls).forEach((key) => {
      const line = edgeEls[key];
      const on =
        active && show && show.has(line.dataset.s) && show.has(line.dataset.b);
      line.style.opacity = on ? 0.9 : active ? 0.04 : 0.35;
      line.style.stroke = on && active ? "#58a6ff" : "#2d3748";
    });
    if (active) nodeLayer.appendChild(nodeEls[active].g); // bring to front
    labelLayer.innerHTML = "";
    if (active) {
      const n = byId[active];
      const t = document.createElementNS(NS, "text");
      t.setAttribute("x", n.x);
      t.setAttribute("y", n.y - radiusOf(n) - 6);
      t.setAttribute("text-anchor", "middle");
      t.setAttribute("class", "node-title");
      t.setAttribute("fill", "#e6edf3");
      t.setAttribute("font-size", 26);
      t.setAttribute("stroke", "#0d1117");
      t.setAttribute("stroke-width", 5);
      t.setAttribute("paint-order", "stroke");
      t.textContent = n.id;
      labelLayer.appendChild(t);
    }
  }

  /* ---------- rendering (positions) ---------- */
  function positionNodes() {
    nodes.forEach((n) => {
      const { g } = nodeEls[n.id];
      g.setAttribute("transform", "translate(" + n.x + "," + n.y + ")");
    });
    links.forEach((l) => {
      const a = byId[l.s], b = byId[l.b];
      const line = edgeEls[l.s + "\u0001" + l.b];
      line.setAttribute("x1", a.x);
      line.setAttribute("y1", a.y);
      line.setAttribute("x2", b.x);
      line.setAttribute("y2", b.y);
    });
  }

  /* ---------- selection / panel ---------- */
  function esc(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }
  function chipFor(id, dir) {
    const n = byId[id];
    const el = document.createElement("div");
    el.className = "chip";
    const dot = document.createElement("span");
    dot.className = "dot";
    dot.style.background = colorOf(n);
    el.appendChild(dot);
    el.appendChild(document.createTextNode(id + "  ·  " + n.label));
    el.addEventListener("click", () => {
      selectNode(id);
      flyTo(id);
    });
    void dir;
    return el;
  }
  function selectNode(id) {
    selected = id;
    updateHighlight();
    const n = byId[id];
    panel.innerHTML = "";
    const h = document.createElement("h2");
    h.textContent = n.id;
    panel.appendChild(h);
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.textContent = "domain: " + n.label + (n.type ? "  ·  type: " + n.type : "");
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
    gh.href =
      "https://github.com/zeroes-ones/Skills/blob/main/" + n.path + "/SKILL.md";
    gh.target = "_blank";
    gh.rel = "noopener";
    gh.textContent = "view on GitHub ↗";
    const ss = document.createElement("a");
    ss.href = "https://skills.sh/zeroes-ones/Skills/" + n.id;
    ss.target = "_blank";
    ss.rel = "noopener";
    ss.textContent = "skills.sh ↗";
    linksBox.appendChild(gh);
    linksBox.appendChild(ss);
    panel.appendChild(linksBox);

    const cons = (into[n.id] || []).slice();
    const feeds = (outOf[n.id] || []).slice();
    if (cons.length) {
      const t = document.createElement("h3");
      t.textContent = "consumes from (" + cons.length + ")";
      panel.appendChild(t);
      const box = document.createElement("div");
      box.className = "neighbors";
      cons.sort().forEach((c) => box.appendChild(chipFor(c)));
      panel.appendChild(box);
    }
    if (feeds.length) {
      const t = document.createElement("h3");
      t.textContent = "feeds into (" + feeds.length + ")";
      panel.appendChild(t);
      const box = document.createElement("div");
      box.className = "neighbors";
      feeds.sort().forEach((f) => box.appendChild(chipFor(f)));
      panel.appendChild(box);
    }
  }
  function flyTo(id) {
    const n = byId[id];
    const r = svg.getBoundingClientRect();
    const target = 0.9;
    view.k = target;
    view.x = r.width / 2 - n.x * target;
    view.y = r.height / 2 - n.y * target;
    setTransform();
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
  svg.addEventListener("pointerup", (e) => {
    panning = null;
    svg.classList.remove("panning");
  });
  svg.addEventListener(
    "wheel",
    (e) => {
      e.preventDefault();
      const r = svg.getBoundingClientRect();
      zoomAt(e.clientX - r.left, e.clientY - r.top, e.deltaY < 0 ? 1.12 : 0.89);
    },
    { passive: false }
  );
  svg.addEventListener("dblclick", (e) => {
    if (e.target.closest(".node")) return;
    const p = dataPoint(e.clientX, e.clientY);
    fit();
    void p;
  });

  function onNodeOver(e) {
    const g = e.target.closest(".node");
    if (!g) return;
    hovered = g.dataset.id;
    updateHighlight();
    const n = byId[hovered];
    const r = svg.getBoundingClientRect();
    tooltip.style.display = "block";
    tooltip.style.left = e.clientX - r.left + 14 + "px";
    tooltip.style.top = e.clientY - r.top + 14 + "px";
    tooltip.innerHTML =
      "<b>" + esc(n.id) + "</b><br><span style='color:#8b949e'>" +
      esc(n.label) + (n.type ? " · " + esc(n.type) : "") +
      "</span><br>" + (adj[n.id] ? adj[n.id].size : 0) + " connections";
  }
  function onNodeOut() {
    hovered = null;
    tooltip.style.display = "none";
    updateHighlight();
  }
  svg.addEventListener("pointerover", onNodeOver);
  svg.addEventListener("pointerout", onNodeOut);
  nodeLayer.addEventListener("click", (e) => {
    const g = e.target.closest(".node");
    if (g) {
      selectNode(g.dataset.id);
      flyTo(g.dataset.id);
    }
  });

  /* ---------- search ---------- */
  const search = document.getElementById("search");
  search.addEventListener("input", () => {
    const q = search.value.trim().toLowerCase();
    if (!q) {
      updateHighlight();
      return;
    }
    const hits = nodes
      .filter(
        (n) =>
          n.id.toLowerCase().includes(q) ||
          n.label.toLowerCase().includes(q) ||
          (n.desc || "").toLowerCase().includes(q)
      )
      .slice(0, 30);
    const ids = new Set(hits.map((n) => n.id));
    Object.keys(nodeEls).forEach((id) => {
      nodeEls[id].g.style.opacity = ids.has(id) ? 1 : 0.05;
    });
    if (hits.length === 1) flyTo(hits[0].id);
  });
  search.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && search.value.trim()) {
      const q = search.value.trim().toLowerCase();
      const hit = nodes.find((n) => n.id.toLowerCase() === q) ||
        nodes.find(
          (n) =>
            n.id.toLowerCase().includes(q) || n.label.toLowerCase().includes(q)
        );
      if (hit) {
        selectNode(hit.id);
        flyTo(hit.id);
      }
      e.preventDefault();
    }
  });

  /* ---------- domain filter ---------- */
  const filter = document.getElementById("domainFilter");
  domainOrder.forEach((d) => {
    const opt = document.createElement("option");
    opt.value = d;
    opt.textContent = d + " (" + stats.domains[d] + ")";
    filter.appendChild(opt);
  });
  filter.addEventListener("change", () => {
    const d = filter.value;
    Object.keys(nodeEls).forEach((id) => {
      const n = byId[id];
      nodeEls[id].g.style.opacity = !d || n.label === d ? 1 : 0.06;
    });
  });

  /* ---------- stats header ---------- */
  const statsEl = document.getElementById("stats");
  if (statsEl && stats.nodes) {
    statsEl.innerHTML =
      "<span><b>" + stats.nodes + "</b> skills</span>" +
      "<span><b>" + stats.directed_edges + "</b> chain edges</span>" +
      "<span><b>" + stats.undirected_edges + "</b> connections</span>" +
      "<span><b>" + (stats.domains ? Object.keys(stats.domains).length : 0) +
      "</b> domains</span>" +
      "<span>avg degree <b>" + stats.avg_degree + "</b></span>";
  }

  /* ---------- boot ---------- */
  window.addEventListener("resize", fit);
  positionNodes();
  fit();
  const first = (stats.hubs && stats.hubs[0] && stats.hubs[0].id) || nodes[0].id;
  selectNode(first);
  flyTo(first);
})();
