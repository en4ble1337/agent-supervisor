from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.agent import Agent


@pytest.mark.asyncio
async def test_trigger_action_success(async_client: AsyncClient, db_session: AsyncSession):
    agent = Agent(
        name="Test Agent",
        ip_address="127.0.0.1",
        ssh_username="admin",
        ssh_password="pwd",
        api_endpoint="http://localhost:8000",
        business_group="TestGroup",
    )
    db_session.add(agent)
    await db_session.commit()
    await db_session.refresh(agent)

    with patch("backend.api.agents.HermesAdapter.trigger_action") as mock_trigger:
        mock_trigger.return_value = {"status": "success", "task_id": "123"}
        
        response = await async_client.post(
            f"/api/agents/{agent.id}/actions",
            json={"action": "restart", "params": {"force": True}}
        )
        
        assert response.status_code == 200
        assert response.json() == {"status": "success", "task_id": "123"}
        mock_trigger.assert_called_once_with(agent.api_endpoint, "restart", {"force": True})

@pytest.mark.asyncio
async def test_add_cron_success(async_client: AsyncClient, db_session: AsyncSession):
    agent = Agent(
        name="Test Agent",
        ip_address="127.0.0.1",
        ssh_username="admin",
        ssh_password="pwd",
        api_endpoint="http://localhost:8000",
        business_group="TestGroup",
    )
    db_session.add(agent)
    await db_session.commit()
    await db_session.refresh(agent)

    with patch("backend.api.agents.HermesAdapter.add_cron") as mock_add_cron:
        mock_add_cron.return_value = {"status": "cron added"}
        
        response = await async_client.post(
            f"/api/agents/{agent.id}/crons",
            json={"name": "cleanup", "schedule": "0 0 * * *", "command": "rm -rf /tmp/*"}
        )
        
        assert response.status_code == 200
        assert response.json() == {"status": "cron added"}
        mock_add_cron.assert_called_once_with(agent.api_endpoint, "cleanup", "0 0 * * *", "rm -rf /tmp/*")

@pytest.mark.asyncio
async def test_delete_cron_success(async_client: AsyncClient, db_session: AsyncSession):
    agent = Agent(
        name="Test Agent",
        ip_address="127.0.0.1",
        ssh_username="admin",
        ssh_password="pwd",
        api_endpoint="http://localhost:8000",
        business_group="TestGroup",
    )
    db_session.add(agent)
    await db_session.commit()
    await db_session.refresh(agent)

    with patch("backend.api.agents.HermesAdapter.delete_cron") as mock_delete_cron:
        mock_delete_cron.return_value = {"status": "cron deleted"}
        
        response = await async_client.delete(f"/api/agents/{agent.id}/crons/cleanup")
        
        assert response.status_code == 200
        assert response.json() == {"status": "cron deleted"}
        mock_delete_cron.assert_called_once_with(agent.api_endpoint, "cleanup")
