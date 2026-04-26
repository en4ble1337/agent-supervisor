from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageResponse(BaseModel):
    id: UUID
    agent_id: UUID
    role: str
    content: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
