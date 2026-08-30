# Version Matrix Reference — RN/Expo/Hermes Compatibility

> `[VERIFIED 2026-08]` — verify against the installed packages at research time (RP1). RN ships monthly; Expo SDKs ship ~quarterly.

## The Compatibility Contract

- **RN core ↔ native templates** must upgrade together (a partial upgrade yields launch-time "version mismatch").
- **Expo SDK ↔ RN core** are pinned: each Expo SDK targets a specific RN version. Use `npx expo install` to keep aligned.
- **Native dependencies** must be compatible with the Expo SDK's native version — `npx expo install --check` surfaces drift.
- **New Architecture** is default in modern RN; libraries must declare New-Arch compatibility or use the interop layer.

## Commands That Anchor You

```bash
npx expo install --check        # Expo: surface version drift
npx expo install --fix          # Expo: align versions
npx react-native config         # bare: dump native config
npx react-native info           # environment + versions
npx expo-doctor                 # Expo: health check
```

## Upgrade Protocol

1. Read the release notes / upgrade guide for the target version (breaking changes, deprecations).
2. Upgrade RN core + native templates + libraries as one unit (never RN alone).
3. Run `expo-doctor` / `install --check`; fix drift before building.
4. Build both platforms; run the E2E matrix.
5. Roll back path: keep the previous lockfile; a failed upgrade reverts cleanly.

## Rules That Save Builds

- **Never `latest` in production** — pin every RN-adjacent dependency; `latest` breaks future builds.
- **One source of truth** — package.json + lockfile are the contract; never hand-edit node_modules.
- **Verify after any install** — `npx expo install --check` after adding a library; a mismatch breaks prebuild.

## Hermes Notes

- Hermes is the default engine; its bytecode is smaller and starts faster than JSC.
- Hermes semantics differ slightly (e.g., `Intl`, proxies, debugger); test on Hermes, not JSC.
- Keep Hermes enabled for production; only disable it for specific debugging.
