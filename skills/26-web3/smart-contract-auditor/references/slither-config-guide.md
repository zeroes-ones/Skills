# Slither Configuration Guide

## Installation
```bash
pip install slither-analyzer
slither --version  # verify
```

## Base Configuration (slither.config.json)
```json
{
  "detectors_to_run": "reentrancy-eth,reentrancy-no-eth,reentrancy-events,unchecked-transfer,access-control,delegatecall,arbitrary-send,timestamp,assembly,low-level-calls,naming-convention,pragma,unused-state,dead-code",
  "filter_paths": "test|mock|Migrations",
  "exclude_dependencies": true
}
```

## Key Detectors
| Detector | Severity | What It Finds |
|----------|----------|---------------|
| reentrancy-eth | High | ETH reentrancy via .call{}() |
| reentrancy-no-eth | High | State reentrancy without ETH |
| unchecked-transfer | High | Unchecked low-level calls |
| delegatecall | High | delegatecall usage patterns |
| arbitrary-send | High | ETH send to arbitrary addresses |
| timestamp | Medium | block.timestamp dependence |
| assembly | Low | Inline assembly usage |

## Triage Mode
```bash
# Fast scan for critical only
slither . --detect reentrancy-eth,reentrancy-no-eth,delegatecall,unchecked-transfer

# Print call graph
slither . --print call-graph > call-graph.dot

# Human-readable summary
slither . --print human-summary
```

## CI Integration
```yaml
- name: Slither Static Analysis
  run: |
    pip install slither-analyzer
    slither . --fail-high --exclude-dependencies
```
