# Shader Optimization Techniques

## HLSL/GLSL Best Practices
- **Use `half`/`min16float` precision** for colors, normals, UVs. Full `float` only for positions and accumulators
- **Avoid dynamic branching on uniform divergence** — use `[branch]` attribute only when branch is coherent across wavefront
- **Prefer `mad()` over `a * b + c`** — single FMA instruction vs multiply + add
- **Pack G-Buffer:** Normal RG16_SNORM (4 bytes), albedo RGB10A2 (4 bytes), roughness/metalness R8G8 (2 bytes)

## Compute Shaders
- **Workgroup size:** 64 (AMD), 32 (NVIDIA), 256 (Apple Silicon). Tune per platform
- **Shared memory:** Use `groupshared` for wavefront-wide reductions. Max 32KB on most GPUs
- **Barriers:** `GroupMemoryBarrierWithGroupSync()` between read-after-write in same workgroup
- **Indirect draw:** GPU-driven rendering — compute writes to indirect draw buffer, render pass consumes it

## Unity Shader Graph
- **Custom Function nodes** for math-heavy operations (single function call vs graph traversal)
- **Keywords vs variants:** Each keyword multiplies shader variants. 5 keywords = 32 variants. Use static branching for quality toggles
- **ShaderVariantCollection:** Pre-warm all variants at loading screen. Ship with build

## Unreal Material Editor
- **Material Functions** for reusable logic. Avoid deep function nesting (>3 levels)
- **Quality Switch node** for platform-specific optimizations (low/medium/high/epic)
- **PSO caching:** `r.ShaderPipelineCache.Enabled=1`, `.upipelinecache` file pre-baked from gameplay coverage

## SPIR-V Cross-Compilation (wgpu)
- **Source:** HLSL/GLSL → `glslangValidator`/`dxc -spirv` → SPIR-V → `spirv-cross` → target backend
- **wgpu 0.19+:** Accepts SPIR-V directly via `wgpu::ShaderModuleDescriptorSpirV`
- **Reflection:** `spirv-cross --reflect` for descriptor set layout generation
