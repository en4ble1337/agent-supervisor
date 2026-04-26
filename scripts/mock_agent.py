import asyncio

import asyncssh
import uvicorn
from fastapi import Body, FastAPI

# --- FastAPI Mock API ---

app = FastAPI(title="Mock Agent API")

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
    if command and command.startswith('tail'):
        process.stdout.write('Mock Log: System booted.\nMock Log: All systems go.\n')
    else:
        process.stdout.write('Mock SSH Shell - Type exit to quit\n')
    process.exit(0)

async def start_ssh_server():
    # Load or generate a host key
    key = asyncssh.generate_private_key('ssh-rsa')
    await asyncssh.create_server(
        MockSSHServer, '', 8022,
        server_host_keys=[key],
        process_factory=handle_client
    )

# --- Combined Runner ---

async def main():
    # Start SSH in background
    await start_ssh_server()
    print("Mock SSH server started on port 8022")
    
    # Run FastAPI
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
