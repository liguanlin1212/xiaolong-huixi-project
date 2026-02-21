from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from core.enums import JudgementStatus
from core.types import JudgementVersion
from app.services.version_service import version_service
from app.services.correction_service import correction_service

@dataclass
class DiscomfortSignal:
    """不适感触发信号"""
    signal_id: str
    discomfort_type: str  # 不适感类型：逻辑冲突、证据不足、结论可疑等
    severity: float  # 严重程度：0-1
    user_id: Optional[str] = None
    judgement_id: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: str = ""

class DiscomfortService:
    def __init__(self):
        self._discomfort_signals: Dict[str, DiscomfortSignal] = {}
        self._judgement_discomforts: Dict[str, List[str]] = {}  # judgement_id -> [signal_id]
    
    def report_discomfort(
        self,
        judgement_id: str,
        discomfort_type: str,
        severity: float,
        description: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DiscomfortSignal:
        """
        用户反馈接口：报告对判断的不适感
        
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
        import uuid
        from datetime import datetime
        
        signal_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        signal = DiscomfortSignal(
            signal_id=signal_id,
            discomfort_type=discomfort_type,
            severity=severity,
            user_id=user_id,
            judgement_id=judgement_id,
            description=description,
            metadata=metadata,
            created_at=created_at
        )
        
        # 存储信号
        self._discomfort_signals[signal_id] = signal
        
        # 关联到判断
        if judgement_id not in self._judgement_discomforts:
            self._judgement_discomforts[judgement_id] = []
        self._judgement_discomforts[judgement_id].append(signal_id)
        
        # 处理触发信号
        self.process_discomfort_signal(signal)
        
        return signal
    
    def process_discomfort_signal(self, signal: DiscomfortSignal) -> Dict[str, Any]:
        """
        处理触发信号
        
        Args:
            signal: 触发信号
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        result = {
            "signal_id": signal.signal_id,
            "processed": False,
            "actions": []
        }
        
        # 检查信号有效性
        if not signal.judgement_id:
            result["error"] = "Missing judgement_id"
            return result
        
        # 根据严重程度决定行动
        if signal.severity >= 0.7:
            # 高严重度：立即触发重新审视
            review_result = self.trigger_review(signal.judgement_id, signal)
            result["actions"].append("triggered_review")
            result["review_result"] = review_result
        elif signal.severity >= 0.3:
            # 中等严重度：标记为需要关注
            result["actions"].append("marked_for_attention")
        else:
            # 低严重度：记录但不采取行动
            result["actions"].append("noted")
        
        result["processed"] = True
        return result
    
    def trigger_review(self, judgement_id: str, trigger_signal: DiscomfortSignal) -> Dict[str, Any]:
        """
        触发重新审视判断的流程
        
        Args:
            judgement_id: 判断ID
            trigger_signal: 触发信号
            
        Returns:
            Dict[str, Any]: 审视结果
        """
        result = {
            "judgement_id": judgement_id,
            "reviewed": False,
            "actions": []
        }
        
        # 获取最新版本
        latest_version = version_service.get_latest_version(judgement_id)
        if not latest_version:
            result["error"] = "Judgement not found"
            return result
        
        # 分析判断内容，寻找可能的问题
        issues = self._identify_issues(latest_version, trigger_signal)
        result["identified_issues"] = issues
        
        if issues:
            # 创建重新审视版本
            review_version = self._create_review_version(
                latest_version,
                issues,
                trigger_signal
            )
            result["actions"].append("created_review_version")
            result["review_version_id"] = review_version.version_id
            result["reviewed"] = True
        else:
            result["actions"].append("no_issues_found")
        
        return result
    
    def _identify_issues(self, version: JudgementVersion, signal: DiscomfortSignal) -> List[str]:
        """
        识别判断中的问题
        
        Args:
            version: 判断版本
            signal: 触发信号
            
        Returns:
            List[str]: 识别出的问题
        """
        issues = []
        content = version.content
        
        # 根据不适感类型识别问题
        if signal.discomfort_type == "逻辑冲突":
            if "conclusion" in content and "facts" in content:
                issues.append("可能存在逻辑冲突，需要重新分析")
        elif signal.discomfort_type == "证据不足":
            if "evidence" not in content or len(content.get("evidence", [])) < 2:
                issues.append("证据不足，需要补充")
        elif signal.discomfort_type == "结论可疑":
            issues.append("结论可疑，需要重新验证")
        elif signal.discomfort_type == "假设不合理":
            if "assumptions" in content:
                issues.append("假设可能不合理，需要重新评估")
        else:
            issues.append(f"用户反馈{signal.discomfort_type}，需要重新审视")
        
        return issues
    
    def _create_review_version(
        self,
        current_version: JudgementVersion,
        identified_issues: List[str],
        trigger_signal: DiscomfortSignal
    ) -> JudgementVersion:
        """
        创建重新审视版本
        
        Args:
            current_version: 当前版本
            identified_issues: 识别出的问题
            trigger_signal: 触发信号
            
        Returns:
            JudgementVersion: 新创建的版本
        """
        # 创建新版本内容
        new_content = current_version.content.copy()
        
        # 添加重新审视信息
        new_content["review_notes"] = identified_issues
        new_content["review_trigger"] = {
            "type": trigger_signal.discomfort_type,
            "severity": trigger_signal.severity,
            "description": trigger_signal.description,
            "triggered_at": trigger_signal.created_at
        }
        
        # 更新状态
        new_status = JudgementStatus.PARTIALLY_CORRECTED
        
        # 创建新版本
        metadata = {
            "review_trigger": trigger_signal.signal_id,
            "review_reason": "User discomfort feedback",
            "review_issues": identified_issues
        }
        
        new_version = version_service.create_new_version(
            judgement_id=current_version.judgement_id,
            content=new_content,
            status=new_status,
            previous_version=current_version,
            metadata=metadata
        )
        
        return new_version
    
    def get_discomfort_history(self, judgement_id: Optional[str] = None) -> List[DiscomfortSignal]:
        """
        获取不适感历史
        
        Args:
            judgement_id: 可选的判断ID
            
        Returns:
            List[DiscomfortSignal]: 不适感信号列表
        """
        if judgement_id:
            # 获取特定判断的不适感
            signal_ids = self._judgement_discomforts.get(judgement_id, [])
            return [self._discomfort_signals[sid] for sid in signal_ids if sid in self._discomfort_signals]
        else:
            # 获取所有不适感
            return list(self._discomfort_signals.values())
    
    def get_discomfort_summary(self, judgement_id: str) -> Dict[str, Any]:
        """
        获取判断的不适感摘要
        
        Args:
            judgement_id: 判断ID
            
        Returns:
            Dict[str, Any]: 不适感摘要
        """
        signals = self.get_discomfort_history(judgement_id)
        
        summary = {
            "judgement_id": judgement_id,
            "total_signals": len(signals),
            "average_severity": 0.0,
            "discomfort_types": {},
            "recent_signals": []
        }
        
        if signals:
            # 计算平均严重程度
            total_severity = sum(s.severity for s in signals)
            summary["average_severity"] = total_severity / len(signals)
            
            # 统计不适感类型
            for s in signals:
                if s.discomfort_type not in summary["discomfort_types"]:
                    summary["discomfort_types"][s.discomfort_type] = 0
                summary["discomfort_types"][s.discomfort_type] += 1
            
            # 获取最近的信号
            recent_signals = sorted(signals, key=lambda x: x.created_at, reverse=True)[:5]
            summary["recent_signals"] = [
                {
                    "signal_id": s.signal_id,
                    "type": s.discomfort_type,
                    "severity": s.severity,
                    "created_at": s.created_at
                }
                for s in recent_signals
            ]
        
        return summary

# 全局不适感服务实例
discomfort_service = DiscomfortService()
