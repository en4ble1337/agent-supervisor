from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.core.database import get_db
from backend.models.agent import Agent
from backend.schemas.broadcast_schemas import BroadcastRequest
from backend.services.broadcast_service import BroadcastService

router = APIRouter()
broadcast_service = BroadcastService()


@router.post("")
async def send_broadcast(request: BroadcastRequest, db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    stmt = select(Agent)

    if request.agent_ids:
        stmt = stmt.where(Agent.id.in_(request.agent_ids))
    elif request.business_group:
        stmt = stmt.where(Agent.business_group == request.business_group)
    else:
        # If neither specified, broadcast to ALL (or maybe return error?)
        # Let's default to all for now as per "capability to send a single message... filtered by..."
        pass

    result = await db.execute(stmt)
    agents = list(result.scalars().all())

    if not agents:
        return {}  # No agents to target

    results = await broadcast_service.broadcast(agents, request.content)
    return results
