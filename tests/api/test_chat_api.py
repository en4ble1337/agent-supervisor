import uuid
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.core.config import settings
from backend.models.agent import Agent
from backend.models.chat import ChatMessage
from backend.services.crypto_service import CryptoService


@pytest.mark.asyncio
@patch("backend.api.proxy.HermesAdapter.send_message")
async def test_chat_with_agent_success(mock_send, async_client: AsyncClient, db_session: AsyncSession):
    mock_send.return_value = "I am the agent response"

    agent_id = str(uuid.uuid4())
    cs = CryptoService(settings.ENCRYPTION_KEY)
    encrypted_pwd = cs.encrypt("pwd")

    agent = Agent(
        id=agent_id,
        name="Chat Agent",
        ip_address="10.0.0.1",
        ssh_username="admin",
        ssh_password=encrypted_pwd,
        api_endpoint="http://10",
        business_group="Acme",
    )
    db_session.add(agent)
    await db_session.commit()

    payload = {"content": "Hello agent"}
    response = await async_client.post(f"/api/agents/{agent_id}/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "agent"
    assert data["content"] == "I am the agent response"

    # Check if both messages stored in DB
    stmt = select(ChatMessage).where(ChatMessage.agent_id == agent_id)
    result = await db_session.execute(stmt)
    messages = list(result.scalars().all())
    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[1].role == "agent"


@pytest.mark.asyncio
async def test_get_chat_history_success(async_client: AsyncClient, db_session: AsyncSession):
    agent_id = str(uuid.uuid4())
    m1 = ChatMessage(agent_id=agent_id, role="user", content="msg 1")
    m2 = ChatMessage(agent_id=agent_id, role="agent", content="msg 2")
    db_session.add_all([m1, m2])
    await db_session.commit()

    response = await async_client.get(f"/api/agents/{agent_id}/chat")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["content"] == "msg 1"
    assert data[1]["content"] == "msg 2"
