from typing import List, Dict, Any, Optional, Tuple
from core.enums import JudgementStatus
from core.types import JudgementVersion
from app.services.version_service import version_service
from app.services.correction_service import correction_service, ImpactAnalysisResult
from app.services.discomfort_service import discomfort_service, DiscomfortSignal
from app.services.state_machine_service import state_machine, StateTransition


def build_timeline(analysed_entries: list) -> list:
    """
    输入：按时间排序的 AnalysedEntry
    输出：时间轴结构（list）
    """
    # 确保按时间顺序排序
    sorted_entries = sorted(analysed_entries, key=lambda x: x["time"])
    return sorted_entries

def create_versioned_judgement(
    judgement_id: str,
    content: Dict[str, Any],
    status: JudgementStatus,
    previous_version: Optional[JudgementVersion] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> JudgementVersion:
    """
    创建版本化的判断
    """
    return version_service.create_new_version(
        judgement_id=judgement_id,
        content=content,
        status=status,
        previous_version=previous_version,
        metadata=metadata
    )

def get_judgement_history(judgement_id: str) -> List[JudgementVersion]:
    """
    获取判断的版本历史
    """
    return version_service.get_version_history(judgement_id)

def get_latest_judgement(judgement_id: str) -> Optional[JudgementVersion]:
    """
    获取判断的最新版本
    """
    return version_service.get_latest_version(judgement_id)

def validate_judgement_versions(version: JudgementVersion) -> bool:
    """
    验证判断版本链的完整性
    """
    return version_service.validate_version_chain(version)

def analyse_information_impact(new_information: Dict[str, Any]) -> ImpactAnalysisResult:
    """
    分析新信息对现有判断的影响
    
    Args:
        new_information: 新信息，包含事实、证据等
        
    Returns:
        ImpactAnalysisResult: 影响分析结果
    """
    return correction_service.analyse_impact(new_information)

def create_correction(judgement_id: str, new_information: Dict[str, Any], impact_analysis: ImpactAnalysisResult) -> Optional[JudgementVersion]:
    """
    创建判断的修正版本
    
    Args:
        judgement_id: 判断ID
        new_information: 新信息
        impact_analysis: 影响分析结果
        
    Returns:
        Optional[JudgementVersion]: 新创建的修正版本
    """
    return correction_service.create_correction_version(
        judgement_id=judgement_id,
        new_information=new_information,
        impact_analysis=impact_analysis
    )

def report_discomfort(
    judgement_id: str,
    discomfort_type: str,
    severity: float,
    description: Optional[str] = None,
    user_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> DiscomfortSignal:
    """
    报告对判断的不适感
    
    Args:
        judgement_id: 判断ID
        discomfort_type: 不适感类型
        severity: 严重程度（0-1）
        description: 详细描述
        user_id: 用户ID
        metadata: 附加元数据
        
    Returns:
        DiscomfortSignal: 创建的触发信号
    """
    return discomfort_service.report_discomfort(
        judgement_id=judgement_id,
        discomfort_type=discomfort_type,
        severity=severity,
        description=description,
        user_id=user_id,
        metadata=metadata
    )

def get_discomfort_history(judgement_id: Optional[str] = None) -> List[DiscomfortSignal]:
    """
    获取不适感历史
    
    Args:
        judgement_id: 可选的判断ID
        
    Returns:
        List[DiscomfortSignal]: 不适感信号列表
    """
    return discomfort_service.get_discomfort_history(judgement_id)

def get_discomfort_summary(judgement_id: str) -> Dict[str, Any]:
    """
    获取判断的不适感摘要
    
    Args:
        judgement_id: 判断ID
        
    Returns:
        Dict[str, Any]: 不适感摘要
    """
    return discomfort_service.get_discomfort_summary(judgement_id)

def transition_judgement_state(
    judgement_id: str,
    to_state: JudgementStatus,
    reason: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Tuple[Optional[JudgementVersion], Optional[StateTransition]]:
    """
    执行判断状态转换
    
    Args:
        judgement_id: 判断ID
        to_state: 目标状态
        reason: 转换原因
        metadata: 附加元数据
        
    Returns:
        Tuple[Optional[JudgementVersion], Optional[StateTransition]]: (新版本, 转换记录)
    """
    return state_machine.transition_state(
        judgement_id=judgement_id,
        to_state=to_state,
        reason=reason,
        metadata=metadata
    )

def get_judgement_state(judgement_id: str) -> Optional[JudgementStatus]:
    """
    获取判断的当前状态
    
    Args:
        judgement_id: 判断ID
        
    Returns:
        Optional[JudgementStatus]: 当前状态
    """
    return state_machine.get_current_state(judgement_id)

def get_state_history(judgement_id: str) -> List[StateTransition]:
    """
    获取判断的状态转换历史
    
    Args:
        judgement_id: 判断ID
        
    Returns:
        List[StateTransition]: 状态转换历史
    """
    return state_machine.get_state_history(judgement_id)

def can_transition_to(judgement_id: str, to_state: JudgementStatus) -> bool:
    """
    检查是否可以转换到指定状态
    
    Args:
        judgement_id: 判断ID
        to_state: 目标状态
        
    Returns:
        bool: 是否可以转换
    """
    return state_machine.can_transition_to(judgement_id, to_state)

def get_available_transitions(judgement_id: str) -> List[JudgementStatus]:
    """
    获取可用的状态转换目标
    
    Args:
        judgement_id: 判断ID
        
    Returns:
        List[JudgementStatus]: 可用的目标状态
    """
    return state_machine.get_available_transitions(judgement_id)
