# Source-of-Truth Anchoring — The Anti-Hallucination Pattern

> **Purpose:** This reference teaches skills how to anchor themselves to runtime reality — the actual installed versions of frameworks, languages, and libraries — instead of relying on training data which may be stale or hallucinated. When a skill follows this pattern, it cannot generate code for APIs that don't exist in the user's installed versions.

## The Problem: Training Data Is Always Stale

Every AI model has a training cutoff. If the model was trained in January 2024 but the user has Next.js 15 (released October 2024), the model will generate Next.js 14 API calls. Those calls **will fail**. The model doesn't know they'll fail because it doesn't know Next.js 15 exists.

**The same problem applies to every framework, library, and language runtime.** The model's "knowledge" is frozen at its training cutoff, but the user's project is living code with actively maintained dependencies.

## The Solution: Read Before You Write

Instead of generating code from memory, skills must:

1. **Detect** which frameworks and versions are actually installed using `scripts/runtime-version-detect.sh`
2. **Anchor** all API usage to those detected versions
3. **Verify** that proposed API calls exist in the detected version's documentation
4. **Calibrate** — when the detected version is newer than training data, explicitly state lower confidence and request user verification

## How to Use `runtime-version-detect.sh`

### Step 1: Run Detection on the Target Project
```bash
# Run against the user's project, not the skill repository
./scripts/runtime-version-detect.sh /path/to/user/project --skill-context
```

### Step 2: Parse the Output
The `--skill-context` flag outputs a block designed for the skill to consume:

```
## Runtime Environment Detected
- **node** 22.4.1 (pm: npm)
  - react: 19.0.0
  - next: 15.1.0
  - prisma: 6.0.0
  - tailwindcss: 4.0.0

**Documentation to consult:**
- react v19.0.0: https://react.dev/reference/react/
- next v15.1.0: https://nextjs.org/docs/
- prisma v6.0.0: https://www.prisma.io/docs/
```

### Step 3: Anchor Your Code Generation
For every framework-specific API call, compare against the detected version:

```
DETECTED: next@15.1.0
→ If next@15 is newer than training data:
  → Prefer Next.js 15 docs over training data
  → Generate with // VERIFY: comments on framework-specific API calls
  → Request user to validate generated code against their installed version
```

## Confidence Calibration System

| Situation | Confidence | What to Do |
|---|---|---|
| Detected version ≤ training cutoff AND API is well-known | **HIGH** | Generate normally. Use type-safe patterns from training data. |
| Detected version ≤ training cutoff but API is obscure | **MEDIUM** | Generate with `// VERIFY:` comment on obscure API calls. |
| Detected version > training cutoff (new major) | **LOW** | Generate structure only. Add `// VERIFY: This API may have changed in v{N}` on every framework-specific call. Request user to check docs. |
| Detection failed (no lockfile found) | **UNKNOWN** | Ask user for framework versions. Do not guess. Never say "I'll use the latest version." |
| Detection found a framework not in training data | **NONE** | Refuse to generate framework-specific code. "I don't have knowledge of {framework}. I can generate a structural outline, but please verify API correctness." |

## Token Efficiency: The Context-Aware Approach

Loading the full version detection output into every skill invocation would waste tokens. Instead:

1. **Cache the detection output** — Run once per session, store in session state
2. **Include only relevant frameworks** — Frontend skill only loads React/Next/Vue versions; backend skill only loads Node/Python/Go versions
3. **Use the doc URL, not the full docs** — Reference doc URLs rather than loading full documentation into context

### Token Budget Impact
| Approach | Tokens Used | Accuracy |
|---|---|---|
| No anchoring (rely on training data) | 0 extra | ~70% (hallucinations on new APIs) |
| Version + doc URL anchoring | ~80 tokens | ~95% (versions known, APIs verifiable) |
| Full API signature verification | ~500 tokens | ~99% (validates actual installed types) |

## Integration Points in SKILL.md

### 1. Ground Rule
```
| Rn | **ANCHOR to runtime versions before generating code.** Never generate framework-specific API calls from training data alone. Run runtime-version-detect.sh on the target project, compare detected versions against training cutoff, calibrate confidence. | Trigger: skill receives code-generation task involving framework-specific APIs | Respond: "Detected {framework}@{version}. Anchoring all API calls to v{version}. I will flag uncertain APIs with // VERIFY: comments." |
```

### 2. Pre-Flight Verification (add to Core Workflow Phase 1)
```
Before generating any code:
1. Run runtime-version-detect.sh on the target project
2. If detection succeeds:
   a. List detected frameworks and versions
   b. Compare against training cutoff
   c. Calibrate confidence per the calibration table
3. If detection fails:
   a. Ask user: "What version of {framework} are you using?"
   b. Do not proceed without version information
```

## Anti-Patterns: What Anchoring Replaces

| Anti-Pattern | Why It Fails | Anchoring Fix |
|---|---|---|
| "Here's how to set up a Next.js app" | Uses latest template from training data | "Detected Next.js 14.2. Using Pages Router. Here's the setup for your version..." |
| "Import `useFormState` from 'react-dom'" | API renamed in React 19 | "Detected React 18.3.1. Using `useFormState` (renamed to `useActionState` in React 19)." |
| "I'll just use the latest Prisma syntax" | "Latest" is frozen at training cutoff | "Detected Prisma 6.0.0. Training covers Prisma 5.x. Adding // VERIFY: Prisma 6.x migration notes." |
