# Cross-Border Data Transfers

## Legal Framework Post-Schrems II

| Mechanism | Status | Requirements |
|-----------|--------|-------------|
| **EU-US Data Privacy Framework (DPF)** | Active (July 2023) | US organizations must self-certify annually; applies to EU→US transfers only |
| **Standard Contractual Clauses (SCCs 2021)** | Valid with restrictions | Transfer Impact Assessment (TIA) required; supplementary measures may be needed |
| **Binding Corporate Rules (BCRs)** | Valid for intra-group transfers | Approved by EU DPA; covers all entities in corporate group |
| **UK International Data Transfer Agreement (IDTA)** | Active (March 2022) | UK equivalent of SCCs; required for UK→third country transfers |
| **Adequacy Decisions** | Country-specific | List of countries deemed to provide adequate protection (Japan, South Korea, Canada, etc.) |

## Transfer Impact Assessment (TIA)

Required for every SCC-based transfer:

1. **Map the transfer**: What data? From where to where? Under what legal basis?
2. **Assess destination country laws**: Can government authorities access the data? (FISA 702, EO 12333 concerns)
3. **Evaluate necessity and proportionality**: Is the transfer necessary? Is the data minimized?
4. **Implement supplementary measures**: Technical (encryption with customer-held keys), organizational (data minimization), contractual (enhanced SCCs)
5. **Document**: Full TIA on file; reviewed annually or when laws change

## Data Residency Architecture Patterns

| Pattern | Description | Complexity | Best For |
|---------|-------------|-----------|----------|
| **Regional Deployment** | Full stack replicated in each region | High | High data volumes, strict sovereignty requirements |
| **Federated Data Stores** | Data stays in region, compute is global | Medium | Analytics, ML training, data warehousing |
| **Tokenization + Central Processing** | PII/PHI stays local, tokens flow globally | Medium | Low-latency global services with regional data |
| **Customer-Held Keys** | Data encrypted globally, keys held in region | Low | SaaS platforms, cloud services |
