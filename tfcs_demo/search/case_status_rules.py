from enum import Enum

class CaseStatus(Enum):
    """结案状态枚举"""
    PENDING = "待审核"
    OPEN = "未结案"
    CLOSED = "已结案"

class CaseStatusRules:
    """结案状态判定规则"""
    
    @staticmethod
    def is_closed(event_info):
        """判断事件是否已结案
        
        Args:
            event_info: 事件信息字典
            
        Returns:
            bool: 是否已结案
            str: 判断依据
        """
        # 检查是否有明确的结案状态
        case_status = event_info.get("case_status", "").lower()
        if "已结案" in case_status:
            return True, "事件明确标记为已结案"
        elif "未结案" in case_status:
            return False, "事件明确标记为未结案"
        
        # 检查时间范围
        time_range = event_info.get("time_range", "")
        if time_range:
            from datetime import datetime, timedelta
            # 尝试提取结束时间
            end_time_str = time_range.split("至")[-1].strip()
            try:
                # 尝试不同的日期格式
                end_time = None
                for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日"]:
                    try:
                        end_time = datetime.strptime(end_time_str, fmt)
                        break
                    except ValueError:
                        continue
                
                if end_time:
                    # 如果结束时间在3个月内，认为未结案
                    if datetime.now() - end_time < timedelta(days=90):
                        return False, "事件结束时间在3个月内，可能尚未结案"
            except Exception as e:
                pass
        
        # 检查判断演变过程
        judgment_evolution = event_info.get("judgment_evolution", [])
        if not judgment_evolution:
            return False, "事件缺少判断演变过程，无法确定结案状态"
        
        # 检查是否有最终结论
        final_conclusion = event_info.get("final_conclusion", "")
        if not final_conclusion:
            return False, "事件缺少最终结论，可能尚未结案"
        
        # 检查是否有官方声明
        sources = event_info.get("sources", [])
        has_official_source = any("官方" in source or "政府" in source or "权威" in source for source in sources)
        if not has_official_source:
            return False, "事件缺少官方或权威来源，无法确定结案状态"
        
        # 默认认为已结案
        return True, "事件满足已结案条件"
    
    @staticmethod
    def get_status(event_info):
        """获取事件的结案状态
        
        Args:
            event_info: 事件信息字典
            
        Returns:
            CaseStatus: 结案状态
        """
        is_closed, _ = CaseStatusRules.is_closed(event_info)
        if is_closed:
            return CaseStatus.CLOSED
        else:
            return CaseStatus.OPEN
    
    @staticmethod
    def can_transition(current_status, new_status):
        """检查状态转换是否合法
        
        Args:
            current_status: 当前状态
            new_status: 新状态
            
        Returns:
            bool: 是否可以转换
        """
        # 状态转换规则
        allowed_transitions = {
            CaseStatus.PENDING: [CaseStatus.OPEN, CaseStatus.CLOSED],
            CaseStatus.OPEN: [CaseStatus.CLOSED],
            CaseStatus.CLOSED: []  # 已结案状态不能转换
        }
        
        return new_status in allowed_transitions.get(current_status, [])