# Implementation Plan: Database Migrations (Alembic)

## 1. Objective
Set up Alembic for managing database migrations with `aiosqlite`.

## 2. Proposed Changes
- `backend/alembic/`: Alembic directory.
- `alembic.ini`: Configuration file.
- `backend/alembic/env.py`: Async migration setup.
- `requirements.txt`: Add `alembic`.

## 3. Step-by-Step Execution Plan

### Step 1: Initialization
- **Task 1:** Install `alembic`.
- **Task 2:** Run `alembic init -t async backend/alembic`.
- **Task 3:** Configure `alembic.ini` to point to the correct script location.

### Step 2: Configuration
- **Task 4:** Update `backend/alembic/env.py`:
    - Import `Base` from `backend.core.database`.
    - Set `target_metadata = Base.metadata`.
    - Ensure `DATABASE_URL` is read from `settings`.

### Step 3: Initial Migration
- **Task 5:** Generate initial revision: `alembic revision --autogenerate -m "Initial schema"`.
- **Task 6:** Verify by running `alembic upgrade head`.

## 4. Verification Strategy
- **Manual Verification:** Check that `agents` and `chat_messages` tables are created in the SQLite file.
