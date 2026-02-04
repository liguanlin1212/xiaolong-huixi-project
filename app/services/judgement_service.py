"""Determine narrative objects and closure states."""

from core.enums import ClosureState, NarrativeType
from core.types import Judgement


def judge_entries(entries):
    """Classify entries into Judgement records."""
    judgements = []
    for entry in entries:
        narrative_type = NarrativeType.UNKNOWN
        closure_state = ClosureState.OPEN
        judgements.append(Judgement(text=entry, narrative_type=narrative_type, closure_state=closure_state))
    return judgements
