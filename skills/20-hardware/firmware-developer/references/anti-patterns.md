# Anti-Patterns

<!-- QUICK: 30s -- machine-detectable anti-patterns with auto-prevention -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep/lint) | 🛡️ Auto-Prevent |
|---|---|---|---|
| Committing generated code (pin mux, clock config) without review | Generated code goes through same PR review; reviewers verify against datasheet | `grep -l "generated.by\|auto.generated\|CubeMX" src/** && grep -L "reviewed:" src/**` | WARN. Require "Reviewed-by:" comment in generated files before merge. |
| Using `volatile` defensively on every shared variable | Only for MMIO registers, ISR-modified variables, DMA descriptors | `grep -rn "volatile" src/*.[ch] | grep -v "MMIO\|ISR\|DMA\|hardware.reg" | wc -l` > 10 | WARN. Flag and require justification for each non-MMIO/ISR/DMA volatile. |
| Removing assertions from release builds to "save flash" | Keep assertions: 200-byte assert handler with file+line+reset reason | `grep -L "configASSERT\|assert\|NDEBUG" build/*release*` | STOP. Assertion handler MUST be present in release. Auto-inject assert handler if missing. |
| Linking against newlib without understanding heap pull-in | Audit linker map diff after every dependency change | `arm-none-eabi-nm --size-sort build/firmware.elf | grep -E "_sbrk\|malloc\|__aeabi_"` | WARN. Post linker map diff in CI. Block merge if `.heap` grows >1KB without justification. |
| Shipping firmware without versioned flash layout | Magic number + version at known offset (0x0800F000); bootloader checks compatibility | `grep -L "flash.layout\|magic.*0x\|layout.*version\|FLASH_LAYOUT" bootloader/src/*` | STOP. Auto-inject magic number and layout version into flash layout header. |
| Trusting compiler to optimize away unused code without verification | Post `arm-none-eabi-nm --size-sort` diff in every CI run | `arm-none-eabi-nm --size-sort build/*.elf | grep -E "__weak\|WEAK"` AND no CI diff check | WARN. Auto-post nm diff on every PR. Flag any symbol >1KB without corresponding source change. |
| Building firmware without reproducible build verification | CI must produce bit-identical `.bin` from same commit | `diff <(sha256sum build/output.bin) <(sha256sum build-verify/output.bin)` != 0 | STOP. Non-reproducible = cannot ship. Auto-check for `__DATE__`, `__TIME__`, random seeds, build path embedding. |
| Deploying OTA to entire fleet simultaneously | Staged: 1%→5%→25%→100% with auto-halt on elevated crash rate | `grep -q "100%\|entire.fleet\|all.devices" deploy/ota-config*` AND NOT `grep -q "1%\|5%\|staged\|canary" deploy/ota-config*` | STOP. Auto-inject staged rollout config. Block 100% deployment without canary monitoring. |
