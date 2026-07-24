# Transaction Security Patterns

Idempotency, dual control, transaction signing, and atomic guarantees
for financial payment systems handling high-value transfers.

## Idempotency Keys

### The Pattern
Every payment API must accept an idempotency key — a unique client-generated
identifier allowing safe retries without double-charging:

```python
# Stripe-style implementation
@router.post("/payments")
async def create_payment(
    payment: PaymentCreate,
    idempotency_key: str = Header(..., alias="Idempotency-Key")
):
    # Check for existing payment with same key
    existing = await db.find_one("payments", {"idempotency_key": idempotency_key})
    if existing:
        return existing.result  # Return same result, don't re-execute

    # Process new payment
    result = await process_payment(payment)
    await db.insert_one("payments", {
        "idempotency_key": idempotency_key,
        "result": result,
        "created_at": utcnow()
    })
    return result
```

### Key Requirements
- Uniqueness: client generates UUID v4, server scopes to merchant/account
- Persistence: store result for at least 24 hours (at least 7 days recommended)
- Status codes: same HTTP status code on replay (200 if succeeded, 409 if failed)
- Concurrent safety: use unique index + optimistic locking:`db.find_one_and_update( filter={id_key}, update={$setOnInsert: {status: "processing"}}, upsert=True)`
- Expiry: return `409 Conflict` if key >24h old and not found

## Dual Control (Four-Eyes Principle)

For transactions requiring two-person authorization:

### Implementation Pattern
```python
def dual_control_required(transaction_amount: Money) -> bool:
    thresholds = business_config.get("dual_control_thresholds", {
        "USD": 10_000_00,   # $10,000
        "EUR": 10_000_00,
        "GBP": 7_500_00,
        "JPY": 1_000_000,
    })
    return transaction_amount >= thresholds[transaction_amount.currency]
```

### Workflow
1. Maker initiates transaction with full details
2. System marks as PENDING_APPROVAL; holds funds (authorization) but does not settle
3. Checker (different person, must NOT be maker) views and approves/rejects
4. On approval, system settles transaction; on rejection, releases hold + notifies
5. Full audit log: maker identity, checker identity, timestamps, IPs, device fingerprints

### Enforcement Rules
- Maker and checker must be different users (enforced in code, not policy)
- Checker cannot modify transaction — only approve or reject (no alteration risk)
- Session timeout: approval pending >{time} triggers escalation to manager
- Thresholds configurable per currency, product, and jurisdiction

## Transaction Signing (Non-Repudiation)

Cryptographic proof that a specific party authorized a transaction:

```python
def sign_transaction(transaction: Dict, private_key: PrivateKey) -> bytes:
    # Canonical serialization (deterministic byte ordering)
    canonical = json.dumps(transaction, sort_keys=True, separators=(',', ':'))
    # Sign the hash
    signature = private_key.sign(
        hashlib.sha512(canonical.encode()).digest(),
        padding.PSS(mgf=padding.MGF1(hashlib.sha512()), salt_length=padding.PSS.MAX_LENGTH)
    )
    return base64.b64encode(signature)

def verify_transaction(transaction: Dict, public_key: PublicKey, signature: bytes) -> bool:
    canonical = json.dumps(transaction, sort_keys=True, separators=(',', ':'))
    try:
        public_key.verify(
            base64.b64decode(signature),
            hashlib.sha512(canonical.encode()).digest(),
            padding.PSS(mgf=padding.MGF1(hashlib.sha512()), salt_length=padding.PSS.MAX_LENGTH)
        )
        return True
    except InvalidSignature:
        return False
```

### What to Sign
- Transaction ID, amount, currency, timestamp, merchant/counterparty, payment method
- NOT: dynamic values (exchange rates, fee calculations, real-time balances)

## Atomic Transaction Guarantees

| Pattern | Description | Use When |
|---------|-------------|----------|
| 2PC (Two-Phase Commit) | Coordinator: prepare all → commit all. Blocks all resources during gap. | Single database, low contention |
| Saga (Choreographed) | Each step emits event → next step triggered. Compensating action per step. | Multiple services, independent scaling |
| Saga (Orchestrated) | Central orchestrator calls each step sequentially. Compensate in reverse order. | Complex workflows with dependencies |
| Outbox Pattern | Write business entity + outbox record in same DB transaction. Separate process reads outbox and publishes events. | Need guaranteed at-least-once delivery |

### Saga Compensating Transaction Example
```python
async def transfer_funds_saga(from_acct, to_acct, amount):
    steps = []
    try:
        # Step 1: Debit
        txn_id = await debit_account(from_acct, amount)
        steps.append(lambda: credit_account(from_acct, amount))  # compensate
        
        # Step 2: Credit  
        await credit_account(to_acct, amount)
        steps.append(lambda: debit_account(to_acct, amount))  # compensate
        
        return Success(txn_id)
    except Exception as e:
        # Compensate in reverse order
        for compensate in reversed(steps):
            await compensate()
        return Failure(e)
```
