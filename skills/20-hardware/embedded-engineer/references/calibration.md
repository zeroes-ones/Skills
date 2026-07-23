# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can blink an LED and read a sensor over I2C but don't know why your UART drops bytes at 1M baud — it's always "a hardware problem" | You bring up a new MCU from scratch — clock tree, DMA, interrupts, power modes — in under a week, and your drivers pass 10K-iteration stress tests across temperature | An EE hands you a schematic with an MCU you've never used and says "make it work" — 72 hours later you have a booting system with verified peripheral drivers, power profiling, and a factory test firmware |
| Your "error handling" is `while(1)` and you discover your stack size by trial and error — the compiler "just handles it" | You measure stack high-water marks on every task, your watchdog is configured with a worst-case path analysis, and your bootloader has never bricked a device in production | A field return arrives with "sometimes resets" as the only symptom — you identify the root cause (marginal power rail, silicon errata, or race condition) from an oscilloscope trace and 2 hours of bench work |
| You don't know the difference between an inline resistor and a ferrite bead — "that's the hardware engineer's job" | You can read a schematic, identify the MCU pin assignments, spot missing pull-ups on I2C, and flag a regulator that's undersized for the GSM burst current | You're the person hardware and firmware teams both call when a board "works on the bench but not in the field" — and you find the answer without touching the code |

**The Litmus Test:** Can you bring up a bare-metal system on an MCU family you've never used — clock tree, vector table, linker script, bootloader, and UART console — using only the reference manual and no vendor HAL? If you need someone else's BSP or the vendor's code generator to start, you're not L3 yet.
