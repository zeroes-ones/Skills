# Concurrency & Async Patterns

### Thread Pool Sizing

- **CPU-bound tasks**: Pool size = number of cores (or cores + 1 for cache miss tolerance). More threads = context switching overhead with no throughput gain.
- **I/O-bound tasks**: `pool_size = cores × (1 + wait_time / service_time)`. If service_time = 10ms and wait_time (blocking) = 90ms: `cores × (1 + 9) = 10 × cores`. This is the "Little's Law" equivalent for thread pools.
- **Mixed workloads**: Use separate pools for CPU and I/O tasks, or use async I/O to avoid blocking pool threads entirely.

### Async I/O Patterns

- **Event loop model (Node.js)**: Single thread + non-blocking I/O. The event loop never blocks — all blocking operations (file I/O, DNS, crypto) are offloaded to a thread pool (`libuv`). Never use `fs.readFileSync` or synchronous DB calls in the hot path.
- **Reactor pattern (Netty, Java NIO)**: Event demultiplexer (Selector) dispatches I/O events to handlers. Scales to thousands of connections with few threads.
- **Virtual threads (Java 21+)**: Lightweight threads managed by the JVM. Pause on blocking I/O without pinning OS threads. "One thread per request" becomes practical at scale. Eliminates the need for reactive programming in most cases.
- **Async/await**: Syntactic sugar over promises/futures. Non-blocking but cooperative — long CPU-bound sections still block the calling thread.

### Race Condition Detection

- **ThreadSanitizer (TSan)**: Detects data races in C/C++ and Go. Compile with `-fsanitize=thread` (C++) or run `go build -race` (Go). Flags any access to shared memory without synchronization.
- **Go race detector**: `go run -race`, `go test -race`. Instruments all memory accesses. Catches unsynchronized reads/writes to the same variable from different goroutines.
- **Identifying shared mutable state**: If two goroutines/threads both read and write the same variable without a mutex, channel, or atomic — that's a data race. Fix: use channels (Go), locks, or immutable data structures.
