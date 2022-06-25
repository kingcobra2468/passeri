from dataclasses import dataclass, field
from typing import List


@dataclass
class ConversionRequest:
    recipient: str
    links: List
