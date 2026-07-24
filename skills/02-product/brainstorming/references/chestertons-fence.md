# Chesterton's Fence: Constraint Removal Protocol

## The Principle
"There exists in such a case a certain institution or law; let us say, for the sake of simplicity, a fence or gate erected across a road. The more modern type of reformer goes gaily up to it and says, 'I don't see the use of this; let us clear it away.' To which the more intelligent type of reformer will do well to answer: 'If you don't see the use of it, I certainly won't let you clear it away. Go away and think. Then, when you can come back and tell me that you do see the use of it, I may allow you to destroy it.'"
— G.K. Chesterton

## Applied to Software Design

### Origin Tracing
1. Who established this constraint? (Person, team, or event?)
2. When was it established? (Date or release?)
3. What problem did it solve? (Specific incident or design requirement?)
4. Is that problem still relevant? (Has the context changed?)

### Risk Assessment for Removal
- **Can trace origin + problem resolved:** REMOVE with documentation.
- **Can trace origin + problem still exists:** KEEP. Problem is still active.
- **Cannot trace origin:** KEEP. Risk of removal exceeds known cost. Unknown-unknowns are the most expensive class of defects.

### Case Studies
- Rate-limiting middleware removed → $31K cloud overage (buggy client retried in tight loop)
- Deprecated field kept "for backward compatibility" → was preventing SQL injection (removing it exposed the vulnerability)
- Caching layer removed for "simplicity" → database meltdown under normal load (the cache was absorbing 90% of reads)
