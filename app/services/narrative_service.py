"""Business orchestration for narrative timelines."""

from typing import Iterable, List

from app.services.judgement_service import judge_entries
from core.types import TimelineNode


def build_narrative_timeline(entries: Iterable[str]) -> List[TimelineNode]:
    """Build timeline nodes from narrative entries."""
    return [judgement.to_timeline_node() for judgement in judge_entries(entries)]
