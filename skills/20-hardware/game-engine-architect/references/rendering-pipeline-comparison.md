# Rendering Pipeline Comparison

<!-- QUICK: 30s — pipeline selection with concrete G-Buffer layouts and bandwidth budgets -->

## Forward Rendering
- **How it works:** Single pass per object → vertex shader → fragment shader outputs final color directly to framebuffer. Lighting calculated in fragment shader.
- **G-Buffer:** None. Direct output to render target.
- **Bandwidth:** ~32 bytes/pixel (RGBA8 color + D24S8 depth). Lowest of all pipelines.
- **MSAA:** Native support via hardware resolve. Cheap: 4x MSAA = 4x color samples, not 4x shading cost.
- **Transparency:** Sorted back-to-front, rendered in same pass. No separate pass needed.
- **Best for:** Mobile (tile-based deferred GPUs), VR (low latency), transparency-heavy scenes, <10 dynamic lights.
- **Worst for:** >50 dynamic lights (light calculation per fragment per light), many overdraw layers.

## Deferred Rendering
- **How it works:** Geometry pass → G-Buffer (MRT). Lighting pass → fullscreen quad reads G-Buffer, computes lighting.
- **G-Buffer:** `Albedo(RGB8) + Normal(RG16_SNORM) + Roughness/Metalness/AO(R8G8B8) + Depth(D24S8)` = ~28 bytes/pixel compressed, ~48 bytes/pixel uncompressed.
- **Bandwidth:** HIGH. MRT write in geometry pass, readback in lighting pass. 2x bandwidth of forward.
- **MSAA:** Not directly supported on G-Buffer. Use TAA (Temporal Anti-Aliasing) or MSAA resolve before G-Buffer (wasteful).
- **Transparency:** Requires separate forward pass. All transparent objects rendered after lighting, blended front-to-back.
- **Best for:** >100 dynamic lights, PC/console with discrete GPU, scenes without heavy transparency.
- **Worst for:** Mobile (tile memory limited), MSAA requirement, transparency-heavy scenes.

## Clustered Forward (Forward+)
- **How it works:** Depth prepass → compute shader builds light grid (frustum subdivided into 3D clusters) → forward pass reads light list per cluster, shades with only relevant lights.
- **G-Buffer:** Depth-only prepass (D24S8 = 4 bytes/pixel). Light grid in structured buffer (GPU resident).
- **Bandwidth:** Medium. Depth prepass write + forward pass read. No full G-Buffer.
- **MSAA:** Supported (forward pass with hardware MSAA).
- **Transparency:** Same pass as opaque (forward pass). Light grid applies to transparent objects too.
- **Best for:** 50-256 dynamic lights, balance of quality + bandwidth, Unity URP Forward+, mid-range GPUs.
- **Worst for:** >500 lights (cluster resolution insufficient), mobile (compute shader overhead).

## PBR: Cook-Torrance BRDF
```
F = F0 + (1.0 - F0) * pow(1.0 - max(dot(N, H), 0.0), 5.0)   // Fresnel (Schlick)
D = a2 / (PI * pow(max(dot(N, H), 0.0) * max(dot(N, H), 0.0) * (a2 - 1.0) + 1.0, 2.0))  // NDF (GGX)
G = G1(NdotV) * G1(NdotL)   // Geometry (Schlick-GGX)
  where G1(x) = x / (x * (1.0 - k) + k), k = (roughness + 1)^2 / 8
```
- **IBL (Image-Based Lighting):** Pre-filtered environment map at roughness mip levels. BRDF LUT (2D texture) for split-sum approximation.
- **Validation:** Compare against Disney BRDF Explorer. Perceptual error <2% on Macbeth chart.

## Ray Tracing Integration
- **Hybrid:** Rasterize G-Buffer → ray trace reflections/GI/AO → composite with rasterized result.
- **Full path tracing:** Cyberpunk 2077 RT Overdrive, Alan Wake 2. Not yet feasible at 60 FPS on console.
- **Denoising:** NRD (NVIDIA Real-Time Denoiser), Intel Open Image Denoise, FSR 3.1 denoiser.
