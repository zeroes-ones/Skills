---
name: firmware-developer
description: "Firmware development & low-level software: boot flow design (ROM→bootloader→kernel→app), device drivers (DMA, interrupt handlers, MMIO), BSP creation, build systems (CMake+GCC/LLVM, linker scripts), OTA infrastructure (delta updates, rollback, signing), HAL design, secure element integration, factory test firmware, firmware CI/CD, and field debugging. Trigger: firmware, bootloader, BSP, HAL, OTA, linker script, toolchain, cross-compile, DFU, secure element."
author: Sandeep Kumar Penchala
type: hardware
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - firmware-developer
  - hardware
  - bootloader
  - ota
  - hal
token_budget: 3500
dependencies:
  tools: [arm-none-eabi-gcc, cmake, docker, openocd, pyocd]
  packages: [python3, pyserial, imgtool]
  permissions: []
output:
  type: "binary+config"
  path_hint: "firmware/build/"
chain:
  consumes_from: ["embedded-engineer", "hardware-architect"]
  feeds_into: ["qa-engineer", "devops-engineer", "security-engineer"]
  alternatives: ["embedded-engineer"]
---
# Firmware Developer

Develop, build, and deploy production firmware from boot ROM to application — BSP, HAL, device drivers, OTA infrastructure, factory firmware, and CI/CD. Firmware is software that cannot be hot-patched. A bug deployed to 100K field devices is a physical recall costing millions. Treat every commit as irreversible.

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->
```
What are you trying to do?
├── BUILD firmware infrastructure
│   ├── Set up CMake + GCC/LLVM toolchain → "Core Workflow" Phase 1
│   ├── Design linker script & memory map → "Core Workflow" Phase 1
│   ├── Create Board Support Package (BSP) → "Core Workflow" Phase 2
│   └── Cross-compilation in containers → references/build-system-design.md
├── WRITE firmware code
│   ├── Device driver (SPI/I2C/UART/CAN/USB) → "Core Workflow" Phase 2
│   ├── DMA + interrupt handler design → references/device-driver-patterns.md
│   ├── HAL (Hardware Abstraction Layer) → "Decision Trees > HAL vs Direct Register"
│   └── Boot flow design → "Core Workflow" Phase 3
├── DEPLOY or update
│   ├── OTA update infrastructure → "Core Workflow" Phase 4
│   ├── Delta update design → references/ota-infrastructure.md
│   ├── Rollback protection → "Decision Trees > OTA Rollout Strategy"
│   └── Artifact signing pipeline → references/ota-infrastructure.md
├── TEST or debug
│   ├── Manufacturing test firmware → "Core Workflow" Phase 5
│   ├── Firmware CI/CD pipeline → "Core Workflow" Phase 6
│   ├── Field crash dump analysis → "Error Decoder"
│   └── Remote log retrieval → references/field-debugging.md
└── Not sure? → Describe the MCU, RTOS, and connectivity requirements
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- QUICK: 30s — these rules apply to every response -->
<!-- STANDARD: 3min — firmware failures are physical and irreversible -->

- **Never ship firmware without a rollback path.** Every OTA must include: (a) A/B partition with verified boot, (b) auto-revert after N failed boots, (c) hardware recovery mode (ROM bootloader, serial DFU) that works even if the bootloader is dead. SWD-only recovery = time bomb.
- **The linker script is not boilerplate.** Memory layout bugs produce the hardest failures: `.data` overflows into `.bss`, stack collides with heap, ISR vector at wrong offset. Review the linker script line by line with `arm-none-eabi-objdump -h` output. This is your most important code review.
- **Never use `-O0` in production.** Unoptimized firmware is 3-5× larger and slower. But `-O2`/`-Os` can eliminate delay loops, reorder MMIO accesses, optimize away `volatile` reads. Every release must pass tests at BOTH `-Os` AND `-O2`. Regression at optimization level is always a missing `volatile` or memory barrier.
- **Build reproducibility is a requirement, not a luxury.** Same commit + same toolchain + same flags = bit-identical binary. Without this, you cannot audit what's in the field. Pin compiler version, commit `.cmake` config, store artifacts with git SHA in filename.
- **Admit when the problem is hardware.** A driver that "sometimes misses interrupts" after 3 weeks is probably a hardware issue: floating IRQ line, insufficient decoupling, ground bounce. Escalate to embedded-engineer with scope traces, not another driver rewrite. You are not debugging code — you are debugging physics.

<!-- DEEP: 10+min — war story -->
*Smart lock company pushed a firmware update to 100% of 40K-unit fleet simultaneously. The update added a security handshake that was 200ms slower. This coincided with the BLE connection interval, creating a race condition that locked users out. By the time they halted, 40K locks were bricked. Fix: physical recall with SWD reflash at dealer locations. Cost: $2.3M. Lesson: staged rollout with boot-success-rate monitoring catches this at 1%.*

## When to Use
<!-- QUICK: 30s — scan bullets to decide if this skill fits -->
- Designing boot flow: ROM → first-stage bootloader → second-stage bootloader → kernel/RTOS → application
- Writing device drivers: character, block, network with DMA, interrupt handlers, MMIO access patterns, timeout handling
- Creating and maintaining Board Support Packages (BSP) for custom PCBs with pinmux, clock config, power sequencing
- Setting up firmware build systems: CMake + GCC/LLVM toolchains, linker scripts, reproducible builds, memory maps
- Building OTA/firmware update infrastructure: delta updates with bsdiff/hdiffpatch, rollback protection, staged rollouts (1%→5%→25%→100%), artifact signing with Ed25519
- Implementing logging and telemetry for constrained devices: binary protocols (<4KB flash), CBOR/MessagePack (>4KB), buffered upload, heatshrink compression
- Developing manufacturing test firmware: factory test modes, calibration routines, device serialization, <60s test time
- Designing Hardware Abstraction Layers (HAL) that isolate application code from vendor SDKs and enable multi-vendor sourcing
- Integrating secure elements (ATECC608, TPM 2.0, STSAFE, nRF secure immutable bootloader) for key storage and attestation
- Setting up firmware CI/CD: cross-compilation in Docker containers, emulator testing, HIL automation on real hardware
- Field debugging: remote log retrieval via BLE/WiFi, crash dump analysis (Cortex-M fault registers), fleet health dashboards

## Decision Trees
<!-- QUICK: 30s — follow the ASCII tree to your scenario -->
<!-- STANDARD: 3min — concrete tradeoffs, not abstract advice -->

### HAL vs Direct Register Access

```
                          ┌──────────────────────────────┐
                          │ START: Writing peripheral     │
                          │ driver code                   │
                          └────────────┬─────────────────┘
                                       │
                         ┌─────────────▼─────────────────┐
                         │ Will firmware ever run on a    │
                         │ different MCU family?          │
                         └────┬────────────────────┬─────┘
                              │ YES                │ NO
                    ┌─────────▼──────┐    ┌────────▼──────────┐
                    │ HAL required    │    │ Volume >100K       │
                    │ (vendor SDK or  │    │ units?             │
                    │ custom HAL)     │    └───┬──────────┬─────┘
                    └────┬───────────┘        │ YES      │ NO
                         │             ┌──────▼────┐ ┌──▼──────────┐
              ┌──────────▼──────────┐  │ Custom HAL │ │ Direct       │
              │ Zephyr: Devicetree   │  │ recommended│ │ register OK  │
              │ + driver model       │  │            │ │ (fastest,     │
              │ Vendor SDK: use HAL  │  │ 10-20%     │ │ smallest)    │
              │ for bring-up, plan   │  │ smaller    │ │ Only if:     │
              │ to abstract later    │  │ binary     │ │ single MCU   │
              └──────────────────────┘  │ No vendor  │ │ family,      │
                                        │ lock-in    │ │ <50K units   │
                                        └────────────┘ └─────────────┘
```
**Vendor HAL:** rapid prototyping, single MCU, team of 1-2, time-to-market priority.
**Custom HAL:** >100K volume (saves per-unit flash cost), multi-vendor sourcing, vendor SDK too bloated (STM32 HAL adds 40KB for GPIO toggle), MISRA/ISO 26262 compliance.
**Zephyr:** multi-vendor from day one, certified BLE/Thread/Zigbee stacks, product line spans silicon vendors, team invests in Devicetree.

### OTA Rollout Strategy

```
                          ┌──────────────────────────────┐
                          │ START: Deploying firmware     │
                          │ update to fleet               │
                          └────────────┬─────────────────┘
                                       │
                         ┌─────────────▼─────────────────┐
                         │ Fleet >10K devices?            │
                         └────┬────────────────────┬─────┘
                              │ YES                │ NO
                    ┌─────────▼──────┐    ┌────────▼──────────┐
                    │ Staged rollout  │    │ Direct full rollout │
                    │ required:       │    │ OK with monitoring  │
                    │ 1% → 5% → 25%   │    └────────────────────┘
                    │ → 100%          │
                    └────┬───────────┘
                         │
              ┌──────────▼──────────────┐
              │ Monitor per stage:       │
              │ • Crash rate vs previous │
              │ • Boot success rate      │
              │ • Battery life delta     │
              │ • Connectivity uptime %  │
              │ Halt if ANY metric       │
              │ degrades >1% absolute    │
              └──────────────────────────┘
```

### Logging Strategy by Device Constraint

```
                          ┌──────────────────────────────┐
                          │ START: Define logging budget  │
                          └────────────┬─────────────────┘
                                       │
                         ┌─────────────▼─────────────────┐
                         │ Flash budget for logs?         │
                         └────┬────────────────────┬─────┘
                              │                     │
                    ┌─────────▼──────┐    ┌─────────▼──────────┐
                    │ <4KB flash      │    │ >4KB (or SPI flash) │
                    └────┬───────────┘    └────┬───────────────┘
                         │                     │
              ┌──────────▼──────────┐  ┌────────▼──────────────┐
              │ Binary protocol:     │  │ CBOR or MessagePack:   │
              │ • 1-byte event ID    │  │ • Timestamp + event ID │
              │   + timestamp        │  │ • Severity level       │
              │ • Ring buffer in RAM │  │ • Key-value pairs      │
              │ • Upload on connect  │  │ • Human-decodable with │
              │ • Decode offline     │  │   schema file          │
              │   with lookup table  │  │ • Compress: heatshrink │
              └──────────────────────┘  │   or zlib              │
                                        └────────────────────────┘
```

## Core Workflow
<!-- QUICK: 30s — scan phase titles -->
<!-- STANDARD: 3min — Do/Verify/Recover for every phase -->

### Phase 1 (~4 hours): Build System & Toolchain Setup
1. **Do:** Pin GCC ARM toolchain (e.g., `arm-none-eabi-gcc 12.3.rel1`). Never `latest` — a toolchain change invalidates all timing analysis. Docker image with SHA256 hash.
2. **Do:** `CMakeLists.txt` with toolchain file. Enable `-Wall -Wextra -Werror -Wdouble-promotion -Wshadow -Wundef`. Add `-fstack-usage` for `.su` stack analysis files.
3. **Do:** Linker script (`firmware.ld`): FLASH/RAM origin+length from datasheet. Partitions: bootloader + app A + app B + config + logs. Verify: `arm-none-eabi-nm --size-sort firmware.elf | tail -20`.
4. **Verify:** Two builds from same source produce identical `.bin` and `.elf`. Any difference = timestamp/random seed/uninitialized data embedded.
5. **Recover:** Non-reproducible → check for `__DATE__`, `__TIME__`, `__FILE__` macros. Replace with git SHA + build ID. Check linker map ordering.

### Phase 2 (~8 hours): BSP & Device Driver Development
1. **Do:** BSP: `bsp/board_name/` with `board.h` (pins, peripherals, clock), `board.c` (clock init, pinmux, power sequencing), `board_config.h` (feature flags, calibration from EEPROM).
2. **Do:** Driver pattern: `init()` → `configure()` → `start()` → `stop()` → `deinit()`. Every driver supports graceful shutdown. Every driver accepts `const void *config` — no hardcoded pins.
3. **Do:** DMA: double-buffering (ping-pong) for continuous streams. `__attribute__((aligned(32)))` + non-cacheable memory. DMA completion ISR checks errors before processing data.
4. **Verify:** Each driver self-test: SPI loopback 10K packets at max clock, I2C stress with bus resets, UART 1M baud 0% dropped over 1M chars.
5. **Recover:** Intermittent failures → capture bus with logic analyzer. 80% of "driver bugs" are signal integrity: missing I2C pull-ups, no SPI MISO termination, UART baud mismatch from HSI oscillator.

### Phase 3 (~6 hours): Boot Flow Implementation
1. **Do:** Boot sequence: (1) ROM validates boot pin, jumps to flash → (2) First-stage inits critical clocks + external RAM → (3) Second-stage validates app image signature → (4) App inits RTOS, mounts FS, starts tasks.
2. **Do:** Secure boot: public key hash in OTP or secure element. SHA-256 of app image, Ed25519 signature verify. Fail → attempt previous image boot.
3. **Do:** Boot reason detection: read reset cause register (RCC_CSR STM32, RESETREAS nRF) at boot. Log: power-on, pin reset, watchdog, brown-out, software reset, CPU lockup. Single most valuable field-debugging data point.
4. **Verify:** Every boot reason path tested with programmable PSU + fault injection. Image validation rejects: unsigned, wrong key, corrupted header, truncated.
5. **Recover:** Bootloader validates all but fails → check: flash offset alignment, signature format (raw Ed25519 vs ASN.1 DER), endianness mismatch (x86 gen vs big-endian MCU).

### Phase 4 (~6 hours): OTA Update Infrastructure
1. **Do:** OTA pipeline: CI builds → signs with release key → uploads to CDN/S3 with version metadata → devices poll → download to inactive partition with range-request resume → verify signature → set boot flag → reboot.
2. **Do:** Delta updates: `bsdiff` or `hdiffpatch` for NB-IoT/LTE-M links. Delta <20% of full image or not worthwhile. Delta decoding must fit in available RAM.
3. **Do:** Rollback: `boot_attempt_count` in persistent register/EEPROM. Increment per boot, clear on successful app heartbeat. >N (default 3) → mark image bad → revert.
4. **Verify:** OTA tested: power loss at 25%/50%/75%/99% of download → resume, corrupt payload → detect+reject, wrong version → reject downgrade, 1000 simultaneous devices → CDN handles load.
5. **Recover:** OTA failure must not require cloud connectivity to revert. Bootloader makes the revert decision locally. Network outage ≠ bricked devices.

### Phase 5 (~4 hours): Manufacturing Test Firmware
1. **Do:** Separate "factory" firmware: enters test mode on GPIO hold at power-on or UART magic sequence. Never ships to end users.
2. **Do:** Test routines: (a) peripheral self-test (SPI loopback, I2C ping, ADC test point, GPIO loopback), (b) radio test (TX CW for power, RX sensitivity sweep), (c) flash test (write/read/verify), (d) unique ID burn (MAC, serial, public key hash).
3. **Do:** Serialization: use factory-programmed unique ID (STM32 UID, nRF DEVICEID) as identity root. MAC in OTP/external EEPROM — never hardcoded in firmware.
4. **Verify:** All tests <60 seconds per device. 1000 units/day production line can't wait. Output: machine-parseable (JSON over UART or USB mass storage).
5. **Recover:** Test fails → output "FAIL: ADC ch3, expected 1.65V±0.05, measured 2.11V" to UART. Red LED pattern is not enough.

### Phase 6 (~5 hours): Firmware CI/CD Pipeline
1. **Do:** Docker build: pinned GCC, CMake, Python, device tools (nrfjprog, STM32_Programmer_CLI, esptool). Build matrix for all HW revisions.
2. **Do:** CI stages: (1) Lint (clang-format, cppcheck, MISRA), (2) Build all targets, (3) Unit tests on host with mocked HAL, (4) HIL on real hardware, (5) Sign artifacts, (6) Upload with version tag.
3. **Do:** Versioning: `MAJOR.MINOR.PATCH-buildID`. MAJOR: incompatible OTA format. MINOR: new features, backward-compat. PATCH: bug fixes. Never reuse a version.
4. **Verify:** PR → build + unit + HIL smoke. Merge → full HIL suite. Release → signing + upload. HIL runner down → pipeline fails noisily, never silently skips hardware tests.
5. **Recover:** HIL runner health checks. Maintain standby HIL rig. Hardware tests are the gate — never bypass.

## Best Practices
<!-- STANDARD: 3min — rules from firmware teams shipping >500K devices -->

1. **Linker map review is part of code review.** Post `arm-none-eabi-nm --size-sort` diff. A new `printf` pulling in `malloc` adds 20KB — invisible in source diff, obvious in map diff.
2. **Never block in an ISR.** Capture state (<5 lines), defer to task/DPC, return. `while(flag)` in an ISR adds unbounded jitter. Refactor immediately.
3. **Use `volatile` correctly, not defensively.** Required: MMIO registers, ISR-modified variables, DMA descriptors. Harmful on regular variables — prevents optimization, 3-5× overhead. Missing memory barrier is the real bug, not missing `volatile`.
4. **Every peripheral has a timeout.** UART receive, I2C transaction, SPI DMA, flash erase — all have timeouts. Watchdog reset > infinite loop on dead hardware from a loose connector.
5. **Version your flash layout.** Magic number + layout version at known offset (e.g., `0x0800F000`). Bootloader checks compatibility. Without this, partition layout change → silent data corruption.
6. **Compression is cheaper than you think.** `heatshrink` (50-200 bytes decompressor, LZSS) compresses logs 4-8×. On BLE where 1KB flash = $0.02, compression pays for itself in 100 log lines. `miniz` (inflate, 12KB) for OTA delta decode.
7. **Assertions in release builds are worth the flash.** A 200-byte `assert()` that logs file + line + reset reason before reboot saves weeks of field debugging. Without it, you have zero clues.
8. **RAM functions for flash operations.** Code that erases/programs flash runs from RAM (`__attribute__((section(".ramfunc")))`). Silicon errata exists for nearly every MCU around this — read the errata.
9. **Initialize all stack memory.** FreeRTOS `configCHECK_FOR_STACK_OVERFLOW` paints stack with 0xA5. Catches overflow early instead of silent corruption for weeks.
10. **First 100ms after power-on are most dangerous.** Rails stabilizing, oscillators locking, BOD not armed. External supervisor IC (TPS3839) holds MCU in reset until rails stable. Firmware delays peripheral init 10ms after clock lock.

## Error Decoder
<!-- STANDARD: 3min — exact error → root cause → fix -->

| Error / Symptom | Root Cause | Fix |
|-----------------|------------|-----|
| `arm-none-eabi-gcc: unrecognized '-mcpu=cortex-m33'` | GCC too old — M33 support added in GCC 8 | Pin GCC 12.3.rel1+. Someone updated base image. |
| `section '.bss' will not fit in region 'RAM'` | RAM overflow — .data + .bss + heap + stacks > physical | `arm-none-eabi-nm --size-sort \| tail -20`. Move large buffers to `.noinit`, reduce heap, replace `printf` (20KB) with minimal formatter. |
| Device resets immediately after OTA | New firmware `.data` LMA overlaps bootloader flash region | Check linker script: bootloader region excluded from app flash origin. Compare `objdump -h` old vs new. |
| `HardFault_Handler` during `memcpy` to DMA buffer | Buffer not in non-cacheable memory — CPU cache and DMA disagree | Add buffer to `.nocache` linker section. `SCB_CleanInvalidateDCache()` before DMA, `SCB_InvalidateDCache()` after. |
| Image 50% larger than previous build | Dependency pulled in `malloc`, `printf`, or exception handling | `grep 'malloc\|_sbrk\|__aeabi_' build/firmware.map`. Remove dependency or link `-nostdlib` with minimal stubs. |
| OTA signature verification fails, download succeeded | Endianness mismatch — x86 (LE) sig vs big-endian MCU | Use `mbedtls_mpi_read_binary()` (big-endian), not `_le` variant. Verify byte order explicitly in both signer and verifier. |
| Debug (`-Og`) works; release (`-Os`) crashes on boot | Missing `volatile` or memory barrier — compiler reordered/eliminated "redundant" MMIO read | Add `volatile` to register struct. Add `__DSB()` after critical writes. Diff assembly between `-Og` and `-Os` at crash site. |
| Build not reproducible: SHA256 differs between runs | `__DATE__`/`__TIME__` macros, random seed, non-deterministic linker ordering | Replace with git SHA + build ID. Set linker `SORT_NONE`? Check `.cmake` toolchain for non-deterministic flags. |

### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Device crashes randomly in the field | Watchdog timer not configured or reset incorrectly | Configure the hardware watchdog timer with a proper reset handler. The watchdog must be kicked (reset) only in the main loop after all critical subsystems have reported healthy. Never kick the watchdog in an interrupt handler — it masks the crash. |
| I2C bus locks up after 24 hours of operation | No bus recovery mechanism on lock condition | Implement I2C bus recovery: if the bus is busy for >100ms without a stop condition, toggle SCL 9 times to reset slave devices. Add a bus health monitor that detects lockups and triggers re-initialization. Missing this is the #1 cause of "works in the lab, fails in the field." |
| Firmware OTA update bricks 5% of devices | No rollback mechanism in bootloader | Every OTA update requires: dual-bank flash with a confirmed-good fallback image, CRC check before applying the update, and a bootloader that boots the previous image if the new one fails to start. If the bootloader can't roll back, every OTA is a potential bricking event. |
| ADC readings drift with temperature | No temperature compensation in firmware | Add a temperature sensor near the ADC reference. Read temperature at each conversion cycle and apply a compensation curve. If the ADC has an internal temperature sensor, use it. ADC drift without compensation can be 10-50% across the operating temperature range. |
| Production test fails 30% of units, all pass in re-test | Test fixture has poor contact or timing issues | Review test fixture: pogo pin alignment, contact resistance, settling time after power-up. Add a "pretest" sequence that checks fixture contact before running tests. The first test after a power cycle should be a known-good reference measurement. |
| Interrupt latency causes missed events | Shared interrupt priority or long critical sections | Assign interrupt priorities carefully: time-critical interrupts (timers, communication) get highest priority. Limit critical section duration to <10μs. Use a real-time trace (logic analyzer or Segger SystemView) to measure worst-case interrupt latency. If latency exceeds your timing budget, restructure critical sections. |
| Power budget exceeded by 40% | Sleep mode not configured for peripherals | Every peripheral must be in its lowest power state when not in use. GPIO pins should not float (internal pull-up/down or driven). Use the MCU's lowest sleep mode that can wake from the required source. Measure actual current at the PSU, not the datasheet typical — it's always higher. |


## Production Checklist
<!-- QUICK: 30s — binary pass/fail. All must pass before release. -->

- [ ] **[F1]** Build reproducible: same SHA + Docker image = bit-identical `.bin`; toolchain pinned in Dockerfile with SHA256
- [ ] **[F2]** Linker script reviewed: FLASH/RAM match datasheet, partitions verified with `objdump -h`, >20% headroom
- [ ] **[F3]** Bootloader: Ed25519/ECDSA signature verification; unsigned/corrupt/wrong-key rejected; boot reason logged from reset cause register
- [ ] **[F4]** A/B OTA with auto-rollback: boot attempt counter in persistent storage, 3-failure revert; power-loss tested at every 10% of download
- [ ] **[F5]** All drivers have timeout handling: no unbounded `while(flag)`; watchdog serviced in dedicated task with health check-ins
- [ ] **[F6]** Stack high-water marks <80% after 24h stress; `configASSERT` and stack overflow detection enabled in RELEASE builds
- [ ] **[F7]** DMA buffers aligned to cache line, non-cacheable memory; cache clean/invalidate before/after DMA transactions
- [ ] **[F8]** Flash layout versioned (magic + version at known offset); bootloader checks layout compatibility at boot
- [ ] **[F9]** Factory firmware: all peripheral self-tests + serialization <60s; output machine-parseable (JSON over UART)
- [ ] **[F10]** CI: PR → build + unit + HIL smoke; merge → full HIL; release → signing + upload; HIL failure blocks pipeline
- [ ] **[F11]** OTA staged rollout: 1%→5%→25%→100% with crash-rate and boot-success monitoring; auto-halt on >1% degradation
- [ ] **[F12]** Secure element or OTP for private key storage; no keys in firmware binary; bootloader public key hash in OTP
- [ ] **[F13]** Assertion handler in RELEASE builds: logs file+line+reset reason, reboots; no silent corruption allowed
- [ ] **[F14]** External reset supervisor holds MCU in reset until all rails stable; firmware delays peripheral init 10ms after clock lock

## Cross-Skill Coordination
<!-- QUICK: 30s — who to talk to, when, what to share -->

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Embedded Engineer** | BSP bring-up, driver design, bootloader architecture | Pin mux, clock tree for target power states, ISR priorities, DMA channel allocation |
| **Hardware Architect** | Memory map changes, new peripherals, boot pin strapping | Flash/RAM sizing, external memory interface timing, secure element I2C address and speed |
| **QA Engineer** | Factory firmware, HIL scenarios, OTA test plans | Test mode entry sequence, test command protocol, calibration verification, regression list |
| **DevOps Engineer** | CI/CD, Docker images, artifact signing+storage | Toolchain Docker spec, HIL runner hardware requirements, artifact retention, signing key management |
| **Security Engineer** | Secure boot, OTA signing, key management | Signature algorithm, key storage (secure element vs OTP), firmware encryption, vulnerability disclosure |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| New chip revision needs toolchain upgrade | Embedded Engineer, DevOps Engineer | Regression test entire fleet; breaks all Docker images |
| OTA download failure >5% fleet-wide | DevOps Engineer, Security Engineer | CDN health check; TLS cert expiry; storage outage |
| Bootloader bug found in production | Security Engineer, Embedded Engineer | Emergency OTA or physical recall; vulnerability severity |
| Build reproducibility broken | DevOps Engineer, QA Engineer | Audit toolchain pins; check for timestamps, random seeds |
| Factory test failure rate >2% spike | QA Engineer, Hardware Architect | PCB assembly vs firmware regression; halt production line |

### Escalation Path

```
Fleet bricking >0.1%? → Halt OTA → VP Engineering → Physical recall assessment
Build unreproducible >24h? → DevOps Engineer → Cannot ship → Escalate to CTO
Secure boot bypass found? → Security Engineer → Emergency OTA / HW respin + physical recall
Factory firmware blocking production? → QA Engineer → Production Manager → Revenue: $X/day
```

### Cross-Skill Chain

```bash
# Embedded bring-up → Firmware → QA → DevOps
/embedded-engineer && /firmware-developer && /qa-engineer && /devops-engineer
```

## What Good Looks Like
<!-- DEEP: 10+min — concrete success criteria -->

- Build system produces bit-identical `.bin` from same commit; `sha256sum firmware.bin` matches CI ↔ developer machine.
- Every driver passes 10K-iteration stress: SPI at max clock, I2C with bus resets, UART at 1M baud with 1M chars, DMA with buffer wrap — zero timeouts.
- Bootloader validates signatures, rejects unsigned/corrupt images, boots previous after 3 failures, logs boot reason — all on real hardware.
- OTA survives power loss at every 10% of download; after 100 random power-loss tests, device always boots a valid image (old or new, never corrupted).
- Factory firmware completes all tests <60s, outputs pass/fail with measured values; operator interprets without engineering knowledge.
- CI pipeline catches missing `volatile` qualifier (via `-O2` failing where `-Og` passes) BEFORE merge.
- Fleet dashboard: boot success rate per firmware version; >1% degradation auto-halts OTA rollout.

## References
<!-- QUICK: 30s — links to deeper reading -->
- `references/build-system-design.md` — CMake + GCC cross-compilation: toolchain files, Docker images, reproducible builds, linker script anatomy, `objdump`/`nm`/`readelf` guide
- `references/device-driver-patterns.md` — Driver architecture: init/start/stop/deinit state machines, DMA double-buffering, interrupt deferral, timeout implementation, bus recovery
- `references/ota-infrastructure.md` — Full OTA pipeline: signing (Ed25519, ECDSA), delta generation (bsdiff, hdiffpatch), CDN distribution, staged rollout with metrics, rollback state machine
- `references/field-debugging.md` — Remote log retrieval via BLE/WiFi, crash dump (Cortex-M fault registers, stack trace), fleet health monitoring, watchdog-based recovery telemetry
- `references/hal-design.md` — HAL architecture: abstraction thickness tradeoffs, Zephyr driver model, vendor SDK abstraction, compile-time vs runtime polymorphism
- `references/secure-element-integration.md` — ATECC608, TPM 2.0, STSAFE, nRF secure immutable bootloader: key storage, attestation, secure provisioning flow
- `assets/linker-script-template.ld` — Production linker script template: bootloader/app/config/log partitions, `.nocache` section, stack/heap guards, MPU region alignment
- `assets/factory-test-protocol.md` — UART/JSON test command protocol, test result schema, serialization format, calibration value storage layout
