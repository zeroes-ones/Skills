# Fraud Detection Architecture

Signal pipeline, velocity checks, ML scoring, decision engine design
for real-time financial fraud detection with <200ms p99 latency.

## Signal Pipeline Architecture

```
Transaction Events -> Signal Collection -> Feature Engineering -> Scoring -> Decision
```

### Signal Categories

| Category | Signals | Collection Method |
|----------|---------|-------------------|
| Transaction | amount, currency, MCC, timestamp, payment method, BIN | Payment gateway event |
| Device | fingerprint (canvas, WebGL, fonts, audio), IP, user agent, language, timezone, screen resolution | JS fingerprinting SDK |
| Behavioral | typing speed, mouse movements, navigation path, time-on-page, form completion time | JS behavioral SDK |
| Identity | account age, KYC level, previous disputes, email domain age, phone carrier, email verification status | User profile database |
| Network | IP reputation, ASN, proxy/VPN/Tor detection, hosting provider flag, IP geolocation | IP intelligence API |
| Historical | last 30-day tx count/amount, average ticket size, chargeback rate, device count, location count | Feature store |

## Velocity Checks (Foundation Layer)

Velocity is the highest-signal fraud indicator. Implement before any ML.

```
Window-based velocity per dimension:
  Account-level:    count of [tx, login, add-card, change-address] in [1m, 10m, 1h, 24h, 7d]
  Device-level:     distinct accounts per device fingerprint in [1h, 24h, 7d]
  IP-level:         distinct accounts, payment methods, shipping addresses in [1h, 24h]
  Geo-velocity:     distance between consecutive transactions / time difference
                    Flag if speed > 500 mph (commercial flight max)
  Amount velocity:  sum of transactions in rolling windows, Z-score from 30-day average

Threshold strategy:
  Use Z-score (dynamic) not fixed values:
    Z = (current_value - rolling_30d_mean) / rolling_30d_stddev
    Z > 3.0 -> high risk
    Z > 5.0 -> block
  This adapts to each user's normal behavior — a power user making 50 tx/day
  is not flagged, but a user jumping from 2 to 20 tx/day is.
```

## ML Scoring

### Supervised Model (Primary)
- Algorithm: XGBoost or LightGBM (gradient boosting trees)
- Labels: chargeback = fraud (positive), no chargeback after 120 days = legitimate
- Feature count: 100-200 engineered features
- Training: weekly retraining on rolling 6-month window
- Validation: time-based split (train on earlier, test on later data)

### Unsupervised Model (Secondary — Zero-Day Detection)
- Algorithm: Isolation Forest or Autoencoder
- No labels needed — detects anomalous patterns
- Use for: flagging novel fraud patterns not in training data
- Score: anomaly score combined with supervised score via weighted average

### Graph ML (Fraud Ring Detection)
- Build graph: nodes (account, device, IP, email, phone, address), edges (used-by, accessed-from)
- Community detection: Louvain algorithm on graph with fraud-labeled seeds
- Node embeddings: Node2Vec/GraphSAGE to create feature vectors
- Link prediction: probability that new account connects to known fraud community

## Real-Time Decision Engine

| Score Range | Action | Description |
|------------|--------|-------------|
| 0-19 | ALLOW | Low risk, no additional checks |
| 20-39 | ALLOW + MONITOR | Process but flag for post-transaction review |
| 40-59 | CHALLENGE | Step-up authentication: SCA, biometric, OTP |
| 60-79 | MANUAL REVIEW | Queue for human analyst (15-minute SLA) |
| 80-100 | BLOCK | High confidence fraud, block transaction |

### Decision Latency Budget
- Signal collection: <50ms
- Feature computation: <50ms
- Rule engine: <30ms
- ML inference: <50ms
- Decision + response: <20ms
- Total: <200ms p99
