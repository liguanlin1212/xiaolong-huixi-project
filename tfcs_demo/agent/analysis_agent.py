from typing import Dict, Any, List
from .base_agent import BaseAgent
from ai.config import AIConfig
from ai.inference.model_factory import ModelFactory

class AnalysisAgent(BaseAgent):
    """
    分析Agent，负责判断分析与时间线构建
    """
    
    def __init__(self, agent_id: str = None):
        """
        初始化分析Agent
        
        参数:
            agent_id: Agent ID
        """
        super().__init__(agent_id)
        self.config = AIConfig()
        self.model_config = self.config.get_model_config("OPENAI")
        # 移除model_config中的model_name字段，避免参数重复
        model_config = self.model_config.copy()
        model_config.pop("model_name", None)
        self.runner = ModelFactory.create_runner("OPENAI", **model_config)
    
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理分析任务
        
        参数:
            task: 任务数据，包含需要分析的信息
            
        返回:
            Dict[str, Any]: 分析结果
        """
        self.update_status("BUSY")
        
        try:
            search_results = task.get("search_results", [])
            if not search_results:
                return {
                    "status": "error",
                    "message": "搜索结果不能为空"
                }
            
            # 分析判断演变
            analysis_result = self._analyze_judgment_evolution(search_results)
            
            # 构建时间线
            timeline = self._build_timeline(analysis_result)
            
            self.update_status("IDLE")
            return {
                "status": "success",
                "analysis": analysis_result,
                "timeline": timeline
            }
        except Exception as e:
            self.update_status("ERROR")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _analyze_judgment_evolution(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析判断演变
        
        参数:
            search_results: 搜索结果
            
        返回:
            Dict[str, Any]: 分析结果
        """
        # 模拟分析判断演变
        return {
            "initial_judgment": "初始判断",
            "evolved_judgment": "演变后的判断",
            "key_factors": ["因素1", "因素2", "因素3"],
            "confidence": 0.85
        }
    
    def _build_timeline(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        构建时间线
        
        参数:
            analysis_result: 分析结果
            
        返回:
            List[Dict[str, Any]]: 时间线数据
        """
        # 模拟构建时间线
        return [
            {
                "timestamp": "2026-02-20",
                "event": "事件发生",
                "judgment": "初始判断",
                "evidence": "初步证据"
            },
            {
                "timestamp": "2026-02-25",
                "event": "新证据出现",
                "judgment": "判断调整",
                "evidence": "新证据"
            },
            {
                "timestamp": "2026-03-01",
                "event": "最终结论",
                "judgment": "最终判断",
                "evidence": "完整证据链"
            }
        ]
    
    def receive_message(self, sender: BaseAgent, message: Dict[str, Any]) -> None:
        """
        接收来自其他Agent的消息
        
        参数:
            sender: 发送消息的Agent
            message: 消息内容
        """
        super().receive_message(sender, message)
        
        # 处理分析请求消息
        if message.get("type") == "analysis_request":
            search_results = message.get("search_results", [])
            if search_results:
                result = self.process({"search_results": search_results})
                # 发送分析结果回 sender
                self.send_message(sender, {
                    "type": "analysis_result",
                    "analysis": result.get("analysis"),
                    "timeline": result.get("timeline")
                })
