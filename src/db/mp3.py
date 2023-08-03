from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class Mp3(BaseModel):
    """An input request record.
    """
    # The Youtube link to download
    link: str = Field()
    # The time of the request
    inserted_at: datetime = Field(default_factory=datetime.utcnow)
    # The recipient email for email requests
    recipient: Optional[str] = None
