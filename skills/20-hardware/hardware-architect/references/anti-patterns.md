# Anti-Patterns

<!-- QUICK: 30s -- machine-detectable anti-patterns with auto-prevention -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep/lint) | 🛡️ Auto-Prevent |
|---|---|---|---|
| Selecting SoC "because we've always used it" | Scored selection matrix: interfaces, power, cost, ecosystem, lifecycle, second-source — 3+ options | `file_contains("*", "(same.as|always.used|standard.choice|default).*chip\|MCU\|SoC\|processor")` AND NOT `file_exists("*selection-matrix*")` | STOP. Auto-generate selection matrix template. Require 3+ scored options. |
| Using datasheet typical current for power budgeting | Max numbers + 20% regulator derating; measure at -20°C, 25°C, 60°C on prototype | `grep -rn "typ\." docs/power* BOM* \| grep -i "µA\|mA\|current"` | WARN. Replace typical with max values. Add 20% derating to budget. |
| Skipping thermal simulation because "enclosure has vents" | Run simulation before PCB layout; worst-case: max ambient + max power + 20% margin | `grep -q "vents\|natural.convection\|passive.cooling" docs/thermal*` AND NOT `test -f sim/thermal-*` | STOP. Generate thermal simulation checklist. Require junction temp verification. |
| Selecting single-source components without alternatives | Mark BOM: single-source (risk), multi-source (safe), EOL-risk; document alternative | `grep "single.source\|sole.source\|no.alternate" BOM*.csv` | WARN. Auto-flag single-source lines. Generate alternative search query per component. |
| EMC pre-compliance after PCB fab | Run at prototype/breadboard; include EMC engineer in layout review; budget 1 respin | `file_exists("*.kicad_pcb")` AND NOT `file_exists("*emc*report*")` AND NOT `file_exists("*pre-compliance*")` | STOP. Generate EMC pre-compliance checklist. Require test date before fab signoff. |
| Designing without DFT provisions | Test points for every power rail, critical signal, programming interface, UART debug, bootloader LED | `grep -c "test.point\|TP[0-9]" *.kicad_sch` < 5 | WARN. Auto-generate DFT checklist. Flag missing test points by net class. |
| Selecting clock without analyzing accuracy requirements | Match clock to interface: USB/CAN ±0.25% (crystal required); UART 115200 ±2%; internal OSC ±5% not enough for most | `grep "HSE\|LSE\|HSI\|LSI\|internal.osc\|external.crystal" docs/clock*` AND NOT `grep "ppm\|accuracy\|tolerance.*%" docs/clock*` | STOP. Auto-generate clock accuracy matrix per interface. Verify ppm against requirements. |
| Committing to PCB fab before pin mux review with firmware | Every pin assignment must pass firmware review before schematic freeze | `file_exists("*.kicad_sch")` AND NOT `file_exists("*pin-mux-review*")` AND `file_exists("*.kicad_pcb")` | BLOCK fab release. Auto-generate pin mux checklist for firmware team signoff. |
