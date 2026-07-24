# Constraint Inventory: Template and Methodology

## Constraint Categories

### Technical Constraints
- Language/platform requirements ("must run on Java 17")
- Integration requirements ("must use existing auth service")
- Infrastructure constraints ("must deploy to AWS us-east-1")
- Performance requirements ("must respond in < 200ms p95")

### Organizational Constraints
- Team capability ("team has Go experience, no Rust")
- Hiring velocity ("can hire 2 engineers/quarter")
- Ownership boundaries ("payments team owns payment flow")

### Budget Constraints
- Infrastructure budget ("$5K/month cloud budget")
- Tool/license budget ("can spend up to $10K/year on tools")
- Headcount ("2 engineers for 3 months")

### Timeline Constraints
- Hard deadlines ("regulatory compliance by Q3")
- Market windows ("competitor launching in 6 months")
- Contractual obligations ("client contract requires delivery by Dec")

### Regulatory Constraints
- Data residency ("EU user data must stay in EU")
- Compliance ("SOC 2 required for enterprise customers")
- Industry standards ("PCI-DSS for payment processing")

## Origin Tracking
For each constraint, document: Who established it? When? What problem did it solve? Is that problem still relevant?
