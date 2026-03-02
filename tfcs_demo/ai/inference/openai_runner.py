from typing import Dict, Any
import time
import openai
from .base_runner import BaseAIModelRunner

class OpenAIModelRunner(BaseAIModelRunner):
    """
    OpenAI模型运行器，使用OpenAI的大模型进行文本分类
    """
    
    def __init__(self):
        """
        初始化OpenAI模型运行器
        """
        self.api_key = None
        self.model_name = "gpt-4o"
        self.client = None
        self.max_retries = 3
        self.retry_delay = 1
    
    def initialize(self, **kwargs) -> None:
        """
        初始化模型运行器
        
        参数:
            **kwargs: 初始化参数，包括api_key和model_name
        """
        self.api_key = kwargs.get("api_key")
        self.model_name = kwargs.get("model_name", "gpt-4o")
        
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            print("警告: 未提供OpenAI API密钥")
    
    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        对文本进行分类
        
        参数:
            text: 待分类的文本
            
        返回:
            Dict[str, Any]: 分类结果，包含label和confidence字段
        """
        if not self.client:
            return {
                "label": "EMOTIONAL",
                "confidence": 0.5
            }
        
        prompt = f"""
        请对以下文本进行分类，返回最匹配的类别和置信度：
        
        文本：{text}
        
        类别选项：
        - EMOTIONAL: 情感表达，如悲伤、愤怒、恐惧等
        - EVIDENCE: 证据或事实陈述
        - LEGAL: 法律相关内容
        
        请以JSON格式返回结果，包含label和confidence字段，confidence为0-1之间的浮点数。
        """
        
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "你是一个文本分类助手，擅长将文本分类为情感表达、证据或法律相关内容。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                
                # 解析响应
                result = eval(response.choices[0].message.content)
                return result
            except Exception as e:
                print(f"OpenAI API调用失败: {e}")
                retry_count += 1
                if retry_count < self.max_retries:
                    print(f"第{retry_count}次重试...")
                    time.sleep(self.retry_delay * (2 ** (retry_count - 1)))
                else:
                    print("达到最大重试次数，返回默认结果")
                    return {
                        "label": "EMOTIONAL",
                        "confidence": 0.5
                    }
    
    def health_check(self) -> bool:
        """
        健康检查，验证模型是否可以正常工作
        
        返回:
            bool: 模型是否健康
        """
        if not self.client:
            return False
        
        try:
            # 发送一个简单的测试请求
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": "健康检查测试"
                    }
                ],
                max_tokens=10
            )
            return True
        except Exception as e:
            print(f"健康检查失败: {e}")
            return False
