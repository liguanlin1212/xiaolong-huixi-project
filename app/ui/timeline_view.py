"""Timeline view placeholders for the UI layer."""


def render_timeline(nodes):
    """Render a list of timeline nodes.

    Args:
        nodes: Iterable of timeline node objects.
    """
    return [getattr(node, "label", str(node)) for node in nodes]
