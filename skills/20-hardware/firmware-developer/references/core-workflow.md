# Core Workflow — Full Implementation

<!-- QUICK: 30s — scan phase titles -->
<!-- STANDARD: 3min — Do/Verify/Recover for every phase -->
<!-- DEEP: 10+min -->

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
