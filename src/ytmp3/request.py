from dataclasses import dataclass
from typing import List


@dataclass
class ConversionRequest:
    """ConversionRequest contains meta for a given ytmp3 to
    email request.
    """
    recipient: str
    links: List
