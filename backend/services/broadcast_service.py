import asyncio
from typing import Any

from backend.models.agent import Agent
from backend.services.agent_service import HermesAdapter


class BroadcastService:
    def __init__(self) -> None:
        # Default to Hermes for MVP
        self.adapter = HermesAdapter()

    async def broadcast(self, agents: list[Agent], message: str) -> dict[str, dict[str, Any]]:
        """
        Sends a message to multiple agents in parallel.
        Returns a mapping of agent_id to result (success/error).
        """
        tasks = [self._send_to_agent(agent, message) for agent in agents]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        broadcast_results: dict[str, dict[str, Any]] = {}
        for agent, result in zip(agents, results, strict=False):
            if isinstance(result, Exception):
                broadcast_results[str(agent.id)] = {"status": "error", "error": str(result)}
            else:
                broadcast_results[str(agent.id)] = {"status": "success", "reply": result}
        return broadcast_results

    async def _send_to_agent(self, agent: Agent, message: str) -> str:
        # Note: In a real system, we might want to save these to the chat history DB too.
        # But per ARCH, we just return the individual replies.
        return await self.adapter.send_message(agent.api_endpoint, message)
