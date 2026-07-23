# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can write a driver from a datasheet but your ISRs still use busy-waits, your error handling is `while(1)`, and you discover your stack size by waiting for the crash | You've shipped firmware on 3+ hardware revisions; your OTA updates have never bricked a device; you catch race conditions in code review before they reach hardware — and can explain why the `volatile` keyword isn't enough for DMA | A silicon vendor's field application engineer asks YOU for guidance on a peripheral errata workaround — because you've already characterized it, written the fix, and published it on your team's wiki |
| You treat the vendor HAL as a black box and don't know how many clock cycles `HAL_SPI_Transmit()` actually takes | You read the generated assembly for every ISR, know the cycle count of every critical path, and can optimize a hot loop from 47 cycles to 12 by reordering instructions | You can look at a boot loop field report with zero debug logs — just a power consumption trace and the firmware version — and identify the root cause from behavior pattern alone |
| You set compiler flags by copying from a 5-year-old `Makefile` and don't know what `-fno-strict-aliasing` does | You maintain your own linker script, understand every section in your map file, and can squeeze 6KB from a 512KB flash by removing unused library code | You write the coding standard other firmware teams adopt — and it prevents the top 3 classes of field bugs across 5 different MCU architectures |

**The Litmus Test:** Can you debug a boot loop on a sealed device with no debug header — working only from a UART log, a power consumption trace, and your knowledge of the boot sequence — and identify the exact line of code or hardware fault causing it within 2 hours? If you need a JTAG probe to start, you're not L3 yet.
