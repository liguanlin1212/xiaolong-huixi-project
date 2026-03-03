from ai.inference.model_factory import ModelFactory
from search.case_status_rules import CaseStatus

class CaseStatusJudge:
    """大模型辅助判断逻辑"""
    
    def __init__(self):
        self.model_factory = ModelFactory()
        self.ai_model = self.model_factory.create_runner("OPENAI")
        self.prompt_template = """
你是一个专业的事件分析专家，负责判断事件的结案状态。

请根据以下事件信息，判断该事件是否已结案：

事件信息：
{event_info}

判断标准：
1. 已结案：事件有明确的最终结论，相关方已发布官方声明，且在过去3个月内没有重要的新进展
2. 未结案：事件仍在发展中，没有明确的最终结论，或在过去3个月内有重要的新进展

请返回：
- 结案状态：[已结案/未结案]
- 判断依据：[详细说明判断理由]
- 置信度：[0-100的数字，表示判断的置信程度]
"""
    
    def judge_case_status(self, event_info):
        """判断事件的结案状态
        
        Args:
            event_info: 事件信息字典
            
        Returns:
            tuple: (CaseStatus, str, int) - (状态, 判断依据, 置信度)
        """
        # 构建事件信息字符串
        event_info_str = self._build_event_info_str(event_info)
        
        # 构建prompt
        prompt = self.prompt_template.format(event_info=event_info_str)
        
        # 调用大模型
        try:
            response = self.ai_model.classify_text(prompt)
            
            # 解析响应
            status, reason, confidence = self._parse_response(response)
            
            return status, reason, confidence
        except Exception as e:
            # 如果大模型调用失败，使用规则判断
            from search.case_status_rules import CaseStatusRules
            is_closed, reason = CaseStatusRules.is_closed(event_info)
            status = CaseStatus.CLOSED if is_closed else CaseStatus.OPEN
            return status, f"大模型调用失败，使用规则判断：{reason}", 70
    
    def _build_event_info_str(self, event_info):
        """构建事件信息字符串
        
        Args:
            event_info: 事件信息字典
            
        Returns:
            str: 事件信息字符串
        """
        info_parts = []
        
        if event_info.get("title"):
            info_parts.append(f"事件名称：{event_info['title']}")
        
        if event_info.get("time_range"):
            info_parts.append(f"时间范围：{event_info['time_range']}")
        
        if event_info.get("description"):
            info_parts.append(f"事件描述：{event_info['description']}")
        
        if event_info.get("judgment_evolution"):
            info_parts.append("判断演变过程：")
            for i, evolution in enumerate(event_info['judgment_evolution'], 1):
                info_parts.append(f"  {i}. {evolution}")
        
        if event_info.get("evidence"):
            info_parts.append("关键证据：")
            for i, evidence in enumerate(event_info['evidence'], 1):
                info_parts.append(f"  {i}. {evidence}")
        
        if event_info.get("final_conclusion"):
            info_parts.append(f"最终结论：{event_info['final_conclusion']}")
        
        if event_info.get("sources"):
            info_parts.append("信息来源：")
            for i, source in enumerate(event_info['sources'], 1):
                info_parts.append(f"  {i}. {source}")
        
        return "\n".join(info_parts)
    
    def _parse_response(self, response):
        """解析大模型响应
        
        Args:
            response: 大模型响应文本
            
        Returns:
            tuple: (CaseStatus, str, int) - (状态, 判断依据, 置信度)
        """
        # 提取结案状态
        if "已结案" in response:
            status = CaseStatus.CLOSED
        elif "未结案" in response:
            status = CaseStatus.OPEN
        else:
            status = CaseStatus.OPEN
        
        # 提取判断依据
        reason_start = response.find("判断依据：")
        if reason_start != -1:
            reason_end = response.find("置信度：", reason_start)
            if reason_end != -1:
                reason = response[reason_start + 5:reason_end].strip()
            else:
                reason = response[reason_start + 5:].strip()
        else:
            reason = "大模型未提供判断依据"
        
        # 提取置信度
        confidence_start = response.find("置信度：")
        if confidence_start != -1:
            confidence_str = response[confidence_start + 4:].strip()
            try:
                # 提取数字
                import re
                confidence_match = re.search(r'\d+', confidence_str)
                if confidence_match:
                    confidence = int(confidence_match.group())
                    # 确保置信度在0-100之间
                    confidence = max(0, min(100, confidence))
                else:
                    confidence = 70
            except Exception:
                confidence = 70
        else:
            confidence = 70
        
        return status, reason, confidence