"""Local API entrypoints for narrative analysis."""

from typing import Iterable, List

from app.services.narrative_service import build_narrative_timeline
from core.types import TimelineNode


def analyse_payload(payload: Iterable[str]) -> List[TimelineNode]:
    """Analyse a payload and return timeline results."""
    return build_narrative_timeline(payload)
