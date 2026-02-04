"""Model input/output schema definitions."""

from dataclasses import dataclass
from typing import List


@dataclass
class NarrativeRequest:
    texts: List[str]


@dataclass
class NarrativeResponse:
    labels: List[str]
