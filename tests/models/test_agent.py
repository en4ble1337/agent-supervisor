import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.agent import Agent


@pytest.mark.asyncio
async def test_agent_model_create(db_session: AsyncSession):
    agent = Agent(
        name="Test Agent",
        ip_address="10.0.0.1",
        ssh_username="admin",
        ssh_password="encrypted_password",
        api_endpoint="http://10.0.0.1:8000",
        business_group="Acme Corp",
    )
    db_session.add(agent)
    await db_session.commit()

    assert agent.id is not None
    assert agent.created_at is not None
    assert str(agent.id)
    assert agent.name == "Test Agent"
