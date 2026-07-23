# Production Checklist

<!-- QUICK: 30s -- binary pass/fail with validation commands and auto-fix -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|----------------|--------------------|----------|
| E1 | MCU/MPU selection documented: power budget, peripheral count, flash/RAM >20% headroom, BOM cost | `test -f docs/mcu-selection.md && grep -q "BOM\|power.budget\|peripheral.*count\|headroom" docs/mcu-selection.md` | Generate selection matrix template with all required columns. |
| E2 | Bootloader: Ed25519/ECDSA P-256 signature verification; unsigned images rejected; boot reason logged | `grep -q "ed25519\|ecdsa\|mbedtls_pk_verify" bootloader/src/*.[ch] && grep -q "RCC_CSR\|reset.*reason" bootloader/src/*.[ch]` | Auto-inject signature verification stub (mbedTLS) and reset cause logging. |
| E3 | A/B partition with fallback: 3 failed boots → auto-revert | `grep -q "boot.attempt\|revert\|fallback\|dual.bank" bootloader/src/*.[ch]` | Generate boot attempt counter in persistent storage with fallback logic. |
| E4 | Hardware watchdog: 2s timeout; external WDT IC for safety-critical | `grep -q "WDT\|IWDG\|watchdog" src/main.c && grep -q "2000\|2.*sec" src/main.c` | WARN: prompt for external WDT IC selection for ISO 26262/IEC 61508. |
| E5 | Power profile measured on production PCB at -20°C, 25°C, 60°C; 10-unit soak | `test -f test/power-profile.csv && grep -c "\-20\|25\|60" test/power-profile.csv | awk '{exit $1<3}'` | Generate power test plan and CSV template. |
| E6 | All ISRs <10µs; critical interrupt latency <1µs at max CPU load; jitter <5% | `grep -q "GPIO.toggle\|DWT_CYCCNT\|cycle.count" src/*isr* && test -f test/isr-timing-report.md` | Auto-inject GPIO toggle instrumentation for scope measurement. |
| E7 | Stack high-water marks <80% after 24h stress; all tasks >20% headroom | `grep "uxTaskGetStackHighWaterMark\|stack.*high.water" test/*.[ch] && test -f test/stack-report.csv` | Generate stack monitoring task. Auto-log watermark in CSV. |
| E8 | I2C bus recovery tested; SPI signal integrity on scope at max clock | `grep -q "SCL.*pulse\|bus.*recover\|9.*clock" src/drivers/*i2c* && test -f test/scope-captures/spi-eye*` | Auto-inject I2C recovery pattern. Prompt for scope capture. |
| E9 | Brown-out detection: 10% voltage margin, 50mV hysteresis; tested with programmable supply | `grep -q "BOR\|brown.out\|UVLO\|under.voltage" src/init* && test -f test/brownout-report.md` | Generate brown-out test procedure and config. |
| E10 | Board revision detected at boot (GPIO strapping or EEPROM); firmware branches per rev | `grep -q "BOARD_REV\|board.*revision\|hw.*version" src/init*` | Auto-generate GPIO strapping config and revision enum. |
| E11 | HIL 24h soak with randomized fault injection passes; zero manual resets | `test -f test/hil-24h-report.log && grep -c "PASS\|FAIL\|RESET" test/hil-24h-report.log` | Generate randomized fault injection test harness stub. |
| E12 | OTA power-loss tested at every 10% of download; device always recovers | `test -f test/ota-powerloss-report.log && grep "10%\|20%\|30%\|...\|100%" test/ota-powerloss-report.log | wc -l | awk '{exit $1<10}'` | Generate OTA power-loss test script with percentage checkpoints. |
| E13 | ADC calibrated at factory (min 3 temp points if internal VREF); validated vs reference | `test -f cal/adc-calibration.csv && grep -c "cal.point\|temp.*point" cal/adc-calibration.csv | awk '{exit $1<3}'` | Generate 3-point calibration routine with polynomial fit. |
| E14 | FCC/CE/ISED pre-compliance scan: emissions within limits with 3dB margin | `test -f test/emc-precompliance-report.pdf && grep -q "margin.*3.*dB\|pass" test/emc-precompliance-report.*` | Generate EMC pre-compliance test plan and checklist. |
