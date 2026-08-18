import uuid

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.core.config import settings
from backend.core.database import get_db
from backend.models.agent import Agent
from backend.models.chat import ChatMessage
from backend.schemas.agent_schemas import AgentRuntimeIntel, AgentStatusResponse
from backend.schemas.chat_schemas import ChatMessageCreate, ChatMessageResponse
from backend.services.agent_service import HermesAdapter
from backend.services.crypto_service import CryptoService
from backend.services.ssh_service import SSHService

router = APIRouter()
ssh_service = SSHService()
crypto_service = CryptoService(settings.ENCRYPTION_KEY)


async def _safe_collect_runtime_intel(agent: Agent, password: str) -> AgentRuntimeIntel | None:
    try:
        data = await ssh_service.collect_runtime_intel(agent.ip_address, agent.ssh_username, password)
        return AgentRuntimeIntel.model_validate(data)
    except Exception:
        return None


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
        try:
            password = crypto_service.decrypt(agent.ssh_password)
        except Exception:
            runtime_intel = None
        else:
            runtime_intel = await _safe_collect_runtime_intel(agent, password)
    except Exception as e:
        try:
            password = crypto_service.decrypt(agent.ssh_password)
            diagnostics = await ssh_service.inspect_runtime(agent.ip_address, agent.ssh_username, password)
            runtime_intel = await _safe_collect_runtime_intel(agent, password)
        except Exception as ssh_exc:
            raise HTTPException(
                status_code=502,
                detail={"code": "AGENT_UNREACHABLE", "message": f"Failed to fetch status from agent: {e!s}"},
            ) from ssh_exc

        diagnostic_lines = [str(diagnostics.get("summary", "Native API is unreachable."))]
        api_hint = diagnostics.get("api_hint")
        if api_hint:
            diagnostic_lines.append(str(api_hint))
        processes = diagnostics.get("processes") or []
        listeners = diagnostics.get("listeners") or []
        if processes:
            diagnostic_lines.append("Processes: " + " | ".join(str(line) for line in processes[:3]))
        if listeners:
            diagnostic_lines.append("Listeners: " + " | ".join(str(line) for line in listeners[:3]))

        return AgentStatusResponse(
            id=uuid.UUID(agent.id),
            status="api_unreachable",
            active_tasks=[{"id": "ssh-diagnostics", "description": "\n".join(diagnostic_lines)}],
            cron_jobs=[],
            intel=runtime_intel,
        )

    return AgentStatusResponse(
        id=uuid.UUID(agent.id),
        status=status_data.get("status", "unknown"),
        active_tasks=status_data.get("active_tasks", []),
        cron_jobs=status_data.get("cron_jobs", []),
        intel=runtime_intel,
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
