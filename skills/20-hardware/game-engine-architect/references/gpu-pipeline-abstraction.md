# GPU Pipeline Abstraction

## wgpu (WebGPU Native) 0.19+
- **Cross-platform:** D3D12 (Windows), Vulkan (Linux/Android), Metal (macOS/iOS), OpenGL (fallback)
- **Shader:** SPIR-V input, compiled via naga or SPIRV-Cross to backend
- **Descriptor sets:** `wgpu::BindGroupLayout` → `wgpu::BindGroup` → bind at `wgpu::RenderPass::set_bind_group()`
- **Strengths:** Safe by default (validation layer), Rust-native, browser-compatible (WebGPU)
- **Weaknesses:** Performance gap vs native APIs (5-15%), limited indirect draw support, no mesh shaders yet

## Vulkan
- **Pipeline:** `VkGraphicsPipelineCreateInfo` with `VkPipelineCache` for serialization
- **Descriptor sets:** `VkDescriptorSetLayout` → pool → `vkAllocateDescriptorSets`. Use `VK_DESCRIPTOR_TYPE_DYNAMIC_UNIFORM_BUFFER` for per-draw data
- **Synchronization:** `VkSemaphore` (GPU-GPU), `VkFence` (GPU-CPU). Pipeline barriers: image layout transitions, buffer ownership
- **Ray tracing:** `VK_KHR_ray_tracing_pipeline` with acceleration structures

## Metal 3
- **Pipeline:** `MTLRenderPipelineState` from `MTLRenderPipelineDescriptor`. PSO caching via `MTLBinaryArchive`
- **Heap:** `MTLHeap` for sub-allocation (reduces resource creation overhead)
- **Argument buffers:** Encoded descriptor sets. Bind via `setFragmentBuffer:offset:atIndex:`
- **Ray tracing:** `MTLAccelerationStructure` + `MTLIntersectionFunctionTable` (M3+)

## DirectX 12
- **Pipeline:** `ID3D12PipelineState` from `D3D12_GRAPHICS_PIPELINE_STATE_DESC`. PSO caching via `ID3D12PipelineLibrary`
- **Descriptor heaps:** `ID3D12DescriptorHeap` (CBV/SRV/UAV or Sampler). Bind via `SetGraphicsRootDescriptorTable()`
- **Ray tracing:** DXR 1.1 with `ID3D12StateObjectProperties`. Agility SDK for latest features
- **PIX:** GPU captures, timing, occupancy analysis

## Descriptor Set Layout Optimization
- **Frequency-based:** Frame-level (camera, lights) → Pass-level (shadow map, G-Buffer) → Material-level (textures) → Draw-level (transform)
- **Bindless:** `VK_EXT_descriptor_indexing` / D3D12 Resource Binding Tier 3. Single descriptor set for all textures
- **D3D12:** Root signature = Vulkan pipeline layout. Keep root parameters < 13 DWORDs for fast path
