import re

class SearchAnalyzer:
    def __init__(self):
        pass
    
    def analyze_results(self, raw_results):
        """分析搜索结果"""
        if not raw_results:
            return []
        
        # 解析搜索结果
        results = []
        
        # 处理字典类型的输入（如OpenAI模型返回的结果）
        if isinstance(raw_results, dict):
            # 对于字典类型，创建一个模拟的搜索结果
            result = {
                "title": "搜索结果",
                "description": "这是一个搜索结果",
                "time_range": "2024-2026",
                "case_status": "已结案",
                "judgment_evolution": ["初始判断", "修正判断", "最终结论"],
                "evidence": ["证据1", "证据2", "证据3"],
                "final_conclusion": "最终结论",
                "sources": []
            }
            results.append(result)
        else:
            # 假设raw_results是大模型返回的文本
            # 这里实现对文本的解析
            parsed_result = self.parse_model_response(str(raw_results))
            if parsed_result:
                results.append(parsed_result)
        
        return results
    
    def parse_model_response(self, response):
        """解析大模型响应"""
        result = {
            "title": "",
            "description": "",
            "time_range": "",
            "case_status": "",
            "judgment_evolution": [],
            "evidence": [],
            "final_conclusion": "",
            "sources": []
        }
        
        # 解析事件概述
        overview_match = re.search(r'## 事件概述(.*?)## 判断演变过程', response, re.DOTALL)
        if overview_match:
            overview_text = overview_match.group(1)
            # 提取事件名称
            name_match = re.search(r'- 事件名称：(.*)', overview_text)
            if name_match:
                result["title"] = name_match.group(1).strip()
            # 提取时间范围
            time_match = re.search(r'- 时间范围：(.*)', overview_text)
            if time_match:
                result["time_range"] = time_match.group(1).strip()
            # 提取事件描述
            desc_match = re.search(r'- 事件描述：(.*)', overview_text)
            if desc_match:
                result["description"] = desc_match.group(1).strip()
            # 提取结案状态
            status_match = re.search(r'- 结案状态：(.*)', overview_text)
            if status_match:
                result["case_status"] = status_match.group(1).strip()
        
        # 解析判断演变过程
        evolution_match = re.search(r'## 判断演变过程(.*?)## 关键证据', response, re.DOTALL)
        if evolution_match:
            evolution_text = evolution_match.group(1)
            # 提取演变过程
            evolution_items = re.findall(r'\d+\. (.*?)(?=\n\d+\. |\n## |$)', evolution_text, re.DOTALL)
            result["judgment_evolution"] = [item.strip() for item in evolution_items]
        
        # 解析关键证据
        evidence_match = re.search(r'## 关键证据(.*?)## 最终结论', response, re.DOTALL)
        if evidence_match:
            evidence_text = evidence_match.group(1)
            # 提取证据
            evidence_items = re.findall(r'\d+\. (.*?)(?=\n\d+\. |\n## |$)', evidence_text, re.DOTALL)
            result["evidence"] = [item.strip() for item in evidence_items]
        
        # 解析最终结论
        conclusion_match = re.search(r'## 最终结论(.*?)## 信息来源', response, re.DOTALL)
        if conclusion_match:
            result["final_conclusion"] = conclusion_match.group(1).strip()
        
        # 解析信息来源
        sources_match = re.search(r'## 信息来源(.*)', response, re.DOTALL)
        if sources_match:
            sources_text = sources_match.group(1)
            # 提取来源
            sources_items = sources_text.strip().split('\n')
            result["sources"] = [item.strip() for item in sources_items if item.strip()]
        
        return result
    
    def extract_judgment_evolution(self, text):
        """提取判断演变过程"""
        # 这里可以实现更复杂的提取逻辑
        # 例如，从文本中识别时间点和对应的判断
        return []
    
    def validate_results(self, results):
        """验证搜索结果的有效性"""
        valid_results = []
        for result in results:
            if result.get("title") and result.get("description"):
                valid_results.append(result)
        return valid_results