# Metrics and Measurement

<!-- STANDARD: 3min -- the measurables and how to capture them -->

## Why measure type

Every other claim in this skill is measurable. A type system that cannot state its payload,
its shift contribution, its measure and its contrast floor is a set of preferences, not a
system. Measurement is also what makes typography *arguable* — "this feels tighter" ends a
conversation; "the measured CLS contribution is 0.03 on Slow 4G" starts one.

## The metric set

| Metric | What it answers | Target | How to capture |
|---|---|---|---|
| Font payload, cold view | how much typography costs on the critical path | ≤ 100 KB total | transfer size of font requests, cache cleared, throttled |
| Font-attributable CLS | does the swap move the page | ≈ 0 | `layout-shift` entries during the swap window |
| Characters per line | is body text readable | 45–75 | `ch` measurement on the longest real string |
| Contrast floor across roles | is text legible | ≥ 4.5:1 normal, ≥ 3:1 large | automated pass over every role/surface pair |
| Largest text at 200% zoom | does resize break layout | no clipping | zoom test on the densest screen |
| Line-height at 200% | does spacing break layout | no loss | the four-override test |
| Font count above the fold | how many blocking resources | ≤ 2 | resource waterfall |
| Unused axes/weights | is the payload paying for nothing | 0 unused | compare declared weight set against used values |

## Payload

```bash
# What do font requests actually cost on a cold, throttled load?
# (Chrome DevTools: Network → disable cache → throttle → filter Font)
# Or from the command line with a headless capture:

npx lighthouse https://example.com \
  --only-audits=font-display,render-blocking-resources,total-byte-weight \
  --throttling-method=simulate \
  --output=json --output-path=/tmp/lh-font.json --quiet

python3 - <<'PY'
import json
d = json.load(open("/tmp/lh-font.json"))
for k in ("total-byte-weight", "font-display", "render-blocking-resources"):
    a = d["audits"].get(k)
    if a:
        print(f"{k}: {a.get('score')} — {a.get('displayValue')}")
PY
```

Measure per subset, not in aggregate: a Latin page that downloads the CJK subset has a payload
problem disguised by a reasonable total.

## CLS contribution

```js
// Attribute layout shift to the font swap specifically
const fontSwapWindow = 3000;   // ms after navigation; generous for a throttled load
let total = 0;

new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.hadRecentInput) continue;
    if (entry.startTime > fontSwapWindow) continue;
    total += entry.value;
    const nodes = (entry.sources || []).map(s => s.node?.nodeName).filter(Boolean);
    console.log(`shift ${entry.value.toFixed(4)} at ${Math.round(entry.startTime)}ms`, nodes);
  }
  console.log("font-window CLS:", total.toFixed(4));
}).observe({ type: "layout-shift", buffered: true });
```

Procedure that produces a defensible number:

1. Record the profile (device, network throttling, CPU slowdown).
2. Disable the cache so the font genuinely arrives after first paint.
3. Measure **with** the metric-matched fallback and **without** it.
4. Report both numbers. The delta is the fallback's value; the absolute number is the residual.

A measured residual above roughly 0.02 attributable to font swap means the fallback is not
matched for the face or size that shifted — usually because the fallback was matched for body
text but the shift is happening in a display element with different metrics.

## Measure (line length)

```js
// Characters per line, computed from the rendered element, not by eye
function charsPerLine(el, chWidth) {
  const width = el.getBoundingClientRect().width;
  return width / chWidth;
}

// ch width in the current font
const probe = document.createElement("span");
probe.textContent = "0".repeat(100);
probe.style.cssText = "position:absolute;visibility:hidden;white-space:nowrap";
document.body.appendChild(probe);
const chWidth = probe.getBoundingClientRect().width / 100;
document.body.removeChild(probe);

for (const el of document.querySelectorAll(".prose")) {
  console.log(charsPerLine(el, chWidth).toFixed(1), el.className);
}
```

Verify with the **longest real string** from the content, not the average. A 78-character
German compound is the case that decides whether the measure needs hyphenation.

## Contrast across roles

```js
// Walk every text role against its actual computed background
function relLum([r, g, b]) {
  const f = (c) => {
    c /= 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
}
function ratio(a, b) {
  const [l1, l2] = [relLum(a), relLum(b)].sort((x, y) => y - x);
  return (l1 + 0.05) / (l2 + 0.05);
}
function rgb(s) { return s.match(/\d+/g).slice(0, 3).map(Number); }

const failures = [];
for (const el of document.querySelectorAll("h1,h2,h3,h4,p,span,label,td,th,li,a,button")) {
  if (!el.textContent.trim()) continue;
  const cs = getComputedStyle(el);
  const fg = rgb(cs.color);
  // Walk up for the first non-transparent background
  let node = el, bg = null;
  while (node && !bg) {
    const b = getComputedStyle(node).backgroundColor;
    if (b && !/rgba?\(0, 0, 0, 0\)/.test(b)) bg = rgb(b);
    node = node.parentElement;
  }
  if (!bg) continue;
  const px = parseFloat(cs.fontSize);
  const bold = parseInt(cs.fontWeight, 10) >= 700;
  const large = px >= 24 || (bold && px >= 18.66);
  const need = large ? 3 : 4.5;
  const r = ratio(fg, bg);
  if (r < need) failures.push({ el: el.tagName, cls: el.className, r: r.toFixed(2), need, px });
}
console.log(failures.length ? failures : "no contrast failures");
```

The value of automating this is that it covers the roles teams forget: captions, placeholder
text, disabled states, text over a scrim, and table headers.

## The resize test

```text
1. Open the densest screen (usually a table or a form).
2. Browser zoom → 200%.
3. Also set the root font size to 24px (simulating a large-font user).
4. Check: no clipped text, no truncated labels, no overlap, no horizontal scroll for text.
5. Apply the four 1.4.12 spacing overrides; re-check.
```

## Budget worksheet

Record this per release. It is short enough to keep honest.

| Metric | Value | Profile / method | Budget | Status |
|---|---|---|---|---|
| Font payload (all requests) | e.g. 84 KB | Slow 4G, cache disabled | 100 KB | pass |
| Font-attributable CLS | e.g. 0.004 | Slow 4G, 4× CPU | 0.02 | pass |
| Body measure (longest string) | e.g. 68 chars | longest catalogue string | 45–75 | pass |
| Contrast floor (lowest role) | e.g. 4.62:1 | automated role sweep | 4.5:1 | pass |
| Unused axes | e.g. none | declared set vs used values | 0 | pass |
| Faces above the fold | e.g. 2 | resource waterfall | ≤ 2 | pass |

## Anti-patterns in measurement

| Anti-pattern | Why it misleads |
|---|---|
| Measuring on an unthrottled desktop | the swap window barely exists, so CLS appears to be zero |
| Measuring with a warm cache | the font never swaps, so the fallback is never exercised |
| Reporting one aggregate payload | hides that a Latin page fetched a CJK subset |
| Measuring measure with placeholder text | lorem ipsum is not the longest string your content produces |
| Checking contrast only on the happy path | captions, placeholders and disabled states are where it fails |
| Asserting zero CLS without the observer | unmeasured claims are indistinguishable from guesses (AR-02) |
