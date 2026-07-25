---
name: browser-testing-with-devtools
description: >
  Use when debugging live web applications in a browser, inspecting DOM structure
  and CSS layout issues, analyzing network requests and API responses, profiling
  JavaScript performance and memory usage, verifying accessibility compliance in
  the rendered DOM, capturing console errors and warnings, emulating mobile
  devices and network conditions, or auditing third-party script behavior.
  Handles Chrome DevTools integration for runtime debugging: DOM inspection,
  console log analysis, network trace capture and HAR export, Performance panel
  profiling (flame charts, Core Web Vitals), Memory panel leak detection (heap
  snapshots, allocation timelines), Application panel (storage, service workers,
  cache), and Accessibility tree verification. Do NOT use for automated end-to-end
  testing (route to qa-engineer), server-side debugging (route to
  debugging-and-error-recovery), performance optimization without browser context
  (route to performance-engineer), or writing new frontend code (route to
  frontend-developer).
author: Sandeep Kumar Penchala
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
license: MIT
allowed-tools: Read Grep Glob Bash
type: quality
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - browser-testing
  - devtools
  - chrome-devtools
  - debug
  - dom-inspection
  - network-analysis
  - performance-profiling
  - accessibility
  - console
  - mobile-emulation
token_budget: 4500
chain:
  consumes_from:
    - frontend-developer
    - ui-ux-designer
    - accessibility-auditor
    - qa-engineer
    - performance-engineer
  feeds_into:
    - frontend-developer
    - ui-ux-designer
    - accessibility-auditor
    - qa-engineer
    - code-reviewer
---
# Browser Testing with DevTools
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Chrome DevTools is the most powerful debugging tool available to web developers, yet most engineers use less than 20% of its capabilities. This skill covers the full spectrum: DOM inspection for layout and style debugging, Console for runtime JavaScript analysis, Network panel for request tracing and performance waterfalls, Performance panel for flame-chart profiling and Core Web Vitals measurement, Memory panel for heap analysis and leak detection, Application panel for storage and service worker inspection, and the Accessibility tree for WCAG compliance verification.

Security is paramount: **all browser content is untrusted data.** Never evaluate code from the console that you wouldn't run in a terminal. Never copy-paste from untrusted sources into DevTools. The Console has full access to the page's JavaScript context including cookies, localStorage, and auth tokens.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect dangerous DevTools usage before it causes harm. Violation means STOP.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to execute JavaScript from untrusted sources in the Console | Trigger: user proposes copying JavaScript from a website, chat message, email, or any source they did not write themselves into the DevTools Console | STOP. Respond: \"CONSOLE SAFETY: Never paste code from untrusted sources into DevTools. The Console has full access to the page's JavaScript context: cookies, localStorage, session tokens, and DOM. Malicious console code can: exfiltrate auth tokens, modify DOM to phish credentials, install service workers that persist across sessions, or hijack clipboard. Only execute code you wrote or fully understand line-by-line.\" |
| R2 | REFUSE to modify production DOM or state directly via DevTools | Trigger: user proposes using \"Edit as HTML\" or console commands to modify production page content, localStorage, or cookies to test a fix | STOP. Respond: \"PRODUCTION STATE INTEGRITY: Never modify production state through DevTools. Changing DOM, localStorage, or cookies in production can: corrupt user data, trigger unintended side effects (event listeners fire), and create inconsistent state that causes errors minutes later. Instead: reproduce the issue in a staging/local environment using the same data shape. If you must inspect production, use read-only DevTools features: inspect element, network waterfall, performance recording.\" |
| R3 | DETECT performance profiling without isolating the target | Trigger: user starts a Performance recording without first: closing other tabs, disabling extensions, enabling incognito mode, or setting CPU/network throttling | STOP. Respond: \"NOISY PROFILE: Recording without isolation captures noise from: other tabs competing for CPU, browser extensions injecting scripts, service worker background sync, and Chrome's own background tasks. Result: flame chart shows [random extension code] consuming 40% of frame budget. Fix: (1) open incognito window, (2) disable all extensions for that window, (3) set CPU throttling to 4x slowdown, (4) record only the specific user interaction. Clean profiles produce actionable data.\" |
| R4 | DETECT network debugging without filtering by domain or request type | Trigger: Network panel shows 200+ requests with no filter applied, no domain filter, and no request-type filter (XHR/JS/CSS/Img) | STOP. Respond: \"NETWORK NOISE: Unfiltered network trace contains extraneous noise: analytics beacons (10-30% of requests), third-party ads, CDN prefetches, and extension traffic. Filter: (1) domain filter: your API domain only, (2) request type: XHR/Fetch for API calls, (3) status filter: isolate errors (status >= 400). A 200-request trace becomes a 15-request trace that shows the actual problem.\" |
| R5 | REFUSE to take a heap snapshot without understanding what you're looking for | Trigger: user opens Memory panel and takes a heap snapshot with no specific hypothesis about what is leaking or which object type is accumulating | STOP. Respond: \"AIMLESS HEAP SNAPSHOT: A heap snapshot is 10-50MB of memory addresses. Without a hypothesis, you will spend 30 minutes scrolling through retainers with no insight. Before taking a snapshot: (1) identify the symptom (memory grows over time, GC doesn't reclaim), (2) predict the leaking object type (detached DOM nodes? closure-captured arrays? event listeners?), (3) take TWO snapshots 30 seconds apart and compare them (Comparison view shows what was allocated between snapshots), (4) sort by delta to find accumulating objects.\" |
| R6 | DETECT accessibility audit that checks only the DOM source, not the rendered accessibility tree | Trigger: accessibility check references HTML source (\"there's an alt attribute\") but does NOT open the Accessibility panel to verify the computed accessible name, role, and description | STOP. Respond: \"SOURCE VS RENDERED A11Y: The HTML source says `<div role=\"button\" aria-label=\"Submit\">` but the accessibility tree might say: `button \"\" focusable: false` (empty name, unfocusable). Why? CSS `display: none`, `visibility: hidden`, `aria-hidden=\"true\"` on a parent, or a JS framework re-rendering without attributes. Always verify in the Accessibility panel (Elements > Accessibility pane) -- the rendered accessibility tree is what screen readers actually consume.\" |
| R7 | DETECT Console filter misuse that hides the error being debugged | Trigger: Console shows \"0 errors, 0 warnings\" but the user is experiencing a bug -- Console filter is set to \"Info\" only, \"Verbose\" is off, or \"Hide network\" is checked | STOP. Respond: \"CONSOLE FILTER BLIND SPOT: The Console has 5 filter levels: Verbose, Info, Warnings, Errors, and a text filter. If the filter hides the log level of your error, you will see nothing. Check: (1) All levels enabled (Verbose through Error), (2) text filter is empty, (3) 'Hide network' is unchecked if the bug involves failed requests, (4) 'Preserve log' is checked to retain logs across page navigations. Default Console state shows all messages.\" |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

DevTools mastery separates senior frontend engineers from junior ones. A senior engineer can diagnose a rendering bug, memory leak, or performance regression in minutes using DevTools -- without adding a single console.log. The DevTools-first mindset: every question about runtime behavior has an answer in DevTools if you know which panel to open.

#

## Mental Models

| Model | Description |
|---|---|
| **The Panels are a diagnostic stack** | Elements answers \"what is rendered?\", Console answers \"what happened?\", Network answers \"what was sent/received?\", Performance answers \"what is slow?\", Memory answers \"what is leaking?\", Application answers \"what is stored?\". The first diagnostic step is choosing the right panel. |
| **Read-only first, write never in production** | DevTools provides tremendous power to modify the page. In production, use only read-only features: inspect, profile, trace. Modifying production state via DevTools is a self-inflicted incident. |
| **The accessibility tree is the source of truth** | Screen readers do not read HTML. They read the accessibility tree. The HTML source can be perfectly semantic while the accessibility tree is broken due to CSS, JS, or ARIA conflicts. Always verify in the Accessibility panel. |
| **Every performance problem leaves a trace** | If a page is slow, the flame chart knows why. If a page is janky, the frames timeline shows dropped frames. If memory is growing, the heap comparison shows accumulating objects. The data is there -- you just need to know where to look. |

#

## Cognitive Biases That Weaken Browser Debugging

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Source-code myopia** | Debugging by reading source code instead of inspecting the live runtime state | Rule: \"Inspect before you read.\" Open Elements panel first. Check computed styles, event listeners, and the accessibility tree. The source code shows what you intended; DevTools shows what actually rendered. |
| **Console.log as first resort** | Adding console.log for every debugging session instead of using breakpoints, watch expressions, and conditional breakpoints | Next time you type `console.log`, instead: click the line number to set a breakpoint, right-click > \"Add conditional breakpoint\", enter `user.id === 1234`. Now you stop exactly when the condition is met. |
| **Ignoring the waterfall** | Looking at a single slow request without examining the request waterfall for blocking, queueing, or connection limits | A 200ms API call that spent 180ms queued behind 5 other requests reveals a connection pool issue, not a slow backend. Always check the timing breakdown: Queueing, Stalled, DNS Lookup, Initial Connection, SSL, Request Sent, Waiting (TTFB), Content Download. |
| **Disabling cache as a debugging crutch** | Always checking \"Disable cache\" without understanding caching behavior | Disable cache is for development. But production bugs are often caused by stale cached assets. Test with cache ENABLED to reproduce real user conditions. Clear specific cache entries in Application > Cache Storage rather than disabling entirely. |

#

## What Masters Know That Others Don't

- **The `$0` magic variable.** After inspecting an element in Elements panel, `$0` in Console references that exact DOM node. `$1` is the previously inspected node. `$r` references the React component instance (with React DevTools).
- **Conditional breakpoints save hours.** Instead of stepping through 500 loop iterations, set a conditional breakpoint: `i === 473`. Chrome pauses exactly on the iteration you care about.
- **The Rendering panel reveals layout thrashing.** Enable \"Paint flashing\" to see every repaint. Enable \"Layout Shift Regions\" to see CLS (Cumulative Layout Shift) culprits. Enable \"Frame Rendering Stats\" to see real-time FPS.
- **HAR files are portable debugging artifacts.** Export a Network trace as HAR (HTTP Archive). The HAR file contains every request with headers, timing, and responses. A 30-second recording captures the complete story of a slow page load. Shareable, replayable, analyzable.
- **`monitor()` and `monitorEvents()` for zero-code instrumentation.** In Console: `monitor(fn)` logs every call to `fn` with arguments. `monitorEvents(window, 'resize')` logs every resize event. Zero code changes, instant instrumentation.

## Operating at Different Levels

- **Quick scan (30s):** Open the page. Check Console for red errors. Check Network for red (4xx/5xx) requests. Check Elements > Computed for obviously broken styles (0x0 elements, display:none when visible expected). If nothing obvious, the bug is likely in logic/state, not rendering.
- **Standard engagement (10min):** Reproduce the bug with DevTools open. Set a breakpoint at the suspected function. Step through execution watching variable values in Scope pane. Check Network waterfall for the failing request's timing breakdown. Verify the fix with Live Edit (edit CSS/HTML in Elements panel to preview).
- **Deep dive (full session):** Performance: record a Performance profile, analyze flame chart for long tasks (>50ms), identify forced synchronous layouts, measure Core Web Vitals. Memory: take 3 heap snapshots at 30-second intervals during usage, compare snapshots to find accumulating objects, trace retainers to find the leaking reference. Accessibility: full accessibility tree audit with axe DevTools extension, verify focus order with Tab key, test with screen reader.
- **Incident response (live site broken):** Network panel with \"Preserve log\" checked. Filter to XHR/Fetch. Identify the failing API call. Check response body (Preview tab). If auth-related, check Application > Cookies for expired/missing tokens. Export HAR for postmortem. Do NOT modify production state.

## When to Use

Use browser-testing-with-devtools when investigating runtime behavior of a web application that is running in a browser -- the focus is on what the browser actually renders and executes, not what the source code intended.

- DOM inspection: elements not rendering, wrong styles applied, layout broken, event listeners not firing
- Console analysis: JavaScript errors, unhandled promise rejections, warnings, custom log messages
- Network debugging: API calls failing, slow responses, missing headers, incorrect payloads, CORS errors
- Performance profiling: slow page loads, janky animations, unresponsive UI, high CPU usage, Core Web Vitals regressions
- Memory leak detection: page gets slower over time, tab crashes, memory usage climbs without GC
- Accessibility verification: screen reader compatibility, focus order, ARIA attribute correctness, color contrast
- Mobile device emulation: responsive layout bugs, touch event issues, viewport problems, device-specific rendering
- Storage and cache inspection: cookies, localStorage, sessionStorage, IndexedDB, Cache API, service workers
- Third-party script auditing: what scripts are loading, what data they send, performance impact
- Security inspection: CSP violations, mixed content warnings, certificate issues, cookie security attributes

Do NOT use browser-testing-with-devtools for automated cross-browser testing (route to qa-engineer). Do NOT use for server-side debugging (route to debugging-and-error-recovery). Do NOT use for writing new frontend code (route to frontend-developer). Do NOT use for pure performance optimization without browser context (route to performance-engineer). Do NOT use for static code analysis (route to code-reviewer).

## Route the Request

#

## Auto-Route by Artifacts

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("SKILL.md", "browser-testing-with-devtools")` -- this is your skill | Redirect: \"I am Browser Testing with DevTools. Route by intent matching below.\" |
| A2 | Error description contains \"not rendering\" , \"layout broken\", \"CSS issue\", \"element missing\" | **DOM/RENDERING** -- Go to **Core Workflow: Phase 1 (Elements Panel)**. Inspect computed styles and box model. |
| A3 | Error includes JavaScript stack trace, \"undefined is not a function\", or \"cannot read property\" | **JS RUNTIME** -- Go to **Core Workflow: Phase 2 (Console + Sources)**. Set breakpoints at stack trace locations. |
| A4 | Error mentions \"slow\", \"janky\", \"freezes\", \"unresponsive\", or Core Web Vitals metrics | **PERFORMANCE** -- Jump to **Decision Trees: Performance Issue**. Record Performance profile with throttling. |
| A5 | Error describes \"memory\", \"crash\", \"tab reloads\", or \"gets slower over time\" | **MEMORY LEAK** -- Jump to **Decision Trees: Memory Leak Detection**. Heap snapshot comparison. |
| A6 | Error mentions \"API\", \"request\", \"network\", \"CORS\", \"timeout\", or HTTP status codes | **NETWORK** -- Go to **Core Workflow: Phase 3 (Network Panel)**. Filter for failing requests. |
| A7 | Error references accessibility, \"screen reader\", \"WCAG\", \"ARIA\", or \"a11y\" | **ACCESSIBILITY** -- Jump to **Decision Trees: Accessibility Verification**. Accessibility tree inspection. |
| A8 | Error involves \"mobile\", \"responsive\", \"viewport\", \"touch\", or device-specific behavior | **DEVICE EMULATION** -- Jump to **Decision Trees: Mobile Device Testing**. |
| A9 | No specific triggers -- general browser debugging request | **STANDARD** -- Full workflow: Phase 1 (Elements) → Phase 2 (Console) → Phase 3 (Network). |

#

## Intent Route (Ask the User)

```
What browser debugging task are you working on?
├── Something is not rendering correctly → Start at "Core Workflow > Phase 1"
├── I have a JavaScript error → Start at "Core Workflow > Phase 2"
├── An API call is failing or slow → Go to "Core Workflow > Phase 3"
├── The page is slow or janky → Jump to "Decision Trees > Performance Issue"
├── Memory usage keeps growing → Jump to "Decision Trees > Memory Leak Detection"
├── I need to verify accessibility → Jump to "Decision Trees > Accessibility Verification"
├── Testing on mobile devices → Jump to "Decision Trees > Mobile Device Testing"
├── I need to export debugging data for others → Jump to "Decision Trees > HAR Export and Sharing"
├── Third-party scripts causing issues → Jump to "Decision Trees > Third-Party Script Audit"
└── Not sure what's wrong → "Core Workflow > Phase 0" — systematic triage across all panels
```

## Core Workflow **(STANDARD)**
<!-- Full 105 lines extracted to references/core-workflow-1.md -->

#

## Phase 0: Systematic Triage
Open DevTools (F12 or Cmd+Option+I). Work through panels in order until you find the signal:
1. Console (Esc to toggle): Any red errors? Fix those first. Errors cascade.
2. Network: Any red (4xx/5xx) requests? Check response for error messages.
...
> 📎 **[references/core-workflow-1.md](references/core-workflow-1.md)** — 105 lines of detailed guidance

## Decision Trees **(QUICK)**
#

## Decision Tree 1: Performance Issue Investigation

```
Phase 1: Record and Classify
├── Open Performance panel → Start recording → Reproduce the slow interaction → Stop
├── Look at the flame chart:
│   ├── Wide yellow bars (Scripting) → JavaScript is the bottleneck
│   ├── Wide purple bars (Rendering) → Layout/paint is the bottleneck
│   ├── Wide green bars (Painting) → Too many paint operations
│   └── Gaps between frames (white space) → Idle time, not a performance issue

Phase 2: Diagnose by Category
├── Scripting bottleneck:
│   ├── Find the widest yellow bar → click to see function name + file + line
│   ├── Is it a single long task (>50ms)? → Split with setTimeout or requestIdleCallback
│   ├── Is it forced synchronous layout? (purple bars inside yellow) → Batch reads+writes
│   └── Is it garbage collection? (gray GC bars) → Reduce object allocation rate
├── Rendering bottleneck:
│   ├── Enable Rendering panel → Paint flashing ON
│   ├── Reproduce. Entire page flashing = layout thrashing
│   ├── Check: are you reading layout properties (offsetHeight, getBoundingClientRect)
│   │   then immediately writing styles in a loop? → Batch reads, then batch writes
│   └── Use CSS containment: `contain: layout style paint` on off-screen elements
└── Network bottleneck:
    ├── Check Network waterfall during the same recording
    ├── Are critical resources (CSS, JS) render-blocking? → Inline critical CSS, defer JS
    └── Are images loading without dimensions? → Set width/height to prevent layout shifts (CLS)
```

#

## Decision Tree 2: Memory Leak Detection

```
Phase 1: Confirm It's a Leak
├── Open Memory panel → Select 'Allocation instrumentation on timeline'
├── Start recording → Use the app normally for 2-3 minutes → Stop recording
├── Look at the timeline: does memory grow monotonically (never drops)?
│   ├── Sawtooth pattern (grows, drops, grows, drops) → Normal GC behavior
│   └── Staircase pattern (grows, never drops) → Leak confirmed

Phase 2: Identify the Leaking Objects
├── Take Heap Snapshot #1 (baseline)
├── Perform the suspect action 10 times
├── Take Heap Snapshot #2
├── Switch to Comparison view (dropdown: 'Comparison' instead of 'Summary')
├── Sort by 'Delta' (allocated size) descending
├── The top objects by positive delta are accumulating → click to see retainers
├── Follow the retainer chain to find what's holding the reference
│   ├── Detached DOM nodes → Event listener not removed, closure referencing DOM
│   ├── Arrays growing unbounded → Cache without eviction, event log never cleared
│   ├── Closure retaining large scope → Extract only needed variables
│   └── Unmounted component references → useEffect cleanup missing
```

#

## Decision Tree 3: Accessibility Verification

```
Phase 1: Automated Scan
├── Open axe DevTools extension (free, official Deque extension)
├── Run scan on the current page
├── Review violations sorted by severity: Critical, Serious, Moderate, Minor
├── Each violation shows: element, issue, fix suggestion, WCAG criteria reference

Phase 2: Manual Verification (what automation misses)
├── Accessibility tree verification:
│   ├── Elements panel → Accessibility pane (right sidebar)
│   ├── Inspect each interactive element
│   ├── Verify: Name (not empty), Role (correct semantic role), Focusable (not false for buttons/inputs)
│   └── Verify: ARIA attributes are correctly applied in the computed tree
├── Keyboard navigation:
│   ├── Press Tab through the page
│   ├── Every interactive element: reachable? visible focus ring?
│   ├── Focus order: logical reading order? or jumping around?
│   └── Modal dialogs: focus trapped inside? Closeable with Escape?
├── Screen reader test (macOS VoiceOver: Cmd+F5):
│   ├── Navigate through page with VO + arrow keys
│   ├── Every image: does it announce alt text or filename?
│   ├── Forms: does it announce labels for each input?
│   └── Dynamic content: does it announce live region updates? (aria-live)
└── Color and contrast:
    ├── Rendering panel → Enable 'CSS Overview' → Colors tab
    ├── Check contrast ratios against text. <4.5:1 for normal text = WCAG AA fail
    └── Emulate vision deficiencies: Rendering panel → Emulate vision deficiencies
```

#

## Decision Tree 4: Mobile Device Emulation

```
Phase 1: Set Up Device Emulation
├── Toggle Device Toolbar (Cmd+Shift+M or click phone icon)
├── Select a device preset: iPhone 15, Pixel 7, Galaxy S23, iPad
├── Key settings to verify:
│   ├── Viewport dimensions match target device
│   ├── Device pixel ratio (DPR): 3 for iPhone, 2-3 for modern Android
│   ├── Network throttling: 4G (4 Mbps down, 0.6 Mbps up) for realistic mobile
│   └── CPU throttling: 4x slowdown (mobile CPUs are 2-5x slower than desktop)

Phase 2: Test Device-Specific Issues
├── Touch events: does the emulator correctly simulate touch? (Device Toolbar enables touch)
│   ├── Hover-dependent UI: tooltips, dropdown menus → won't work on touch devices
│   └── Replace hover with: click-to-toggle patterns, or use @media (hover: hover)
├── Viewport and orientation:
│   ├── Rotate device (portrait/landscape) → does layout reflow correctly?
│   ├── Test at 320px width (smallest supported) → no horizontal scroll?
│   └── Test with device toolbar OFF → does meta viewport tag work?
├── Network conditions:
│   ├── Test on Slow 3G (400 Kbps) → does the page load at all?
│   ├── Test offline → does the app show meaningful offline state? (service worker)
│   └── Test with 'Disable cache' ON and OFF → caching behavior correct?
└── Sensors emulation:
    ├── More tools → Sensors → Geolocation → set custom coordinates
    ├── Test location-based features with known coordinates
    └── Test orientation API (alpha/beta/gamma) for device motion features
```

#

## Decision Tree 5: HAR Export and Cross-Team Debugging

```
Phase 1: Capture the Evidence
├── Open Network panel → Check 'Preserve log' → Clear existing logs
├── Reproduce the bug exactly once
├── Right-click any request → Save all as HAR with content
├── HAR file contains: every request URL, method, headers, timing, response body
├── Also: take a screenshot (Cmd+Shift+4) and a Console log export (right-click → Save as)

Phase 2: Annotate and Share
├── Open HAR file in a HAR viewer (Google 'HAR Viewer' or use Chrome's Network panel import)
│   ├── Identify the failing request(s) by HTTP status code or response content
│   ├── Note the exact timestamp of the failure
│   └── Note the timing breakdown: TTFB, Content Download, Queueing
├── Create a bug report package:
│   ├── HAR file (network evidence)
│   ├── Screenshot (visual evidence)
│   ├── Console log export (JS errors)
│   └── Steps to reproduce (written steps + expected vs actual)
└── Backend teams need: HAR file + specific request that failed + timestamp
    Frontend teams need: HAR + screenshot + Console log + reproduction steps
```

#

## Decision Tree 6: Third-Party Script Audit

```
Phase 1: Inventory All Third-Party Scripts
├── Network panel → Filter: JS → Sort by domain
├── Identify all non-first-party domains loading JavaScript
├── For each third-party script, answer:
│   ├── What does it do? (analytics, ads, chat widget, CDN, A/B testing)
│   ├── What is its performance cost? (click request → Timing tab → total duration)
│   ├── Is it render-blocking? (appears before page content in waterfall)
│   └── Is it still needed? (was it added for a campaign that ended?)

Phase 2: Measure Impact
├── Performance panel → Record page load with and without each third-party script
│   ├── Block the script in Network panel → right-click → Block request URL
│   ├── Record Performance profile → compare LCP, FCP, TBT
│   └── If a script adds >500ms to page load → flag for review
├── Coverage panel (Cmd+Shift+P → 'Show Coverage')
│   ├── Start instrumenting coverage → reload page → interact normally → stop
│   ├── Shows: % of each JS/CSS file actually used
│   ├── Third-party scripts often show <10% usage → you're paying for 90% unused code
│   └── Consider: load script on interaction (click-to-load), not on page load
└── Security: check what data third-party scripts send
    ├── Network → Filter by third-party domain → inspect request payloads
    ├── Are they sending: page URLs? user IDs? form data? cookies?
    └── Unexpected data exfiltration = security incident → escalate to security-reviewer
```

#

## Decision Tree 7: Console Power-User Techniques

```
Phase 1: DOM and Element Shortcuts
├── $('selector') → document.querySelector('selector')
├── $$('selector') → document.querySelectorAll('selector') — returns Array
├── $0 → currently inspected element in Elements panel
├── $1 → previously inspected element
├── $_ → value of last evaluated expression
├── $x('//div[@class="foo"]') → XPath selector (for complex DOM queries)

Phase 2: Monitoring and Events
├── monitor(fn) → logs every call to fn with arguments. monitor(myComponent.render)
├── unmonitor(fn) → stops monitoring
├── monitorEvents(el, 'click') → logs every click event on el
├── monitorEvents(el, ['click', 'keydown']) → multiple event types
├── unmonitorEvents(el) → stops monitoring
├── getEventListeners(el) → shows all registered event listeners on el with handler source

Phase 3: Performance and Debugging
├── console.time('label') / console.timeEnd('label') → measure execution duration
├── console.table(array) → displays array of objects as a sortable table
├── console.trace() → prints stack trace from current execution point
├── debug(fn) → automatically pauses execution when fn is called (alias for breakpoint)
├── undebug(fn) → removes auto-breakpoint
├── copy(obj) → copies obj to clipboard as JSON.stringify(obj, null, 2)
└── Store as global variable: right-click object in Console → "Store as global variable" → temp1
```


## Best Practices

1. **Start every performance investigation with the Performance panel, not the code.** Record the slow interaction, examine the flame chart, and identify whether the bottleneck is scripting (yellow), rendering (purple), or painting (green). Reading 800 lines of source code and adding `console.log` at random points takes 3 hours; a Performance recording takes 30 seconds and shows you exactly which function is slow. DevTools-first debugging is faster by an order of magnitude.

2. **Analyze the Network waterfall before optimizing assets.** Sort by waterfall, not by size. Look for: render-blocking resources (CSS/JS at the top of `<head>`), long TTFB (>500ms indicates a backend issue, not a frontend one), sequential request chains (waterfall stair-step pattern), and resources loading before the ones they depend on. Export as HAR and share with backend teams for TTFB/latency issues.

3. **Use the Memory panel's allocation timeline to find leaks, not heap snapshots alone.** Take a baseline heap snapshot, perform the suspect operation, take another, and compare. But allocation timelines are more powerful — record while the leak happens and the timeline shows you exactly which functions allocated the objects that were never freed. Filter by "Objects allocated between X and Y" and sort by retained size.

4. **Monitor the Console panel proactively — errors cascade.** Open DevTools, enable "Preserve log", and reproduce the bug. Red errors (uncaught exceptions) are your starting point. But also check yellow warnings (`[Deprecation]`, `[Intervention]`) — deprecation warnings mean your code will break in a future browser version. Fix errors from the top down; the first error often causes every subsequent error.

5. **Run Coverage analysis before removing any code.** Open the Coverage panel (Cmd+Shift+P → "Show Coverage"), start recording, and interact with the page. The panel shows how much of each JS/CSS file is unused (red bars). Focus on files with >80% unused bytes and large absolute sizes (>50KB). Coverage tells you what's actually dead, not what looks dead. Combined with source maps, it identifies specific functions that never execute.

6. **Audit with Lighthouse for holistic quality scores.** Run Lighthouse (Audits panel) in incognito mode with no extensions for a clean baseline. Check all four categories: Performance (LCP, FCP, TBT, CLS, SI), Accessibility, Best Practices, and SEO. Set Lighthouse CI budgets in the pipeline and block deploys on score drops. Lighthouse won't replace panel-by-panel debugging, but it surfaces regressions you'd miss.

7. **Inspect frame rendering with the Rendering panel.** Enable "Paint flashing" to see what's repainting (green flashes), "Layout Shift Regions" to see CLS culprits (blue rectangles), "Layer borders" to see compositing layers (orange borders), and "FPS meter" for real-time frame rate. If the entire page flashes green on every scroll, you have a layout thrashing problem — batched reads and writes are the fix.

8. **Inspect Service Workers, Web Workers, and Worklets in the Application panel.** The Application panel's "Service Workers" section shows registration status, update lifecycle, and cache contents. For Web Workers and Worklets, use the Sources panel's Threads list to pause and debug worker code. Workers have their own console — click the worker name in the Console panel's context selector. Worker errors are silent unless you're watching the right context.

9. **Test on throttled networks and slowed CPUs by default.** Set Network throttle to "Slow 3G" and CPU throttle to "4x slowdown" in the Performance panel. Every page you debug under load conditions reveals bottlenecks invisible on localhost + gigabit. Most desktop-developed apps fail the "can I complete the primary flow in under 30 seconds on Slow 3G" test — fix the top 3 bottlenecks before the first user hits them on a 4-year-old Android with spotty LTE.

10. **Never leave `debugger;` statements, disabled cache, or throttling enabled when shipping.** Before closing DevTools, reset: remove `debugger;` breakpoints (Sources → Breakpoints pane → right-click → "Remove all breakpoints"), uncheck "Disable cache" (Network panel), reset throttling to "No throttling". A `debugger;` in production freezes the page for any user with DevTools open (including your support team). A disabled-cache production build wastes CDN bandwidth and regresses LCP.


## Error Recovery **(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

| Scenario | Skill to Invoke |
|---|---|
| Need to write automated tests for browser behavior | `qa-engineer` — Playwright/Cypress test automation |
| Accessibility audit needs WCAG gap analysis | `accessibility-auditor` — full WCAG 2.2 compliance audit |
| Performance issue requires build optimization | `performance-engineer` — bundling, code splitting, lazy loading |
| Bug found during browser testing needs a code fix | `frontend-developer` — React/Vue/Next.js implementation |
| Browser testing reveals security vulnerability | `security-reviewer` — assess severity and recommend fix |
| Need systematic debugging methodology for complex bug | `debugging-and-error-recovery` — 6-phase systematic debug |
| UI rendering issue needs design system alignment | `ui-ux-designer` — component spec, design tokens, responsive layout |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `code-reviewer` | Code quality assessment, security patterns, testing gaps | Before finalizing implementation or shipping to production |

## Proactive Triggers

- **Trigger: error console shows >5 unique JavaScript errors on page load.** Auto-flag: page is shipping broken. Prioritize errors by frequency. Fix top error first.
- **Trigger: Largest Contentful Paint (LCP) > 2.5 seconds in Performance panel.** Auto-trigger: LCP audit. Check render-blocking resources, image optimization, server response time.
- **Trigger: Network panel shows a request with TTFB > 500ms.** Auto-flag: backend latency issue. Export HAR, share with backend team with specific request timestamp.
- **Trigger: Memory panel heap comparison shows >10MB growth over 30 seconds of idle usage.** Auto-trigger: memory leak investigation. Take allocation timeline to identify leaking code path.
- **Trigger: Accessibility panel shows a missing accessible name on an interactive element.** Auto-flag: WCAG violation. Add aria-label, aria-labelledby, or visible text label before merge.
- **Trigger: Console shows `[Deprecation]` or `[Intervention]` warnings.** Auto-flag: using deprecated or blocked APIs. These warnings mean your code will break in a future Chrome version.

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

#

## How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "browser-testing-with-devtools",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

#

## State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

#

## Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?


## Production Checklist **(STANDARD)**

Before closing DevTools and shipping a fix, verify every item:

- [ ] **Root cause identified using the appropriate DevTools panel.** Evidence captured (screenshot, HAR, Performance profile, or heap snapshot) attached to bug ticket. The bug is understood at the mechanism level, not just "the symptom disappeared."
- [ ] **Console panel: zero red errors (uncaught exceptions) remain.** Yellow warnings reviewed — `[Deprecation]` and `[Intervention]` warnings either addressed or documented with browser version caveat. Console "Preserve log" verified across page navigation.
- [ ] **Network panel: no 4xx or 5xx requests on critical flows.** All requests return expected status codes. TTFB < 500ms for primary API calls. Render-blocking resources identified and deferred/inlined. Critical-path requests prioritized.
- [ ] **Performance panel: LCP < 2.5s, TBT < 200ms, CLS < 0.1.** Before/after Performance profiles compared. No regression in any Core Web Vital. Flame chart shows no single task > 50ms (long task). No forced synchronous layout (purple bars inside yellow).
- [ ] **Memory panel: no leak introduced.** Heap comparison before/after fix shows stable memory. Allocation timeline shows no unretained object growth over 30 seconds of idle usage. No detached DOM nodes accumulating.
- [ ] **Coverage panel checked for unused code.** No JS/CSS files with >80% unused bytes AND >50KB absolute size shipped. Code-splitting verified: route-level chunks load only when needed.
- [ ] **Accessibility panel: zero new violations vs baseline.** axe DevTools scan passes. Accessible names present on all interactive elements. Focus order follows visual order. `[aria-*]` attributes have valid values.
- [ ] **Mobile: tested on at least one real device, not just emulation.** Verified: touch targets ≥ 44x44dp, viewport meta tag correct, no horizontal scroll on narrow viewports, font sizes legible without zoom. Emulation verified against real device — discrepancies documented.
- [ ] **Throttling reset before closing DevTools.** Network: "No throttling." CPU: "No throttling." Cache: "Disable cache" unchecked. All breakpoints removed. No `debugger;` statements in shipping code.
- [ ] **Lighthouse audit run in incognito with no extensions.** All four categories (Performance, Accessibility, Best Practices, SEO) at acceptable scores. No regression from previous audit. Budget thresholds enforced.
- [ ] **HAR file (if shared) stripped of sensitive headers.** `Authorization`, `Cookie`, and `X-API-Key` values replaced with `[REDACTED]` before sharing. HAR file not committed to repository.
- [ ] **Third-party scripts audited.** Render-blocking third-party scripts identified. Non-critical third-party scripts deferred or loaded async. Third-party script performance impact quantified (request count, transfer size, main-thread blocking time).
- [ ] **Frame rendering verified with Rendering panel.** Paint flashing shows no unnecessary repaints. Layout Shift Regions shows no unexpected CLS. FPS meter confirms 60fps during animations and scrolling. Layer borders show compositing working as expected.
- [ ] **Service Workers / Web Workers inspected in Application panel.** Worker registration status confirmed. Cache storage contents reviewed — no stale or incorrect cached responses. Worker error console checked (separate context from main thread).


## What Good Looks Like

**Before — DevTools-free debugging:**
```
Dev: "The checkout page is slow. Let me look at the code..."
Dev: reads 800 lines of checkout logic
Dev: "Maybe it's the shipping calculation?"
Dev: adds console.log at 15 points in the code
Dev: refreshes page, checks console: "totalTime: 3200ms"
Dev: "Where is the 3200ms coming from?"
Dev: adds more console.logs. Splits shipping logic. Re-deploys.
Dev: "Still slow. Maybe the database query?"
Total time: 3 hours. No clarity on the actual bottleneck.
```

**After — DevTools-first debugging:**
```
Dev: Opens Performance panel. Clicks record. Checks out. Stops record.
Dev: Flame chart shows: 2800ms in Scripting (yellow), 200ms in Rendering.
Dev: Clicks the wide yellow bar → `calculateShippingDiscount` at shipping.ts:142
Dev: Function takes 2400ms. Drill down: calls `fetchShippingRates()` 47 times.
Dev: Network waterfall confirms 47 identical API calls in sequence.
Dev: Fix: cache the shipping rates response. Total time: 15 minutes.
Dev: Verification: record new Performance profile → 340ms total (8x improvement).
```

## Deliberate Practice

1. **Flame Chart Literacy:** Record a Performance profile of any page load. Identify: (1) the longest task, (2) whether it is scripting, rendering, or painting, (3) the specific function and file. Goal: go from raw profile to root cause in under 2 minutes.
2. **HAR File Analysis:** Export a HAR file from any website. Open it in a HAR viewer. Find: (1) the slowest request, (2) the largest response, (3) any request that blocked rendering. Quantify how much faster the page would load if you removed the slowest request.
3. **Breakpoint-Only Debugging:** Fix a JavaScript bug using ONLY breakpoints, conditional breakpoints, and watch expressions. Zero console.log statements. This forces you to learn the Sources panel deeply.
4. **Accessibility Tree Audit:** For any web page, open the Accessibility panel. Inspect 10 interactive elements. Verify: name, role, focusable state, and ARIA attributes. Count how many elements have discrepancies between HTML source and accessibility tree. The ratio will surprise you.
5. **Mobile Emulation Realism:** Load your application on a Slow 3G throttle and 4x CPU slowdown. Time the full page load. Can you complete the primary user flow in under 30 seconds? Most desktop-developed apps fail this test on first attempt. Fix the top 3 bottlenecks.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "It looks fine on my machine — tested on Chrome, good to go." | Your machine is a MacBook Pro on gigabit fiber. Your users are on a 4-year-old Android with 3G in a rural area. DevTools emulation doesn't replicate GPU rendering, real CPU/memory constraints, or Safari WebKit flexbox quirks. Cost: **$15K-$50K** in post-release hotfixes for device-specific bugs found by users. |
| "Mobile emulation in DevTools is enough — I don't need a real device." | Chrome DevTools emulates viewport, touch events, and user agent — but NOT actual GPU rendering, browser engine quirks (Safari/iOS handles flexbox differently), real network variability, or device-specific bugs. Cost: **$15K-$50K** in device-specific regressions discovered post-launch. |
| "I'll just leave the debugger statement — I'll remove it before the PR merges." | The `debugger;` statement ships to production. When a support agent opens DevTools to help a customer, the page freezes. Cost: **$1K-$5K** per incident + emergency hotfix deploy + support team blocked from assisting customers. |
| "The Accessibility panel shows zero violations — we're accessible." | Automated tools catch ~30% of WCAG issues. They miss keyboard traps, focus order violations, meaningful alt text quality, and screen reader announcement errors. Cost: **$20K-$100K** in accessibility lawsuit risk from issues that only manifest on real assistive technology. |
| "I disabled cache for debugging — the production build will be fine." | You spent the entire debugging session with `Disable cache` checked, so you added cache-busting query params everywhere. In production, users get zero cache benefit and LCP regresses. Cost: **$5K-$15K/month** in excess CDN bandwidth and slower user experience. |

## Anti-Patterns

- **Debugging with cache disabled by default, then shipping a build that assumes cache is disabled.** The `Disable cache` checkbox is on in your DevTools, so you add cache-busting query params to every request. In production, users would benefit from caching but your build prevents it. **Total cost: $5,000-$15,000/month in excess CDN bandwidth and slower user experience (LCP regressions).**
- **Using `console.log(JSON.stringify(largeObject))` in a hot path.** `JSON.stringify` on a large object in a render loop can block the main thread for 50-200ms per call, creating the jank you are trying to debug. Use `console.log('checkpoint', performance.now())` for timing, and `copy(obj)` for inspecting objects when paused at a breakpoint. **Total cost: $2,000-$8,000 in wasted debugging time chasing phantom jank caused by the debugging code itself.**
- **Leaving `debugger;` statements in production code.** A `debugger;` statement that ships to production has no effect on most users (DevTools closed), but if ANY user has DevTools open, the page freezes. This happens most often with support staff who use DevTools to help customers. **Total cost: $1,000-$5,000 per incident of support team unable to assist customers + emergency hotfix deploy.**
- **Taking a heap snapshot of a production tab with 500MB+ heap.** Chrome DevTools copies the entire heap to take a snapshot. On a 500MB heap, this can freeze the tab for 10-30 seconds. If this is a production tab serving users, you just caused an outage. **Total cost: $10,000-$50,000 in self-inflicted production downtime.**
- **Trusting the Accessibility panel alone without testing with an actual screen reader.** The Accessibility panel shows the computed tree, but screen readers have bugs, quirks, and different interpretations. VoiceOver on macOS, NVDA on Windows, and TalkBack on Android can announce the same element differently. Automated tools catch ~30% of accessibility issues. **Total cost: $20,000-$100,000 in accessibility lawsuit risk from issues that only manifest on real screen readers.**
- **Exporting a HAR file that contains authentication tokens or session cookies and sharing it insecurely.** A HAR file contains every request header including `Authorization: Bearer eyJ...` and `Cookie: session=...`. Sharing this file in Slack, email, or a public bug tracker is a credential leak. Always strip sensitive headers before sharing: open HAR in text editor, search for `Authorization` and `Cookie`, replace values with `[REDACTED]`. **Total cost: $50,000-$500,000 in security incident response and credential rotation.**
- **Using mobile emulation and assuming it matches real device behavior.** Chrome DevTools emulates viewport, touch events, and user agent — but NOT: GPU rendering differences, actual CPU/memory constraints, browser engine quirks (Safari/iOS WebKit handles flexbox differently than Chrome), real network variability, or device-specific bugs. Always verify on a real device before shipping. **Total cost: $15,000-$50,000 in post-release hotfixes for device-specific bugs found by users.**

## Verification

- [ ] Reproduced the bug with DevTools open and captured evidence (screenshot, HAR, or profile)
- [ ] Identified root cause using the appropriate panel (Elements, Console, Network, Performance, Memory)
- [ ] Fix verified with Live Edit or local overrides before changing source code
- [ ] Network: no 4xx/5xx requests remain after fix
- [ ] Console: no new errors or warnings introduced by the fix
- [ ] Performance: no regression (compare before/after Performance profiles)
- [ ] Memory: no leak introduced (heap comparison before/after fix shows stable memory)
- [ ] Accessibility: no regression (axe DevTools scan shows no new violations)
- [ ] Mobile: tested on at least one real mobile device, not just emulation
- [ ] Evidence exported and attached to bug report/ticket (HAR, screenshot, console log)

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.
### Scale Depth

#### Solo Developer
Open DevTools when something breaks. Use Console for errors, Network for failed requests, Elements for CSS issues. No systematic profiling. Performance checked via Lighthouse occasionally. Memory investigated only when crashes occur. Keyboard testing manual and ad-hoc.

#### Small Team (2-10)
Systematic DevTools triage (Console → Network → Performance) for every reported bug. Performance profiles saved and compared before/after fixes. Lighthouse CI run on PRs with advisory budgets. HAR files exported for backend-reported latency issues. Mobile emulation used before every release. Coverage panel checked quarterly for dead code.

#### Medium Team (10-50)
Performance budgets enforced in CI (LCP < 2.5s, TBT < 200ms, CLS < 0.1). Memory leak regression tests automated in E2E suite. Production Real User Monitoring (RUM) correlated with lab data. HAR files archived for postmortems. Third-party script performance measured monthly. Web Vitals dashboard with per-route scoring. Dedicated performance sprint per quarter.

#### Enterprise (50+)
Lab data (Lighthouse CI, WebPageTest) + field data (CrUX, RUM) combined for holistic performance governance. Performance budgets enforced at PR, release, and production monitoring levels. Synthetic monitoring on real devices across geographies. Dedicated performance engineering team. A/B test every major change against performance baseline. SLI/SLO defined for Core Web Vitals (e.g., 95th percentile LCP < 2.5s). Performance regression = incident (same severity as error regression).

**Transition Triggers:** Scale up when: (a) bug reports take > 30 min average to triage → Small, (b) LCP exceeds 2.5s in production RUM → Medium, (c) page performance directly impacts revenue (ecommerce, ad-supported) → Enterprise, (d) user base crosses 1M or revenue > $50M → Enterprise.

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Page loads in 800ms on developer's M3 MacBook, 8 seconds on a $200 Android phone — "it works on my machine" | Dev testing on gigabit WiFi, 32GB RAM, no CPU throttling. Production users on 4G, 2GB RAM, mid-range CPU. JavaScript bundle is 2MB uncompressed, blocking render | Enable CPU throttling (4x slowdown) and network throttling (Slow 3G) in DevTools Performance panel. Set performance budgets: JS bundle <200KB, LCP <2.5s on throttled connection. Test on a real mid-range device (Moto G4 or equivalent) | "My machine" has more processing power than your entire user base combined. If you only test on a developer laptop, you're testing a benchmark — not your product. |
| Lighthouse score is 98 but users report 6-second First Input Delay — lab data != field data | Lighthouse measures in a controlled environment with no extensions, no third-party scripts, no CPU contention. Real users have ad blockers, antivirus, 47 open tabs, and a 5-year-old laptop | Add Real User Monitoring (RUM) with `web-vitals` library. Track FID/INP percentiles. Set performance budgets on field data, not lab data. Lab score of 98 with field FID of 1800ms = the lab is lying to you | Lighthouse is a clean-room measurement. Real users browse with 47 tabs, 15 extensions, and a CPU thermal-throttling on their lap. Only field data tells the truth about performance. |
| `console.log` left in production — logging 100K user objects per hour, visible in DevTools, contains PII | Developer added `console.log(user)` for debugging, code passed review, shipped to production. No lint rule, no build-time stripping | Add ESLint rule `no-console` for production builds. Use `debug` library with namespaced loggers that compile away in production. CI check: `grep -r "console\." dist/` must return empty | console.log is a debug tool, not a logging framework. It ships to every user's browser, consumes memory, and leaks data to anyone who opens DevTools. Production code needs zero console statements. |
| CSP `script-src 'unsafe-inline'` — developer's workaround becomes production security hole for 2 years | Developer added `unsafe-inline` to get a third-party widget working during a Friday deploy. Intended to fix it Monday. Two years later, it's still there — and now XSS is trivial | Never commit `unsafe-inline` or `unsafe-eval`. If a third-party script requires it, file a security exception with an expiration date. Add CSP report-only mode in CI: `Content-Security-Policy-Report-Only` with strict policy, alert on violations | Security workarounds are the most permanent kind of temporary. `unsafe-inline` committed on Friday will be in production on Monday, next quarter, and after you leave the company. Never commit it. |
| Paint flashing — entire page re-renders on every keystroke in a search input. 55 FPS drops to 8 FPS | `onChange` handler calls `setState` which triggers full component tree reconciliation. Search input is in a parent component — state change causes every child to re-render even though only the search results list changed | Use React DevTools Profiler to identify wasted renders. Lift search state into a separate context or use `useDeferredValue`. Memoize expensive children with `React.memo`. For keystroke rendering: `requestAnimationFrame` + debounce 150ms | State changes at the top of the component tree cause O(n) re-renders where n is the entire tree. A search input in the root component means every keystroke re-renders your entire application. |
| Recorder shows 15-second gap between "button click" and "API call" — developer insists the code runs synchronously | Third-party analytics script (`gtag`, `segment`, `fullstory`) blocks the main thread during page interaction. The click handler is queued behind a 500ms analytics beacon | Audit third-party scripts: block them in DevTools and record again. If the gap disappears, the third-party script is the culprit. Load analytics with `async` + `defer`. Use Partytown to run third-party scripts in a Web Worker | Third-party scripts don't show up in your flame chart as "third-party overhead" — they show up as "your code is mysteriously slow." Audit by elimination: block scripts until the gap vanishes, then you know the culprit. |

## References

- [Core Workflow](../references/core-workflow.md) — Panel-by-panel deep dive with advanced techniques
- [Anti-Patterns](../references/anti-patterns.md) — Common DevTools mistakes and their fixes
- [Best Practices](../references/best-practices.md) — Pro tips from Chrome DevTools engineers
- [Calibration](../references/calibration.md) — Performance budgets and when to stop optimizing
- [Checklist](../references/checklist.md) — Pre-launch browser testing checklist
- [Error Decoder](../references/error-decoder.md) — Common Console errors decoded with solutions
- [Footguns](../references/footguns.md) — DevTools features that frequently cause problems
- [Scale Depth](../references/scale-depth.md) — Browser testing at scale: large SPAs, micro-frontends, Web Workers
