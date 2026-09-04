# Additional Resources — on-device-ai-engineer

> Deep knowledge loaded on demand. Deployment-surface matrix, runtimes, and reference material.

## Deployment Surface Matrix

| Surface | Typical runtimes | Memory reality | Delivery | Watch-outs |
|---------|------------------|----------------|----------|-----------|
| Mobile (iOS) | CoreML, llama.cpp, ExecuTorch | App-usable RAM 2-5GB typical; ANE offload | App bundle + on-demand download | ANE op support varies; thermal on sustained gen |
| Mobile (Android) | ExecuTorch, llama.cpp (JNI), Google AI Edge, TFLite, MediaPipe | 2-6GB usable; StrongBox for keys not models | APK/AAB + download | Device fragmentation; battery |
| Desktop app (packaged) | Ollama embedded, llama.cpp | 8-64GB; GPU optional | Ship runtime; download model on first run | Multi-arch (Apple Silicon/Intel/ARM Win); GPU drivers |
| In-browser | WebLLM, transformers.js, ONNX Runtime Web, llama.cpp/WASM | Browser tab budget; WebGPU vs WASM fallback | Model fetched to Cache API/OPFS | WebGPU support gate; no guaranteed persistence; cold-start download |
| Self-hosted backend/edge | vLLM, TGI, llama.cpp server, Ollama, ONNX Runtime | VRAM per GPU; KV cache grows with concurrency | Container/image + model registry | Concurrency & batching; multi-tenant isolation; GPU ops |
| Embedded | ExecuTorch, TFLite Micro, MediaPipe | KBs-MBs | Flashed/firmware | Fixed ops; no dynamic shapes |

## Quantization Cheat-Sheet

| Format | Typical use | Size effect | Notes |
|--------|-------------|-------------|-------|
| fp16 | Desktop/server GPU, quality-first | 2 bytes/param | Baseline to compare against |
| int8 (W8A8) | Server throughput, mobile vision | 1 byte/param | Good accuracy; needs int8 kernels |
| Q4_K_M / Q5_K_M (llama.cpp) | Mobile/desktop LLM sweet spot | ~0.55-0.65 bytes/param | GGUF; the practical phone choice |
| Q3_K / Q2_K | Tiny/embedded or desperate fits | ~0.4 bytes/param | Visible quality loss — eval before shipping |
| int4 (GPTQ/AWQ) | Server GPU LLM | ~0.6 bytes/param | Batch-friendly; needs calibration set |

Rule of thumb: memory ≈ params × bytes-per-param + runtime overhead + KV cache. Always add 20-30% headroom and measure peak RSS/VRAM on the real target.

## In-Browser AI (WebGPU/WASM)

- **When it wins:** no install, instant shareability, data never leaves the machine, works offline after first load (cached), privacy story is maximal.
- **When it loses:** model size (users won't download 4GB into a browser), cold-start latency, WebGPU support gaps (older Safari/Edge variants), no guaranteed storage persistence, background execution limits.
- **Stack:** WebLLM (chat LLMs, WebGPU), transformers.js (Hugging Face models, WASM/WebGPU), ONNX Runtime Web, llama.cpp WASM builds. Download to OPFS/Cache API; check `navigator.gpu` and fall back to WASM or cloud.
- **Security note:** the model and weights are fully client-side — anyone can extract them. Don't put proprietary weights in a browser. Treat in-browser as "the user owns the model" by design.

## Self-Hosted Backend (your infra, not a third-party API)

- **When it wins:** data-residency/on-prem requirements, per-token cost control at high volume, no rate limits, full observability, model choice freedom.
- **When it loses:** you own GPU ops, capacity planning, upgrades, and pager duty. Total cost beats an API only past a usage threshold — model it before committing.
- **Serving:** vLLM (throughput, PagedAttention), TGI, llama.cpp server, Ollama (easy start), ONNX Runtime. Batch + continuous batching for throughput; keep KV cache headroom for concurrency.
- **Security note:** self-hosted is not automatically private — the data stays on your infra, but you still own access control, logging, and compliance for it. Route to backend-developer/security-reviewer for the serving layer.

## War Stories

- **The flagship-only model:** A team shipped one 8B model to every Android device; the mid-tier phones OOM-killed the app within a week of release. Fix: tier models by device class (8B flagship / 3B mid / task models low-end) with a device-capability check at install. Lesson: one model for every device punishes the low end and wastes the flagship.
- **The "private" browser AI with a cloud fallback leak:** A WebGPU feature fell back to a cloud API on unsupported browsers — without telling the user or the privacy review. The fallback sent prompts to a third party. Fix: consent-gated fallback with explicit disclosure. Lesson: a fallback path is part of the privacy architecture; audit every route data can take.
- **The self-hosted cost surprise:** A team moved to vLLM to "save money" and discovered GPU reservation costs exceeded the API bill below ~1M tokens/day. Fix: model the break-even before migrating; keep hybrid routing. Lesson: self-hosting wins on data control and marginal cost, not on low usage — the total-cost model decides.
- **The unquantized desktop deployment:** A desktop app shipped an fp16 7B model — 14GB download, 30s cold start, and users on 8GB laptops swapped to swap. Fix: Q4_K_M (~4GB), download-on-first-run with progress. Lesson: desktop has more RAM than a phone, but "more" is not "unlimited" — budget and measure per surface.

## Reference Material

- llama.cpp / Ollama docs — quantization formats (GGUF), server modes
- WebLLM / transformers.js / ONNX Runtime Web docs — WebGPU support matrix and fallbacks
- vLLM / TGI docs — continuous batching, quantization (GPTQ/AWQ), serving patterns
- CoreML / ExecuTorch / TFLite / MediaPipe docs — per-platform operator and quantization support
- MLPerf / LLM-perf harnesses — reproducible on-device measurement
