# PRD: Single-Pane-of-Glass Supervisor Dashboard

## Executive Summary

A single-pane-of-glass supervisor dashboard acting as a thin layer on top of agent runtimes like OpenClaw and Hermes. It provides operational visibility (tasks, logs, files) and direct 1-on-1 messaging for multiple autonomous agents across different business units. The dashboard connects directly to agents via their native APIs and SSH, providing a centralized "operator cockpit" without replacing the underlying agent frameworks or intercepting their external approval workflows (e.g., Telegram).

## Mission and Core Principles

**Mission Statement:** Provide a centralized operator cockpit to monitor and directly communicate with multiple autonomous AI agents across various businesses without abstracting away their underlying runtimes.

**Core Principles:**
1. **Thin Layer Abstraction** — The dashboard must remain a stateless supervisor; the agents (OpenClaw/Hermes) are the source of truth for their state.
2. **Business-Centric Scoping** — All interactions and views can be filtered by business group to maintain focus across multiple companies.
3. **Direct Operator Access** — The system prioritizes 1-on-1 communication and direct filesystem access (via SSH) to understand exactly what an agent is doing.

## Target Users

**Primary: Technical Operator / Entrepreneur**
- Runs multiple businesses and utilizes agent teams for marketing, research, CRM, etc.
- High technical comfort (comfortable with self-hosting, Docker, SSH, Linux, custom infrastructure).
- **Key need:** Supervise all agent activity centrally, check their local files, and directly message individual agents without logging into multiple separate servers or terminal windows.

## Scope

**In Scope:**
- Dashboard UI with a global view and business group filtering.
- Direct 1-on-1 messaging with individual agents via their native REST APIs.
- Adding/discovering agents via SSH credentials and API endpoints (network reachable).
- Viewing agent files/directories via SSH/SFTP.
- Operational visibility: tasks, logs, sessions, cron jobs (polled every ~15 minutes or on demand).
- Local storage for minimal configuration (agent connection details, encrypted credentials, business group mappings).

**Out of Scope:**
- Multi-agent broadcasting (messaging multiple agents at once).
- Human-in-the-loop approval workflows inside the dashboard (agents will continue to use external channels like Telegram).
- A heavy centralized database for mirroring or aggregating agent state (data is fetched on demand).
- Real-time WebSocket syncing for live data (polling is sufficient for MVP).
- Modifying the underlying agent runtimes (OpenClaw/Hermes).

## User Stories

### US-001: Add Agent via SSH
**Description:** As an operator, I want to add a new agent to the dashboard by providing its SSH credentials and API endpoint so that I can monitor it.

**Example:** I click "Add Agent", select a business group (e.g., "X Marketing"), enter the IP address, SSH username/password, and Hermes API port. The dashboard verifies the connection and adds the agent to the group.

**Acceptance Criteria:**
- [ ] Form to input IP, SSH credentials, API port, and Business Group
- [ ] System validates SSH connection and API reachability upon submission
- [ ] Credentials are encrypted at rest in the local database
- [ ] Agent appears in the global agent list under the correct business group
- [ ] Verify in browser using dev-browser skill

### US-002: Filter Agents by Business Group
**Description:** As an operator, I want to filter my dashboard view by business group so I can focus on one company's operations at a time.

**Example:** The global view shows 20 agents. I select "Acme Corp" from the top dropdown. The view updates to show only the 4 agents assigned to Acme Corp, along with their consolidated task statuses.

**Acceptance Criteria:**
- [ ] Global dropdown for Business Group selection
- [ ] Selecting a group filters the agent list, task board, and active sessions
- [ ] Default view is "All Businesses"
- [ ] Filter selection persists in URL or local storage
- [ ] Verify in browser using dev-browser skill

### US-003: Direct 1-on-1 Chat with Agent
**Description:** As an operator, I want to send a direct message to a specific agent and see its response in a dedicated thread.

**Example:** I click on the "Lead Gen Agent". A chat interface opens. I type "Pause scraping for today". The dashboard sends this to the agent's native API. The agent replies "Scraping paused," which appears in the chat thread.

**Acceptance Criteria:**
- [ ] Dedicated chat UI for each individual agent
- [ ] Messages are sent to the agent's native REST API endpoint
- [ ] Responses from the agent are displayed in the chat thread
- [ ] Chat history is fetched from the agent's API (if supported) or temporarily cached locally
- [ ] Verify in browser using dev-browser skill

### US-004: View Agent Filesystem via SSH
**Description:** As an operator, I want to browse the files in an agent's working directory so I can inspect its output or internal state.

**Example:** From the agent's detail page, I click the "Files" tab. The dashboard uses the agent's SSH connection to list the contents of `/opt/hermes/workspace`. I click on `prospects.csv` to view its contents in a data grid or text view.

**Acceptance Criteria:**
- [ ] File browser UI showing directories and files
- [ ] Uses SSH/SFTP to fetch directory contents asynchronously
- [ ] Ability to view text, markdown, and csv files directly in the UI
- [ ] Loading states handle SSH latency gracefully
- [ ] Verify in browser using dev-browser skill

### US-005: View Operational Status (Tasks/Logs)
**Description:** As an operator, I want to view the current tasks and logs for an agent to ensure it is running correctly.

**Example:** I click on "Marketing Agent" and see a dashboard showing it is "Running", has 3 active tasks, and a log tail showing recent API calls.

**Acceptance Criteria:**
- [ ] UI displays current agent status (Idle, Running, Error)
- [ ] Lists active tasks and cron jobs fetched from the agent's API
- [ ] Displays a tail of the agent's logs (fetched via SSH `tail` command or API)
- [ ] Manual refresh button available, plus auto-polling every 15 minutes
- [ ] Verify in browser using dev-browser skill

## Feature Specifications

### Global Dashboard
**Location:** `/` (Home)
A unified view showing all registered agents categorized by business group. Includes high-level stats (e.g., total running, total errors). A global dropdown in the navigation bar filters all subsequent views by Business Group. The layout should be dense and information-rich, suited for a technical operator.

### Agent Detail View
**Location:** `/agents/:id`
Clicking an agent opens a multi-tab interface:
- **Chat:** 1-on-1 messaging interface communicating via the agent's native REST API. Looks like a standard terminal or modern chat app.
- **Operations:** Displays current tasks, cron jobs, and high-level status. Data is fetched on load and polled every 15 mins.
- **Files:** A file tree browser utilizing the agent's SSH connection to navigate and read files in its workspace.
- **Logs:** A raw text view of the agent's stdout/stderr or log files, fetched via SSH or API.

## Functional Requirements

- **FR-1:** The system must store agent connection profiles (Name, IP, SSH credentials, API endpoint, Business Group) locally in a SQLite database.
- **FR-2:** The system must encrypt SSH passwords/keys at rest using a master key provided via environment variable.
- **FR-3:** The system must establish SSH connections to agents to read directories and files on demand.
- **FR-4:** The system must send chat messages to an agent's native API endpoint.
- **FR-5:** The system must allow filtering of the dashboard by Business Group.
- **FR-6:** The system must fetch task, cron, and session status from the agent's API at maximum intervals of 15 minutes or upon manual user refresh.

## Non-Goals (Out of Scope Detail)

- **No multi-agent broadcasting:** Excluded because interactions are highly context-specific. Sending one message to many agents risks conflicting commands and unpredictable states. The operator prefers 1-on-1 focus.
- **No human-in-the-loop approvals in UI:** Deferred to keep the dashboard as a passive monitor and direct command tool. Agents will continue using existing channels (Telegram/Slack) for approvals, avoiding complex webhook/callback routing through the dashboard.
- **No real-time WebSocket syncing:** Not needed for MVP. 15-minute polling or manual refresh is sufficient for the operator's workflow and drastically reduces backend complexity.

## Design Considerations

- **Aesthetic:** UI should be dense and information-rich, acting as a true "operator cockpit." Dark mode should be the default to fit the terminal/hacker aesthetic.
- **Responsiveness:** Desktop-first design. While mobile is nice, the primary use case is a technical user at a workstation.
- **Error Handling:** SSH connections can be flaky. The UI must clearly distinguish between "Agent is offline/unreachable" and "Agent reported an error in its task."

## Technical Considerations

- **Backend:** Python (FastAPI) or Node.js (Express/NestJS) to handle SSH connections, encryption, and proxying API requests to avoid CORS issues.
- **Storage:** SQLite is sufficient for storing the agent registry (IPs, credentials, business groups). 
- **Networking:** The dashboard must be deployed on a network (e.g., Proxmox VLAN or Tailscale) that has SSH and HTTP routing access to all agent VMs/containers.
- **Security:** The dashboard itself should not handle user auth beyond basic protection; it expects to be deployed behind secure infrastructure (e.g., Authelia, Cloudflare Access, or internal VPN).

## Implementation Phases

### Phase 1: Foundation & Discovery (MVP)
- **Goal:** Get the dashboard running, connected to agents, and displaying basic status.
- **Deliverables:**
  - SQLite database and backend API for agent registry.
  - Add Agent UI with SSH/API connection validation.
  - Global dashboard list with Business Group filtering.
  - Operational view fetching basic status (idle/running) via API.

### Phase 2: Deep Inspection
- **Goal:** Enable the operator to see exactly what the agent is doing under the hood.
- **Deliverables:**
  - SSH File Browser tab (list directories, read files).
  - Logs tab (tailing remote logs via SSH).
  - Task and Cron Job lists fetched from the agent API.

### Phase 3: Control & Messaging
- **Goal:** Allow the operator to interact directly with the agents.
- **Deliverables:**
  - Chat interface tab.
  - Integration with Hermes/OpenClaw native messaging APIs.
  - Displaying chat history.

### Phase 4: Advanced Operations (Extended)
- **Goal:** Scalability and automated environment management.
- **Deliverables:**
  - **Multi-agent broadcasting:** Send a single message/command to all agents in a selected Business Group.
  - **Mock Agent Runtime:** A developer utility to simulate agent behavior (SSH/API) for testing and CI.
  - **Dockerization:** Complete container orchestration for easy self-hosting deployment.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| SSH connections hang, causing UI requests to timeout/freeze | Medium | Implement strict timeouts (e.g., 5 seconds) on backend SSH calls. Use async processing and return cached data or clear error messages to the UI. |
| Storing SSH credentials in a central dashboard creates a high-value attack target | High | Encrypt all credentials in SQLite using AES-256. Do not expose the dashboard to the public internet; require VPN/Zero Trust access. |
| OpenClaw and Hermes APIs differ significantly, complicating the "thin layer" | Medium | Build an Adapter Pattern in the backend. Define a standard internal interface (e.g., `getTasks()`, `sendMessage()`) and implement separate adapters for Hermes and OpenClaw. |

## Future Considerations

- Implementing centralized approvals directly in the dashboard (if Telegram becomes unwieldy).
- Live WebSocket streaming of logs for real-time debugging.
- Cross-agent analytics (e.g., total API spend across all businesses).
- Agent provisioning (spinning up new OpenClaw/Hermes instances directly from the dashboard via Proxmox/Docker APIs).

## Success Metrics

- Operator can view the status of all agents across all businesses in under 5 seconds.
- Operator can read an agent's workspace file without opening an external SSH terminal.
- Operator can successfully send a command and receive a reply from an agent via the UI.

## Open Questions

- What specific native API endpoints will we hit for Hermes and OpenClaw to send messages? (Need to audit their current Swagger/OpenAPI docs).
- Where are the logs typically stored on the agent VMs for the SSH log tail feature? (e.g., `/var/log/syslog` vs docker logs vs local `.log` files).
- Should the file browser support write access (editing files directly in the dashboard) or read-only for MVP? (Assuming read-only for MVP).
