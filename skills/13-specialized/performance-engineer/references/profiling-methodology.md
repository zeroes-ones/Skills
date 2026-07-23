# Profiling Methodology

### CPU Profiling

- **Sampling profilers**: Periodically interrupts the program and records the call stack. The frequency determines granularity (default: 99-1000 Hz). Lower overhead than instrumentation.
- **Flame graph interpretation**:
  - **x-axis**: Proportion of samples (width = time spent on-cpu).
  - **y-axis**: Call stack depth (root at bottom, leaves at top).
  - **Plateaus**: Wide top-edge functions — these are your hot functions consuming the most CPU.
  - **Towers**: Deep call stacks — may indicate over-abstracted code paths.
  - **Search**: Interactive flame graphs let you search for function names and highlight their footprint across all stacks.
- **Sampling vs instrumentation**: Sampling (pprof, perf) shows _where_ time is spent. Instrumentation (gprof, Java HPROF) adds probes to every function — higher overhead but gives exact call counts.

### Memory Profiling

- **Allocation profiling** (`pprof --alloc_space`, `async-profiler alloc`): Shows what code allocates the most memory — this is different from what _retains_ the most. High allocation rate causes GC pressure.
- **Heap profiling** (`pprof --inuse_space`, heap snapshots): Shows what is currently in the heap. Good for finding leaks.
- **The distinction**: A function that allocates 1GB per second but releases it immediately (high allocation rate, low heap-in-use) is a GC pressure problem. A function that holds 1MB that never gets freed (low allocation rate, high heap-in-use) is a memory leak.

### I/O Profiling

- **strace**: Trace system calls. Look for: excessive `read`/`write` syscalls (many small I/O operations), slow `open`/`stat` (cold file system cache), `epoll_wait` delays.
- **iostat**: Per-disk metrics. Key columns: `%util` (time disk is busy — >80% is saturated), `await` (average I/O latency per request — >10ms indicates problem), `r/s` + `w/s` (IOPS).
- **iotop**: Per-process I/O usage. Find which process is generating disk I/O.
- **Signs of trouble**: High `iowait` in `top` or `mpstat`, combined with high disk `await` in `iostat` — processes are stuck waiting for disk.
