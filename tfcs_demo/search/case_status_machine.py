from search.case_status_rules import CaseStatus, CaseStatusRules
from search.case_status_judge import CaseStatusJudge
from search.case_status_storage import CaseStatusStorage

class CaseStatusMachine:
    """状态转换机制"""
    
    def __init__(self):
        self.status_judge = CaseStatusJudge()
        self.status_storage = CaseStatusStorage()
    
    def transition(self, event_id, current_status, event_info):
        """执行状态转换
        
        Args:
            event_id: 事件ID
            current_status: 当前状态
            event_info: 事件信息字典
            
        Returns:
            tuple: (CaseStatus, str, int) - (新状态, 转换原因, 置信度)
        """
        # 调用大模型辅助判断
        new_status, reason, confidence = self.status_judge.judge_case_status(event_info)
        
        # 检查状态转换是否合法
        if CaseStatusRules.can_transition(current_status, new_status):
            # 保存状态
            self.status_storage.save_status(event_id, new_status, reason, confidence)
            return new_status, reason, confidence
        else:
            # 状态转换不合法，保持当前状态
            return current_status, f"状态转换不合法，保持当前状态", 100
    
    def get_initial_status(self, event_info, event_id=None):
        """获取初始状态
        
        Args:
            event_info: 事件信息字典
            event_id: 事件ID
            
        Returns:
            CaseStatus: 初始状态
        """
        # 调用大模型辅助判断
        status, reason, confidence = self.status_judge.judge_case_status(event_info)
        
        # 如果提供了事件ID，保存状态
        if event_id:
            self.status_storage.save_status(event_id, status, reason, confidence)
        
        return status
    
    def validate_status(self, event_id, status):
        """验证状态是否有效
        
        Args:
            event_id: 事件ID
            status: 状态
            
        Returns:
            bool: 是否有效
        """
        # 检查状态是否是CaseStatus枚举的成员
        return isinstance(status, CaseStatus)
    
    def get_status_history(self, event_id):
        """获取状态历史
        
        Args:
            event_id: 事件ID
            
        Returns:
            list: 状态历史列表
        """
        # 从状态存储中获取历史记录
        return self.status_storage.get_status_history(event_id)
    
    def get_current_status(self, event_id):
        """获取当前状态
        
        Args:
            event_id: 事件ID
            
        Returns:
            tuple: (CaseStatus, str, int, str) - (状态, 转换原因, 置信度, 时间戳)
        """
        return self.status_storage.get_status(event_id)