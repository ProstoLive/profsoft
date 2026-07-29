from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskOut(BaseModel):
    id: int
    external_id: str
    status: str
    result: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
