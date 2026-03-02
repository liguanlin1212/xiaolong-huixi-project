from typing import Dict, Any, List
from .base_agent import BaseAgent

class OrganizationAgent(BaseAgent):
    """
    整理Agent，负责信息整理与展示
    """
    
    def __init__(self, agent_id: str = None):
        """
        初始化整理Agent
        
        参数:
            agent_id: Agent ID
        """
        super().__init__(agent_id)
    
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理整理任务
        
        参数:
            task: 任务数据，包含分析结果和时间线
            
        返回:
            Dict[str, Any]: 整理结果
        """
        self.update_status("BUSY")
        
        try:
            analysis = task.get("analysis")
            timeline = task.get("timeline", [])
            
            if not analysis:
                return {
                    "status": "error",
                    "message": "分析结果不能为空"
                }
            
            # 整理信息
            organized_info = self._organize_information(analysis, timeline)
            
            # 生成展示内容
            presentation = self._generate_presentation(organized_info)
            
            self.update_status("IDLE")
            return {
                "status": "success",
                "organized_info": organized_info,
                "presentation": presentation
            }
        except Exception as e:
            self.update_status("ERROR")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _organize_information(self, analysis: Dict[str, Any], timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        整理信息
        
        参数:
            analysis: 分析结果
            timeline: 时间线数据
            
        返回:
            Dict[str, Any]: 整理后的信息
        """
        # 整理信息
        return {
            "summary": "事件判断演变 summary",
            "initial_judgment": analysis.get("initial_judgment"),
            "evolved_judgment": analysis.get("evolved_judgment"),
            "key_factors": analysis.get("key_factors", []),
            "confidence": analysis.get("confidence"),
            "timeline": timeline,
            "insights": ["洞察1", "洞察2", "洞察3"]
        }
    
    def _generate_presentation(self, organized_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成展示内容
        
        参数:
            organized_info: 整理后的信息
            
        返回:
            Dict[str, Any]: 展示内容
        """
        # 生成展示内容
        return {
            "title": "事件判断演变分析报告",
            "summary": organized_info.get("summary"),
            "sections": [
                {
                    "title": "判断演变",
                    "content": [
                        f"初始判断: {organized_info.get('initial_judgment')}",
                        f"演变后判断: {organized_info.get('evolved_judgment')}",
                        f"置信度: {organized_info.get('confidence', 0) * 100}%"
                    ]
                },
                {
                    "title": "关键因素",
                    "content": organized_info.get("key_factors", [])
                },
                {
                    "title": "时间线",
                    "content": [
                        f"{item['timestamp']}: {item['event']} - {item['judgment']}"
                        for item in organized_info.get("timeline", [])
                    ]
                },
                {
                    "title": "洞察",
                    "content": organized_info.get("insights", [])
                }
            ]
        }
    
    def receive_message(self, sender: BaseAgent, message: Dict[str, Any]) -> None:
        """
        接收来自其他Agent的消息
        
        参数:
            sender: 发送消息的Agent
            message: 消息内容
        """
        super().receive_message(sender, message)
        
        # 处理整理请求消息
        if message.get("type") == "organization_request":
            analysis = message.get("analysis")
            timeline = message.get("timeline", [])
            if analysis:
                result = self.process({"analysis": analysis, "timeline": timeline})
                # 发送整理结果回 sender
                self.send_message(sender, {
                    "type": "organization_result",
                    "organized_info": result.get("organized_info"),
                    "presentation": result.get("presentation")
                })
