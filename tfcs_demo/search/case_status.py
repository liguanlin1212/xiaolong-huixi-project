from datetime import datetime, timedelta

class CaseStatusChecker:
    def __init__(self):
        pass
    
    def check_case_status(self, event_info):
        """检查事件的结案状态"""
        if not event_info:
            return False, "事件信息为空"
        
        # 从事件信息中提取结案状态
        case_status = event_info.get("case_status", "").lower()
        
        if "未结案" in case_status:
            return False, "该事件尚未结案，暂不展示"
        elif "已结案" in case_status:
            return True, ""
        else:
            # 如果没有明确的结案状态，需要进一步判断
            return self.judge_case_status(event_info)
    
    def judge_case_status(self, event_info):
        """判断事件的结案状态"""
        # 检查时间范围
        time_range = event_info.get("time_range", "")
        if time_range:
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
                        return False, "该事件结束时间在3个月内，可能尚未结案"
            except Exception as e:
                print(f"解析时间失败: {e}")
        
        # 检查判断演变过程
        judgment_evolution = event_info.get("judgment_evolution", [])
        if not judgment_evolution:
            return False, "该事件缺少判断演变过程，无法确定结案状态"
        
        # 检查是否有最终结论
        final_conclusion = event_info.get("final_conclusion", "")
        if not final_conclusion:
            return False, "该事件缺少最终结论，可能尚未结案"
        
        # 默认认为已结案
        return True, ""
    
    def is_case_closed(self, event_info):
        """判断事件是否已结案"""
        is_closed, message = self.check_case_status(event_info)
        return is_closed
    
    def get_rejection_message(self, event_info):
        """获取拒绝展示的消息"""
        is_closed, message = self.check_case_status(event_info)
        if not is_closed:
            return message
        return ""