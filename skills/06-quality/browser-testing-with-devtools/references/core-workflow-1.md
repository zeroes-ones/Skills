## Core Workflow

### Phase 0: Systematic Triage

Open DevTools (F12 or Cmd+Option+I). Work through panels in order until you find the signal:

```
1. Console (Esc to toggle): Any red errors? Fix those first. Errors cascade.
2. Network: Any red (4xx/5xx) requests? Check response for error messages.
3. Elements: Inspect the problematic element. Check computed styles.
4. If the problem is visual: Rendering panel > Paint Flashing ON. Reproduce. See what repaints.
5. If the problem is interactive: Sources panel > Event Listener Breakpoints > Mouse > click.
6. If no signal from panels 1-5: The bug is likely in application state/logic.
```

### Phase 1: Elements Panel — DOM and Style Debugging

```
Technique 1: Force element state
  Right-click element → Force state → :hover / :focus / :active / :visited / :focus-within
  Debug hover styles without moving your mouse.

Technique 2: Break on subtree modifications
  Right-click parent element → Break on → subtree modifications
  JS that modifies DOM children will pause in Sources panel with full call stack.

Technique 3: Computed styles detective work
  Elements → Computed tab → click on a property value
  Shows: which CSS rule set this value, file, and line number.
  A crossed-out value with a chain link = overridden by more specific rule.

Technique 4: Box model visualization
  Elements → Styles → scroll to box model diagram
  Hover over margin/border/padding/content regions to highlight on page.
  Identifies: collapsed margins, unexpected overflow, box-sizing issues.
```

### Phase 2: Console + Sources — JavaScript Debugging

```
Technique 1: Conditional breakpoints
  Right-click line number → Add conditional breakpoint
  Enter: user.role === 'admin' && cart.items.length > 0
  Only pauses when the condition is true. Saves hours over manual stepping.

Technique 2: Logpoints (no-code console.log)
  Right-click line number → Add logpoint
  Enter: "User: " + user.name + ", Items: " + items.length
  Logs to Console without modifying source code. Removed when DevTools closes.

Technique 3: Watch expressions
  Sources → Watch → add expressions: user, cart.total, items.length
  Expressions evaluate in real-time as you step through code.
  No need to hover over variables repeatedly.

Technique 4: Blackbox scripts
  Right-click framework file in Sources → Blackbox script
  Chrome skips framework code when stepping through. You only step through YOUR code.
```

### Phase 3: Network Panel — Request Debugging

```
Technique 1: HAR export for offline analysis
  Network panel → right-click any request → Save all as HAR with content
  HAR = HTTP Archive. Contains every request: headers, timing, response body.
  Share with backend team: "Here's exactly what the browser sent and received."

Technique 2: Timing breakdown
  Click a request → Timing tab
  Shows: Queueing (waiting for connection slot), Stalled, DNS Lookup,
  Initial Connection, SSL, Request Sent, Waiting (TTFB), Content Download.
  High TTFB (>200ms) = backend is slow. High Content Download = large payload.
  High Queueing/Stalled = browser connection limit (6 per domain for HTTP/1.1).

Technique 3: Request blocking
  Network panel → right-click a script/request → Block request URL
  Simulates: "What happens if this third-party script fails to load?"
  Tests: error handling, fallback behavior, degraded experience.

Technique 4: Override responses (Local Overrides)
  Network → right-click request → Override content → edit response
  Simulates API responses without touching backend. Test error states,
  empty states, loading states by modifying the API response locally.
```

ASCII diagram:
```
┌────────────────────────────────────────────────────┐
│              DEVTOOLS DEBUGGING FLOW                │
├────────────────────────────────────────────────────┤
│  Phase 0: Systematic Triage (all panels quick scan) │
│     │                                               │
│     ├── Console errors? ──► Phase 2 (Breakpoints)   │
│     ├── Network red? ──► Phase 3 (HAR + Timing)     │
│     ├── Rendering wrong? ──► Phase 1 (Computed CSS) │
│     ├── Slow? ──► DT1 (Performance Profile)         │
│     ├── Memory? ──► DT2 (Heap Snapshot)             │
│     └── A11y? ──► DT3 (Accessibility Tree)          │
│                                                      │
│  Phase 4: Verify Fix (Live Edit → no refresh)        │
│  Phase 5: Export Evidence (HAR, screenshots, profile)│
└────────────────────────────────────────────────────┘
```
