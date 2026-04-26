from unittest.mock import patch

import pytest

from backend.models.agent import Agent
from backend.services.broadcast_service import BroadcastService


@pytest.mark.asyncio
@patch("backend.services.agent_service.HermesAdapter.send_message")
async def test_broadcast_service_send(mock_send):
    mock_send.side_effect = ["Reply 1", Exception("Failed"), "Reply 3"]

    agents = [
        Agent(id="1", name="A1", api_endpoint="http://1"),
        Agent(id="2", name="A2", api_endpoint="http://2"),
        Agent(id="3", name="A3", api_endpoint="http://3"),
    ]

    service = BroadcastService()
    results = await service.broadcast(agents, "Hello all")

    assert len(results) == 3
    assert results["1"]["status"] == "success"
    assert results["1"]["reply"] == "Reply 1"
    assert results["2"]["status"] == "error"
    assert "Failed" in results["2"]["error"]
    assert results["3"]["status"] == "success"

    assert mock_send.call_count == 3
