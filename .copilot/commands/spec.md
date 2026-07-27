# /copilot-skill spec — Generate a specification from an idea or requirement

Route the user's idea through the `idea-to-spec` skill to produce a structured Product Requirements Document (PRD) with data model, API contract, and screen inventory.

**When to use**: Before writing any code for a new feature or product.

**Workflow**:
1. Invoke `brainstorming` skill to refine the idea (Socratic interview pattern)
2. Invoke `idea-to-spec` skill to produce the structured PRD
3. Invoke `product-manager` to prioritize features and create work items
4. Output: PRD, prioritized feature list, ready for `/plan`

**What it produces**: A complete spec with problem statement, user stories, data model, API contracts, screen inventory, acceptance criteria, and "Not Doing" list.
