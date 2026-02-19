from ai.inference.npu_runner import classify_text

print("=== 测试用户示例文本 ===")

# 用户提供的示例文本
sample_text = "刘鑫在案发当晚锁门，导致江歌无法逃生，这不是无辜。"
print(f"测试文本: {sample_text}")

# 测试NPU模型
print("\n1. 测试NPU模型:")
npu_result = classify_text(sample_text, model_name="NPU")
print(f"分类结果: {npu_result['label']}, 置信度: {npu_result['confidence']}")
if 'judgement_basis' in npu_result:
    print(f"判断依据: {npu_result['judgement_basis']}")
if 'system_note' in npu_result:
    print(f"系统说明: {npu_result['system_note']}")

# 测试OpenAI模型（如果配置了API密钥）
print("\n2. 测试OpenAI模型:")
try:
    openai_result = classify_text(sample_text, model_name="OPENAI")
    print(f"分类结果: {openai_result['label']}, 置信度: {openai_result['confidence']}")
    if 'judgement_basis' in openai_result:
        print(f"判断依据: {openai_result['judgement_basis']}")
    if 'system_note' in openai_result:
        print(f"系统说明: {openai_result['system_note']}")
except Exception as e:
    print(f"OpenAI模型测试失败: {e}")
    print("请确保已配置OpenAI API密钥")

print("\n=== 测试完成 ===")
