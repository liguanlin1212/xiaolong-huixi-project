from dataclasses import dataclass
from core.enums import NarrativeType

@dataclass
class TextEntry:
    time: str
    text: str

@dataclass
class AnalysedEntry:
    time: str
    text: str
    narrative: NarrativeType
    confidence: float
