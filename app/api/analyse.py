"""Local API entrypoints for narrative analysis."""

from app.services.narrative_service import build_narrative_timeline


def analyse_payload(payload):
    """Analyse a payload and return timeline results."""
    return build_narrative_timeline(payload)
