from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.core.config import settings
from backend.core.database import get_db
from backend.models.agent import Agent
from backend.services.crypto_service import CryptoService
from backend.services.ssh_service import SSHService

router = APIRouter()
ssh_service = SSHService()
crypto_service = CryptoService(settings.ENCRYPTION_KEY)


@router.get("/{id}/files")
async def get_agent_files(
    id: str = Path(..., description="The ID of the agent"),
    path: str = Query("/", description="The directory path to list"),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, str]]:
    stmt = select(Agent).where(Agent.id == id)
    result = await db.execute(stmt)
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Agent not found"})

    try:
        password = crypto_service.decrypt(agent.ssh_password)
        files = await ssh_service.list_directory(agent.ip_address, agent.ssh_username, password, path)
        return files
    except Exception as e:
        raise HTTPException(
            status_code=502, detail={"code": "AGENT_UNREACHABLE", "message": f"SSH communication failed: {e!s}"}
        ) from e


@router.get("/{id}/logs")
async def get_agent_logs(
    id: str = Path(..., description="The ID of the agent"),
    log_path: str = Query("/var/log/syslog", description="The path to the log file"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    stmt = select(Agent).where(Agent.id == id)
    result = await db.execute(stmt)
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Agent not found"})

    try:
        password = crypto_service.decrypt(agent.ssh_password)
        logs = await ssh_service.read_log_file(agent.ip_address, agent.ssh_username, password, log_path)
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(
            status_code=502, detail={"code": "AGENT_UNREACHABLE", "message": f"SSH communication failed: {e!s}"}
        ) from e
