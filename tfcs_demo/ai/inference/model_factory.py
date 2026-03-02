from typing import Dict, Type, Optional
from .base_runner import BaseAIModelRunner
from .npu_runner import NPURunner
from .openai_runner import OpenAIModelRunner

class ModelFactory:
    """
    模型工厂类，用于根据配置创建不同的AI模型运行器
    """
    
    # 模型运行器映射
    _runners: Dict[str, Type[BaseAIModelRunner]] = {
        "NPU": NPURunner,
        "OPENAI": OpenAIModelRunner
    }
    
    @classmethod
    def create_runner(cls, model_name: str, **kwargs) -> Optional[BaseAIModelRunner]:
        """
        根据模型名称创建模型运行器
        
        参数:
            model_name: 模型名称
            **kwargs: 初始化参数
            
        返回:
            Optional[BaseAIModelRunner]: 模型运行器实例
        """
        if model_name not in cls._runners:
            print(f"不支持的模型类型: {model_name}")
            return None
        
        try:
            runner_class = cls._runners[model_name]
            runner = runner_class()
            runner.initialize(**kwargs)
            return runner
        except Exception as e:
            print(f"创建模型运行器失败: {e}")
            return None
    
    @classmethod
    def list_supported_models(cls) -> list:
        """
        列出所有支持的模型类型
        
        返回:
            list: 支持的模型类型列表
        """
        return list(cls._runners.keys())
    
    @classmethod
    def is_model_supported(cls, model_name: str) -> bool:
        """
        检查模型是否支持
        
        参数:
            model_name: 模型名称
            
        返回:
            bool: 是否支持
        """
        return model_name in cls._runners
