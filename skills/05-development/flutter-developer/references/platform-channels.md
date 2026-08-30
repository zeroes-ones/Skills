# Platform Channels — Pigeon, Threading, Error Handling

## The Contract Mindset

Every call across the Dart↔native boundary is an async contract: a method name, a typed payload, a result (or error), and a defined threading model. Treat it like a mini-API.

## Pigeon (Recommended)

`pigeon` generates the typed glue from a single definition file — eliminating stringly-typed channel names and the "MissingPluginException" class of bugs.

```dart
// channel.dart (pigeon definition)
@HostApi()
abstract class BiometricApi {
  Future<bool> canAuthenticate();
}
```

Run `dart run pigeon --input channel.dart --dart_out lib/... --swift_out ios/... --kotlin_out android/...`. Both sides get compile-checked typed methods.

## Threading Rules

- **Dart side:** channel calls are async — never block the UI isolate waiting for a result.
- **Native side (Android):** `MethodChannel` handlers run on the main thread; move heavy work to a background thread, then invoke the result on the main thread.
- **Native side (iOS):** handlers run on the main thread; use `DispatchQueue` for heavy work, return on the main queue.

## Error Handling

- Every call has a try/catch (Dart) and a `PlatformException` surface (native).
- Never let a native exception escape as a crash — convert to a `PlatformException` and handle it in Dart.
- Add timeouts for calls that could hang (biometrics, hardware).

## Serialization

- Data crossing the boundary must be JSON-serializable (maps, lists, primitives).
- Pass IDs, not objects — the native side fetches what it needs.
- Large payloads: chunk or stream; a 10MB JSON over a channel blocks and copies memory.

## Common Failure Modes

| Failure | Fix |
|---------|-----|
| MissingPluginException | Channel name/signature mismatch; plugin not registered; stale build (`flutter clean`) |
| Hang | Native side blocked the main thread or never invoked the result |
| Data corruption | Non-serializable object passed (e.g., a DateTime, not a string) |
| Main-thread ANR | Native work ran on the main thread; move to a background queue |
