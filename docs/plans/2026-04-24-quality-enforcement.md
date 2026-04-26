# Implementation Plan: Quality Enforcement & Linting

## 1. Objective
Configure and enforce code quality tools (`ruff`, `mypy`, `eslint`, `prettier`) across the codebase.

## 2. Proposed Changes
- `pyproject.toml`: Configure `ruff` and `mypy`.
- `backend/requirements.txt`: Add `ruff` and `mypy`.
- `frontend/package.json`: Ensure `lint` script exists.
- `scripts/check_quality.ps1`: Root script to run all checks.
- `.pre-commit-config.yaml`: Pre-commit hooks configuration.

## 3. Step-by-Step Execution Plan

### Step 1: Backend Quality
- **Task 1:** Install `ruff` and `mypy`.
- **Task 2:** Create `pyproject.toml` with `ruff` and `mypy` configurations.
- **Task 3:** Run `ruff check .` and `mypy .` on backend and fix initial issues if any.

### Step 2: Frontend Quality
- **Task 4:** Ensure `eslint` is working in `frontend/`.
- **Task 5:** Add `prettier` if not present.

### Step 3: CI/Hooks
- **Task 6:** Create `.pre-commit-config.yaml`.
- **Task 7:** Create `scripts/check_quality.ps1`.

## 4. Verification Strategy
- **Manual Verification:** Run the quality script and ensure it returns exit code 0.
