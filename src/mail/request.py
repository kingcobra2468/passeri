from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MailQueueRequest:
    """MailQueueRequest holds meta for a EmailDownloaderQueue item.
    """
    recipient: Optional[str]
    links: List
