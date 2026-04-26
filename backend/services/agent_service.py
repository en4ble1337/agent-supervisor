import logging
from abc import ABC, abstractmethod
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class AgentAdapter(ABC):
    @abstractmethod
    async def validate_endpoint(self, endpoint: str) -> bool:
        """Validate if the agent API is reachable."""
        pass

    @abstractmethod
    async def get_status(self, endpoint: str) -> dict[str, Any]:
        """Fetch status, active tasks, and cron jobs."""
        pass

    @abstractmethod
    async def send_message(self, endpoint: str, message: str) -> str:
        """Send a direct message to the agent."""
        pass

    @abstractmethod
    async def trigger_action(self, endpoint: str, action: str, params: dict[str, Any]) -> dict[str, Any]:
        """Trigger a specific agent tool or task."""
        pass

    @abstractmethod
    async def add_cron(self, endpoint: str, name: str, schedule: str, command: str) -> dict[str, Any]:
        """Add a new scheduled job."""
        pass

    @abstractmethod
    async def delete_cron(self, endpoint: str, name: str) -> dict[str, Any]:
        """Delete an existing scheduled job."""
        pass


class HermesAdapter(AgentAdapter):
    async def validate_endpoint(self, endpoint: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{endpoint}/status")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Hermes validation failed for {endpoint}: {e}")
            return False

    async def get_status(self, endpoint: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{endpoint}/status")
            response.raise_for_status()
            data = response.json()
            # Ensure standard shape
            return {
                "status": data.get("status", "unknown"),
                "active_tasks": data.get("active_tasks", []),
                "cron_jobs": data.get("cron_jobs", []),
            }

    async def send_message(self, endpoint: str, message: str) -> str:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{endpoint}/chat", json={"message": message})
            response.raise_for_status()
            data = response.json()
            return str(data.get("reply", "No reply received."))

    async def trigger_action(self, endpoint: str, action: str, params: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{endpoint}/actions", json={"action": action, "params": params})
            response.raise_for_status()
            return dict(response.json())

    async def add_cron(self, endpoint: str, name: str, schedule: str, command: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{endpoint}/crons", json={"name": name, "schedule": schedule, "command": command}
            )
            response.raise_for_status()
            return dict(response.json())

    async def delete_cron(self, endpoint: str, name: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.delete(f"{endpoint}/crons/{name}")
            response.raise_for_status()
            return dict(response.json())


class OpenClawAdapter(AgentAdapter):
    # OpenClaw might have different endpoints, but for MVP we assume same or similar
    async def validate_endpoint(self, endpoint: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{endpoint}/status")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"OpenClaw validation failed for {endpoint}: {e}")
            return False

    async def get_status(self, endpoint: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{endpoint}/status")
            response.raise_for_status()
            return dict(response.json())

    async def send_message(self, endpoint: str, message: str) -> str:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{endpoint}/chat", json={"message": message})
            response.raise_for_status()
            data = response.json()
            return str(data.get("reply", "No reply received."))

    async def trigger_action(self, endpoint: str, action: str, params: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{endpoint}/actions", json={"action": action, "params": params})
            response.raise_for_status()
            return dict(response.json())

    async def add_cron(self, endpoint: str, name: str, schedule: str, command: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{endpoint}/crons", json={"name": name, "schedule": schedule, "command": command}
            )
            response.raise_for_status()
            return dict(response.json())

    async def delete_cron(self, endpoint: str, name: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.delete(f"{endpoint}/crons/{name}")
            response.raise_for_status()
            return dict(response.json())
