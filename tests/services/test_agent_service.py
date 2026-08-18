from unittest.mock import MagicMock, patch

import httpx
import pytest

from backend.services.agent_service import AgentAdapter, HermesAdapter, OpenClawAdapter


@pytest.mark.asyncio
async def test_agent_adapter_is_abstract():
    # Should not be able to instantiate AgentAdapter directly
    with pytest.raises(TypeError):
        AgentAdapter()

@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_hermes_adapter_validate_endpoint(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    adapter = HermesAdapter()
    result = await adapter.validate_endpoint("http://10.0.0.5:8000")
    assert result is True


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_hermes_adapter_validate_endpoint_accepts_health_fallback(mock_get):
    mock_get.side_effect = [
        MagicMock(status_code=404),
        MagicMock(status_code=200),
    ]
    adapter = HermesAdapter()

    result = await adapter.validate_endpoint("http://10.0.0.5:8642")

    assert result is True
    assert mock_get.call_args_list[0].args[0] == "http://10.0.0.5:8642/status"
    assert mock_get.call_args_list[1].args[0] == "http://10.0.0.5:8642/health"

@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_openclaw_adapter_validate_endpoint(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    adapter = OpenClawAdapter()
    result = await adapter.validate_endpoint("http://10.0.0.6:8000")
    assert result is True

@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_adapters_get_status(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "online",
        "active_tasks": [],
        "cron_jobs": []
    }
    mock_get.return_value = mock_response
    
    hermes = HermesAdapter()
    openclaw = OpenClawAdapter()

    for adapter in [hermes, openclaw]:
        status = await adapter.get_status("http://mock")
        assert status["status"] == "online"
        assert "active_tasks" in status
        assert "cron_jobs" in status


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_hermes_adapter_get_status_uses_health_fallback(mock_get):
    status_response = MagicMock(status_code=404)
    status_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "not found", request=MagicMock(), response=status_response
    )
    health_response = MagicMock(status_code=200)
    health_response.json.return_value = {"status": "ok", "platform": "hermes-agent"}
    mock_get.side_effect = [status_response, health_response]

    adapter = HermesAdapter()
    status = await adapter.get_status("http://10.0.0.5:8642")

    assert status == {"status": "ok", "active_tasks": [], "cron_jobs": []}
    assert mock_get.call_args_list[0].args[0] == "http://10.0.0.5:8642/status"
    assert mock_get.call_args_list[1].args[0] == "http://10.0.0.5:8642/health"
