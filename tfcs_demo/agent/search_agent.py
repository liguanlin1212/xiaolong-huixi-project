from typing import Dict, Any, List
from .base_agent import BaseAgent
from ai.config import AIConfig
from ai.inference.model_factory import ModelFactory

class SearchAgent(BaseAgent):
    """
    搜索Agent，负责全网信息检索
    """
    
    def __init__(self, agent_id: str = None):
        """
        初始化搜索Agent
        
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
        处理搜索任务
        
        参数:
            task: 任务数据，包含搜索关键词
            
        返回:
            Dict[str, Any]: 搜索结果
        """
        self.update_status("BUSY")
        
        try:
            keyword = task.get("keyword", "")
            if not keyword:
                return {
                    "status": "error",
                    "message": "搜索关键词不能为空"
                }
            
            # 使用大模型进行全网搜索
            search_results = self._perform_search(keyword)
            
            # 处理搜索结果
            processed_results = self._process_search_results(search_results)
            
            self.update_status("IDLE")
            return {
                "status": "success",
                "results": processed_results
            }
        except Exception as e:
            self.update_status("ERROR")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _perform_search(self, keyword: str) -> str:
        """
        执行搜索
        
        参数:
            keyword: 搜索关键词
            
        返回:
            str: 搜索结果
        """
        if not self.runner:
            # 如果没有大模型，返回模拟结果
            return f"模拟搜索结果：{keyword}的相关信息"
        
        # 使用大模型进行搜索
        prompt = f"""
        请模拟全网搜索关于"{keyword}"的信息，包括：
        1. 事件背景
        2. 相关事实
        3. 不同观点
        4. 最新进展
        
        请提供详细的搜索结果，不要编造信息。
        """
        
        # 这里使用分类接口作为临时解决方案，实际应该使用专门的搜索接口
        # 后续会实现更完善的搜索功能
        result = self.runner.classify_text(prompt)
        return prompt  # 临时返回提示词作为结果
    
    def _process_search_results(self, search_results: str) -> List[Dict[str, Any]]:
        """
        处理搜索结果
        
        参数:
            search_results: 搜索结果
            
        返回:
            List[Dict[str, Any]]: 处理后的搜索结果
        """
        # 模拟处理搜索结果
        return [
            {
                "title": "搜索结果1",
                "content": search_results[:200] + "...",
                "source": "模拟来源",
                "timestamp": "2026-03-02"
            },
            {
                "title": "搜索结果2",
                "content": "更多相关信息...",
                "source": "模拟来源2",
                "timestamp": "2026-03-01"
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
        
        # 处理搜索请求消息
        if message.get("type") == "search_request":
            keyword = message.get("keyword")
            if keyword:
                result = self.process({"keyword": keyword})
                # 发送搜索结果回 sender
                self.send_message(sender, {
                    "type": "search_result",
                    "results": result.get("results", [])
                })
