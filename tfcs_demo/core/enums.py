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
    CONFIRMED = "已确认"
    WITHDRAWN = "已撤回"
    UNDER_REVIEW = "审核中"

    @classmethod
    def get_transition_states(cls, current_status):
        """
        获取当前状态可以转换到的状态
        
        参数:
            current_status: 当前状态
            
        返回:
            list: 可以转换到的状态列表
        """
        transitions = {
            cls.UNRESOLVED: [cls.PARTIALLY_CORRECTED, cls.FALSIFIED, cls.CONDITIONALLY_TRUE, cls.CONFIRMED, cls.UNDER_REVIEW],
            cls.PARTIALLY_CORRECTED: [cls.FALSIFIED, cls.CONDITIONALLY_TRUE, cls.CONFIRMED, cls.UNDER_REVIEW],
            cls.FALSIFIED: [cls.UNDER_REVIEW],
            cls.CONDITIONALLY_TRUE: [cls.PARTIALLY_CORRECTED, cls.FALSIFIED, cls.CONFIRMED, cls.UNDER_REVIEW],
            cls.CONFIRMED: [cls.UNDER_REVIEW, cls.WITHDRAWN],
            cls.WITHDRAWN: [cls.UNDER_REVIEW],
            cls.UNDER_REVIEW: [cls.UNRESOLVED, cls.PARTIALLY_CORRECTED, cls.FALSIFIED, cls.CONDITIONALLY_TRUE, cls.CONFIRMED]
        }
        return transitions.get(current_status, [])

    def can_transition_to(self, new_status):
        """
        检查是否可以转换到新状态
        
        参数:
            new_status: 新状态
            
        返回:
            bool: 是否可以转换
        """
        return new_status in self.get_transition_states(self)
