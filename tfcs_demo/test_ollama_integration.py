from ai.inference.model_factory import ModelFactory
from ai.config import AIConfig

def test_ollama_model():
    """
    测试Ollama模型集成
    """
    print("=== 测试Ollama模型集成 ===")
    
    # 加载配置
    config = AIConfig()
    ollama_config = config.get_model_config("OLLAMA")
    
    print(f"Ollama配置: {ollama_config}")
    
    # 创建Ollama模型运行器
    ollama_runner = ModelFactory.create_runner("OLLAMA", **ollama_config)
    
    if not ollama_runner:
        print("创建Ollama模型运行器失败")
        return
    
    # 测试健康检查
    health_status = ollama_runner.health_check()
    print(f"健康检查: {'通过' if health_status else '失败'}")
    
    # 测试文本分类
    test_texts = [
        "我真的很可怜，失去了妈妈",
        "有聊天记录作为证据",
        "法院判决他承担刑事责任",
        "今天天气很好，适合出去散步"
    ]
    
    for text in test_texts:
        print(f"\n测试文本: {text}")
        result = ollama_runner.classify_text(text)
        print(f"分类结果: {result}")
    
    print("\n=== 测试完成 ===")

def test_model_factory():
    """
    测试模型工厂
    """
    print("\n=== 测试模型工厂 ===")
    
    # 列出支持的模型
    supported_models = ModelFactory.list_supported_models()
    print(f"支持的模型: {supported_models}")
    
    # 验证OLLAMA模型是否在支持列表中
    assert "OLLAMA" in supported_models, "OLLAMA模型未在支持列表中"
    print("OLLAMA模型已在支持列表中")
    
    # 验证模型工厂能够创建OLLAMA模型
    ollama_runner = ModelFactory.create_runner("OLLAMA")
    assert ollama_runner is not None, "创建OLLAMA模型运行器失败"
    print("OLLAMA模型运行器创建成功")
    
    print("=== 模型工厂测试完成 ===")

if __name__ == "__main__":
    test_model_factory()
    test_ollama_model()