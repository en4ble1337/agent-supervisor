from pydantic import BaseModel


class BroadcastRequest(BaseModel):
    content: str
    business_group: str | None = None
    agent_ids: list[str] | None = None
