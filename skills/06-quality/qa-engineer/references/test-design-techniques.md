# Test Design Techniques — Deep Reference

> **Authoritative catalog of black-box test design techniques.** Each technique includes the underlying theory, step-by-step application guide, concrete code examples (Python/pytest), and decision rules for when to use it.

---

## 1. Equivalence Partitioning (EP)

### Theory
Given a domain of input values, partition it into **equivalence classes** — subsets where the system should behave identically for any member. If one value in a class detects a defect, all values in that class likely detect the same defect. Conversely, if one value passes, testing more values from the same class adds negligible confidence.

**Single-fault assumption**: Defects are rarely the product of two independent faults simultaneously. Therefore, test one invalid partition at a time while holding all others in valid partitions.

### Strength Levels

| Level | Description | When to Use |
|-------|-------------|-------------|
| **Weak normal** | One value from each valid class, no invalid classes | Smoke/regression, time-constrained runs |
| **Strong normal** | Cartesian product of all valid classes | Security, financial, safety-critical |
| **Weak robust** | One value from each valid class + one invalid class at a time | Standard functional testing |
| **Strong robust** | Cartesian product including invalid classes | Certification testing, FDA, DO-178C |

### Multi-Dimensional Partitioning Strategy

When inputs are interdependent (e.g., shipping cost depends on weight × destination × speed), don't partition each dimension in isolation. Use a **partition matrix**:

1. Identify all input dimensions.
2. For each dimension, list valid and invalid equivalence classes.
3. Create a decision table crossing dimensions where interactions matter.
4. Apply pairwise/orthogonal array reduction if the full matrix exceeds budget.

### Worked Example: Date Field (DD/MM/YYYY)

```python
import pytest
from datetime import date

# ── Equivalence classes for date-of-birth ──
# D1: Day   → valid (1-31), invalid (<1, >31), boundary-special (29-31 for Feb)
# D2: Month → valid (1-12), invalid (<1, >12)
# D3: Year  → valid (1900-current-18), invalid (<1900, >current-18, non-numeric)
# D4: Format → valid (DD/MM/YYYY), invalid (MM/DD/YYYY, YYYY-MM-DD, empty, "today")

# ── Weak robust test cases ──
# TC1: 15/06/1990 — all valid
# TC2: 00/06/1990 — invalid day (<1)
# TC3: 32/06/1990 — invalid day (>31)
# TC4: 15/00/1990 — invalid month (<1)
# TC5: 15/13/1990 — invalid month (>12)
# TC6: 15/06/1800 — invalid year (<1900)
# TC7: 15/06/2030 — invalid year (must be ≥ 18 years old)
# TC8: "abc"     — invalid format

DATE_CLASSES = {
    "valid": ["15/06/1990", "01/01/2000", "31/12/2005"],
    "day_too_low": ["00/06/1990"],
    "day_too_high": ["32/06/1990"],
    "month_too_low": ["15/00/1990"],
    "month_too_high": ["15/13/1990"],
    "year_too_low": ["15/06/1800"],
    "year_too_high": ["15/06/2030"],
    "non_date_string": ["abc", "", "15-06-1990", "06/15/1990"],
}

@pytest.mark.parametrize("dob", DATE_CLASSES["valid"])
def test_valid_dates_accepted(dob: str):
    """Any valid date within range should parse without error."""
    result = parse_date_of_birth(dob)
    assert result is not None
    assert isinstance(result, date)

@pytest.mark.parametrize("dob", DATE_CLASSES["day_too_low"] + DATE_CLASSES["day_too_high"])
def test_invalid_day_rejected(dob: str):
    """Day values outside 1-31 must produce a validation error."""
    with pytest.raises(ValidationError, match="day"):
        parse_date_of_birth(dob)

@pytest.mark.parametrize("dob", DATE_CLASSES["month_too_low"] + DATE_CLASSES["month_too_high"])
def test_invalid_month_rejected(dob: str):
    with pytest.raises(ValidationError, match="month"):
        parse_date_of_birth(dob)
```

### Worked Example: Username Field

```
Constraints: 3–20 chars, alphanumeric + underscore, must start with letter, case-insensitive uniqueness.

Partitions:
  P1 (length):   valid [3..20], invalid [0..2], invalid [21+]
  P2 (char set): valid [a-zA-Z0-9_], invalid [spaces, emoji, SQL meta, Unicode control]
  P3 (first char): valid [a-zA-Z], invalid [0-9, _]
  P4 (uniqueness): unique, duplicate (case-variant: "User" vs "user")

Risk-based selection: P4 (uniqueness) is critical for auth — test thoroughly.
P2 (SQL meta) is critical for security — include ' OR '1'='1, <script>, ../../../etc/passwd.
```

---

## 2. Boundary Value Analysis (BVA)

### Theory
Defects cluster at boundaries. If a system accepts integers 1–100, the highest-probability failure points are 0, 1, 2, 99, 100, 101 — not 50.

### 2-Value vs 3-Value Boundary

| Technique | Tests per Boundary | Example (range 1–100) | Confidence |
|-----------|-------------------|----------------------|------------|
| **2-value** | boundary, boundary+1 | 1, 2, 100, 101 | Standard |
| **3-value** | boundary-1, boundary, boundary+1 | 0, 1, 2, 99, 100, 101 | Higher (catches off-by-2) |

**Decision rule**: Use 3-value for financial calculations, safety-critical, and any boundary involving currency or user safety. Use 2-value for standard business logic.

```python
# ── BVA: Age field (valid range 18–120) ──

BOUNDARY_AGES = [
    # (value, expected_valid)
    (17, False),   # boundary-1 (3-value lower)
    (18, True),    # boundary   (lower)
    (19, True),    # boundary+1 (3-value lower)
    (119, True),   # boundary-1 (3-value upper)
    (120, True),   # boundary   (upper)
    (121, False),  # boundary+1 (3-value upper)
]

@pytest.mark.parametrize("age,expected", BOUNDARY_AGES)
def test_age_boundaries(age: int, expected: bool):
    result = validate_age(age)
    assert result == expected, f"Age {age} should be {'valid' if expected else 'invalid'}"


# ── BVA: Ordered sets ──
# A dropdown "Priority" with options: [Low, Medium, High, Critical]
# Boundaries: first item (Low), last item (Critical)
# Also test: selection by index, selection by value, default selection (none)

ORDERED_SET_TESTS = [
    ("Low", True),
    ("Critical", True),
    ("Medium", True),
    ("NonExistent", False),
    (None, False),     # no selection
]

# ── BVA: Collections ──
# "Select 1–5 tags"
@pytest.mark.parametrize("count,expected", [
    (0, False),   # empty
    (1, True),    # boundary lower
    (5, True),    # boundary upper
    (6, False),   # boundary+1
    (100, False), # excessive
])
def test_tag_selection_count(count: int, expected: bool):
    tags = [f"tag_{i}" for i in range(count)]
    assert validate_tag_selection(tags) == expected

# ── BVA: Time-based inputs ──
# "Start date must be before end date, max range 365 days"
# Boundaries: same day, 1 day apart, 365 days apart, 366 days apart, reversed order
TIME_BOUNDARY_TESTS = [
    ("2025-01-01", "2025-01-01", False, "same day"),
    ("2025-01-01", "2025-01-02", True, "1 day apart"),
    ("2025-01-01", "2025-12-31", True, "365 days — max allowed"),
    ("2025-01-01", "2026-01-01", False, "366 days — exceeds max"),
    ("2025-06-01", "2025-01-01", False, "end before start"),
]
```

---

## 3. Decision Tables

### Theory
When business rules involve multiple conditions that combine to produce specific actions, decision tables provide exhaustive coverage of condition combinations. Every column is a test case.

### Structure

| Component | Description |
|-----------|-------------|
| **Condition stub** | List of all conditions (inputs) |
| **Action stub** | List of all possible actions (outputs) |
| **Rule columns** | Each column = one combination of conditions → actions |

**Rule count**: For n binary conditions, there are 2^n rules before collapsing.

### Collapsing Rules

When two rules differ in only one condition but produce identical actions, and that condition doesn't affect the outcome, replace the differing condition with "—" (don't care). This reduces test count without loss of coverage.

### Limited-Entry vs Extended-Entry

| Type | Condition Values | Example |
|------|-----------------|---------|
| **Limited-entry** | Binary (T/F, Y/N) | "Is employed? Y/N" |
| **Extended-entry** | Multi-valued | "Income: <50K / 50–100K / >100K" |

### Worked Example: Loan Approval

```
Conditions:
  C1: Credit score > 700          (Y/N)
  C2: Income > $50,000            (Y/N)
  C3: Employment > 2 years        (Y/N)
  C4: Existing debt < 40% income  (Y/N)

Actions:
  A1: Approve
  A2: Approve with higher rate
  A3: Reject
  A4: Request co-signer
```

**Full table (16 rules) → Collapsed (8 rules):**

```
┌──────────────────────┬────┬────┬────┬────┬────┬────┬────┬────┐
│ Conditions           │ R1 │ R2 │ R3 │ R4 │ R5 │ R6 │ R7 │ R8 │
├──────────────────────┼────┼────┼────┼────┼────┼────┼────┼────┤
│ C1: Score > 700      │ Y  │ Y  │ Y  │ Y  │ N  │ N  │ N  │ N  │
│ C2: Income > 50K     │ Y  │ Y  │ N  │ N  │ —  │ —  │ —  │ —  │
│ C3: Employment > 2yr │ Y  │ N  │ Y  │ N  │ Y  │ Y  │ N  │ N  │
│ C4: Debt < 40%       │ —  │ —  │ Y  │ N  │ Y  │ N  │ Y  │ N  │
├──────────────────────┼────┼────┼────┼────┼────┼────┼────┼────┤
│ Actions              │    │    │    │    │    │    │    │    │
├──────────────────────┼────┼────┼────┼────┼────┼────┼────┼────┤
│ A1: Approve          │ X  │    │    │    │    │    │    │    │
│ A2: Higher rate      │    │ X  │    │    │    │    │    │    │
│ A3: Reject           │    │    │    │ X  │    │ X  │ X  │ X  │
│ A4: Co-signer        │    │    │ X  │    │ X  │    │    │    │
└──────────────────────┴────┴────┴────┴────┴────┴────┴────┴────┘
```

```python
import pytest

LOAN_DECISION_TABLE = [
    # (score_gt_700, income_gt_50k, emp_gt_2yr, debt_lt_40pct, expected_action)
    (True,  True,  True,  True,  "approve"),
    (True,  True,  True,  False, "approve"),  # C4 = don't care when first 3 are Y
    (True,  True,  False, True,  "higher_rate"),
    (True,  True,  False, False, "higher_rate"),
    (True,  False, True,  True,  "co_signer"),
    (True,  False, True,  False, "co_signer"),
    (True,  False, False, True,  "co_signer"),
    (True,  False, False, False, "reject"),
    (False, True,  True,  True,  "co_signer"),
    (False, True,  True,  False, "reject"),
    (False, True,  False, True,  "reject"),
    (False, True,  False, False, "reject"),
    (False, False, True,  True,  "co_signer"),
    (False, False, True,  False, "reject"),
    (False, False, False, True,  "reject"),
    (False, False, False, False, "reject"),
]

@pytest.mark.parametrize("score,income,emp,debt,expected", LOAN_DECISION_TABLE)
def test_loan_decision_table(score, income, emp, debt, expected):
    result = evaluate_loan(credit_score_gt_700=score, income_gt_50k=income,
                           employment_gt_2yr=emp, debt_lt_40pct=debt)
    assert result.action == expected
```

---

## 4. State Transition Testing

### Theory
Systems that exhibit different behavior based on current state (workflows, sessions, order lifecycles) must be tested for every valid transition, invalid transition, and transition sequence.

### Notation

| Element | Symbol | Meaning |
|---------|--------|---------|
| State | Rectangle | A stable condition of the system |
| Transition | Arrow S1→S2 | Movement from one state to another |
| Event | Label on arrow | The trigger that causes the transition |
| Guard | [condition] | Precondition for the transition to fire |
| Action | /action() | Side effect executed during transition |

### N-Switch Coverage

| Level | Definition | Tests |
|-------|-----------|-------|
| **0-switch** | Every individual transition | 1 transition at a time |
| **1-switch** | Every pair of consecutive transitions | 2 transitions in sequence |
| **2-switch** | Every triple of consecutive transitions | 3 transitions in sequence |

**Decision rule**: 0-switch for standard features, 1-switch for payment/auth workflows, 2-switch for safety-critical state machines. Each additional switch level roughly squares the test count.

### Worked Example: Order Lifecycle

```
States: Cart → Placed → Confirmed → Shipped → Delivered
                                ↘ Cancelled
                                ↘ Returned

Transitions:
  T1: Cart      → Placed     [checkout]
  T2: Placed    → Confirmed  [payment_captured]
  T3: Placed    → Cancelled  [payment_failed | user_cancelled < 30min]
  T4: Confirmed → Shipped    [warehouse_picked]
  T5: Confirmed → Cancelled  [out_of_stock | fraud_review_failed]
  T6: Shipped   → Delivered  [carrier_confirmed]
  T7: Delivered → Returned   [return_requested < 30days]
  T8: Shipped   → Cancelled  [lost_in_transit]
```

```python
from enum import Enum, auto
import pytest

class OrderState(Enum):
    CART = auto()
    PLACED = auto()
    CONFIRMED = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()
    RETURNED = auto()

# 0-switch: every individual transition
ZERO_SWITCH_TESTS = [
    # (from_state, event, to_state)
    (OrderState.CART,      "checkout",              OrderState.PLACED),
    (OrderState.PLACED,    "payment_captured",      OrderState.CONFIRMED),
    (OrderState.PLACED,    "payment_failed",        OrderState.CANCELLED),
    (OrderState.PLACED,    "user_cancelled",        OrderState.CANCELLED),
    (OrderState.CONFIRMED, "warehouse_picked",      OrderState.SHIPPED),
    (OrderState.CONFIRMED, "out_of_stock",          OrderState.CANCELLED),
    (OrderState.CONFIRMED, "fraud_review_failed",   OrderState.CANCELLED),
    (OrderState.SHIPPED,   "carrier_confirmed",     OrderState.DELIVERED),
    (OrderState.DELIVERED, "return_requested",      OrderState.RETURNED),
    (OrderState.SHIPPED,   "lost_in_transit",       OrderState.CANCELLED),
]

@pytest.mark.parametrize("from_state,event,expected_state", ZERO_SWITCH_TESTS)
def test_order_transitions(from_state, event, expected_state):
    order = create_order_in_state(from_state)
    result = order.apply_event(event)
    assert result.state == expected_state

# Invalid transitions — must not change state
INVALID_TRANSITIONS = [
    (OrderState.CART,      "payment_captured"),   # can't pay before checkout
    (OrderState.DELIVERED, "warehouse_picked"),    # can't ship delivered
    (OrderState.CANCELLED, "carrier_confirmed"),   # can't deliver cancelled
    (OrderState.RETURNED,  "warehouse_picked"),    # can't ship returned
    (OrderState.CART,      "return_requested"),    # can't return from cart
]

@pytest.mark.parametrize("from_state,event", INVALID_TRANSITIONS)
def test_invalid_transitions_raise_error(from_state, event):
    order = create_order_in_state(from_state)
    with pytest.raises(InvalidTransitionError):
        order.apply_event(event)

# 1-switch: pairs of consecutive transitions
ONE_SWITCH_TESTS = [
    # checkout → payment success path
    (OrderState.CART, ["checkout", "payment_captured"], OrderState.CONFIRMED),
    # checkout → payment failure
    (OrderState.CART, ["checkout", "payment_failed"], OrderState.CANCELLED),
    # full happy path
    (OrderState.CART, ["checkout", "payment_captured", "warehouse_picked"],
     OrderState.SHIPPED),
]

@pytest.mark.parametrize("from_state,events,expected_state", ONE_SWITCH_TESTS)
def test_order_transition_sequences(from_state, events, expected_state):
    order = create_order_in_state(from_state)
    for event in events:
        order.apply_event(event)
    assert order.state == expected_state

# ── State transition tree (exhaustive depth-2 from PLACED) ──
# PLACED → Confirmed → Shipped
# PLACED → Confirmed → Cancelled (out_of_stock)
# PLACED → Confirmed → Cancelled (fraud)
# PLACED → Cancelled (payment_failed)
# PLACED → Cancelled (user_cancelled)
# This gives us test coverage of all 2-transition paths from PLACED.
```

---

## 5. Pairwise / Orthogonal Array Testing

### Theory
Most software defects are caused by a single condition or the interaction of **two** conditions. Higher-order interactions (3-way, 4-way) are exponentially rarer. Pairwise testing covers all 2-way interactions, reducing the test space from exponential to roughly O(v² × log k) where v = values per parameter and k = parameters.

### The Combinatorial Explosion Problem

| Params | Values Each | Exhaustive | Pairwise (~) |
|--------|------------|------------|--------------|
| 5 | 2 | 32 | 6 |
| 10 | 2 | 1,024 | 14 |
| 10 | 3 | 59,049 | 17 |
| 5 | 5 | 3,125 | 29 |
| 20 | 2 | 1,048,576 | 22 |

### Tools

| Tool | Language | Key Feature |
|------|----------|-------------|
| **PICT** (Microsoft) | CLI | Constraints via `IF [A] = "X" THEN [B] <> "Y"` |
| **ACTS** (NIST) | CLI/GUI | Supports up to 6-way coverage, constraint solver |
| **AllPairs** | Python | `metacomm.com' library, ~50 lines of Python |
| **pairwise** | npm | `pairwise` npm package, JS-friendly |
| **Hexawise** | SaaS | Visual modeling, requirements traceability |

### Worked Example: Cross-Browser Configuration

```
Parameters:
  Browser:  Chrome, Firefox, Safari, Edge        (4 values)
  OS:       Windows 10, Windows 11, macOS 14, Ubuntu 22.04  (4 values)
  Screen:   1366×768, 1920×1080, 2560×1440, 375×812 (mobile) (4 values)
  Network:  WiFi, 4G, 3G, Offline                 (4 values)
  Auth:     OAuth, Password, SSO, Guest            (4 values)

Exhaustive: 4^5 = 1,024 combinations
Pairwise:   ~20 combinations (generated via PICT/AllPairs)
```

```python
from allpairspy import AllPairs

parameters = [
    ["Chrome", "Firefox", "Safari", "Edge"],
    ["Windows 10", "Windows 11", "macOS 14", "Ubuntu 22.04"],
    ["1366x768", "1920x1080", "2560x1440", "375x812"],
    ["WiFi", "4G", "3G", "Offline"],
    ["OAuth", "Password", "SSO", "Guest"],
]

print("Pairwise test suite (AllPairs):")
for i, combo in enumerate(AllPairs(parameters), 1):
    print(f"  TC{i:02d}: {combo}")

# ── PICT model file (browser_config.pict) ──
"""
Browser:  Chrome, Firefox, Safari, Edge
OS:       Windows 10, Windows 11, macOS 14, Ubuntu 22.04
Screen:   1366x768, 1920x1080, 2560x1440, 375x812
Network:  WiFi, 4G, 3G, Offline
Auth:     OAuth, Password, SSO, Guest

# Constraints
IF [Browser] = "Safari" THEN [OS] IN {"macOS 14"}
IF [Browser] = "Edge" THEN [OS] IN {"Windows 10", "Windows 11"}
IF [Network] = "Offline" THEN [Auth] = "Guest"
"""

import subprocess, json

def generate_pict_tests(model_path: str, order: int = 2) -> list[dict]:
    """Run PICT with n-way coverage and parse tab-separated output."""
    result = subprocess.run(
        ["pict", model_path, f"/o:{order}"],
        capture_output=True, text=True
    )
    lines = result.stdout.strip().split("\n")
    headers = lines[0].split("\t")
    return [dict(zip(headers, line.split("\t"))) for line in lines[1:]]

@pytest.mark.parametrize("config", generate_pict_tests("browser_config.pict"))
def test_cross_browser_pairwise(config: dict):
    """Verify login works across all pairwise browser × OS × screen combinations."""
    result = run_login_test(
        browser=config["Browser"],
        os=config["OS"],
        screen=config["Screen"],
        network=config["Network"],
        auth=config["Auth"],
    )
    assert result.success, f"Login failed for config: {config}"
```

### Coverage Guarantees

| Coverage Level | Interaction Depth | When to Use |
|---------------|-------------------|-------------|
| **Pairwise (2-way)** | All pairs of parameters | Standard risk |
| **3-way** | All triples | Financial, medical, aviation |
| **4-way** | All quads | Life-critical systems |
| **Exhaustive** | Full Cartesian | < 100 total combos |

---

## 6. Error Guessing

### Theory
Leverage experience, domain knowledge, and heuristics catalogs to anticipate where bugs are likely to reside. This is not random guessing — it's structured, experience-driven probe testing.

### Heuristics Catalog

```python
# ── Systematic error guessing heuristics catalog ──

ERROR_HEURISTICS = {
    "null_and_empty": [
        None, "", [], {}, set(), 0, 0.0, False,
        "   ", "\t", "\n", "\r\n",
    ],
    "boundary_busters": [
        -1, 0, 1, 2**31 - 1, 2**31, 2**63 - 1, 2**63,
        -2**31, -2**63, float("inf"), float("-inf"), float("nan"),
    ],
    "special_characters": [
        "O'Brien",           # SQL quote
        "'; DROP TABLE--",   # SQL injection
        "<script>alert(1)</script>",  # XSS
        "&amp;&lt;&gt;",     # HTML entities
        "../../../etc/passwd",  # Path traversal
        "\\x00\\x1F\\x7F",   # Control characters
        "𝕳𝖊𝖑𝖑𝖔",             # Unicode outside BMP
        "Z͑ͫ̓ͪ̂ͫ̽͏̴͙̤̞͉A͗ͫ͗̅ͦ̃ͥͤͥ҉̵̫̟̥Lͧͩ͆͑̋G̺̳̞̬ͤͩ͗͒ͮ͊̓͜O̽̈́̓̿ͯͤ",  # Zalgo text
        "\u200B\u200C\u200D",  # Zero-width characters
    ],
    "concurrent_and_timing": [
        "rapid_double_click",
        "submit_twice_before_response",
        "back_button_during_processing",
        "browser_refresh_during_post",
        "timeout_mid_transaction",
        "clock_change_during_session",  # DST transition
    ],
    "data_type_confusion": [
        "123" (string where int expected),
        123   (int where string expected),
        "true" (string) vs True (boolean),
        "2025-13-45" (impossible date),
        "not-an-email",
        "00000000000",  # all zeros where unique ID expected
    ],
}

@pytest.mark.parametrize("malicious_input", ERROR_HEURISTICS["special_characters"])
def test_search_field_rejects_special_chars(malicious_input):
    """Search field must sanitize or reject known attack vectors."""
    response = api_search(query=malicious_input)
    assert response.status_code in (200, 422), "Should not 500 on special chars"
    if response.status_code == 200:
        assert malicious_input not in response.text  # must be escaped

@pytest.mark.parametrize("empty_value", ERROR_HEURISTICS["null_and_empty"])
def test_required_fields_reject_empty(empty_value):
    with pytest.raises(ValidationError):
        validate_required_field("username", empty_value)
```

### Risk-Based Error Guessing

Assign exploitability scores when prioritizing:

```
Risk = Exploitability × Impact

Exploitability factors:
  - Input is user-controlled: +3
  - Input appears in URLs: +2
  - Input is stored and displayed: +3
  - Input is used in SQL/OS command: +5
  - Input is processed by legacy system: +1
```

---

## 7. Use Case Testing

### Theory
Tests derived from use cases (requirements artifacts) verify that the system delivers value through realistic user scenarios. Unlike atomic test techniques, use case testing follows end-to-end threads.

### Structure

| Scenario Type | Coverage | Example |
|--------------|----------|---------|
| **Main success scenario** | The happy path | User places order successfully |
| **Alternate flows** | Different valid paths to success | User applies coupon, user uses gift card |
| **Exception flows** | Error recovery paths | Payment declined → retry with different card |
| **Perverse flows** | Deliberately malicious/bizarre | Rapid add-remove-add of same item 100× |

```python
# ── Use case: "Customer checks out shopping cart" ──

class TestCheckoutUseCase:
    """Use case UC-07: Checkout."""

    def test_main_success_scenario(self, authenticated_user, cart_with_items):
        """1. User views cart → 2. Enters shipping → 3. Selects payment →
           4. Reviews order → 5. Confirms → 6. Receives confirmation."""
        cart_page = CartPage.open()
        assert cart_page.item_count == 3

        shipping_page = cart_page.proceed_to_shipping()
        shipping_page.fill_address(standard_us_address())
        shipping_page.select_method("Standard (3-5 days)")

        payment_page = shipping_page.continue_to_payment()
        payment_page.enter_card("4242424242424242", "12/28", "123")

        review_page = payment_page.review_order()
        assert review_page.total == cart_with_items.expected_total

        confirmation_page = review_page.confirm_order()
        assert confirmation_page.order_number is not None
        assert confirmation_page.message == "Order confirmed"

    def test_alternate_flow_apply_coupon(self, authenticated_user, cart_with_items):
        """User applies a valid coupon, discount is reflected in total."""
        cart_page = CartPage.open()
        cart_page.apply_coupon("SAVE20")
        assert cart_page.discount_amount > 0
        assert cart_page.total == cart_with_items.subtotal - cart_page.discount_amount

    def test_exception_flow_payment_declined(self, authenticated_user, cart_with_items):
        """Payment declined → error message → user retries with different card."""
        payment_page = CartPage.open().proceed_to_shipping() \
            .fill_address(standard_us_address()).select_method("Standard") \
            .continue_to_payment()

        payment_page.enter_card("4000000000000002", "12/28", "123")  # decline card
        payment_page.submit()
        assert payment_page.has_error("Card declined")

        payment_page.enter_card("4242424242424242", "12/28", "123")
        review_page = payment_page.submit()
        assert review_page.is_displayed()

    def test_perverse_flow_rapid_checkout_attempts(self, authenticated_user, cart_with_items):
        """User rapidly submits checkout 5× within 1 second — no duplicate orders."""
        import asyncio
        order_ids = []
        for _ in range(5):
            response = api_post_checkout(cart_id=cart_with_items.id)
            if response.status_code == 201:
                order_ids.append(response.json()["order_id"])
        assert len(order_ids) == 1, "Idempotency failed — duplicate orders created"

# Scenario coverage metrics
SCENARIO_COVERAGE = {
    "main_success": "1 of 1 covered",
    "alternate_flows": "3 of 5 covered (coupon, gift_card, guest_checkout — missing: express_checkout, split_payment)",
    "exception_flows": "2 of 3 covered (payment_declined, item_out_of_stock — missing: shipping_unavailable)",
    "perverse_flows": "1 of 2 covered (rapid_duplicate — missing: concurrent_checkout_two_tabs)",
}
```

---

## Technique Selection Decision Tree

```
Is the input domain continuous or range-based?
  ├─ YES → Equivalence Partitioning + Boundary Value Analysis
  │        3-value BVA for financial/safety, 2-value for standard
  │
  └─ NO → Are there complex business rules with multiple interacting conditions?
           ├─ YES → Decision Table
           │        Collapse "don't care" rules to minimize test count
           │
           └─ NO → Does the system have distinct states with transitions?
                    ├─ YES → State Transition Testing
                    │        0-switch minimum, 1-switch for auth/payment
                    │
                    └─ NO → Do multiple parameters interact combinatorially?
                             ├─ YES → Pairwise Testing (if exhaustively infeasible)
                             │
                             └─ NO → Are there clear user scenarios?
                                      ├─ YES → Use Case Testing
                                      └─ NO → Error Guessing + Exploratory
```

---

## Combining Techniques (Test Strategy Integration)

For a single feature — e.g., "password reset" — combine:

| Technique | What It Covers |
|-----------|---------------|
| **Equivalence partitioning** | Valid/invalid email formats, token validity classes |
| **Boundary value analysis** | Token expiry at boundaries (just expired, just valid) |
| **State transition** | States: idle → email_sent → token_validated → password_changed |
| **Error guessing** | SQL injection in email, token reuse, brute force rate limiting, HTML injection in reset page |
| **Use case** | "User resets forgotten password" — main + alternate + exception flows |

This layered approach provides depth that no single technique achieves alone.
