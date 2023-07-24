from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class Mp3(BaseModel):
    link: str = Field()
    inserted_at: datetime = Field(default_factory=datetime.utcnow)
    recipient: Optional[str] = None
