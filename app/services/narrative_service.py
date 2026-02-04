"""Business orchestration for narrative timelines."""

from app.services.judgement_service import judge_entries


def build_narrative_timeline(entries):
    """Build timeline nodes from narrative entries."""
    return [judgement.to_timeline_node() for judgement in judge_entries(entries)]
