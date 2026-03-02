from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIModelRunner(ABC):
    """
    AI模型运行器抽象基类，定义统一的接口规范
    """
    
    @abstractmethod
    def initialize(self, **kwargs) -> None:
        """
        初始化模型运行器
        
        参数:
            **kwargs: 初始化参数
        """
        pass
    
    @abstractmethod
    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        对文本进行分类
        
        参数:
            text: 待分类的文本
            
        返回:
            Dict[str, Any]: 分类结果，包含label和confidence字段
        """
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """
        健康检查，验证模型是否可以正常工作
        
        返回:
            bool: 模型是否健康
        """
        pass
