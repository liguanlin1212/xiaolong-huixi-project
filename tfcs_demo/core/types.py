from dataclasses import dataclass
from typing import Optional, Dict, Any
from core.enums import NarrativeType, JudgementStatus

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

@dataclass
class JudgementVersion:
    version_id: str
    judgement_id: str
    content: Dict[str, Any]
    status: JudgementStatus
    created_at: str
    previous_version_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version_id": self.version_id,
            "judgement_id": self.judgement_id,
            "content": self.content,
            "status": self.status.value,
            "created_at": self.created_at,
            "previous_version_id": self.previous_version_id,
            "metadata": self.metadata
        }
