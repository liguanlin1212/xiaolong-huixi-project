import unittest
from ai.config import AIConfig
from ai.inference.model_factory import ModelFactory
from ai.inference.npu_runner import classify_text, batch_classify_text

class TestAIIntegration(unittest.TestCase):
    """
    AI集成测试类
    """
    
    def setUp(self):
        """
        测试前的设置
        """
        self.config = AIConfig()
    
    def test_config_management(self):
        """
        测试配置管理功能
        """
        # 测试默认模型
        default_model = self.config.get_default_model()
        self.assertEqual(default_model, "NPU")
        
        # 测试模型配置
        npu_config = self.config.get_model_config("NPU")
        self.assertEqual(npu_config.get("type"), "NPU")
        
        openai_config = self.config.get_model_config("OPENAI")
        self.assertEqual(openai_config.get("type"), "OPENAI")
        
        # 测试模型列表
        models = self.config.list_models()
        self.assertIn("NPU", models)
        self.assertIn("OPENAI", models)
    
    def test_model_factory(self):
        """
        测试模型工厂功能
        """
        # 测试支持的模型列表
        supported_models = ModelFactory.list_supported_models()
        self.assertIn("NPU", supported_models)
        self.assertIn("OPENAI", supported_models)
        
        # 测试模型支持检查
        self.assertTrue(ModelFactory.is_model_supported("NPU"))
        self.assertTrue(ModelFactory.is_model_supported("OPENAI"))
        self.assertFalse(ModelFactory.is_model_supported("UNKNOWN"))
        
        # 测试创建NPU模型
        npu_runner = ModelFactory.create_runner("NPU")
        self.assertIsNotNone(npu_runner)
        
        # 测试创建不存在的模型
        unknown_runner = ModelFactory.create_runner("UNKNOWN")
        self.assertIsNone(unknown_runner)
    
    def test_npu_classification(self):
        """
        测试NPU模型分类功能
        """
        # 测试情感文本分类
        emotional_text = "我真的很可怜，失去了妈妈"
        result = classify_text(emotional_text, model_name="NPU")
        self.assertIn("label", result)
        self.assertIn("confidence", result)
        self.assertIsInstance(result["confidence"], float)
        
        # 测试证据文本分类
        evidence_text = "有聊天记录作为证据"
        result = classify_text(evidence_text, model_name="NPU")
        self.assertIn("label", result)
        self.assertIn("confidence", result)
        
        # 测试法律文本分类
        legal_text = "法院判决他承担刑事责任"
        result = classify_text(legal_text, model_name="NPU")
        self.assertIn("label", result)
        self.assertIn("confidence", result)
    
    def test_batch_classification(self):
        """
        测试批量分类功能
        """
        texts = [
            "我真的很可怜，失去了妈妈",
            "有聊天记录作为证据",
            "法院判决他承担刑事责任"
        ]
        
        results = batch_classify_text(texts, model_name="NPU")
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIn("label", result)
            self.assertIn("confidence", result)
    
    def test_model_selection(self):
        """
        测试模型选择功能
        """
        # 测试默认模型（应该是NPU）
        text = "测试文本"
        result = classify_text(text)
        self.assertIn("label", result)
        self.assertIn("confidence", result)
        
        # 测试指定NPU模型
        result = classify_text(text, model_name="NPU")
        self.assertIn("label", result)
        self.assertIn("confidence", result)
    
    def test_health_check(self):
        """
        测试健康检查功能
        """
        # 创建NPU模型并测试健康检查
        npu_runner = ModelFactory.create_runner("NPU")
        if npu_runner:
            health_status = npu_runner.health_check()
            self.assertTrue(health_status)

if __name__ == "__main__":
    unittest.main()
