# Provenance and Trust

An entry you cannot age is an entry you cannot trust.

## Required fields on every write

| Field | Why |
|---|---|
| `source` | Who or what produced it; enables auditing |
| `timestamp` | Enables ageing and retention |
| `workflow` | Enables scoping retrieval to a task class |
| `run_id` | Enables tracing back to the actual run |
| `outcome` | Turns a conclusion into a record with a result |
| `trust` | Standing: verified fact, conclusion, preference, estimate |

## Trust classes

| Class | Meaning | Retention |
|---|---|---|
| `verified_fact` | Externally confirmed | Long; no ageing |
| `context_only` | A run's conclusion | Ages out; retrievable as prior |
| `user_stated` | A declared preference | Until superseded |
| `estimated` | Derived; carries its assumption | Short; must show the assumption |

## Failure modes

- **No timestamp.** Cannot age; cannot apply retention.
- **No source.** Cannot audit; cannot judge whether to trust.
- **Conclusion stored as fact.** Later runs inherit an error as a premise.
- **Trust class missing.** Everything degrades to the weakest handling — or worse, to trust.
- **Assumption dropped from an estimate.** The number survives without its caveat, which is how a guess becomes a premise.
- **Provenance added only at consolidation.** Too late; the original context is gone.
