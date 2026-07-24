# Metal on macOS — GPU Compute & Rendering

<!-- STANDARD: 3min -- Metal framework for GPU-accelerated compute and rendering -->

## Metal Overview on macOS

Metal is Apple's low-level GPU API. On macOS, Metal has distinct characteristics vs iOS:

| Feature | macOS | iOS/iPadOS |
|---|---|---|
| **GPU families** | Apple family (M-series), Mac family (Intel/AMD) | Apple family only |
| **Buffers** | Managed mode + Shared mode | Shared mode only |
| **Tile shading** | Available (Apple Silicon) | Available |
| **Ray tracing** | Available (M3+) | Available (A17+) |
| **External GPU** | Supported (Intel Macs) | Not supported |
| **Headless rendering** | Supported (command-line tools) | Not supported |
| **Display link** | `CVDisplayLink` for vsync | `CADisplayLink` |

---

## Device Selection

```swift
import Metal

// Default system device (preferred for single-GPU Macs)
guard let device = MTLCreateSystemDefaultDevice() else {
    fatalError("Metal is not supported on this Mac")
}

print("GPU: \(device.name)")
// Apple Silicon: "Apple M1", "Apple M2 Pro", etc.
// Intel Mac (AMD dGPU): "AMD Radeon Pro 5500M"
// Intel Mac (integrated): "Intel UHD Graphics 630"

// Enumerate all GPUs (multi-GPU Macs)
let devices = MTLCopyAllDevices()
for d in devices {
    print("\(d.name) — \(d.isHeadless ? "headless" : "display") — \(d.isLowPower ? "low power" : "high perf")")
}

// Select the high-performance GPU (discrete GPU on Intel Macs)
let highPerfDevice = devices.first { !$0.isLowPower && !$0.isHeadless }
    ?? device
```

---

## Buffer Management — The macOS Difference

Unlike iOS where GPU and CPU share memory (`MTLStorageMode.shared`), macOS has discrete GPUs (Intel Macs with AMD GPUs) where GPU and CPU have separate memory pools. This requires `MTLStorageMode.managed`.

```swift
// Detect whether shared memory is available
let useSharedMemory = device.hasUnifiedMemory  // True for Apple Silicon

let storageMode: MTLStorageMode = useSharedMemory
    ? .shared    // Apple Silicon: CPU + GPU share memory
    : .managed   // Discrete GPU: explicit synchronization needed

let buffer = device.makeBuffer(length: 4096, options: storageMode)!

// For .managed buffers: synchronize CPU writes before GPU reads
if storageMode == .managed {
    buffer.didModifyRange(0..<buffer.length)
}

// Commit to GPU
commandBuffer.addCompletedHandler { _ in
    // For .managed buffers: synchronize GPU writes before CPU reads
    if storageMode == .managed {
        // Data is now available on CPU
        let ptr = buffer.contents().assumingMemoryBound(to: Float.self)
        print("Result: \(ptr[0])")
    }
}
```

---

## Compute Kernel — Full Example

### Shader (Metal Shading Language)

```metal
// compute.metal
#include <metal_stdlib>
using namespace metal;

kernel void multiply_by_scalar(
    device const float* input [[buffer(0)]],
    device float* output [[buffer(1)]],
    constant float& scalar [[buffer(2)]],
    uint id [[thread_position_in_grid]]
) {
    output[id] = input[id] * scalar;
}
```

### Swift Host Code

```swift
import Metal

func multiplyArray(_ input: [Float], by scalar: Float) -> [Float] {
    guard let device = MTLCreateSystemDefaultDevice(),
          let library = device.makeDefaultLibrary(),
          let function = library.makeFunction(name: "multiply_by_scalar"),
          let pipeline = try? device.makeComputePipelineState(function: function),
          let commandQueue = device.makeCommandQueue()
    else { return [] }

    let count = input.count
    let inputBuffer = device.makeBuffer(
        bytes: input,
        length: MemoryLayout<Float>.stride * count,
        options: .storageModeShared
    )!

    let outputBuffer = device.makeBuffer(
        length: MemoryLayout<Float>.stride * count,
        options: .storageModeShared
    )!

    var scalar = scalar
    let scalarBuffer = device.makeBuffer(
        bytes: &scalar,
        length: MemoryLayout<Float>.stride,
        options: .storageModeShared
    )!

    guard let commandBuffer = commandQueue.makeCommandBuffer(),
          let encoder = commandBuffer.makeComputeCommandEncoder()
    else { return [] }

    encoder.setComputePipelineState(pipeline)
    encoder.setBuffer(inputBuffer, offset: 0, index: 0)
    encoder.setBuffer(outputBuffer, offset: 0, index: 1)
    encoder.setBuffer(scalarBuffer, offset: 0, index: 2)

    let threadsPerGrid = MTLSize(width: count, height: 1, depth: 1)
    let maxThreads = min(pipeline.maxTotalThreadsPerThreadgroup, count)
    let threadsPerGroup = MTLSize(width: maxThreads, height: 1, depth: 1)
    encoder.dispatchThreads(threadsPerGrid, threadsPerThreadgroup: threadsPerGroup)

    encoder.endEncoding()
    commandBuffer.commit()
    commandBuffer.waitUntilCompleted()

    let result = outputBuffer.contents()
        .assumingMemoryBound(to: Float.self)
    return Array(UnsafeBufferPointer(start: result, count: count))
}
```

---

## Rendering — `MTKView` in AppKit

`MTKView` is an `NSView` subclass (AppKit) / `UIView` subclass (UIKit) that provides a Metal-aware drawable.

```swift
import AppKit
import MetalKit

final class MetalView: MTKView {
    private var commandQueue: MTLCommandQueue!
    private var pipelineState: MTLRenderPipelineState!

    override init(frame: NSRect, device: MTLDevice?) {
        super.init(frame: frame, device: device)
        setup()
    }

    required init(coder: NSCoder) {
        super.init(coder: coder)
        setup()
    }

    private func setup() {
        guard let device = self.device else { return }

        commandQueue = device.makeCommandQueue()
        clearColor = MTLClearColor(red: 0.1, green: 0.1, blue: 0.2, alpha: 1.0)
        colorPixelFormat = .bgra8Unorm
        depthStencilPixelFormat = .depth32Float

        let library = device.makeDefaultLibrary()!
        let vertexFunction = library.makeFunction(name: "vertex_main")
        let fragmentFunction = library.makeFunction(name: "fragment_main")

        let descriptor = MTLRenderPipelineDescriptor()
        descriptor.vertexFunction = vertexFunction
        descriptor.fragmentFunction = fragmentFunction
        descriptor.colorAttachments[0].pixelFormat = colorPixelFormat
        descriptor.depthAttachmentPixelFormat = depthStencilPixelFormat

        pipelineState = try! device.makeRenderPipelineState(descriptor: descriptor)
    }

    override func draw(_ rect: NSRect) {
        guard let drawable = currentDrawable,
              let descriptor = currentRenderPassDescriptor,
              let commandBuffer = commandQueue.makeCommandBuffer(),
              let encoder = commandBuffer.makeRenderCommandEncoder(descriptor: descriptor)
        else { return }

        encoder.setRenderPipelineState(pipelineState)
        // Set vertex buffers, uniforms, textures...
        encoder.drawPrimitives(type: .triangle, vertexStart: 0, vertexCount: 3)
        encoder.endEncoding()

        commandBuffer.present(drawable)
        commandBuffer.commit()
    }
}
```

---

## Performance Profiling

| Tool | What It Profiles |
|---|---|
| **Metal System Trace** | Command buffer execution timeline, GPU utilization, shader occupancy |
| **Metal Debugger** | Frame capture, shader debugging, resource inspection |
| **GPU History** | GPU frequency, temperature, power, memory bandwidth over time |
| **Time Profiler** | CPU-side Metal API call stacks and timing |

### Key Metrics

- **GPU occupancy**: Ratio of active threads to max threads. Target > 50%.
- **Memory bandwidth**: `device.maxBufferLength` and bandwidth limited. Profile with large buffers.
- **Command buffer count**: Too many small command buffers = launch overhead. Batch draw calls.
- **Resource synchronization**: `waitUntilCompleted()` is a performance killer. Use completion handlers instead.

---

## macOS-Specific Metal Tips

1. **Use `hasUnifiedMemory`** to decide buffer storage mode. Apple Silicon uses `.shared`; discrete GPUs need `.managed`.
2. **Headless rendering** is available on macOS. Create a `MTLDevice` without a window — useful for server-side or CLI rendering tools.
3. **Multi-GPU support**: On Mac Pro, you can target specific GPUs via `MTLCopyAllDevices()`. Explicitly select the GPU you want.
4. **`CVDisplayLink`** for display-synchronized updates. Better than `CADisplayLink` for macOS because it runs on a dedicated thread.
5. **Metal-cpp** is available on macOS. Use `metal-cpp` if your project is C++ and you want to avoid the Swift/ObjC bridge.
