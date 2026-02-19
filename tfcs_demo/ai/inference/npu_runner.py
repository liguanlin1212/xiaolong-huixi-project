from typing import Dict, Any
import os
import numpy as np

class NPURunner:
    """
    基于 ONNX Runtime 的 NPU 运行器
    """
    
    def __init__(self):
        self.model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "ai", "models", "narrative_classifier.onnx"
        )
        self.session = None
        self._initialize_onnx_session()
    
    def _initialize_onnx_session(self):
        """
        初始化 ONNX Runtime 会话
        """
        try:
            import onnxruntime as ort
            if os.path.exists(self.model_path):
                # 优先使用 NPU 执行提供程序（如果可用）
                providers = ["CPUExecutionProvider"]
                # 尝试添加 NPU 执行提供程序（如果可用）
                available_providers = ort.get_available_providers()
                if "DmlExecutionProvider" in available_providers:
                    providers.insert(0, "DmlExecutionProvider")
                elif "CUDAExecutionProvider" in available_providers:
                    providers.insert(0, "CUDAExecutionProvider")
                
                self.session = ort.InferenceSession(
                    self.model_path,
                    providers=providers
                )
                print(f"成功加载 ONNX 模型，使用执行提供程序: {providers[0]}")
            else:
                print(f"ONNX 模型文件不存在: {self.model_path}")
                print("将使用关键词规则分类作为备用方案")
        except Exception as e:
            print(f"初始化 ONNX Runtime 失败: {e}")
            print("将使用关键词规则分类作为备用方案")
    
    def _preprocess_text(self, text: str) -> np.ndarray:
        """
        文本预处理
        
        参数:
            text: 待分类的文本
            
        返回:
            np.ndarray: 模型输入
        """
        # 简单的文本预处理（根据实际模型需求调整）
        # 这里使用一个简单的特征提取方法作为示例
        emotional_keywords = ["可怜", "害怕", "失去", "妈妈"]
        evidence_keywords = ["证据", "聊天记录", "现场", "表明"]
        legal_keywords = ["法院", "判决", "刑事责任", "民事赔偿"]
        
        emotional_score = sum(1 for keyword in emotional_keywords if keyword in text)
        evidence_score = sum(1 for keyword in evidence_keywords if keyword in text)
        legal_score = sum(1 for keyword in legal_keywords if keyword in text)
        
        # 生成特征向量
        features = np.array([[emotional_score, evidence_score, legal_score]], dtype=np.float32)
        return features
    
    def _postprocess_result(self, model_output: np.ndarray) -> Dict[str, Any]:
        """
        结果后处理
        
        参数:
            model_output: 模型输出
            
        返回:
            Dict: 分类结果
        """
        # 假设模型输出是 [batch_size, 3] 的概率分布
        if len(model_output.shape) == 2:
            probabilities = model_output[0]
        else:
            probabilities = model_output
        
        # 获取最大概率的类别
        class_idx = np.argmax(probabilities)
        confidence = float(probabilities[class_idx])
        
        # 映射到标签
        labels = ["EMOTIONAL", "EVIDENCE", "LEGAL"]
        label = labels[class_idx]
        
        return {
            "label": label,
            "confidence": confidence
        }
    
    def _keyword_based_classification(self, text: str) -> Dict[str, Any]:
        """
        基于关键词规则的分类（备用方案）
        
        参数:
            text: 待分类的文本
            
        返回:
            Dict: 分类结果
        """
        emotional_keywords = ["可怜", "害怕", "失去", "妈妈"]
        evidence_keywords = ["证据", "聊天记录", "现场", "表明"]
        legal_keywords = ["法院", "判决", "刑事责任", "民事赔偿"]
        
        emotional_score = sum(1 for keyword in emotional_keywords if keyword in text)
        evidence_score = sum(1 for keyword in evidence_keywords if keyword in text)
        legal_score = sum(1 for keyword in legal_keywords if keyword in text)
        
        scores = {
            "EMOTIONAL": emotional_score,
            "EVIDENCE": evidence_score,
            "LEGAL": legal_score
        }
        
        # 选择得分最高的类别
        max_score = max(scores.values())
        if max_score == 0:
            # 默认类别
            return {
                "label": "EMOTIONAL", 
                "confidence": 0.5
            }
        
        label = max(scores, key=scores.get)
        # 计算置信度（简单归一化）
        total_score = sum(scores.values())
        confidence = max_score / total_score
        
        return {
            "label": label, 
            "confidence": confidence
        }
    
    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        基于 ONNX Runtime 对文本进行分类
        
        参数:
            text: 待分类的文本
            
        返回:
            Dict包含label和confidence字段
        """
        try:
            if self.session:
                # 使用 ONNX Runtime 进行推理
                input_tensor = self._preprocess_text(text)
                input_name = self.session.get_inputs()[0].name
                output_name = self.session.get_outputs()[0].name
                
                # 执行推理
                model_output = self.session.run([output_name], {input_name: input_tensor})[0]
                
                # 后处理结果
                result = self._postprocess_result(model_output)
                return result
            else:
                # 使用关键词规则分类作为备用方案
                return self._keyword_based_classification(text)
        except Exception as e:
            print(f"ONNX 推理失败: {e}")
            # 发生错误时使用关键词规则分类作为备用
            return self._keyword_based_classification(text)

# 主推理函数
def classify_text(text: str) -> dict:
    """
    输入：
        text: 舆论文本（str）

    输出：
        {
          "label": "EMOTIONAL" | "EVIDENCE" | "LEGAL",
          "confidence": float
        }
    """
    runner = NPURunner()
    return runner.classify_text(text)

# 批处理推理函数（用于提高性能）
def batch_classify_text(texts: list) -> list:
    """
    批量分类文本
    
    参数:
        texts: 文本列表
        
    返回:
        list: 分类结果列表
    """
    runner = NPURunner()
    results = []
    for text in texts:
        result = runner.classify_text(text)
        results.append(result)
    return results
