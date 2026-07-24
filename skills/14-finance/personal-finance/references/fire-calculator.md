# FIRE Calculator: Financial Independence, Retire Early

## The Core Formula

```
FI Number = Annual Expenses x 25 (for 4% rule, 30yr retirement)
          = Annual Expenses x 30 (for 3.33% rule, 40+ year retirement)
          = Annual Expenses x 33 (for 3% rule, perpetual withdrawal)

Years to FI = LN((FI Number x Rate of Return / Savings per Year) + 1) / LN(1 + Rate of Return)
```

## Savings Rate to Years-to-FI Table

Assumes 7% real return (10% nominal - 3% inflation), starting from $0 net worth.

| Savings Rate | Years to FI | Age if Starting at 25 | Age if Starting at 35 |
|-------------|-------------|----------------------|----------------------|
| 10% | 51 | 76 | 86 |
| 15% | 43 | 68 | 78 |
| 20% | 37 | 62 | 72 |
| 25% | 32 | 57 | 67 |
| 30% | 28 | 53 | 63 |
| 35% | 25 | 50 | 60 |
| 40% | 22 | 47 | 57 |
| 50% | 17 | 42 | 52 |
| 60% | 12.5 | 37.5 | 47.5 |
| 70% | 8.5 | 33.5 | 43.5 |
| 80% | 5.5 | 30.5 | 40.5 |

## Coast FIRE Calculator

```
Coast FIRE Number = FI Number / (1 + Expected Return)^Years to Traditional Retirement

Example:
  FI Number: $1,500,000
  Years to age 65: 25
  Expected return: 7%

  Coast FI = $1,500,000 / (1.07^25) = $1,500,000 / 5.427 = $276,400

  If current investments >= $276,400: You have reached Coast FIRE.
  No additional contributions needed to reach FI by 65.
```

## FIRE Type Calculator

```
Current annual expenses: $________
Target annual expenses in retirement: $________

Lean FIRE (bare minimum):    $________ x 25 = $________
Regular FIRE (comfortable):   $________ x 25 = $________
Fat FIRE (luxurious):        $________ x 25 = $________

Current portfolio: $________
Monthly contributions: $________
Expected return: ____% (use 5-7% real)

Projected FI date: ________ (age ____)

Coast FIRE: Already reached? ___ (Yes/No)
  If not, Coast FI number: $________
  Expected Coast FI date: ________
```

## Withdrawal Rate Safety

| Withdrawal Rate | 30-Year Success | 40-Year Success | 50-Year Success | Perpetual |
|----------------|-----------------|-----------------|-----------------|-----------|
| 3.0% | 100% | 100% | 100% | ~100% |
| 3.5% | 100% | 98% | 93% | ~95% |
| 4.0% | 95% | 87% | 78% | ~85% |
| 4.5% | 85% | 70% | 55% | ~70% |
| 5.0% | 70% | 50% | 35% | ~50% |

Source: Trinity Study extension, Monte Carlo simulations with 75% stocks / 25% bonds.

**Recommendation:** Use 3.5% for retirements >40 years, 4% for traditional 30-year retirement, 3% for multi-generational wealth.
