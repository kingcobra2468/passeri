from dataclasses import dataclass
from typing import List


@dataclass
class ConversionRequest:
    recipient: str
    links: List
