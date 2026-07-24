# Anti-Shipping Patterns: How Prototype Code Enters Production

## The 10 Deadly Patterns

1. **The "Almost Done" Rationalization:** "This prototype is 90% of what we need. Let's just finish it." → Missing error handling, edge cases, and tests. The "last 10%" is actually 90% of the work.

2. **The Deadline Panic:** "We don't have time to rewrite, ship the prototype." → Short-term gain, long-term disaster. Technical debt at 500% interest.

3. **The Silent Survivor:** Prototype code was committed to a feature branch during exploration and merged without review. Nobody knew it was a prototype.

4. **The Author Left:** The person who wrote the prototype left the company. The code is in production and nobody knows what shortcuts were taken.

5. **The Gradual Upgrade:** "I'll refactor one piece at a time." → Half the code is refactored, half is prototype. The hybrid is worse than either extreme.

6. **The Configuration Cascade:** Prototype configuration (hardcoded ports, test credentials, debug logging) survives into production because "it works."

7. **The Dependency Snare:** The prototype introduced a dependency that becomes entrenched. Removing it requires rewriting dependent code.

8. **The "It Passed Tests" Trap:** Someone added tests to prototype code. Tests create a false sense of safety — they test the prototype's behavior, not production-correct behavior.

9. **The Manager Override:** "I don't care if it's a prototype, we need to ship." → Manager accepts the risk. Engineer documents the objection. System fails. Manager blames engineer.

10. **The Open Source Contamination:** Prototype code from a public repo is copy-pasted without license review or security audit.

## Prevention
For each pattern: detection signal → automated check → prevention mechanism.
