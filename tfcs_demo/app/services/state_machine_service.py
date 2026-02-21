from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from core.enums import JudgementStatus
from core.types import JudgementVersion
from app.services.version_service import version_service

@dataclass
class StateTransition:
    """状态转换记录"""
    transition_id: str
    judgement_id: str
    from_state: JudgementStatus
    to_state: JudgementStatus
    reason: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: str = ""

class JudgementStateMachine:
    """判断结案状态机"""
    
    def __init__(self):
        self._state_transitions: Dict[str, StateTransition] = {}
        self._judgement_transitions: Dict[str, List[str]] = {}  # judgement_id -> [transition_id]
        self._valid_transitions = {
            JudgementStatus.UNRESOLVED: [
                JudgementStatus.PARTIALLY_CORRECTED,
                JudgementStatus.FALSIFIED,
                JudgementStatus.CONDITIONALLY_TRUE
            ],
            JudgementStatus.PARTIALLY_CORRECTED: [
                JudgementStatus.FALSIFIED,
                JudgementStatus.CONDITIONALLY_TRUE
            ],
            JudgementStatus.CONDITIONALLY_TRUE: [
                JudgementStatus.FALSIFIED,
                JudgementStatus.PARTIALLY_CORRECTED
            ],
            JudgementStatus.FALSIFIED: []  # 已证伪状态不可转换
        }
    
    def validate_transition(self, from_state: JudgementStatus, to_state: JudgementStatus) -> bool:
        """
        验证状态转换是否有效
        
        Args:
            from_state: 起始状态
            to_state: 目标状态
            
        Returns:
            bool: 转换是否有效
        """
        if from_state == to_state:
            return True  # 同一状态转换总是有效的
        
        return to_state in self._valid_transitions.get(from_state, [])
    
    def transition_state(
        self,
        judgement_id: str,
        to_state: JudgementStatus,
        reason: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[Optional[JudgementVersion], Optional[StateTransition]]:
        """
        执行状态转换
        
        Args:
            judgement_id: 判断ID
            to_state: 目标状态
            reason: 转换原因
            metadata: 附加元数据
            
        Returns:
            Tuple[Optional[JudgementVersion], Optional[StateTransition]]: (新版本, 转换记录)
        """
        import uuid
        from datetime import datetime
        
        # 获取最新版本
        latest_version = version_service.get_latest_version(judgement_id)
        if not latest_version:
            return None, None
        
        # 验证转换是否有效
        if not self.validate_transition(latest_version.status, to_state):
            return None, None
        
        # 如果状态没有变化，直接返回
        if latest_version.status == to_state:
            return latest_version, None
        
        # 创建状态转换记录
        transition_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        transition = StateTransition(
            transition_id=transition_id,
            judgement_id=judgement_id,
            from_state=latest_version.status,
            to_state=to_state,
            reason=reason,
            metadata=metadata,
            created_at=created_at
        )
        
        # 存储转换记录
        self._state_transitions[transition_id] = transition
        if judgement_id not in self._judgement_transitions:
            self._judgement_transitions[judgement_id] = []
        self._judgement_transitions[judgement_id].append(transition_id)
        
        # 创建新的状态版本
        new_content = latest_version.content.copy()
        new_content["state_transition"] = {
            "from_state": latest_version.status.value,
            "to_state": to_state.value,
            "reason": reason,
            "transitioned_at": created_at
        }
        
        # 创建新版本
        version_metadata = {
            "state_transition_id": transition_id,
            "state_transition_reason": reason,
            "transitioned_from": latest_version.status.value,
            "transitioned_to": to_state.value
        }
        
        new_version = version_service.create_new_version(
            judgement_id=judgement_id,
            content=new_content,
            status=to_state,
            previous_version=latest_version,
            metadata=version_metadata
        )
        
        return new_version, transition
    
    def get_state_history(self, judgement_id: str) -> List[StateTransition]:
        """
        获取判断的状态转换历史
        
        Args:
            judgement_id: 判断ID
            
        Returns:
            List[StateTransition]: 状态转换历史
        """
        transitions = []
        if judgement_id in self._judgement_transitions:
            for transition_id in self._judgement_transitions[judgement_id]:
                if transition_id in self._state_transitions:
                    transitions.append(self._state_transitions[transition_id])
        
        # 按时间排序
        transitions.sort(key=lambda x: x.created_at)
        return transitions
    
    def get_current_state(self, judgement_id: str) -> Optional[JudgementStatus]:
        """
        获取判断的当前状态
        
        Args:
            judgement_id: 判断ID
            
        Returns:
            Optional[JudgementStatus]: 当前状态
        """
        latest_version = version_service.get_latest_version(judgement_id)
        if latest_version:
            return latest_version.status
        return None
    
    def can_transition_to(self, judgement_id: str, to_state: JudgementStatus) -> bool:
        """
        检查是否可以转换到指定状态
        
        Args:
            judgement_id: 判断ID
            to_state: 目标状态
            
        Returns:
            bool: 是否可以转换
        """
        current_state = self.get_current_state(judgement_id)
        if not current_state:
            return False
        
        return self.validate_transition(current_state, to_state)
    
    def get_available_transitions(self, judgement_id: str) -> List[JudgementStatus]:
        """
        获取可用的状态转换目标
        
        Args:
            judgement_id: 判断ID
            
        Returns:
            List[JudgementStatus]: 可用的目标状态
        """
        current_state = self.get_current_state(judgement_id)
        if not current_state:
            return []
        
        return self._valid_transitions.get(current_state, [])

# 全局状态机服务实例
state_machine = JudgementStateMachine()
