# Best Practices

<!-- STANDARD: 3min -- rules extracted from hardware engineering experience -->

- **Measure power, don't estimate.** Datasheet typical currents assume perfect conditions. Your firmware driving every peripheral will be 20-50% higher. Measure actual current on the first prototype — build a power measurement test point into every design.
- **Derate every component.** 50V capacitor on a 12V rail: OK. 25V capacitor on a 12V rail with 10% tolerance: 2.5V headroom — reliability risk. Derate capacitors 50% (use 16V on 5V, 25V on 12V). Derate resistors 20%. Derate MOSFETs 50% on Vds and Id.
- **Start thermal simulation before the PCB layout.** A 10°C rise in junction temperature reduces component lifetime by 50% (Arrhenius). Identify hot components (regulators, processors, power amplifiers) early and plan for heatsinking, airflow, and thermal vias.
- **Clock generation is a design choice, not an afterthought.** External crystal: most accurate (±10-50ppm), but requires PCB area and two load capacitors. Internal oscillator: saves pins and BOM, but ±1-5% accuracy — too loose for USB, CAN, or high-speed serial without PLL.
- **Test at temperature extremes.** Products that work at 25°C but fail at -20°C or +60°C are the most common field failure pattern. Test all critical interfaces (DDR timing, USB negotiation, ADC accuracy) at minimum and maximum rated temperature.
- **Design for test (DFT) saves development time.** Add test points for every power rail, critical signal, and programming interface. Include a UART debug header. Add an LED that the bootloader toggles — when the device won't boot, that LED tells you whether the bootloader ran.
- **Have a BOM risk plan.** Mark every component: single-source (risk), multi-source (safe), or EOL-risk (obsolete). For single-source parts, have an alternative part identified before the design review. Lead times > 20 weeks should trigger a back-up plan.
