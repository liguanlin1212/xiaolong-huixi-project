import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ai.inference.npu_runner import classify_text, batch_classify_text

def test_single_inference():
    """
    测试单个文本推理
    """
    print("测试单个文本推理...")
    test_texts = [
        "刘鑫也是受害者，她当时也很害怕",
        "聊天记录显示她提前意识到危险",
        "法院判决认定不构成刑事责任"
    ]
    
    for text in test_texts:
        result = classify_text(text)
        print(f"文本: {text}")
        print(f"分类结果: {result}")
        print()

def test_batch_inference():
    """
    测试批量文本推理
    """
    print("测试批量文本推理...")
    test_texts = [
        "刘鑫也是受害者，她当时也很害怕",
        "聊天记录显示她提前意识到危险",
        "法院判决认定不构成刑事责任"
    ]
    
    results = batch_classify_text(test_texts)
    for i, (text, result) in enumerate(zip(test_texts, results)):
        print(f"文本 {i+1}: {text}")
        print(f"分类结果: {result}")
        print()

if __name__ == "__main__":
    print("=== NPU 推理功能测试 ===")
    test_single_inference()
    test_batch_inference()
    print("=== 测试完成 ===")
