# Leverage Calculation

## What Is Leverage?

**Leverage** measures how many callers benefit from a module's behavior. A deep module with high leverage is the ideal: lots of behavior, small interface, used everywhere. A deep module with low leverage is still good. A shallow module with high leverage is a liability that hurts many callers.

## Measuring Leverage

### Step 1: Count Callers
Count every production code site that calls a public method on the module. Exclude tests — they don't represent production benefit.

### Step 2: Estimate Benefit Per Caller
How many lines of code would each caller need to write if the module didn't exist? This is the module's value to each caller.

### Step 3: Compute Maintenance Cost
How many lines of code in the module itself? How many files change when the module changes?

### Step 4: Leverage Score
```
Leverage = (CallerCount × AvgBenefitPerCaller) / (ModuleLoC × ChangeFrequency)
```

## Interpretation

| Leverage Score | Classification |
|---------------|----------------|
| > 10 | High leverage — module is a codebase asset |
| 3-10 | Moderate leverage — acceptable, monitor |
| 1-3 | Low leverage — consider consolidating |
| < 1 | Negative leverage — module costs more than it saves |

## Depth vs. Leverage

A module can be deep (high behavior, low interface cost) but have low leverage (few callers). That's fine — depth is about internal quality. Leverage is about external impact. The best modules have both: deep internally, high leverage externally.
