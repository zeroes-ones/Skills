# Drawdown Analysis

## Drawdown Computation
```
Drawdown_t = (P_t / Running_Max_P_0_to_t) - 1
Max_Drawdown = min(Drawdown_t) over t
```

## Drawdown Properties
For each drawdown exceeding the minimum threshold (typically 5%):
| Property | Definition | Significance |
|----------|-----------|--------------|
| Depth | % decline from peak to trough | Measures severity |
| Duration | Days from peak to recovery | Measures time under water |
| Recovery Time | Days from trough to recovery | Measures bounce speed |
| Peak Date | Date of high-water mark before decline | Start of stress |
| Trough Date | Date of lowest point | Maximum pain |
| Recovery Date | Date when HWM is reclaimed | Stress ends |

## Drawdown Metrics
| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Average Drawdown | Mean of all DD depths | Typical stress event |
| Max Drawdown | Maximum DD depth | Worst-case historical |
| Drawdown Frequency | Count of DD events / Years | How often stress occurs |
| Ulcer Index | sqrt(Σ DD_t² / N) | Combines depth and duration |
| Pain Index | Average of all DD depths and durations | Comprehensive stress metric |

## Intra-Month Drawdown Estimation
If only monthly data is available:
```
Estimated_IntraMonth_MaxDD = Monthly_MaxDD * (1.3 to 1.5)
```
- Multiplier derived from comparison of daily vs monthly DD for similar strategies
- Higher multiplier for volatile strategies, lower for low-vol strategies
- [ESTIMATED] — daily data always preferred

## Underwater Chart Construction
An underwater chart plots drawdown over time:
```
Time on x-axis, Drawdown % on y-axis (from 0% to negative)
```
Key visual signals:
- Prolonged below 0%: extended recovery time
- Shallow but frequent: death by a thousand cuts
- Deep and fast: tail event
- Deep and prolonged: capital impairment

## Provenance
[COMPUTED] Drawdown methodology from risk management literature
[AS OF 2026-01]

