# Testing Matrix — Unit, Widget, Integration

## The Pyramid for Flutter

| Layer | Tool | Scope | Run where |
|-------|------|-------|-----------|
| Unit | `test` package | Models, repositories (with fakes), pure logic | CI, fast |
| Widget | `flutter_test` | Widget render, interaction, providers/blocs | CI, fast |
| Integration | `integration_test` | Full app flows on devices/emulators | CI device farm + pre-release |

## Rules

1. **Integration tests on both platforms** — a release that only passed on one platform is not tested (Ground Rule R6).
2. **Oldest supported OS** — test the lowest OS you support.
3. **No skipped tests in the release path** — a skipped test counts as a failure.
4. **Fake the boundaries, not the logic** — fake repositories/network (not your own logic); never hit live APIs in tests.
5. **Deterministic time** — fake clocks and timers; never real sleeps.

## Widget Test Patterns

```dart
testWidgets('shows user name', (tester) async {
  await tester.pumpWidget(ProviderScope(overrides: [...], child: const App()));
  expect(find.text('Alice'), findsOneWidget);
});
```

- Override providers with fakes via `ProviderScope(overrides:)` (Riverpod) or mock blocs.
- Use `tester.pumpAndSettle()` carefully (infinite animations hang it); prefer bounded pumps.

## Integration Test Patterns

```dart
IntegrationTestWidgetsFlutterBinding.ensureInitialized();
testWidgets('login flow', (tester) async {
  await app.main();
  await tester.pumpAndSettle();
  await tester.enterText(find.byKey(const Key('email')), 'a@b.com');
  ...
});
```

- Run with `flutter test integration_test -d <device>` on each platform in CI.
- Mock the network at the integration level (mock server) or use a test environment.

## Release Gate

- [ ] `flutter analyze` clean
- [ ] Unit + widget tests green
- [ ] Integration tests green on both platforms
- [ ] Oldest supported OS covered
- [ ] Zero skipped tests
