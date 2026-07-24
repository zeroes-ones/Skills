# Profiling Toolchain

## RenderDoc (Cross-platform)
- **GPU capture:** Frame capture on D3D11, D3D12, Vulkan, OpenGL
- **Draw call inspection:** Mesh viewer, texture viewer, pipeline state
- **Performance counters:** GPU duration per draw call, shader resource usage
- **Hotkey:** F12 or Print Screen to capture frame
- **Command line:** `renderdoccmd capture -w <process_name>`

## PIX (DirectX 12 / Xbox)
- **GPU captures:** Timing captures (GPU durations), occupancy analysis
- **Ray tracing:** Acceleration structure visualization, shader table inspection
- **Shader debugging:** HLSL debugger with register inspection
- **Console:** Xbox Series X|S GPU captures via PIX on Windows

## Xcode GPU Capture (Metal)
- **Frame capture:** Metal application profiling on macOS/iOS
- **Shader profiler:** Per-line GPU cost, register pressure, occupancy
- **Memory:** Texture memory usage, buffer allocations, memory warnings
- **Dependency viewer:** Command encoder dependencies, synchronization gaps

## Unity Profiler
- **CPU:** Module breakdown (Scripts, Rendering, Physics, Animation)
- **GPU:** `GraphicsProfiler` for draw call timing, shader complexity
- **Memory:** Managed heap, native allocations, texture/audio memory
- **Deep Profile:** Per-method CPU cost (slowdown: 3-5x)

## Unreal Insights
- **Trace:** Frame-level timing, GPU markers, CPU/GPU sync points
- **Memory:** Asset memory, streaming pool, allocation tracking
- **Network:** Replication stats, RPC timing, bandwidth per actor
- **Command:** `-trace=default,memory,gpu,net` launch argument

## Key Metrics to Track
- **Frame time:** P99 < budget. Budget = 16.67ms (60 FPS), 33.33ms (30 FPS)
- **GPU duration:** Render thread < 80% of frame budget
- **Draw calls:** <1000 on PC, <500 on console, <200 on mobile
- **Shader complexity:** ALU/Bandwidth/Texture ratio per draw call
- **Memory:** Peak <85% of budget, fragmentation <15%
- **GC Allocs:** Unity: <1KB/frame in hot path. Unreal: track `FMemory` stats
