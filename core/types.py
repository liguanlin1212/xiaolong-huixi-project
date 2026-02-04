"""Core types for narrative judgement and timeline."""

from dataclasses import dataclass

from core.enums import ClosureState, NarrativeType


@dataclass
class TimelineNode:
    label: str
    narrative_type: NarrativeType
    closure_state: ClosureState


@dataclass
class Judgement:
    text: str
    narrative_type: NarrativeType
    closure_state: ClosureState

    def to_timeline_node(self):
        return TimelineNode(
            label=self.text,
            narrative_type=self.narrative_type,
            closure_state=self.closure_state,
        )
