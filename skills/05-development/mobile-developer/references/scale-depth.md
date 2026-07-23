# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Mobile = React Native with Expo (managed workflow). No native code. One codebase for iOS + Android. Auth = Firebase Auth or Supabase Auth. Deploy via EAS Build. No CI/CD beyond Expo. Manual testing on one device.
- **What to skip**: Native development (Swift/Kotlin). Custom native modules. Offline-first. Feature flags. CodePush/OTA updates. Performance profiling. Detox/Maestro E2E tests. Multi-device testing.
- **Coordination**: You own mobile + backend. Ship to TestFlight manually.

### Small Team (2-10 people, 100-10K users)
- **What changes**: React Native with Expo (managed or bare). TypeScript. CI/CD with EAS Build. Basic offline support (cached API responses). Push notifications (FCM + APNs). Crash reporting (Sentry). Testing on 2-3 devices (low-end + high-end). Platform-specific styling where needed.
- **What to skip**: Native modules. Offline-first with sync. E2E tests (Detox/Maestro). Performance budgets in CI. Root/jailbreak detection. Certificate pinning.
- **Coordination**: PR review with another mobile dev. API contract sync with backend. Bi-weekly mobile sync.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: React Native with native modules where needed. Offline-first with sync for critical flows. E2E tests (Maestro/Detox) on CI. Performance budgets (cold start < 2s, 60fps). Biometric auth. Secure storage (Keychain/Keystore). Multi-device test matrix (5+ devices). OTA updates (CodePush/EAS Update). Feature flags.
- **What to skip**: Full native development (Swift/Kotlin). Custom rendering engine. Advanced animations library (use Reanimated). Multi-platform beyond iOS + Android.
- **Coordination**: Weekly mobile guild. Bi-weekly design review. Monthly performance audit. Pre-release regression pass.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Native development teams (Swift + Kotlin) + cross-platform team. Full offline-first architecture with conflict resolution. Certificate pinning + root/jailbreak detection + code obfuscation. Performance monitoring (cold start, scroll FPS, memory). Advanced CI/CD with automated store submission. A/B testing. Feature flags for gradual rollout. Accessibility testing (VoiceOver/TalkBack). Internationalization (RTL, locale-specific formats).
- **What's full production**: Mobile platform team. Mobile reliability engineering. Store review management. Beta program (TestFlight + Play Console). Cross-platform component library. App performance observability.
- **Coordination**: Mobile platform team weekly. Cross-platform design system council monthly. App store release coordination. Quarterly mobile strategy review.

### Transition Triggers
- **Solo → Small**: Second mobile developer. User complaints about performance or crashes.
- **Small → Medium**: Offline support needed. Performance becomes critical (cold start > 2s). >10K installs.
- **Medium → Enterprise**: Multi-platform team split. Store review rejections need process. >100K installs.
