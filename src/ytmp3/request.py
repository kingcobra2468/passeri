from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ConversionRequest:
    """ConversionRequest contains meta for a given ytmp3 to
    email request.
    """
    recipient: Optional[str]
    links: List
