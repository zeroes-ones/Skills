# Best Practices

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
