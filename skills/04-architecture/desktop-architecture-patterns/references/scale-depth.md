# Scale Depth: Solo → Small → Medium → Enterprise

### Solo
Single developer, single platform (Electron/Tauri), manual testing on one OS. Focus: proof of concept, core functionality, basic window management. Skip: multi-window architecture, auto-update infrastructure, comprehensive cross-platform testing. Coordination: with system architect on backend API contracts.

### Small Team
Small engineering team, 2-3 target platforms, CI/CD pipeline. Focus: production-quality IPC, auto-update pipeline, cross-platform testing on real hardware. Coordination: with desktop developer on architecture ergonomics, with security reviewer on sandboxing and CSP, with DevOps on installer and code signing.

### Medium Team
Cross-functional desktop team, multi-window architecture, enterprise deployment. Focus: platform abstraction layer, DPI-aware UI at all scaling levels, crash recovery and graceful degradation, installer/uninstaller design for IT-managed deployments. Coordination: with QA on E2E testing matrix, with release manager on staged rollouts, with security engineer on certificate pinning and threat model.

### Enterprise
Multi-product desktop platform, global distribution, IT-managed enterprise deployment (MSI/DMG with Group Policy/MDM). Focus: security sandboxing at scale, offline-first with conflict resolution, accessibility compliance (WCAG 2.1 AA), telemetry with privacy-preserving design, zero-downtime updates for mission-critical applications. Coordination: with compliance officer on data residency, with platform engineering on deployment infrastructure, with incident response on crash monitoring and forensic readiness.

### Transition Triggers
| From → To | Trigger |
|-----------|---------|
| Solo → Small | First external beta users; need auto-update to push fixes; >1 target platform |
| Small → Medium | >10K active users; enterprise customer requires MSI deployment; multi-window feature request |
| Medium → Enterprise | Operating in regulated industry (finance/healthcare); >100K active users; IT-managed deployment requirement |
