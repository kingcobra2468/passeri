from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MailQueueRequest:
    """A Youtube to mp3 email request.
    """
    recipient: Optional[str]
    links: List
