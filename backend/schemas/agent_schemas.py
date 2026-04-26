from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AgentBase(BaseModel):
    name: str = Field(..., max_length=100)
    ip_address: str
    ssh_username: str
    api_endpoint: str
    business_group: str


class AgentCreate(AgentBase):
    ssh_password: str


class AgentResponse(AgentBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentStatusResponse(BaseModel):
    id: UUID
    status: str
    active_tasks: list[Any]
    cron_jobs: list[Any]


class AgentActionRequest(BaseModel):
    action: str
    params: dict[str, Any] = Field(default_factory=dict)


class AgentCronRequest(BaseModel):
    name: str
    schedule: str
    command: str
