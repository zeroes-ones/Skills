# Native Modules — TurboModules, Config Plugins, Interop

## Three Ways to Add Native Code

| Approach | When | How |
|----------|------|-----|
| **Expo config plugin** (`app.plugin.js`) | On Expo; the need maps to an existing native module that needs config | Write a plugin that modifies the native project during prebuild; keeps managed workflow |
| **TurboModule** (New Arch) | Bare; a new native capability | Kotlin/Swift module with codegen-generated typed interface; lazy-loaded |
| **Legacy module / interop** | Bare, pre-migration | Classic `RCTBridgeModule`; works via the interop layer under New Arch |

## TurboModule Rules

1. **Lazy load** — TurboModules initialize on first use; don't force-init at launch.
2. **Typed interface via codegen** — define the spec (`.ts` or native spec), codegen generates the glue; never hand-write the bridge glue.
3. **No blocking synchronous calls on the JS thread** — expensive native work returns promises or callbacks.
4. **Thread correctness** — run work on the right queue; never touch UI state off the main thread.
5. **Memory** — release native resources; no leaks in the module lifecycle.

## Config Plugin Pattern (Expo)

```js
// app.plugin.js
const { withAndroidManifest, withInfoPlist } = require('expo/config-plugins');
module.exports = function withMySdk(config, props) {
  config = withInfoPlist(config, (c) => {
    c.modResults.NSFaceIDUsageDescription = props.faceIdDescription || 'Use Face ID';
    return c;
  });
  return config;
};
```

Verify with a clean `npx expo prebuild` and a dev-client build — the plugin must be idempotent (safe to run repeatedly).

## Interop Contract (New Architecture)

Document for every native module: platform(s), lazy-load behavior, threading model, error surface, and version compat with the New Architecture. This contract is what lets OTA updates and native builds move independently without crashes (Error Decoder row 1).

## Common Failure Modes

- **Plugin not idempotent** — prebuild runs multiple times; plugins that append duplicates break builds.
- **Sync native call on JS thread** — jank or ANRs on Android.
- **Missing interop for legacy views** — Fabric can't render Paper views without the interop layer.
- **Module in Expo Go** — Expo Go only ships the Expo module set; test in a dev client.
