---
name: hardware-architect
description: Hardware architecture design & electronic system-level decisions — SoC/microcontroller selection (ARM Cortex, RISC-V, FPGA, ASIC), memory architecture (SRAM, DRAM, Flash, eMMC), power tree design (PMIC, LDO, buck/boost), bus architecture (AMBA, AXI, AHB, APB), PCB stackup & signal integrity, thermal management, EMC/EMI compliance, IP selection & licensing. Use when choosing processors, designing hardware architecture, making PCB stackup decisions, or evaluating silicon tradeoffs for an embedded/IoT product.
author: Sandeep Kumar Penchala
type: hardware
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - hardware-architecture
  - soc-selection
  - memory-architecture
  - power-design
  - signal-integrity
  - emc-compliance
token_budget: 3500
output:
  type: "document"
  path_hint: "./"
chain:
  consumes_from:
    - system-architect
    - embedded-engineer
    - firmware-developer
    - performance-engineer
  feeds_into:
    - embedded-engineer
    - firmware-developer
    - documentation-engineer
---
# Hardware Architect

Hardware architecture and electronic system-level design — from SoC selection through PCB stackup to compliance testing. Covers the critical architectural decisions that determine a product's cost, performance, power consumption, and time-to-market.

## Route the Request
<!-- QUICK: 30s -- ASCII decision tree to determine which skill handles the request -->

```
Request involves hardware design?
├── PCB layout, system architecture, SoC selection, memory/power/bus design
│   └── → Use hardware-architect (this skill)
├── Firmware running on an already-selected MCU — device drivers, RTOS, peripheral config
│   └── → Use embedded-engineer
├── Low-level device driver implementation, bootloader, HAL
│   └── → Use firmware-developer
├── Mechanical enclosure, thermal simulation (CFD), industrial design
│   └── → Mechanical engineer (not in library — consider general engineering guidance)
├── Electrical system design — schematics, component selection, power distribution
│   └── → Electrical engineer (not in library — consider general engineering guidance)
├── System-level architecture, product requirements, cost/power/performance tradeoffs
│   └── → Invoke `system-architect` for cross-disciplinary architecture decisions
├── Performance analysis, signal integrity, power integrity, thermal simulation
│   └── → Invoke `performance-engineer` for SI/PI simulation and EMC pre-compliance
├── Hardware documentation, architecture specifications, compliance test plans
│   └── → Invoke `documentation-engineer` for architecture specs and design decision logs
└── Unclear / need help routing
    └── → Default to hardware-architect and re-route if it's pure firmware
```

## Ground Rules (5)
<!-- MANDATORY: Read before executing any task -->

1. **Design for manufacturing from day one** — a beautiful prototype that can't be produced is art, not engineering.
2. **BOM cost is a design constraint, not an afterthought** — every component decision impacts unit economics at scale.
3. **Thermal design is electrical design** — heat kills electronics. Thermal budget is as critical as power budget.
4. **Regulatory certification (FCC, CE, UL) adds 3-6 months** — plan for it from the start, not as a post-design checkbox.
5. **Every connector, every component, every trace needs a reason to exist** — if you can't justify it, remove it.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- Selecting a processor/SoC for your next embedded product — ARM Cortex-M vs -R vs -A, RISC-V, FPGA, or ASIC
- Defining memory architecture — what goes in SRAM, DRAM, Flash (NOR/NAND/eMMC/UFS), and external storage
- Designing the power tree — PMIC selection, LDO vs buck converter, power sequencing, battery management
- Choosing bus architecture — AMBA AXI vs AHB vs APB, peripheral interconnect, DMA topology
- Making PCB stackup and signal integrity decisions — layer count, impedance control, differential pairs, length matching
- Planning thermal management — heatsinking, airflow, thermal vias, junction temperature, TDP budget
- Evaluating EMC/EMI compliance path — pre-compliance testing, shielding, filtering, radiated emissions
- Making make-vs-buy decisions on IP blocks — licensing ARM cores, buying reference designs, custom silicon

**Use `/embedded-engineer` instead when:** You're implementing firmware on a chosen MCU — writing device drivers, configuring peripherals, optimizing for power. Hardware-architect picks the platform; embedded-engineer builds on it.

## Cross-Skill Coordination
<!-- QUICK: 30s — who to talk to, when, what to share -->

Hardware architecture decisions cascade through the entire product development lifecycle. A wrong SoC selection costs 6+ months and $100K+ in respins. Every architectural decision must be validated with downstream teams before committing to silicon.

### Coordinate With

| Coordinate With | When | What to Share/Ask | Decision Gate / Artifact |
|-----------------|------|-------------------|--------------------------|
| **System Architect** | Product requirements definition, system-level tradeoffs | Power budget, latency budgets, throughput requirements, cost targets | Gate: System architecture review before SoC downselect. Artifact: System requirements document with hardware constraints. |
| **Embedded Engineer** | MCU/MPU selection, peripheral assignment, pin muxing, clock tree | Peripheral conflict analysis, GPIO drive strength, ADC reference, ISR latency budget | Gate: Pin mux review before schematic freeze. Artifact: Pin assignment spreadsheet with alternate functions. |
| **Firmware Developer** | Memory map, boot pin strapping, secure element integration, flash partitioning | Flash/RAM sizing, external memory interface, secure element protocol, boot sequence | Gate: Memory map review before PCB layout. Artifact: Memory map document with linker script constraints. |
| **Performance Engineer** | Signal integrity analysis, power integrity, thermal simulation, EMC pre-compliance | PCB stackup, impedance targets, decoupling strategy, thermal budget | Gate: Signal integrity sign-off before fab. Artifact: SI/PI simulation report with margin analysis. |
| **Documentation Engineer** | Hardware architecture specification, design decisions log, compliance test plan | Architecture decisions, component selection rationale, regulatory requirements | Gate: Architecture spec finalized before detailed design. Artifact: Hardware architecture specification document. |

### Communication Triggers

| Trigger | Notify | Why | Decision Gate |
|---------|--------|-----|---------------|
| Silicon errata with no workaround | System Architect, Embedded Engineer, Firmware Developer | Chip reselection may be required | Gate: Reselection decision within 5 business days. |
| BOM cost exceeds target >15% | System Architect, Product Manager | Design-to-cost review; component substitution | Gate: Cost review board approval before proceeding. |
| EMC pre-compliance failure >6dB | Performance Engineer, Firmware Developer | PCB respin or shielding design | Gate: Fix-or-respin decision with VP Engineering. |
| Power budget exceeded >20% | Embedded Engineer, Firmware Developer | PMIC reselection; power tree redesign | Gate: Power tree review before next prototype. |
| Component EOL with no drop-in replacement | System Architect, Embedded Engineer | Redesign or lifetime buy | Gate: Redesign decision within 10 business days. |

### Escalation Path

```
Silicon errata, no workaround? → System Architect → Chip reselection → +8 weeks schedule impact
EMC failure >6dB over limit? → Performance Engineer → PCB respin → $15K-50K + 4-6 weeks
BOM cost >25% over target? → Product Manager → Redesign or pricing adjustment
Thermal junction temp exceeds rating? → Performance Engineer → Heatsink redesign or clock reduction
```

### Cross-Skill Chain

```bash
# System Architecture → Hardware Architecture → Embedded bring-up → Firmware → QA
/system-architect && /hardware-architect && /embedded-engineer && /firmware-developer && /qa-engineer
```

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Processor Architecture Selection

```
                      ┌──────────────────────────┐
                      │ START: What are your      │
                      │ compute requirements?     │
                      └───────────┬──────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Real-time deterministic    │
                    │ response required?         │
                    └────┬─────────────────┬────┘
                         │ YES (≤1μs jitter)│ NO
                    ┌────▼──────────┐ ┌─────▼──────────────────────┐
                    │ Is compute    │ │ Running Linux or rich OS?  │
                    │ moderate?     │ └────┬─────────────────┬─────┘
                    │ (sensor fusion │      │ YES             │ NO
                    │ motor control,  │ ┌────▼──────────┐ ┌───▼──────────┐
                    │ closed-loop)    │ │ Cortex-A or   │ │ Cortex-M     │
                    └────┬──────────┘ │ RISC-V U54.   │ │ (M0-M7) or   │
                         │ YES        │ MMU required   │ │ RISC-V E31   │
                    ┌────▼──────────┐ │ for memory     │ │ or RISC-V    │
                    │ Cortex-R or   │ │ management.    │ │ based MCU.   │
                    │ RISC-V R      │ └────────────────┘ └──────────────┘
                    │ series.       │
                    │ Lockstep      │
                    │ cores for     │
                    │ safety.       │
                    └───────────────┘
```

**Cortex-M** (M0-M7): MCU class. No MMU, typically FreeRTOS/Zephyr or bare-metal. Power µA to mA. For sensors, wearables, IoT endpoints. **Cortex-R:** Real-time, deterministic, lockstep for safety. For automotive, industrial, medical. **Cortex-A:** Application processor with MMU. Runs Linux/Android. For gateways, HMI, cameras. **RISC-V:** Emerging. No licensing fees, but ecosystem maturity depends on vendor (SiFive, Bouffalo, ESP32-C).

**FPGA vs ASIC decision:** < 10K units → FPGA. 10K-100K → FPGA or structured ASIC. > 100K → custom ASIC. ASIC NRE is $2-10M+ for 28nm and below — only if volume justifies it.

### Memory Architecture Decision

```
                     ┌──────────────────────────┐
                     │ START: What's the primary │
                     │ execution memory?         │
                     └───────────┬──────────────┘
                                 │
                   ┌─────────────▼─────────────┐
                   │ Code executes from?        │
                   └────┬─────────────────┬────┘
                        │ Flash (XIP)     │ RAM
                   ┌────▼──────────┐ ┌─────▼──────────────────────┐
                   │ NOR Flash for  │ │ Need > 512MB?             │
                   │ XIP. Lower     │ └────┬─────────────────┬────┘
                   │ density (up to │ │ YES             │ NO
                   │ 256MB), faster │ ┌────▼──────────┐ ┌───▼──────────┐
                   │ random read.   │ │ DDR3/DDR4     │ │ SRAM or      │
                   │ Typical for    │ │ or LPDDR4.    │ │ SDRAM.       │
                   │ MCU apps.      │ │ DRAM needs    │ │ SRAM is      │
                   └────────────────┘ │ refresh +     │ │ fastest +     │
                        │ NAND Flash  │ longer boot. │ │ lowest power. │
                   ┌────▼──────────┐ └───────────────┘ └──────────────┘
                   │ NAND/eMMC for │
                   │ storage.      │
                   │ Multi-level   │
                   │ (MLC/TLC) for │
                   │ density, SLC  │
                   │ for reliabil- │
                   │ ity. eMMC     │
                   │ simplifies    │
                   │ management.   │
                   └────────────────┘
```

**SRAM:** Fastest, lowest power, most expensive ($10-50+/MB). For cache, < 1MB scratchpad. **SDRAM:** Good balance for MCU applications with > 64KB needs. **DDR:** For application processors. LPDDR for battery-powered. **NOR Flash:** For XIP (eXecute In Place). No boot RAM needed. 1-256MB. **NAND Flash:** For storage. TLC/QLC for density, SLC for reliability. eMMC handles bad block management and wear leveling for you.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~20 min): Requirements Capture
**Steps:** 1) Define compute requirements: MIPS/DMIPS, real-time guarantees, determinism needs, FPU requirement, DSP capability 2) Define I/O requirements: peripheral count (SPI, I2C, UART, CAN, USB, Ethernet), GPIO count, ADC channels/rate, display interface 3) Define power budget: active current, sleep current, peak current, thermal envelope, battery life target 4) Define environmental: operating temperature, vibration, humidity, IP rating, safety certification (IEC 61508, ISO 26262, DO-254) 5) Define cost targets: BOM cost, tooling/NRE, development time, volume ramp plan
**What good looks like:** Requirements document with 5 specific constraints (compute, I/O, power, environmental, cost) — all quantified with ranges, not absolutes.

### Phase 2 (~30 min): SoC/Processor Selection
**Steps:** 1) Map requirements to processor class using the decision tree above 2) Create a shortlist of 3-5 processor families (e.g., STM32H7, NXP i.MX RT, TI AM64x) 3) Compare on: performance, power, price, ecosystem (tools, SDK, community), availability (lead time, lifecycle status), security features (secure boot, TRNG, crypto accelerator) 4) Check for second-sourcing options — what happens if this chip has a 52-week lead time? 5) Select and document rationale — keep the alternatives section for when the chosen chip goes EOL
**What good looks like:** Selection document with 5 processor candidates, scored on 7 criteria (performance, power, price, ecosystem, availability, security, second-source), with the winner and runner-up documented. A new engineer understands why this chip was chosen.

### Phase 3 (~25 min): Memory & Storage Architecture
**Steps:** 1) Determine execution memory (XIP Flash vs DRAM) using decision tree 2) Size Flash: firmware image size × 2 (for OTA dual-bank) + file system (if needed) + bootloader + factory test + 30% headroom 3) Size RAM: stack + heap + buffers (DMA, display, audio) + OS kernel + application data + 30% headroom. Actual measurement beats estimation — build a prototype and measure. 4) Select storage: eMMC for ease (5.1 recommended) vs raw NAND (cheaper but requires ECC + bad block management) vs SDCard (removable but slower) 5) Consider external memory interface: QSPI vs OSPI vs parallel NOR vs DDR
**What good looks like:** Memory map document: base address, size, purpose, and timing requirements for every memory region. No region with "TBD" size.

### Phase 4 (~20 min): Power Tree Design
**Steps:** 1) Calculate total power budget: sum of all rail currents × voltages. Add 30% margin. 2) Choose regulator topology: PMIC (integrated, small footprint) vs discrete LDOs (low noise, analog) vs discrete buck converters (efficient > 100mA). Each rail gets a decision. 3) Define power sequencing: which rails come up in what order, with what delays. Use a sequencer IC or PMIC with configurable sequencing. 4) Define sleep modes: which rails stay on during sleep, wake sources, wake time budget. Measure actual sleep current early — datasheet typicals assume perfect conditions. 5) Battery management: charge IC (linear vs switching), fuel gauge (voltage vs coulomb counting vs impedance track), protection (over-current, over-temperature, under-voltage lockout)
**What good looks like:** Power tree diagram showing every voltage rail, the regulator feeding it, maximum current, sequencing order, and sleep mode state. Measured power consumption at each state (active/idle/sleep/deep sleep) within 10% of estimate.

### Phase 5 (~15 min): PCB & Signal Integrity Planning
**Steps:** 1) Determine layer count based on signal density and impedance requirements: 2-layer (simple, cheap, but SI poor), 4-layer (good SI, dedicated power plane), 6+ (high-speed, many supplies) 2) Define stackup: signal layer order, reference plane assignment, dielectric thickness, target impedance (50Ω single-ended, 90Ω differential, 100Ω differential) 3) Identify critical nets requiring length matching: DDR, high-speed serial (USB 3.0, PCIe, MIPI), differential pairs 4) Plan decoupling: bulk capacitance per rail, high-frequency decoupling per IC, placement proximity 5) Review with layout engineer — paper review before routing saves weeks
**What good looks like:** PCB stackup document with layer stack, target impedance, critical net list, decoupling strategy, and placement guidance. Layout engineer can start routing with zero questions about constraints.

### Phase 6 (~10 min): Compliance & Certification Planning
**Steps:** 1) Identify required certifications: FCC Part 15 (USA), CE (EU), UKCA, ISED (Canada), VCCI (Japan) — plus industry-specific (medical: IEC 60601, automotive: ISO 26262, industrial: IEC 61000) 2) Pre-compliance testing: evaluate radiated emissions, conducted emissions, ESD, surge, and immunity in-house before sending to certified lab. Pre-compliance catches 80% of issues at 10% of the cost. 3) Plan certification timeline: lab reservation (4-8 weeks lead), testing (1-2 weeks), remediation (variable, often 4-8 weeks). FCC certification typically 8-16 weeks from first submission. 4) Budget: FCC/CE pre-compliance $3-5K, full compliance $15-30K per product variant. Add 50% for first product.
**What good looks like:** Compliance plan with required certifications per target market, test house booked, pre-compliance schedule budgeted, and timeline mapped backward from launch date.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from hardware engineering experience -->

- **Measure power, don't estimate.** Datasheet typical currents assume perfect conditions. Your firmware driving every peripheral will be 20-50% higher. Measure actual current on the first prototype — build a power measurement test point into every design.
- **Derate every component.** 50V capacitor on a 12V rail: OK. 25V capacitor on a 12V rail with 10% tolerance: 2.5V headroom — reliability risk. Derate capacitors 50% (use 16V on 5V, 25V on 12V). Derate resistors 20%. Derate MOSFETs 50% on Vds and Id.
- **Start thermal simulation before the PCB layout.** A 10°C rise in junction temperature reduces component lifetime by 50% (Arrhenius). Identify hot components (regulators, processors, power amplifiers) early and plan for heatsinking, airflow, and thermal vias.
- **Clock generation is a design choice, not an afterthought.** External crystal: most accurate (±10-50ppm), but requires PCB area and two load capacitors. Internal oscillator: saves pins and BOM, but ±1-5% accuracy — too loose for USB, CAN, or high-speed serial without PLL.
- **Test at temperature extremes.** Products that work at 25°C but fail at -20°C or +60°C are the most common field failure pattern. Test all critical interfaces (DDR timing, USB negotiation, ADC accuracy) at minimum and maximum rated temperature.
- **Design for test (DFT) saves development time.** Add test points for every power rail, critical signal, and programming interface. Include a UART debug header. Add an LED that the bootloader toggles — when the device won't boot, that LED tells you whether the bootloader ran.
- **Have a BOM risk plan.** Mark every component: single-source (risk), multi-source (safe), or EOL-risk (obsolete). For single-source parts, have an alternative part identified before the design review. Lead times > 20 weeks should trigger a back-up plan.

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
<!-- QUICK: 30s -- binary pass/fail. All must pass before PCB fab. -->

- [ ] **[H1]** SoC/processor selected with documented rationale, alternatives considered, and second-source option identified
- [ ] **[H2]** Memory architecture documented: memory map, type, size, timing requirements for each region
- [ ] **[H3]** Power tree calculated with 30% margin and simulation or bench measurement confirming estimates
- [ ] **[H4]** Power sequencing defined: rail order, ramp timing, and sleep mode configuration
- [ ] **[H5]** Critical nets identified for length matching: DDR, high-speed serial, differential pairs
- [ ] **[H6]** PCB stackup defined: layer count, layer order, dielectric material, target impedance
- [ ] **[H7]** Decoupling strategy documented: bulk capacitance per rail, high-frequency decoupling per IC, placement
- [ ] **[H8]** Thermal simulation completed: junction temperature of all hot components within spec under worst-case ambient
- [ ] **[H9]** Derating review completed for all critical components (caps, resistors, MOSFETs, connectors)
- [ ] **[H10]** Pre-compliance EMC test scheduled or completed: radiated emissions, conducted emissions, ESD
- [ ] **[H11]** Certification plan documented: required certifications per target market, budget, timeline
- [ ] **[H12]** BOM risk assessment completed: single-source parts identified with backup alternatives
- [ ] **[H13]** Test points included for: all power rails, critical signals, programming interface, UART debug
- [ ] **[H14]** Schematics peer-reviewed, layout constraints documented for layout engineer handoff

## Cross-Skill Integration
<!-- QUICK: 30s -- table of who to talk to when -->

| Step | Skill | What It Produces |
|------|-------|-----------------|
| **Before** | `embedded-engineer` | Firmware requirements, peripheral usage patterns, interrupt priorities → informs processor selection |
| **Before** | `firmware-developer` | Bootloader requirements, memory map needs, OTA architecture → informs memory sizing |
| **This** | `hardware-architect` | SoC selection, memory architecture, power tree, PCB stackup, compliance plan |
| **After** | `performance-engineer` | Hardware performance targets (clock speed, memory bandwidth, power budget) → performance baseline |
| **After** | `documentation-engineer` | Hardware architecture document, memory map, power tree → forms the hardware section of the product documentation |
| **After** | `qa-engineer` | Test requirements (thermal testing, EMC pre-compliance, HALT) → test plan input |

## Scale Depth: Solo → Startup → Scale-up → Enterprise
<!-- QUICK: 30s -- how complexity increases with team/organization size -->

- **Solo**: Breadboard/Arduino prototyping, development kits, hobbyist PCB tools (KiCad/EAGLE), single/dual-layer designs, manual assembly.
- **Startup**: Custom PCB design, professional EDA tools (Altium/OrCAD), 4–6 layer boards, contract manufacturing, basic EMC pre-compliance.
- **Scale-up**: DFM optimization, full compliance certification (FCC/CE/UL), multi-board systems, signal integrity simulation, thermal modeling, BOM cost engineering.
- **Enterprise**: Multi-product platform architecture, silicon validation, global regulatory (FCC/CE/ISED/CCC), high-speed design (DDR5/PCIe Gen5), automated test infrastructure, supply chain resilience.

## What Good Looks Like

A well-designed hardware architecture is invisible when it's right — the product works reliably across temperature, meets power targets on the first spin, and passes EMC with margin. Specifically:
- **The first prototype boots and communicates.** No power rail sequencing bugs, no clock configuration that needs a bodge wire, no "turns out this pin doesn't support that function." The SoC selection was right.
- **Power consumption is within 10% of estimate.** The power tree model, simulation, and measurement converge. No last-minute LDO swap because the regulator overheats.
- **EMC passes with margin on the first compliance test.** Pre-compliance caught the issues (bad clock routing, missing ferrites, poorly filtered I/O) before the expensive lab test.
- **Memory map is stable from day one.** No firmware rewrites because the memory architecture changed. The map had headroom for growth.
- **The hardware architecture document is the single source of truth.** A new engineer can read it and understand every decision: why this SoC, why this memory topology, why this regulator topology, why this stackup. The alternatives section explains what was rejected and why.
