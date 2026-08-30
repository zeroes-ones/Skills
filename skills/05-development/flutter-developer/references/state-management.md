# State Management — Riverpod, Bloc, Provider

## The Decision Rule

| Stack | Best for | Why |
|-------|----------|-----|
| **Riverpod** | Most apps (1 team) | Compile-safe providers, automatic rebuild scoping, scales up and down; testable without mocking globals |
| **Bloc** | Large apps, many teams | Strict Event→State discipline, predictable transitions, strong testability, team conventions |
| **Provider** | Small apps / legacy | Simple InheritedWidget wrapper; fine for small scope, weaker rebuild control |

## Rebuild-Scope Discipline (The Core Skill)

- **Selectors / watch granularity** — providers that expose narrow values cause fewer rebuilds than whole-object providers.
- **const widgets** — a const child never rebuilds; split screens so only the changing subtree rebuilds.
- **RepaintBoundary** — isolate expensive paint areas (maps, videos) from the rest of the tree.
- **Never read a provider in build() for data you can pass down** — prefer explicit constructor params for immutable data.

## Riverpod Patterns

```dart
final userProvider = FutureProvider<User>((ref) => repository.fetchUser());
final themeProvider = StateProvider<ThemeMode>((ref) => ThemeMode.system);
```

- `ref.watch` in build for reactive values; `ref.read` in event handlers.
- `FutureProvider`/`StreamProvider` handle async state (loading/error/data) without manual states.

## Bloc Patterns

- Event → `mapEventToState`/`on<Event>` → State. One Bloc per feature.
- Test with `blocTest`: emit events, assert states.
- Keep Blocs pure of widgets; UI listens via `BlocBuilder`/`BlocSelector`.

## Anti-Patterns

- **Everything in one global store** — split by feature/domain.
- **State in the widget tree that three screens need** — lift to a provider/bloc.
- **Rebuilding whole screens on a single toggle** — narrow the watch scope.
- **No dispose discipline** — every StreamSubscription/controller must be disposed (or managed by the framework/provider lifecycle).

## Migration Path

Legacy Provider → Riverpod can migrate module-by-module; legacy setState → lift to a provider incrementally. Never rewrite all at once.
