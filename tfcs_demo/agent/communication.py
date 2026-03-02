from typing import Dict, Any, List, Optional
import queue
import threading
import time
import uuid

class Message:
    """
    消息类，定义消息格式
    """
    
    def __init__(self, sender_id: str, recipient_id: str, message_type: str, content: Dict[str, Any]):
        """
        初始化消息
        
        参数:
            sender_id: 发送者ID
            recipient_id: 接收者ID
            message_type: 消息类型
            content: 消息内容
        """
        self.message_id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.message_type = message_type
        self.content = content
        self.timestamp = time.time()
        self.status = "PENDING"  # PENDING, SENT, DELIVERED, FAILED
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将消息转换为字典
        
        返回:
            Dict[str, Any]: 消息字典
        """
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "message_type": self.message_type,
            "content": self.content,
            "timestamp": self.timestamp,
            "status": self.status
        }

class MessageQueue:
    """
    消息队列类，管理消息的发送和接收
    """
    
    def __init__(self):
        """
        初始化消息队列
        """
        self.queue = queue.Queue()
        self.lock = threading.Lock()
    
    def put(self, message: Message) -> None:
        """
        放入消息
        
        参数:
            message: 消息对象
        """
        with self.lock:
            self.queue.put(message)
    
    def get(self, block: bool = True, timeout: Optional[float] = None) -> Optional[Message]:
        """
        获取消息
        
        参数:
            block: 是否阻塞
            timeout: 超时时间
            
        返回:
            Optional[Message]: 消息对象
        """
        try:
            return self.queue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None
    
    def qsize(self) -> int:
        """
        获取队列大小
        
        返回:
            int: 队列大小
        """
        with self.lock:
            return self.queue.qsize()

class CommunicationManager:
    """
    通信管理器，管理Agent之间的通信
    """
    
    def __init__(self):
        """
        初始化通信管理器
        """
        self.message_queue = MessageQueue()
        self.agent_registry = {}
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_messages, daemon=True)
        self.worker_thread.start()
    
    def register_agent(self, agent_id: str, agent) -> None:
        """
        注册Agent
        
        参数:
            agent_id: Agent ID
            agent: Agent对象
        """
        self.agent_registry[agent_id] = agent
    
    def unregister_agent(self, agent_id: str) -> None:
        """
        注销Agent
        
        参数:
            agent_id: Agent ID
        """
        if agent_id in self.agent_registry:
            del self.agent_registry[agent_id]
    
    def send_message(self, message: Message) -> None:
        """
        发送消息
        
        参数:
            message: 消息对象
        """
        message.status = "SENT"
        self.message_queue.put(message)
    
    def _process_messages(self) -> None:
        """
        处理消息
        """
        while self.running:
            try:
                message = self.message_queue.get(block=True, timeout=1)
                if message:
                    self._deliver_message(message)
            except Exception as e:
                print(f"处理消息时出错: {e}")
    
    def _deliver_message(self, message: Message) -> None:
        """
        传递消息
        
        参数:
            message: 消息对象
        """
        recipient_id = message.recipient_id
        if recipient_id in self.agent_registry:
            try:
                recipient = self.agent_registry[recipient_id]
                # 找到发送者
                sender = None
                if message.sender_id in self.agent_registry:
                    sender = self.agent_registry[message.sender_id]
                # 传递消息
                recipient.receive_message(sender, message.content)
                message.status = "DELIVERED"
            except Exception as e:
                print(f"传递消息时出错: {e}")
                message.status = "FAILED"
        else:
            message.status = "FAILED"
    
    def stop(self) -> None:
        """
        停止通信管理器
        """
        self.running = False
        if self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2)

# 全局通信管理器实例
communication_manager = CommunicationManager()
