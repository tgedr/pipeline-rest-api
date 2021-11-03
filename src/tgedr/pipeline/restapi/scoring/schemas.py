from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class ScoringModelSchema(BaseModel):
    id: UUID
    created: datetime
    name: str


class NewScoringModelSchema(BaseModel):
    name: str


class ScoringModelsSchema(BaseModel):
    models: List[ScoringModelSchema]




