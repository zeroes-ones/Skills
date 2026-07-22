# Profiling Guide

Language-specific playbook for CPU, memory, and concurrency profiling. Use when a dashboard-level metric (high CPU, growing heap, slow response) needs drill-down to the function level.

---

## Node.js

### Tools

| Tool | Best For | Install |
|------|----------|---------|
| **Clinic.js** (Doctor → Bubbleprof → Flame) | High-level diagnosis, async bottleneck visualization, CPU flame graphs | `npm install -g clinic` |
| **0x** | Quick flame graphs from the command line | `npm install -g 0x` |
| Node.js built-in `--cpu-prof` | CPU profiling without external tools | Built-in (Node 12+) |
| Node.js built-in `--heap-prof` | Memory allocation profiling | Built-in (Node 12+) |
| Node.js `--prof` + `--prof-process` | Low-level V8 profiling | Built-in |
| Chrome DevTools (`--inspect`) | Memory snapshots, allocation timeline, CPU profile | Built-in |

### Workflow: Clinic.js

```
clinic doctor -- node app.js          # 1. High-level diagnosis
clinic bubbleprof -- node app.js      # 2. Async operation tracing
clinic flame -- node app.js           # 3. CPU flame graph
```

1. **Start with Doctor**: Run your app under load, hit the slow endpoint, exit. Doctor shows a health score and points to the likely bottleneck category (CPU, I/O, Event Loop delay, Memory).
2. **Drill into Bubbleprof**: If the issue is async (blocked I/O, slow promises), Bubbleprof visualizes async operations as bubble diagrams — wider bubbles = more blocking.
3. **Drill into Flame**: If the issue is CPU, Flame produces a flame graph. Width = CPU time. Look for wide plateaus at the top.

### Node.js Built-in Profiling

```bash
# CPU profile — captures for 30 seconds, outputs to file
node --cpu-prof --cpu-prof-dir ./profiles --cpu-prof-interval 1000 app.js

# Heap profile — tracks allocation over time
node --heap-prof --heap-prof-dir ./profiles app.js

# Low-level V8 profiling (tick-based)
node --prof app.js
# After exit, process the output:
node --prof-process isolate-*.log > processed.txt

# Chrome DevTools — connect and profile in the UI
node --inspect-brk app.js
# Open chrome://inspect, click "Open dedicated DevTools for Node"
```

### Key Node.js Flags

| Flag | Purpose |
|------|---------|
| `--inspect` | Connect Chrome DevTools (no break on start) |
| `--inspect-brk` | Connect Chrome DevTools, break at first line |
| `--max-old-space-size=4096` | Increase heap limit (MB) — default is ~2GB on 64-bit |
| `--expose-gc` | Expose `global.gc()` for manual GC triggering |
| `--trace-gc` | Log all GC events to stdout |
| `--trace-warnings` | Show stack traces for deprecation warnings |

### Memory Leak Investigation (Node.js)

1. **Take two heap snapshots** in Chrome DevTools (Memory tab) — one before and one after performing the leak-causing action.
2. **Use comparison view**: Switch from "Summary" to "Comparison" to see what objects were allocated and not freed between snapshot 1 and snapshot 2.
3. **Look for**: High delta in `# New` or `# Retained` for a class you don't expect to grow. Detached DOM trees (common in SSR memory leaks). Closures capturing large scopes.
4. **Find retainers**: Click an object → "Retainers" panel shows the reference chain to a GC root. The path: `Object → closure scope → module → GC root`. The first object outside of GC root is the culprit.

### GC Analysis (Node.js / V8)

```bash
# Log GC activity
node --trace-gc --trace-gc-verbose app.js

# In Chrome DevTools, check the Performance panel's "Memory" section
# Look for: frequent minor GCs (every few seconds), infrequent full GCs
```

- **Minor GC (Scavenge)**: Fast, young generation collection. If these happen every <1s under moderate load, allocation rate is too high.
- **Major GC (Mark-Sweep-Compact)**: Full heap collection. Causes event loop delay. If >100ms, heap is too large or too many old-generation objects.

---

## Python

### Tools

| Tool | Best For | Install |
|------|----------|---------|
| **py-spy** | Sampling profiler — no code changes, no restart | `pip install py-spy` |
| **cProfile** | Built-in deterministic profiler | Built-in |
| **line_profiler** | Per-line timing of specific functions | `pip install line_profiler` |
| **memory_profiler** | Per-line memory usage | `pip install memory_profiler` |
| **snakeviz** | Visualize cProfile output | `pip install snakeviz` |

### py-spy (Sampling Profiler)

**No code changes needed** — py-spy reads /proc/pid/maps on Linux or uses process_vm_readv on macOS. Attaches to a running process.

```bash
# Record flame graph — run your app, record 30 seconds
py-spy record -o flame.svg -- python app.py

# Top-like live view — see hottest functions in real time
py-spy top -- python app.py

# Attach to running process
py-spy record -o flame.svg --pid 12345 --duration 30

# Native speed profile (includes C extensions)
py-spy record --native -o flame.svg -- python app.py
```

**Async profiling**: py-spy supports async/await natively — it samples the event loop and shows coroutines by name.

### cProfile (Deterministic)

Tracks every function call — higher overhead but gives exact call counts and cumulative times.

```bash
# Profile script, save stats
python -m cProfile -o output.pstats script.py

# View stats in terminal (top 20 by cumulative time)
python -m pstats output.pstats

# Visualize with snakeviz — opens a web UI
snakeviz output.pstats
```

**Key columns in snakeviz**: `cumtime` (cumulative time including children) — sort by this. `tottime` (time in this function only) — sort by this to find hot functions. `ncalls` — primitive calls count.

### line_profiler

Profile specific functions line-by-line:

```python
from line_profiler import LineProfiler
lp = LineProfiler()

@lp  # decorator on the function to profile
def slow_function():
    # ... your code ...

lp.print_stats()
```

```bash
# Or use kernel magic in Jupyter:
# %load_ext line_profiler
# %lprun -f slow_function slow_function()
```

### memory_profiler

```python
from memory_profiler import profile

@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (10 ** 7)
    del b
    return a
```

```bash
python -m memory_profiler script.py
```

Shows: line number, memory usage (MiB), increment, and line content. Look for lines with large increments that persist (not freed).

---

## Go

### Tools

| Tool | Best For | How to Enable |
|------|----------|---------------|
| **pprof** (net/http/pprof) | CPU, memory, goroutine, mutex, block profiling | Import `_ "net/http/pprof"` |
| **pprof** (runtime/pprof) | Programmatic profiles (CLI tools, batch jobs) | `import "runtime/pprof"` |
| **go tool trace** | Execution tracing — goroutine scheduling, GC, network | `import "runtime/trace"` |

### CPU Profiling (pprof)

Enable the HTTP handler:

```go
import _ "net/http/pprof"
// Start an HTTP server (even in a goroutine)
go func() {
    log.Println(http.ListenAndServe("localhost:6060", nil))
}()
```

Collect and analyze profiles:

```bash
# 30-second CPU profile
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Interactive commands inside pprof:
#   top        — show top hot functions by CPU time
#   list Func  — show the source of a function with line-level timing
#   web        — generate SVG call graph and open in browser
#   pdf        — generate PDF call graph
#   flamegraph — generate interactive SVG flame graph

# Export flame graph immediately
go tool pprof -http :8080 http://localhost:6060/debug/pprof/profile?seconds=30
```

### Memory Profiling

```bash
# Current heap (in-use objects)
go tool pprof http://localhost:6060/debug/pprof/heap

# Allocation profile (shows cumulative allocations since start)
go tool pprof -alloc_space http://localhost:6060/debug/pprof/heap
go tool pprof -alloc_objects http://localhost:6060/debug/pprof/heap

# In-use space comparison (useful for finding leaks — compare two snapshots)
# Take snapshot 1, wait, take snapshot 2:
curl -o heap1.pprof http://localhost:6060/debug/pprof/heap
# ... do something that might leak ...
curl -o heap2.pprof http://localhost:6060/debug/pprof/heap
go tool pprof -base heap1.pprof heap2.pprof
```

Use `-alloc_space` to find what allocates the most (GC pressure), `-inuse_space` to find what's retained (leaks).

### Goroutine Profiling

```bash
# List all goroutines with stack traces
go tool pprof http://localhost:6060/debug/pprof/goroutine

# In text format, see how many of each stack
# Look for: hundreds or thousands of goroutines waiting on the same channel/select
#   → goroutine leak. The stack shows exactly where they're blocked.

# Open in web UI for flame graph
go tool pprof -http :8080 http://localhost:6060/debug/pprof/goroutine
```

### Execution Tracing (go tool trace)

```go
import "runtime/trace"

f, _ := os.Create("trace.out")
trace.Start(f)
defer trace.Start(f)
```

```bash
go tool trace trace.out
# Opens a web UI showing:
# - Goroutine analysis: how many running, runnable, blocked
# - Network blocking: which goroutines are blocked on I/O
# - Syscall analysis: system call overhead
# - Scheduler latency profiler: P99 latency per goroutine
# - GC events: when GC runs, how long it pauses
```

### Benchmarks with Profiling

```bash
# Run benchmarks with CPU profiling
go test -bench=. -benchmem -cpuprofile=cpu.out -memprofile=mem.out

# Analyze
go tool pprof cpu.out
go tool pprof mem.out

# Compare with base (before/after optimization)
go test -bench=. -benchmem -cpuprofile=before.cpu.out
# ... apply optimization ...
go test -bench=. -benchmem -cpuprofile=after.cpu.out
go tool pprof -base before.cpu.out after.cpu.out
# Negative percentages = improvement
```

### Race Detection

```bash
go test -race ./...           # Run all tests with race detector
go build -race ./...          # Build with race detector (for integration tests)

# Output format:
# WARNING: DATA RACE
# Read by goroutine 42: ... (stack trace of the read)
# Previous write by goroutine 7: ... (stack trace of the previous write)
```

The race detector only finds races that actually happen during execution. Run with a realistic load to maximize coverage.

---

## JVM (Java / Kotlin / Scala)

### Tools

| Tool | Best For | Install / Enable |
|------|----------|------------------|
| **JDK Flight Recorder (JFR)** | Low-overhead profiling (CPU, memory, I/O, GC) | Built-in (JDK 11+) |
| **JDK Mission Control (JMC)** | JFR analysis GUI | Download from Oracle |
| **async-profiler** | Low-overhead flame graphs, allocation profiling, lock profiling | `apt get` or download from GitHub |
| **JProfiler** | Full-featured commercial profiler | Commercial license |
| **YourKit** | Full-featured commercial profiler | Commercial license |
| **VisualVM** | Basic heap/CPU profiling, GC visualization | `jvisualvm` (JDK 8-11) |

### JDK Flight Recorder (JFR)

Built into the JVM since JDK 11. Overhead < 1-2% in production.

```bash
# Start recording on startup
java -XX:StartFlightRecording=filename=recording.jfr,settings=profile,duration=60s \
     -jar app.jar

# Start recording on a running JVM (requires JDK 9+)
jcmd <pid> JFR.start filename=recording.jfr settings=profile duration=60s
jcmd <pid> JFR.dump filename=recording.jfr

# Analyze with JDK Mission Control
jmc recording.jfr
```

**JFR events to look for**:
- **CPU load**: `jdk.ExecutionSample`, `jdk.CPUTime` — the sampling-based CPU hot spots
- **GC pauses**: `jdk.GCPhasePause` — time spent in GC stop-the-world pauses
- **Allocation**: `jdk.ObjectAllocationOutsideTLAB` — allocations that bypass thread-local buffers
- **Synchronization**: `jdk.JavaMonitorEnter`, `jdk.JavaMonitorBlocked` — lock contention
- **I/O**: `jdk.SocketRead`, `jdk.SocketWrite` — socket read/write duration
- **File I/O**: `jdk.FileRead`, `jdk.FileWrite` — file read/write duration

### async-profiler

Low-overhead sampling profiler, produces SVG flame graphs.

```bash
# CPU profiling — 60 seconds
./profiler.sh -d 60 -o flamegraph -f cpu.svg <pid>

# Allocation profiling — show what allocates most
./profiler.sh -d 60 -e alloc -o flamegraph -f alloc.svg <pid>

# Lock profiling — show contended locks
./profiler.sh -d 60 -e lock -o flamegraph -f lock.svg <pid>

# Wall-clock profiling — includes blocking I/O time (non-CPU time)
./profiler.sh -d 60 -e wall -o flamegraph -f wall.svg <pid>

# Output to JFR format (analyze with JMC)
./profiler.sh -d 60 -o jfr -f recording.jfr <pid>
```

### GC Tuning (JVM)

**G1GC** (default since JDK 9):
```bash
# Target pause time (not a guarantee, but a goal)
-XX:MaxGCPauseMillis=200
# Max heap size
-Xmx8g
# Initiating heap occupancy percent — start concurrent cycle earlier/later
-XX:InitiatingHeapOccupancyPercent=45
# Parallel GC threads
-XX:ConcGCThreads=4
```

**ZGC** (sub-millisecond pauses, JDK 15+):
```bash
-XX:+UseZGC -Xmx8g
```

**Shenandoah** (low-pause, JDK 12+):
```bash
-XX:+UseShenandoahGC -Xmx8g
```

**GC Logging**:
```bash
# JDK 9+
-Xlog:gc*:file=gc.log:time,uptime,level,tags

# JDK 8
-XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:gc.log
```

**Analyzing GC logs**: Use `gceasy.io`, GCViewer, or JMC to parse the log and generate key metrics: average/peak pause time, GC frequency, allocation rate, promotion rate.

---

## Flame Graph Interpretation

### Structure

```
y-axis (depth)
       ^
    🟧🟧🟧🟧🟧          ← leaf functions (top of stack)
    🟧🟧🟧🟧🟧           ← intermediate frames
    🟧🟧🟧🟧🟧            ← calls deeper
    🟧🟧🟧🟧🟧             ← root calls
    ───────────────→ x-axis (proportion of samples)
```

- **x-axis**: Proportion of total samples. The wider a frame, the more CPU time was spent _in that function or its descendants_.
- **y-axis**: Call stack depth. Bottom = root thread/entry point. Top = leaf function executing at sample time.

### Patterns to Recognize

| Pattern | Looks Like | Means |
|---------|-----------|-------|
| **Wide plateau** | A single frame spanning much of the x-axis | Hot function — this is where most CPU time goes. Optimize or inline this. |
| **Narrow tower** | A thin tall column | Deep call chain — may indicate over-abstracted or recursive code. |
| **Multiple wide siblings** | Several wide frames side-by-side at top | Several equally hot functions — look for shared ancestor or loop. |
| **"Needles"** | Very thin tall lines | Rare but deep event — GC (may appear repeatedly), exception stack traces in Java. |
| **Messy mountain range** | Many spiky frames, no clear plateau | Many small contributions — framework overhead, heavy function dispatch. |

### Icicle vs Flame Orientation

- **Flame** (root at bottom, leaf at top): Standard orientation. Read left-to-right within a frame to see hot paths. Function A is at the bottom, calls B, B is wider than C → B is the hot path.
- **Icicle** (root at top, leaf at bottom): Same data, inverted. Used by some tools. Some people find it easier for "top-down" reading.

### Interactive Flame Graphs

Tools like `async-profiler`, `pprof`, and `0x` generate SVG flame graphs that support:

- **Mouseover**: Shows function name, percentage, and sample count
- **Search** (Ctrl+F): Highlight a function name across all stacks — shows its total footprint
- **Click a frame**: Zoom into that frame — reframes the x-axis to show only its children
- **Breadcrumb**: Shows the path from root to the zoomed function

Search is the fastest way to find if a particular function is contributing significantly to CPU or memory.

---

## General Profiling Workflow

1. **Ask the right question**: Is it a CPU problem? Memory? I/O? Lock contention? This determines which tool and which profile type to use.
2. **Choose the right profiler**: Sampling (low overhead, good for production) vs instrumentation (high overhead, good for development).
3. **Profile under realistic load**: A mostly-idle system may not trigger GC or show the real hot paths. Use load testing or production traffic.
4. **Start wide, then narrow**: Begin with a broad profile (e.g., `async-profiler -e wall` for wall-clock, `clinic doctor` for overview), then drill into specific subsystems.
5. **Compare before/after**: Always take a baseline profile before optimizing. The improvement (or lack thereof) is the validation.
6. **Profile across layers**: If a slow endpoint has high CPU on the application server but low query latency, the bottleneck is application code (serialization, business logic), not the database.
