import uuid

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.core.database import get_db
from backend.models.agent import Agent
from backend.models.chat import ChatMessage
from backend.schemas.agent_schemas import AgentStatusResponse
from backend.schemas.chat_schemas import ChatMessageCreate, ChatMessageResponse
from backend.services.agent_service import HermesAdapter

router = APIRouter()


@router.get("/{id}/status", response_model=AgentStatusResponse)
async def get_agent_status(
    id: str = Path(..., description="The ID of the agent"), db: AsyncSession = Depends(get_db)
) -> AgentStatusResponse:
    # Fetch agent
    stmt = select(Agent).where(Agent.id == id)
    result = await db.execute(stmt)
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Agent not found"})

    # For MVP, we default to HermesAdapter.
    # In future, we would check the agent runtime type and instantiate the appropriate adapter.
    adapter = HermesAdapter()
    try:
        status_data = await adapter.get_status(agent.api_endpoint)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail={"code": "AGENT_UNREACHABLE", "message": f"Failed to fetch status from agent: {e!s}"},
        ) from e

    return AgentStatusResponse(
        id=uuid.UUID(agent.id),
        status=status_data.get("status", "unknown"),
        active_tasks=status_data.get("active_tasks", []),
        cron_jobs=status_data.get("cron_jobs", []),
    )


@router.post("/{id}/chat", response_model=ChatMessageResponse)
async def chat_with_agent(
    id: str = Path(..., description="The ID of the agent"),
    chat_in: ChatMessageCreate | None = None,
    db: AsyncSession = Depends(get_db),
) -> ChatMessage:
    if chat_in is None:
        raise HTTPException(status_code=400, detail="Missing chat message")

    # Fetch agent
    stmt = select(Agent).where(Agent.id == id)
    result = await db.execute(stmt)
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Agent not found"})

    # 1. Save user message to DB
    user_msg = ChatMessage(agent_id=id, role="user", content=chat_in.content)
    db.add(user_msg)

    # 2. Call adapter
    adapter = HermesAdapter()
    try:
        reply_content = await adapter.send_message(agent.api_endpoint, chat_in.content)
    except Exception as e:
        await db.commit()  # Save user msg even if agent fails? Or rollback?
        # For now, let's just fail.
        raise HTTPException(
            status_code=502,
            detail={"code": "AGENT_UNREACHABLE", "message": f"Failed to send message to agent: {e!s}"},
        ) from e

    # 3. Save agent reply to DB
    agent_msg = ChatMessage(agent_id=id, role="agent", content=reply_content)
    db.add(agent_msg)

    await db.commit()
    await db.refresh(agent_msg)

    return agent_msg


@router.get("/{id}/chat", response_model=list[ChatMessageResponse])
async def get_chat_history(
    id: str = Path(..., description="The ID of the agent"), db: AsyncSession = Depends(get_db)
) -> list[ChatMessage]:
    stmt = select(ChatMessage).where(ChatMessage.agent_id == id).order_by(ChatMessage.timestamp.asc())
    result = await db.execute(stmt)
    messages = list(result.scalars().all())
    return messages
