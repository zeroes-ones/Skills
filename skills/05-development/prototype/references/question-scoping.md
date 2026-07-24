# Question Scoping: Making Questions Prototype-Answerable

## The 3-Sentence Test
Can you describe the minimum code to test this question in 3 sentences or fewer?
- Yes → the question is well-scoped. Build the prototype.
- No → the question is too broad. Split it.

## Question Splitting Algorithm
1. Identify the sub-questions embedded in the broad question.
2. Rank them by dependency: which must be answered first?
3. Pick the highest-priority sub-question that can be tested in 20 minutes.
4. Prototype that one. The answer may eliminate the need for other sub-questions.

## Falsifiability Criteria
A good prototype question has a clear failure condition:
- Bad: "Will this library work for us?" (What does "work" mean?)
- Good: "Can this library process 1000 records in under 5 seconds on our data shape?"

## Scope Creep Detection
"We should also test..." → Add to the question backlog. Do NOT add to the current prototype.
"But what about edge case X?" → Document as follow-up. The current prototype answers ONE question.
