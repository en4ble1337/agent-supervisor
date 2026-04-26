# Implementation Planning Guide

Before writing any production code for a directive, you MUST create a detailed implementation plan. This ensures that all edge cases are considered, the architecture is followed, and TDD is prioritized.

## Plan Location
Save all plans to `docs/plans/YYYY-MM-DD-<feature-name>.md`.

## Plan Template

### 1. Objective
Briefly state the goal of this specific implementation.

### 2. Proposed Changes
List the files that will be created or modified.

### 3. Step-by-Step Execution Plan
Break down the implementation into small, testable units.
- **Task 1: [RED] Write failing test for X**
- **Task 2: [GREEN] Implement minimal X**
- **Task 3: [REFACTOR] Clean up X**
... and so on.

### 4. Verification Strategy
- **Unit Tests:** List specific test cases.
- **Integration Tests:** How will this interact with other components?
- **Manual Verification:** Steps to verify in the UI or via CLI.

### 5. Potential Risks & Mitigations
- Performance concerns?
- Security risks (e.g., SSH command injection)?
- State management complexities?

## The "Enthusiastic Junior" Rule
Write every plan as if the implementer is an enthusiastic junior engineer who needs clear, unambiguous instructions but already understands the project's core technologies.
