from ai.inference.npu_runner import classify_text
from ai.config import AIConfig
from ai.inference.model_factory import ModelFactory

print("=== AI调用和大模型接入测试 ===")

# 测试1: 测试默认模型（NPU）
print("\n1. 测试默认模型（NPU）:")
test_texts = [
    "我真的很可怜，失去了妈妈",
    "有聊天记录作为证据",
    "法院判决他承担刑事责任"
]

for text in test_texts:
    result = classify_text(text)
    print(f"文本: {text}")
    print(f"分类结果: {result['label']}, 置信度: {result['confidence']}")
    if 'judgement_basis' in result:
        print(f"判断依据: {result['judgement_basis']}")
    if 'system_note' in result:
        print(f"系统说明: {result['system_note']}")

# 测试2: 测试配置管理
print("\n2. 测试配置管理:")
config = AIConfig()
print(f"默认模型: {config.get_default_model()}")
print(f"支持的模型: {ModelFactory.list_supported_models()}")

# 测试3: 测试模型工厂
print("\n3. 测试模型工厂:")
try:
    # 测试创建NPU模型
    npu_runner = ModelFactory.create_runner("NPU")
    print(f"NPU模型创建成功: {npu_runner.health_check()}")
    
    # 测试创建OpenAI模型（如果配置了API密钥）
    openai_config = config.get_model_config("OPENAI")
    if openai_config.get("api_key"):
        openai_runner = ModelFactory.create_runner("OPENAI", **openai_config)
        print(f"OpenAI模型创建成功: {openai_runner.health_check()}")
    else:
        print("OpenAI API密钥未配置，跳过OpenAI模型测试")
except Exception as e:
    print(f"模型工厂测试失败: {e}")

# 测试4: 测试不同模型的分类结果
print("\n4. 测试不同模型的分类结果:")
test_text = "现场有很多证据，表明他是无辜的"

print(f"测试文本: {test_text}")

# 测试NPU模型
npu_result = classify_text(test_text, model_name="NPU")
print(f"NPU模型结果: {npu_result['label']}, 置信度: {npu_result['confidence']}")
if 'judgement_basis' in npu_result:
    print(f"NPU判断依据: {npu_result['judgement_basis']}")
if 'system_note' in npu_result:
    print(f"NPU系统说明: {npu_result['system_note']}")

# 测试OpenAI模型（如果配置了API密钥）
openai_config = config.get_model_config("OPENAI")
if openai_config.get("api_key"):
    try:
        openai_result = classify_text(test_text, model_name="OPENAI")
        print(f"OpenAI模型结果: {openai_result['label']}, 置信度: {openai_result['confidence']}")
        if 'judgement_basis' in openai_result:
            print(f"OpenAI判断依据: {openai_result['judgement_basis']}")
        if 'system_note' in openai_result:
            print(f"OpenAI系统说明: {openai_result['system_note']}")
    except Exception as e:
        print(f"OpenAI模型测试失败: {e}")
else:
    print("OpenAI API密钥未配置，跳过OpenAI模型测试")

print("\n=== 测试完成 ===")
