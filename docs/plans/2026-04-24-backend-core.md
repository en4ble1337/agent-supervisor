# Implementation Plan: Backend Core Setup (DB & Crypto)

## 1. Objective
Initialize the FastAPI backend structure, set up the asynchronous SQLite database connection (`aiosqlite`), and implement the `CryptoService` for secure SSH credential storage using `cryptography` (Fernet).

## 2. Proposed Changes
- `backend/core/config.py`: Application settings using Pydantic `BaseSettings`.
- `backend/core/database.py`: SQLAlchemy async engine and session maker setup.
- `backend/services/crypto_service.py`: Encryption and decryption logic.
- `tests/core/test_config.py`: Tests for configuration loading and validation.
- `tests/core/test_database.py`: Tests for DB connection initialization.
- `tests/services/test_crypto_service.py`: Tests for encryption/decryption.

## 3. Step-by-Step Execution Plan

### Step 1: Configuration (`config.py`)
- **Task 1: [RED]** Write a failing test `tests/core/test_config.py` that asserts `Settings` loads `ENCRYPTION_KEY` and `DATABASE_URL`.
- **Task 2: [GREEN]** Implement `backend/core/config.py` with `BaseSettings`. Add `pydantic-settings` to `requirements.txt` if needed.
- **Task 3: [REFACTOR]** Ensure clean environment variable loading.

### Step 2: CryptoService (`crypto_service.py`)
- **Task 4: [RED]** Write a failing test `tests/services/test_crypto_service.py` verifying that a string is encrypted and correctly decrypted using a valid Fernet key.
- **Task 5: [GREEN]** Implement `backend/services/crypto_service.py` using `cryptography.fernet.Fernet` initialized with `settings.ENCRYPTION_KEY`.
- **Task 6: [REFACTOR]** Handle exceptions (e.g., InvalidToken) gracefully.

### Step 3: Database Setup (`database.py`)
- **Task 7: [RED]** Write a test `tests/core/test_database.py` that verifies `get_db` yields an `AsyncSession` and the engine connects to SQLite.
- **Task 8: [GREEN]** Implement `backend/core/database.py` with `create_async_engine` and `async_sessionmaker`.
- **Task 9: [REFACTOR]** Ensure session dependency `get_db` is clean and robust.

## 4. Verification Strategy
- **Unit Tests:** `pytest tests/core/ test_services/ -v` to ensure configuration, crypto, and DB functions work correctly.
- **Integration Tests:** (Later) DB will be integrated with agent models.
- **Manual Verification:** Running tests passes cleanly.

## 5. Potential Risks & Mitigations
- **Risk:** Fernet requires a base64-encoded 32-byte key. If `ENCRYPTION_KEY` is not the correct format, initialization will fail.
- **Mitigation:** Provide a utility to generate the key or validate length in `Settings`. Document the requirement. Add test to ensure invalid key raises error.
- **Risk:** Async DB connection sharing issues during testing.
- **Mitigation:** Use proper `pytest-asyncio` fixtures for isolated DB connections in tests if needed (though testing `database.py` directly might just test engine creation).
