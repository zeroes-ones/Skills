# Regression Guards

<!-- STANDARD: 3min -- guard design, and proving a guard can fail -->

## The third step

Fix, verify, guard. The guard is the step that makes the first two durable, and the one most often
skipped. Without it, a fixed accessibility defect returns — usually in the next component that
copies the pattern, and usually after the person who fixed it has moved on.

**A guard that has never failed has never been tested.** Asserting a guard exists is not enough; it
must be demonstrated to catch the defect's return.

## The proof procedure

```text
1. Write the guard.
2. Run it against the FIXED component → it must PASS.
3. Revert the fix (in a scratch branch, or by reintroducing the defect in a test fixture).
4. Run it against the REVERTED component → it must FAIL.
5. Re-apply the fix → it must PASS again.
```

Step 4 is the whole point. A guard that passes in both states asserts something unrelated to the
defect — a class name, a wrapper, an implementation detail — and would not catch a regression.

If step 4 cannot be made to fail, the guard is asserting the wrong thing. Replace it with one that
asserts the accessible **outcome**.

## Assert the outcome, not the implementation

| ❌ Guard asserts | ✅ Guard asserts |
|---|---|
| The component has class `btn--primary` | The rendered element has role `button` and an accessible name |
| `aria-label` is present | The accessible name equals the expected string |
| The DOM contains a `div[role="dialog"]` | The dialog has a name, is modal, and receives focus on open |
| A specific CSS rule exists | The focus indicator is visible against both the component and the page |
| The colour is `#767676` | The contrast ratio of the pair is at least the required value |

Outcome assertions survive refactors; implementation assertions break on every rename and, worse,
can pass while the accessible outcome is wrong.

## What to guard, per defect class

| Defect | The guard |
|---|---|
| Missing accessible name | Assert the name of every interactive element is non-empty and matches expectations |
| Wrong role | Assert the role/state on the widget's rendered output |
| Focus trap or lost focus | Assert focus position after open and after close |
| Silent live region | Assert the region exists before the update, and the content change occurs |
| Unassociated error | Assert the invalid state is set and the message is referenced |
| Contrast failure | Assert the computed ratio of each token pair against the required minimum |
| Colour-only meaning | Assert a text or icon affordance accompanies the coloured one |
| Focus ring removed | Assert a focus style is present and visible per theme |
| Reduced motion ignored | Assert the motion substitution applies under the preference |

## The token-level guard

Contrast is a token property (R6), so the strongest guard runs over the tokens, not the components:

```python
# Assert every recorded text/surface token pair meets its required ratio.
# This guard fails when the palette changes and a pairing drops below the threshold,
# which is exactly the regression a per-component fix would not catch.

MIN_NORMAL = 4.5
MIN_LARGE = 3.0

def test_token_contrast_pairs():
    for pair in load_declared_pairs():          # from the token file, not from the components
        ratio = contrast(pair["fg"], pair["bg"])
        required = MIN_LARGE if pair.get("large") else MIN_NORMAL
        assert ratio >= required, f"{pair['name']}: {ratio:.2f} < {required}"
```

The `load_declared_pairs` function matters: the pairs come from the **token file**, where the ratio
was recorded at design time, so adding a new token without checking its pairing fails the guard.

## The structural guard

For the ARIA and semantics defects that recur, a static check catches most of them:

```bash
# The mechanical guards — cheap, and they catch the common regressions
# 1. Click handlers on non-interactive elements (missing semantics + keyboard path)
if grep -rnE '<(div|span)[^>]*onClick' src/; then
  echo "FAIL: click handler on a non-interactive element"; exit 1
fi

# 2. ARIA on elements that already have the semantics
if grep -rnE '<(button|a|input|select|textarea)[^>]*role=' src/; then
  echo "FAIL: redundant role on a semantic element"; exit 1
fi

# 3. Focus visibility removed without a replacement
if grep -rn 'outline:\s*\(none\|0\)' src/ | grep -v -E 'focus-visible|focus-within'; then
  echo "FAIL: focus outline removed"; exit 1
fi

# 4. aria-hidden on focusable content
if grep -rn 'aria-hidden="true"' src/ | grep -iE 'button|link|input|tabindex'; then
  echo "FAIL: aria-hidden on focusable content"; exit 1
fi
```

These are coarse, and they will occasionally flag a legitimate case. That is acceptable: an
occasional false positive that a human dismisses with a comment is far cheaper than a silent
regression.

## Coordinating with the test suite

This skill defines *what* the guards assert; `accessibility-testing` builds the automated gates and
the CI integration. The division:

| This skill | `accessibility-testing` |
|---|---|
| The assertions that matter for each defect class | The runner, the CI wiring, the reporting |
| The token-contrast guard's semantics | Scheduled execution and thresholds in the pipeline |
| The structural greps | Lint integration and pre-commit hooks |
| The AT verification protocol | — (cannot be automated) |

The one thing that cannot be automated is AT verification. It is manual, per fix, and recorded.
Guards exist so that manual verification does not have to be repeated for every regression.

## The guard checklist

- [ ] Every fixed defect has a guard (CR14)
- [ ] Every guard was demonstrated to FAIL on the reverted fix
- [ ] Guards assert accessible outcomes, not implementation details
- [ ] Token contrast pairs are guarded at the token level, not per component
- [ ] Structural guards cover the common ARIA and semantics regressions
- [ ] Guards are wired into the pipeline (with `accessibility-testing`)
- [ ] False positives are handled by documented exceptions, not by weakening the guard
- [ ] The guard suite is reviewed as new defect classes are found
