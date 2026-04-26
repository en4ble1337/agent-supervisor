import pytest
from unittest.mock import patch, MagicMock
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
