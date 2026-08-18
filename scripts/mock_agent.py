import asyncio
import os
from pathlib import Path

import asyncssh
import uvicorn
from fastapi import Body, FastAPI

# --- FastAPI Mock API ---

app = FastAPI(title="Mock Agent API")
DEFAULT_WORKSPACE_ROOT = "/opt/hermes/workspace"

@app.get("/status")
async def get_status():
    return {
        "status": "online",
        "active_tasks": [{"id": "t1", "description": "Mocking around"}],
        "cron_jobs": [{"id": "c1", "schedule": "*/5 * * * *"}]
    }

@app.post("/chat")
async def chat(message: str = Body(..., embed=True)):
    return {"reply": f"Mock received: {message}"}

@app.post("/actions")
async def trigger_action(payload: dict = Body(...)):
    return {"status": "success", "action": payload.get("action"), "task_id": "mock-task-123"}

@app.post("/crons")
async def add_cron(payload: dict = Body(...)):
    return {"status": "cron added", "name": payload.get("name")}

@app.delete("/crons/{name}")
async def delete_cron(name: str):
    return {"status": "cron deleted", "name": name}

# --- AsyncSSH Mock Server ---

class MockSSHServer(asyncssh.SSHServer):
    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        return username == 'agent' and password == 'agent_pass'

def handle_client(process):
    command = process.command
    if command == "true":
        pass
    elif command and command.startswith('tail'):
        process.stdout.write('Mock Log: System booted.\nMock Log: All systems go.\n')
    else:
        process.stdout.write('Mock SSH Shell - Type exit to quit\n')
    process.exit(0)

def prepare_mock_filesystem(filesystem_root: Path) -> Path:
    workspace = filesystem_root / DEFAULT_WORKSPACE_ROOT.lstrip("/")
    reports = workspace / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (workspace / "notes.md").write_text("# Mock workspace notes\nAll systems nominal.\n", encoding="utf-8")
    (reports / "daily.csv").write_text("name,status\nmock,online\n", encoding="utf-8")
    return filesystem_root

async def start_ssh_server(host="", port=8022, filesystem_root=None):
    # Load or generate a host key
    key = asyncssh.generate_private_key('ssh-rsa')
    root = prepare_mock_filesystem(Path(filesystem_root or "/tmp/agent-supervisor-mock").resolve())
    return await asyncssh.create_server(
        MockSSHServer, host, port,
        server_host_keys=[key],
        process_factory=handle_client,
        sftp_factory=lambda chan: asyncssh.SFTPServer(chan, chroot=os.fsencode(root)),
    )

# --- Combined Runner ---

async def main():
    api_port = int(os.getenv("MOCK_AGENT_API_PORT", "8000"))
    ssh_port = int(os.getenv("MOCK_AGENT_SSH_PORT", "8022"))

    # Start SSH in background
    acceptor = await start_ssh_server(port=ssh_port)
    print(f"Mock SSH server started on port {ssh_port}")

    # Run FastAPI
    config = uvicorn.Config(app, host="0.0.0.0", port=api_port)
    server = uvicorn.Server(config)
    try:
        await server.serve()
    finally:
        acceptor.close()
        await acceptor.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
