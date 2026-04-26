# Directive 016: Quality Enforcement & Linting

## Objective

Configure and enforce code quality tools, linters, and type checkers across the codebase to maintain high engineering standards.

## Prerequisites

- [ ] Directive 001: Initial Environment Setup — Complete

## References

**AGENTS.md:**
- Section 6: Verification Before Completion

## Scope

### In Scope
- Configure `ruff` for Python linting and formatting.
- Configure `mypy` for strict Python type checking.
- Configure `eslint` and `prettier` for React/TypeScript.
- Add a `pre-commit` configuration to run these tools before every commit.

### Out of Scope
- Automated fixers that change logic (manual review required).

## Acceptance Criteria

- [ ] `ruff check .` passes without errors.
- [ ] `mypy .` passes with zero "any" or missing type warnings in core logic.
- [ ] `npm run lint` passes for the frontend.
- [ ] Documentation exists explaining how to run these tools locally.

## Status: [x] Complete
