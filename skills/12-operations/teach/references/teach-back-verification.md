# Teach-Back Verification

## The Protocol

Teach-back is the only reliable method for verifying understanding. The learner explains the concept back in their own words as if teaching a colleague. This reveals misconceptions, gaps, and the illusion of competence that self-assessment cannot detect.

## Teach-Back Prompt Template

"Explain [concept] to me as if I'm a colleague who's never heard of it. Include:
1. What it is (definition)
2. Why it exists (the problem it solves)
3. When you'd use it (and when you wouldn't)
4. How it connects to [previously learned concept]"

## Quality Rubric

| Rating | Criteria | Example Indicators |
|--------|----------|-------------------|
| **5 — DEEP** | Accurate, connects to other concepts, can apply to novel scenarios, identifies limitations | "Promises are for one-shot async operations. For streams of data, you'd use Observables because..." |
| **4 — APPLIED** | Accurate, uses own examples, shows practical understanding | "Here's how I'd use a promise to fetch user data and handle the loading state..." |
| **3 — SURFACE** | Correct definition, can parrot examples but can't apply independently | "A promise represents a future value. It has .then() and .catch()." |
| **2 — FRAGILE** | Partially correct, contains misconceptions, conflates with other concepts | "Promises are like callbacks but they're synchronous, right?" |
| **1 — NOT MASTERED** | Unable to explain, fundamentally misunderstands | "I'm not sure. It's something about async?" |

## Misconception Detection Patterns

| What They Say | What It Reveals | Response |
|--------------|-----------------|----------|
| "It's basically just X" (oversimplification) | Surface understanding, missing nuance | "That's part of it. What's different about [concept] that [X] doesn't cover?" |
| Correct definition, wrong application | Rote memorization, no transfer | "Let's try an example where that definition would lead you wrong..." |
| Can't explain without code | Concept tied to syntax, not understanding | "Forget the code for a moment. In plain English, what is this doing?" |
| Explains what but not why | Missing motivation — won't know when to use it | "What problem existed before this concept? Why was it created?" |
| Uses concept name in definition | Circular reasoning — doesn't truly understand | "Define it without using the word [concept name]." |

## Teach-Back Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| "Do you understand?" | Social pressure → "yes" regardless | Always require explanation, never yes/no |
| Accepting the first answer | First answer is often shallow | "Tell me more. What's an example from your own experience?" |
| Correcting during teach-back | Interrupts the learner's thought process | Note misconceptions, address AFTER teach-back is complete |
| Teaching during teach-back | Teach-back is assessment, not instruction | If they can't explain, that's data — reteach separately |
| "Close enough" acceptance | Gaps accepted now become bugs later | "Almost. There's one thing missing. Can you spot it?" |
