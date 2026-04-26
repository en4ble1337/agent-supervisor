import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.chat import ChatMessage


@pytest.mark.asyncio
async def test_chat_message_model_create(db_session: AsyncSession):
    agent_id = str(uuid.uuid4())
    msg = ChatMessage(agent_id=agent_id, role="user", content="Hello agent")
    db_session.add(msg)
    await db_session.commit()

    assert msg.id is not None
    assert msg.agent_id == agent_id
    assert msg.timestamp is not None
    assert msg.role == "user"
