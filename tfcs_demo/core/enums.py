from enum import Enum

class NarrativeType(Enum):
    EMOTIONAL = "情绪叙事"
    EVIDENCE = "证据叙事"
    LEGAL = "法律叙事"

class JudgementStatus(Enum):
    UNRESOLVED = "未结案"
    PARTIALLY_CORRECTED = "部分修正"
    FALSIFIED = "已证伪"
    CONDITIONALLY_TRUE = "条件性成立"
