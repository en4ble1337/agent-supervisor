import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.core.config import settings
from backend.core.database import get_db
from backend.models.agent import Agent
from backend.schemas.agent_schemas import (
    AgentActionRequest,
    AgentCreate,
    AgentCronRequest,
    AgentResponse,
)
from backend.services.agent_service import HermesAdapter
from backend.services.crypto_service import CryptoService
from backend.services.ssh_service import SSHService

router = APIRouter()
logger = logging.getLogger(__name__)

# For MVP, we instantiate services directly. In a larger app, we might use dependency injection for these too.
ssh_service = SSHService()
crypto_service = CryptoService(settings.ENCRYPTION_KEY)


@router.get("", response_model=list[AgentResponse])
async def get_agents(
    business_group: str | None = Query(None, description="Filter by business group"),
    db: AsyncSession = Depends(get_db),
) -> list[Agent]:
    stmt = select(Agent)
    if business_group:
        stmt = stmt.where(Agent.business_group == business_group)

    result = await db.execute(stmt)
    agents = list(result.scalars().all())
    return agents


@router.post("", response_model=AgentResponse, status_code=201)
async def create_agent(agent_in: AgentCreate, db: AsyncSession = Depends(get_db)) -> Agent:
    # Validate SSH
    try:
        is_ssh_valid = await ssh_service.validate_connection(
            agent_in.ip_address, agent_in.ssh_username, agent_in.ssh_password, raise_on_error=True
        )
    except Exception as exc:
        logger.exception("SSH validation raised for %s: %s", agent_in.ip_address, exc)
        raise HTTPException(
            status_code=401, detail={"code": "SSH_AUTH_FAILED", "message": "Invalid SSH credentials or unreachable"}
        ) from exc

    if not is_ssh_valid:
        raise HTTPException(
            status_code=401, detail={"code": "SSH_AUTH_FAILED", "message": "Invalid SSH credentials or unreachable"}
        )

    # Validate API Endpoint (assuming HermesAdapter for MVP)
    adapter = HermesAdapter()
    is_api_valid = await adapter.validate_endpoint(agent_in.api_endpoint)
    if not is_api_valid:
        raise HTTPException(
            status_code=502, detail={"code": "AGENT_UNREACHABLE", "message": "Agent API is unreachable"}
        )

    # Encrypt password
    encrypted_password = crypto_service.encrypt(agent_in.ssh_password)

    # Save to DB
    agent = Agent(
        name=agent_in.name,
        ip_address=agent_in.ip_address,
        ssh_username=agent_in.ssh_username,
        ssh_password=encrypted_password,
        api_endpoint=agent_in.api_endpoint,
        business_group=agent_in.business_group,
    )
    db.add(agent)
    await db.commit()
    await db.refresh(agent)

    return agent


@router.post("/{agent_id}/actions")
async def trigger_action(
    agent_id: str,
    action_in: AgentActionRequest,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    agent = await db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    adapter = HermesAdapter()
    try:
        result = await adapter.trigger_action(agent.api_endpoint, action_in.action, action_in.params)
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.post("/{agent_id}/crons")
async def add_cron(
    agent_id: str,
    cron_in: AgentCronRequest,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    agent = await db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    adapter = HermesAdapter()
    try:
        result = await adapter.add_cron(agent.api_endpoint, cron_in.name, cron_in.schedule, cron_in.command)
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.delete("/{agent_id}/crons/{name}")
async def delete_cron(
    agent_id: str,
    name: str,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    agent = await db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    adapter = HermesAdapter()
    try:
        result = await adapter.delete_cron(agent.api_endpoint, name)
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
