# RESEARCH: AI Agent Supervisor Dashboard

**Search Date:** April 24, 2026
**Tech Stack Context:** FastAPI (Backend), React (Frontend), SQLite (Storage), AsyncSSH (Remote Access)
**Primary Search Terms:** "agent mission control", "open source agent supervisor", "react sftp file browser", "agentic supervisor dashboard ssh"
**Repositories Evaluated:** 6
**Repositories Recommended:** 3

---

## 1. Gap Analysis of Existing Tools

| Constraint | Mission Control | Paperclip | OpenClaw (UI) | Hermes Agent (UI) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Direct REST Control** | **Yes** (101+ endpoints) | **Yes** (API + JWT) | **Yes** (Gateway) | **Yes** (RPC) |
| **2. True "Thin Layer"** | **Partial** (SQLite local) | **No** (Embedded Postgres) | **No** (Heavy sessions) | **No** (Memory loop) |
| **3. Out-of-Band SSH** | **No** (API only) | **No** (Audit logs only) | **Yes** (Internal only) | **Yes** (Internal only) |
| **4. Business Groups** | **Yes** (Multi-tenant) | **Yes** (Multi-company) | **No** (Personal) | **No** (Personal) |
| **5. Multi-Runtime** | **Yes** (Adapters) | **Partial** (Claw/Claude) | **No** (Is runtime) | **Yes** (Bridge) |

### Key Findings:
- **Mission Control** is the closest UI/UX match but strictly relies on the agent's API. It provides no mechanism for "bypassing the agent" via SSH to inspect raw workspace files.
- **Paperclip** is a management/governance layer. It handles budgets and org charts but abstracts the technical "workspace" away, making it unsuitable for a technical operator who needs raw log access.
- **OpenClaw/Hermes** have the SSH logic (using it to run tasks), but their built-in UIs are designed for single-user interaction, not multi-business supervision.

---

## 2. The "Build vs. Fork" Decision

**Definitive Recommendation: B. Build the custom FastAPI/React stack.**

### Why Build from Scratch?
Existing tools fall short primarily on the **intersection of Business Groups and SSH Access**. 
1. **Architecture Impedance:** Mission Control is built as a stateful orchestrator. Forcing it to become a "stateless thin layer" that dynamically establishes SSH tunnels to external hosts would require fighting its core architecture.
2. **The SSH File Browser:** No existing supervisor tool provides a high-quality, SFTP-backed file tree for *external* agents. Building this in FastAPI with `asyncssh` and React with `Chonky` is more straightforward than bolting it onto a heavy framework like Paperclip.
3. **Maintainability:** A custom-built, focused cockpit will have ~10% of the code of a forked Mission Control, making it significantly easier to maintain and adapt as OpenClaw and Hermes APIs evolve.

---

## 3. Cannibalization Strategy

To accelerate the "Build" path, we will steal proven patterns and UI components:

### A. UI Components (Frontend)
- **Agent Cards & Layout:** Cannibalize from `builderz-labs/mission-control`. Their Tailwind/Shadcn components for "Agent Status" and "Task Board" are production-ready.
- **Terminal Emulator:** Use `xterm.js` with the `@xterm/addon-fit`. Reference `Hermes WebUI` for how they handle terminal window resizing over SSH.
- **File Browser:** Use **Chonky.io**. It provides a professional "Finder-like" interface. We will wire its `FileAction` callbacks to our FastAPI `SSHService`.

### B. Logic & Patterns (Backend)
- **Adapter Pattern:** Steal the `FrameworkAdapter` pattern from Mission Control to support both OpenClaw and Hermes through a unified interface (`get_tasks()`, `send_message()`).
- **Encryption at Rest:** Use the Fernet (cryptography.py) pattern seen in many self-hosted ops tools for encrypting SSH credentials in SQLite.
- **AsyncSSH SFTP:** Use the `asyncssh.connect()` context manager pattern to provide non-blocking directory listings.

---

## 4. Pattern Catalog

### Pattern: Multi-Runtime Adapter
**Source:** [mission-control](https://github.com/builderz-labs/mission-control)
**Applies To:** ARCH Section 9 (Integration Points)

```python
# Adaptation of Mission Control's adapter pattern
class AgentAdapter(ABC):
    @abstractmethod
    async def get_status(self, endpoint: str): ...
    
class HermesAdapter(AgentAdapter):
    async def get_status(self, endpoint: str):
        # Specific Hermes /status/ RPC call
        ...

class OpenClawAdapter(AgentAdapter):
    async def get_status(self, endpoint: str):
        # Specific OpenClaw /gateway/status call
        ...
```

### Pattern: SSH File Stream
**Source:** [hermes-agent](https://github.com/NousResearch/hermes-agent)
**Applies To:** PRD US-004 (View Filesystem)

```python
# Logic to be implemented in backend/services/ssh_service.py
async def list_workspace(self, path: str):
    async with asyncssh.connect(self.host, username=self.user, password=self.password) as conn:
        async with conn.start_sftp_client() as sftp:
            attrs = await sftp.readdir(path)
            return [a.filename for a in attrs]
```

---

## 5. Dependency Discoveries

| Library | Purpose | Consider Adding? |
| :--- | :--- | :--- |
| `chonky` | Professional React File Browser | **Yes** - Core for US-004 |
| `react-xtermjs` | Managed xterm.js wrapper | **Yes** - Core for Terminal |
| `asyncssh` | Non-blocking SSH/SFTP | **Yes** - Already in ARCH |
| `cryptography` | AES-256-GCM for SQLite | **Yes** - Already in ARCH |

---

## 6. Anti-Patterns to Avoid

### Anti-Pattern: Monolithic Agent Proxies
**Seen In:** Generic multi-agent dashboards.
**Issue:** Handling API proxying, SSH connection pooling, and business logic in a single file leads to untestable code and "hanging" UI requests.
**Our Approach:** Separate `SSHService` (for raw system access) from `AgentService` (for API orchestration) as per ARCH Section 6.

### Anti-Pattern: Frontend State Mirroring
**Seen In:** Mission Control, Paperclip.
**Issue:** Attempting to sync the entire agent's task state to a central database. This violates our "Thin Layer" constraint and creates a source-of-truth conflict.
**Our Approach:** Fetch data on-demand and use short-lived local caching only for UI responsiveness.

---

## 7. Open Questions for Review

1. **SSH Connection Persistence:** Should the backend maintain persistent SSH connections for all agents, or establish them on-demand? (On-demand is safer for statelessness but slower).
2. **Log Tail Implementation:** For US-005, should we use `tail -f` over SSH or poll the log file at intervals?
3. **Hermes API Maturity:** Does the Hermes native API currently support fetching historic chat threads, or must we implement local session caching immediately?

---

## 8. Final Verdict

Stop searching for a "perfect" fork. The agentic dashboard space is currently split between **runtimes** (which are too low-level) and **management platforms** (which are too high-level). 

**Your fastest path to a production-ready "operator cockpit" is to build the thin FastAPI/React layer described in your ARCH.md.** You can have a functional MVP with Business Groups and SSH File Browsing in less time than it would take to de-bloat and re-tool Mission Control.

**Next Step:** Proceed to Phase 3 (Scaffold) using the `chonky` and `xterm.js` patterns identified here.