"""Timeline view placeholders for the UI layer."""

from typing import Iterable, List

from core.types import TimelineNode


def render_timeline(nodes: Iterable[TimelineNode]) -> List[str]:
    """Render a list of timeline nodes.

    Args:
        nodes: Iterable of timeline node objects.
    """
    return [node.label for node in nodes]
