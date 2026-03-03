import re
from datetime import datetime
from typing import List, Dict, Optional, Set
from search.version_manager import VersionManager
from search.version_history import VersionHistory
from search.case_status_machine import CaseStatusMachine
from ai.inference.model_factory import ModelFactory

class SelfCorrectionMechanism:
    """自查纠错机制"""
    
    def __init__(self, version_manager: VersionManager, version_history: VersionHistory, case_status_machine: CaseStatusMachine):
        """初始化自查纠错机制
        
        Args:
            version_manager: 版本管理器实例
            version_history: 版本历史实例
            case_status_machine: 案件状态机实例
        """
        self.version_manager = version_manager
        self.version_history = version_history
        self.case_status_machine = case_status_machine
        self.model_factory = ModelFactory()
        self.ai_model = self.model_factory.create_runner("OPENAI")
    
    def analyze_new_information(self, new_information: str) -> Dict:
        """分析新信息
        
        Args:
            new_information: 新信息内容
            
        Returns:
            dict: 分析结果，包含关键词、时间信息、事件关联等
        """
        # 提取关键词
        keywords = self._extract_keywords(new_information)
        
        # 提取时间信息
        time_info = self._extract_time_info(new_information)
        
        # 分析事件关联
        related_events = self._find_related_events(keywords)
        
        return {
            "keywords": keywords,
            "time_info": time_info,
            "related_events": related_events
        }
    
    def trace_impact(self, new_information: str) -> Dict[str, List[Dict]]:
        """追踪新信息对旧判断的影响
        
        Args:
            new_information: 新信息内容
            
        Returns:
            dict: 影响分析结果，包含受影响的事件和版本
        """
        analysis = self.analyze_new_information(new_information)
        impact_results = {}
        
        for event_id in analysis["related_events"]:
            versions = self.version_manager.get_versions(event_id)
            affected_versions = []
            
            for version in versions:
                if self._is_version_affected(version, analysis):
                    affected_versions.append({
                        "version_id": version.version_id,
                        "timestamp": version.timestamp,
                        "content": version.content,
                        "impacted_aspects": self._identify_impacted_aspects(version, analysis)
                    })
            
            if affected_versions:
                impact_results[event_id] = affected_versions
        
        return impact_results
    
    def generate_correction_suggestions(self, impact_results: Dict[str, List[Dict]], new_information: str) -> Dict[str, List[Dict]]:
        """生成纠错建议
        
        Args:
            impact_results: 影响分析结果
            new_information: 新信息内容
            
        Returns:
            dict: 纠错建议，包含每个受影响事件的建议
        """
        suggestions = {}
        
        for event_id, affected_versions in impact_results.items():
            event_suggestions = []
            
            for version_info in affected_versions:
                suggestion = self._generate_single_suggestion(version_info, new_information)
                event_suggestions.append({
                    "version_id": version_info["version_id"],
                    "suggestion": suggestion,
                    "confidence": self._calculate_confidence(version_info, new_information)
                })
            
            if event_suggestions:
                suggestions[event_id] = event_suggestions
        
        return suggestions
    
    def process_self_correction(self, new_information: str) -> Dict:
        """处理自查纠错流程
        
        Args:
            new_information: 新信息内容
            
        Returns:
            dict: 完整的自查纠错结果
        """
        # 追踪影响
        impact_results = self.trace_impact(new_information)
        
        # 生成纠错建议
        suggestions = self.generate_correction_suggestions(impact_results, new_information)
        
        # 执行自动纠错（如果需要）
        correction_results = self._execute_corrections(suggestions, new_information)
        
        return {
            "impact_results": impact_results,
            "suggestions": suggestions,
            "correction_results": correction_results
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取逻辑，处理中英文
        import re
        # 分割成单词（英文）和字符（中文）
        words = []
        # 提取中文词语（2个或以上字符）
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        words.extend(chinese_words)
        # 提取英文单词
        english_words = re.findall(r'[a-zA-Z]{2,}', text)
        words.extend(english_words)
        # 提取数字组合
        numbers = re.findall(r'\d+', text)
        words.extend(numbers)
        return words
    
    def _extract_time_info(self, text: str) -> Optional[str]:
        """提取时间信息"""
        # 简单的时间提取逻辑
        time_patterns = [
            r"\d{4}-\d{2}-\d{2}",
            r"\d{2}/\d{2}/\d{4}",
            r"\d{4}年\d{1,2}月\d{1,2}日"
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return None
    
    def _find_related_events(self, keywords: List[str]) -> List[str]:
        """查找相关事件"""
        related_events = []
        
        # 遍历所有事件，检查关键词匹配
        for event_id, version_ids in self.version_manager.event_versions.items():
            for version_id in version_ids:
                version = self.version_manager.get_version(version_id)
                if version:
                    # 简单的关键词匹配
                    if any(keyword in version.content for keyword in keywords):
                        related_events.append(event_id)
                        break
        
        return related_events
    
    def _is_version_affected(self, version, analysis: Dict) -> bool:
        """判断版本是否受影响"""
        # 检查关键词匹配
        if any(keyword in version.content for keyword in analysis["keywords"]):
            return True
        
        # 检查时间冲突
        if analysis["time_info"]:
            # 简单的时间冲突检查
            if analysis["time_info"] in version.content:
                return True
        
        return False
    
    def _identify_impacted_aspects(self, version, analysis: Dict) -> List[str]:
        """识别受影响的方面"""
        impacted = []
        
        # 检查事件描述
        if any(keyword in version.content for keyword in analysis["keywords"]):
            impacted.append("事件描述")
        
        # 检查时间信息
        if analysis["time_info"] and analysis["time_info"] in version.content:
            impacted.append("时间信息")
        
        # 检查结论
        if "结论" in version.content or "判断" in version.content:
            impacted.append("结论")
        
        return impacted
    
    def _generate_single_suggestion(self, version_info: Dict, new_information: str) -> str:
        """生成单个版本的纠错建议"""
        # 使用大模型生成纠错建议
        prompt = f"""
        以下是一个旧的判断版本和新的信息，请分析新信息对旧判断的影响，并生成纠错建议：
        
        旧判断版本内容：
        {version_info['content']}
        
        新信息：
        {new_information}
        
        请生成详细的纠错建议，包括：
        1. 受影响的具体内容
        2. 错误原因分析
        3. 修正建议
        4. 修正后的内容
        """
        
        try:
            response = self.ai_model.classify_text(prompt)
            return response
        except Exception as e:
            return f"生成纠错建议失败: {e}"
    
    def _calculate_confidence(self, version_info: Dict, new_information: str) -> float:
        """计算纠错建议的置信度"""
        # 简单的置信度计算逻辑
        keyword_overlap = len([k for k in self._extract_keywords(new_information) if k in version_info['content']])
        total_keywords = len(self._extract_keywords(new_information))
        
        if total_keywords == 0:
            return 0.0
        
        return min(keyword_overlap / total_keywords, 1.0)
    
    def _execute_corrections(self, suggestions: Dict[str, List[Dict]], new_information: str) -> Dict:
        """执行自动纠错"""
        correction_results = {}
        
        for event_id, event_suggestions in suggestions.items():
            for suggestion_info in event_suggestions:
                if suggestion_info['confidence'] > 0.7:  # 只对高置信度的建议进行自动纠错
                    # 创建新版本
                    latest_version = self.version_manager.get_latest_version(event_id)
                    parent_version_id = latest_version.version_id if latest_version else None
                    
                    # 提取修正后的内容
                    corrected_content = self._extract_corrected_content(suggestion_info['suggestion'])
                    
                    if corrected_content:
                        new_version = self.version_manager.create_version(
                            event_id, 
                            corrected_content, 
                            parent_version_id
                        )
                        
                        if event_id not in correction_results:
                            correction_results[event_id] = []
                        
                        correction_results[event_id].append({
                            "old_version_id": suggestion_info['version_id'],
                            "new_version_id": new_version.version_id,
                            "confidence": suggestion_info['confidence']
                        })
        
        return correction_results
    
    def _extract_corrected_content(self, suggestion: str) -> Optional[str]:
        """从建议中提取修正后的内容"""
        # 处理字典类型的返回值
        if isinstance(suggestion, dict):
            return None
        
        # 简单的提取逻辑，实际应用中可能需要更复杂的解析
        lines = suggestion.split('\n')
        in_corrected_section = False
        corrected_lines = []
        
        for line in lines:
            if '修正后的内容' in line:
                in_corrected_section = True
                continue
            elif in_corrected_section and line.strip() and not line.startswith('---'):
                corrected_lines.append(line)
            elif in_corrected_section and (line.strip() == '' or line.startswith('---')):
                break
        
        if corrected_lines:
            return '\n'.join(corrected_lines)
        return None
