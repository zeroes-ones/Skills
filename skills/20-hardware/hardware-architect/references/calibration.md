# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can read a datasheet and select a part but don't know why two identical-spec LDOs behave differently — one oscillates at 200mA because its output capacitor ESR is wrong | You've taken a design from concept through FCC/CE/ISED certification and into production; your power tree estimates are within 15% of bench measurements; your first PCB spin boots without bodge wires | A contract manufacturer hands you a board that "works sometimes" — you find the marginal timing violation, the ground bounce issue, and the ESD susceptibility in a 2-hour bench session without schematics |
| You route a PCB by connecting pins but don't understand why a 50mm trace at 100MHz is a transmission line, not a wire | You can calculate impedance, length-match to within 2mm, and know when a signal needs termination — and your layouts pass EMC on the first lab visit | You review a competitor's teardown and identify every cost-reduction opportunity, every EMC compromise, and the design philosophy behind their architecture — in 30 minutes |
| You select components by searching "popular MCU for IoT" on Google | You maintain a personal component database with lifecycle status, second-source alternatives, and per-unit pricing at 1K/10K/100K volumes — updated quarterly | A chip shortage hits (like the 2020-2022 STM32 crisis) — you have a pin-compatible alternative designed into the BOM as an alternate population option, and production switches within 4 weeks |

**The Litmus Test:** Can you review a 12-layer PCB layout for a high-speed digital design and identify every signal integrity, power integrity, and EMI risk — before it goes to fab — without running a simulation? If you need the SI tool to find the obvious problems (missing termination, reference plane splits, antenna loops under connectors), you're not L3 yet.
