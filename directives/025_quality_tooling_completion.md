# Directive 025: Quality Tooling Completion

## Objective

Finish the quality-enforcement directive so the repository has the tools it claims to have.

## Prerequisites

- [x] Directive 016: Quality Enforcement & Linting — Core Checks Present

## Scope

### In Scope
- Add Prettier or explicitly remove it from Directive 016 if ESLint/TypeScript formatting is the chosen standard.
- Add `.pre-commit-config.yaml` or an equivalent documented local pre-commit workflow.
- Ensure the quality script is documented and works from a clean checkout after dependency installation.
- Consider adding `ruff` and `mypy` to development requirements or a dedicated requirements-dev file.

### Out of Scope
- CI service setup, unless the user requests it.

## Acceptance Criteria

- [ ] Directive 016 no longer overclaims missing tools.
- [ ] Quality tooling install/run steps are documented.
- [ ] `.\scripts\check_quality.ps1` passes from a clean dependency install.
- [ ] Optional pre-commit path is verified or documented as intentionally deferred.

## Status: [x] Incomplete / [ ] Complete
