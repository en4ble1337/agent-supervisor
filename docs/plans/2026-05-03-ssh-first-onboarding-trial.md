# SSH-First Onboarding Trial

### 1. Objective
Make the first real-agent trial less brittle by allowing an operator to add an agent when SSH works even if the native API is not yet reachable. The supervisor should surface API-unreachable diagnostics instead of blocking registration.

### 2. Proposed Changes
- Update `tests/api/test_agents.py` so API validation failure still creates the Agent after SSH validation succeeds.
- Update `tests/api/test_proxy.py` so status requests fall back to SSH runtime diagnostics when the native API is unreachable.
- Add an SSH command helper and runtime diagnostics method in `backend/services/ssh_service.py`.
- Change `backend/api/agents.py` so `POST /api/agents` treats API validation as a warning, not a hard failure.
- Change `backend/api/proxy.py` so `GET /api/agents/{id}/status` returns a diagnostic status when API calls fail but SSH succeeds.
- Update the Add Agent UI copy/error handling to explain that API reachability can be fixed after SSH onboarding.

### 3. Step-by-Step Execution Plan
- **Task 1: [RED] Write failing registration test**
  Change the API-failed create-agent test to expect `201` and persisted agent data after SSH succeeds.
- **Task 2: [RED] Write failing status fallback test**
  Add a test where `HermesAdapter.get_status` raises and SSH diagnostics return useful runtime details.
- **Task 3: [GREEN] Implement backend minimal behavior**
  Keep SSH validation mandatory, make API validation non-blocking, and add SSH fallback diagnostics for status.
- **Task 4: [GREEN] Update frontend wording**
  Make Add Agent less misleading: API failure should not be presented as a registration blocker if backend allows the add.
- **Task 5: [REFACTOR] Verify locally**
  Run targeted tests, full quality checks if feasible, and restart the local backend/frontend so the user can try from the browser.

### 4. Verification Strategy
- **Unit/API Tests:** `pytest tests/api/test_agents.py tests/api/test_proxy.py tests/services/test_ssh_service.py -q`
- **Regression Tests:** `.\scripts\check_quality.ps1`
- **Manual Verification:** Add a host with valid SSH and unavailable Hermes API. It should register, and the Operations tab should report API diagnostics rather than failing the entire onboarding.

### 5. Potential Risks & Mitigations
- **Risk:** Operators may think chat/control works immediately after adding an API-disabled agent.
  **Mitigation:** Surface `api_unreachable` status and diagnostic task text until the real adapter/API tunnel work lands.
- **Risk:** SSH diagnostics are heuristic.
  **Mitigation:** Keep diagnostics read-only and clearly labeled; Directive 020 will replace assumptions with real runtime adapter behavior.
