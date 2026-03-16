from typing import Dict, Any
from .base_runner import BaseAIModelRunner
import requests

class OllamaModelRunner(BaseAIModelRunner):
    def initialize(self, **kwargs) -> None:
        """
        初始化Ollama模型运行器
        
        参数:
            **kwargs: 初始化参数，包括model_name和base_url
        """
        self.model_name = kwargs.get("model_name", "qwen3:8b")
        self.base_url = kwargs.get("base_url", "http://localhost:11434/api")
        self.timeout = kwargs.get("timeout", 30)
    
    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        使用Ollama模型对文本进行分类
        
        参数:
            text: 待分类的文本
            
        返回:
            Dict[str, Any]: 分类结果，包含label和confidence字段
        """
        # 构建提示词
        prompt = f"Classify the following text into one of the categories: EMOTIONAL, EVIDENCE, LEGAL, FACTUAL, OTHER. Text: {text}"
        
        try:
            # 调用Ollama API
            response = requests.post(
                f"{self.base_url}/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.1
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "").strip()
                
                # 解析分类结果
                label = "OTHER"
                if "EMOTIONAL" in generated_text:
                    label = "EMOTIONAL"
                elif "EVIDENCE" in generated_text:
                    label = "EVIDENCE"
                elif "LEGAL" in generated_text:
                    label = "LEGAL"
                elif "FACTUAL" in generated_text:
                    label = "FACTUAL"
                    
                return {"label": label, "confidence": 0.85}
            else:
                # API调用失败，返回默认结果
                return {"label": "OTHER", "confidence": 0.5}
        except Exception as e:
            # 发生异常，返回默认结果
            print(f"Ollama API调用失败: {e}")
            return {"label": "OTHER", "confidence": 0.5}
    
    def health_check(self) -> bool:
        """
        健康检查，验证Ollama服务是否可以正常工作
        
        返回:
            bool: 模型是否健康
        """
        try:
            # 尝试调用Ollama API的tags端点
            response = requests.get(f"{self.base_url}/tags", timeout=self.timeout)
            return response.status_code == 200
        except Exception:
            # 发生异常，返回False
            return False