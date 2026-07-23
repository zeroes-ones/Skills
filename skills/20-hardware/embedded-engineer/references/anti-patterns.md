# Anti-Patterns

<!-- QUICK: 30s -- machine-detectable anti-patterns with auto-prevention -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep/lint) | 🛡️ Auto-Prevent |
|---|---|---|---|
| Dynamic memory allocation in event loops or IRQ context | Allocate all buffers at boot; static pools with `ACQUIRE_BUFFER()`/`RELEASE_BUFFER()` macros | `grep -n "malloc\|calloc\|realloc\|free" src/*.[ch] \| grep -v "_init\|setup\|boot"` | REFUSE merge if malloc appears outside init functions. |
| Kicking watchdog from ISR without subsystem health checks | Kick only in main loop after ALL subsystems report healthy via heartbeat flags | `grep -rn "WDT.*Feed\|IWDG.*Refresh\|watchdog.*kick" *.[ch] \| grep -v "main\|while(1)\|super.loop"` | WARN. Flag every watchdog kick not in main loop. |
| Using datasheet typical current for power budgeting | Measure actual on first prototype at -20°C, 25°C, 60°C across all power modes | `grep -rn "typical\|typ\." docs/power* \| grep -i "µA\|mA\|current"` | STOP. Replace typical values with max datasheet numbers + 20% regulator derating. |
| Shipping firmware without hardware version detection | Read board revision via GPIO strapping or EEPROM; refuse to run on unsupported rev | `grep -rL "board.*rev\|hw.*version\|REV_\|BOARD_REV" src/` | WARN. Auto-generate HW version detection from GPIO strapping pins. |
| Long interrupt-disabled sections >5µs | Use lock-free data structures; move heavy work to deferred procedure call | `grep -n "__disable_irq\|__asm.*CPSID\|portENTER_CRITICAL" src/ && grep -c "portEXIT_CRITICAL"` | STOP. Flag every critical section. Require timing budget annotation. |
| SPI/I2C without bus recovery or timeout | I2C: 9 SCL pulses recovery; SPI: timeout + peripheral reset; UART: receive timeout | `grep -L "bus.*recover\|SCL.*pulse\|timeout\|bus.reset" src/drivers/*i2c* src/drivers/*spi*` | WARN. Auto-inject bus recovery pattern into peripheral drivers. |
| Floating GPIO pins in low-power sleep | Configure unused pins as analog input (lowest leakage) or driven output | `grep -A5 "sleep\|low.power\|deep.sleep" src/*.[ch] \| grep -v "analog\|pull.up\|pull.down\|output"` | WARN. Generate pin configuration review report for sleep modes. |
| OTA without dual-bank flash + rollback verification | Dual-bank: validate signature, check CRC, revert after 3 failed boots | `grep -l "OTA\|firmware.update" src/ \| xargs grep -L "dual.bank\|rollback\|revert\|fallback"` | STOP. Block OTA PR merge without dual-bank + rollback. |
