"""Enumerations for narrative processing."""

from enum import Enum


class NarrativeType(str, Enum):
    UNKNOWN = "unknown"
    CLAIM = "claim"
    RESPONSE = "response"


class ClosureState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
