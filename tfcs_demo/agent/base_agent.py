from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import uuid

class BaseAgent(ABC):
    """
    Agent基类，定义统一的Agent接口
    """
    
    def __init__(self, agent_id: Optional[str] = None):
        """
        初始化Agent
        
        参数:
            agent_id: Agent ID，如果不提供则自动生成
        """
        self.agent_id = agent_id or str(uuid.uuid4())
        self.status = "IDLE"  # IDLE, BUSY, ERROR
        self.created_at = time.time()
        self.last_activity = time.time()
        self.context = {}
    
    def update_status(self, status: str) -> None:
        """
        更新Agent状态
        
        参数:
            status: 新状态
        """
        self.status = status
        self.last_activity = time.time()
    
    def update_context(self, key: str, value: Any) -> None:
        """
        更新Agent上下文
        
        参数:
            key: 上下文键
            value: 上下文值
        """
        self.context[key] = value
        self.last_activity = time.time()
    
    @abstractmethod
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理任务
        
        参数:
            task: 任务数据
            
        返回:
            Dict[str, Any]: 处理结果
        """
        pass
    
    def send_message(self, recipient: 'BaseAgent', message: Dict[str, Any]) -> None:
        """
        发送消息给其他Agent
        
        参数:
            recipient: 接收消息的Agent
            message: 消息内容
        """
        from .communication import communication_manager, Message
        
        self.last_activity = time.time()
        
        # 创建消息对象
        msg = Message(
            sender_id=self.agent_id,
            recipient_id=recipient.agent_id,
            message_type=message.get('type', 'general'),
            content=message
        )
        
        # 注册Agent到通信管理器
        communication_manager.register_agent(self.agent_id, self)
        communication_manager.register_agent(recipient.agent_id, recipient)
        
        # 发送消息
        communication_manager.send_message(msg)
    
    def receive_message(self, sender: 'BaseAgent', message: Dict[str, Any]) -> None:
        """
        接收来自其他Agent的消息
        
        参数:
            sender: 发送消息的Agent
            message: 消息内容
        """
        self.last_activity = time.time()
        # 实际的消息处理逻辑会在子类中实现
    
    def health_check(self) -> bool:
        """
        健康检查
        
        返回:
            bool: Agent是否健康
        """
        return self.status != "ERROR"
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取Agent信息
        
        返回:
            Dict[str, Any]: Agent信息
        """
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "created_at": self.created_at,
            "last_activity": self.last_activity,
            "context": self.context
        }
