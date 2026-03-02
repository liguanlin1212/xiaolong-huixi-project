from dataclasses import dataclass
from typing import Optional, Dict, Any, List
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
class Event:
    event_id: str
    title: str
    description: str
    start_time: str
    end_time: Optional[str] = None
    judgement_ids: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[JudgementStatus] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "judgement_ids": self.judgement_ids or [],
            "metadata": self.metadata,
            "status": self.status.value if self.status else None
        }

@dataclass
class JudgementVersion:
    version_id: str
    judgement_id: str
    content: Dict[str, Any]
    status: JudgementStatus
    created_at: str
    event_id: Optional[str] = None
    previous_version_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version_id": self.version_id,
            "judgement_id": self.judgement_id,
            "event_id": self.event_id,
            "content": self.content,
            "status": self.status.value,
            "created_at": self.created_at,
            "previous_version_id": self.previous_version_id,
            "metadata": self.metadata
        }
