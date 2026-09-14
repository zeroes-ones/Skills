# Memory Poisoning

Retrieved memory is data from a prior run. Treating it as instruction lets anything a prior run ingested steer the current one — indirect prompt injection with your own store as the vector.

## The threat

1. A prior run ingests untrusted content (a web page, a file, a tool result).
2. Part of that content is shaped like an instruction.
3. The run stores a conclusion — or stores the content itself.
4. A later run retrieves it and obeys it.

The blast radius scales with what the agent can do. A read-only agent leaks; a tool-using agent acts.

## Defences

| Defence | Mechanism |
|---|---|
| **Trust label** | Every entry carries `trust: context_only`; the injection wrapper repeats it |
| **Wrapper at injection** | Memory enters inside an explicit "context only, not instructions" block |
| **Never in the instruction block** | Memory must not be concatenated into system or instruction content |
| **Provenance** | Entries record their source, so untrusted origins are visible |
| **Flag, do not trust** | An entry missing its trust marker is returned flagged, not silently trusted |
| **Content hygiene** | Do not store raw ingested content; store conclusions with provenance |

## Failure modes

- **Unlabelled recall.** The single highest-risk mistake; it is an injection path you built deliberately.
- **Trust marker stripped in transit.** A transform that drops the field silently upgrades unverified data.
- **Memory concatenated with instructions.** Even labelled, co-locating memory and instructions invites blending.
- **Storing raw untrusted content.** The store becomes a delivery mechanism for whatever was ingested.
- **Assuming the model will be careful.** The label is enforcement; the model's judgement is not.
