import posixpath

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.core.config import settings
from backend.core.database import get_db
from backend.models.agent import Agent
from backend.services.crypto_service import CryptoService
from backend.services.ssh_service import DEFAULT_LOG_PATH, DEFAULT_WORKSPACE_ROOT, SSHService

router = APIRouter()
ssh_service = SSHService()
crypto_service = CryptoService(settings.ENCRYPTION_KEY)


def reject_workspace_traversal(path: str | None) -> None:
    raw_path = (path or "/").replace("\\", "/")
    if "\x00" in raw_path:
        raise ValueError("Path contains invalid characters")

    relative_path = raw_path.lstrip("/")
    parts = [part for part in relative_path.split("/") if part not in ("", ".")]
    if any(part == ".." for part in parts):
        raise ValueError("Path traversal is not allowed")


def resolve_workspace_path(path: str | None, workspace_root: str = DEFAULT_WORKSPACE_ROOT) -> str:
    reject_workspace_traversal(path)
    raw_path = (path or "/").replace("\\", "/")
    root = workspace_root.rstrip("/") or "/"
    if raw_path == root or raw_path.startswith(f"{root}/"):
        candidate = posixpath.normpath(raw_path)
    else:
        relative_path = raw_path.lstrip("/")
        parts = [part for part in relative_path.split("/") if part not in ("", ".")]
        if any(part == ".." for part in parts):
            raise ValueError("Path traversal is not allowed")
        candidate = root if not parts else f"{root}/{'/'.join(parts)}"

    if candidate != root and not candidate.startswith(f"{root}/"):
        raise ValueError("Path must stay inside the agent workspace")
    return candidate


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
        reject_workspace_traversal(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"code": "VALIDATION_ERROR", "message": str(e)}) from e

    try:
        password = crypto_service.decrypt(agent.ssh_password)
        workspace_root = await ssh_service.resolve_workspace_root(agent.ip_address, agent.ssh_username, password)
        remote_path = resolve_workspace_path(path, workspace_root)
        files = await ssh_service.list_directory(agent.ip_address, agent.ssh_username, password, remote_path)
        return files
    except Exception as e:
        raise HTTPException(
            status_code=502, detail={"code": "AGENT_UNREACHABLE", "message": f"SSH communication failed: {e!s}"}
        ) from e


@router.get("/{id}/files/content")
async def get_agent_file_content(
    id: str = Path(..., description="The ID of the agent"),
    path: str = Query(..., description="The file path to read"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    stmt = select(Agent).where(Agent.id == id)
    result = await db.execute(stmt)
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Agent not found"})

    try:
        reject_workspace_traversal(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"code": "VALIDATION_ERROR", "message": str(e)}) from e

    try:
        password = crypto_service.decrypt(agent.ssh_password)
        workspace_root = await ssh_service.resolve_workspace_root(agent.ip_address, agent.ssh_username, password)
        remote_path = resolve_workspace_path(path, workspace_root)
        content = await ssh_service.read_file(agent.ip_address, agent.ssh_username, password, remote_path)
        return {"path": path, "content": content, "encoding": "utf-8"}
    except Exception as e:
        raise HTTPException(
            status_code=502, detail={"code": "AGENT_UNREACHABLE", "message": f"SSH communication failed: {e!s}"}
        ) from e


@router.get("/{id}/logs")
async def get_agent_logs(
    id: str = Path(..., description="The ID of the agent"),
    log_path: str | None = Query(None, description="The path to the log file"),
    lines: int = Query(100, ge=1, le=1000, description="The number of log lines to return"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    stmt = select(Agent).where(Agent.id == id)
    result = await db.execute(stmt)
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Agent not found"})

    try:
        password = crypto_service.decrypt(agent.ssh_password)
        resolved_log_path = log_path or await ssh_service.resolve_log_path(agent.ip_address, agent.ssh_username, password)
        logs = await ssh_service.read_log_file(
            agent.ip_address, agent.ssh_username, password, resolved_log_path or DEFAULT_LOG_PATH, lines=lines
        )
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(
            status_code=502, detail={"code": "AGENT_UNREACHABLE", "message": f"SSH communication failed: {e!s}"}
        ) from e
