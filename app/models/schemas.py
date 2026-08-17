from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskOut(BaseModel):
    id: int
    external_id: str
    status: str
    result: str | None
    input_text: str | None
    attempts: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    external_id: str
    input_text: str


class DocumentOut(BaseModel):
    id: int
    source: str
    text: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentCreate(BaseModel):
    source: str
    text: str


class Source(BaseModel):
    source: str
    doc_id: int


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
