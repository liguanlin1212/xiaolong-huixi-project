import time
import psutil
import pytest
from ai.inference.npu_runner import classify_text

def test_inference_speed():
    """
    测试 AI 推理速度
    """
    test_texts = [
        "刘鑫也是受害者，她当时也很害怕",
        "聊天记录显示她提前意识到危险",
        "法院判决认定不构成刑事责任"
    ]
    
    # 测量推理时间
    start_time = time.time()
    for text in test_texts:
        result = classify_text(text)
        assert isinstance(result, dict)
        assert "label" in result
        assert "confidence" in result
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time / len(test_texts)
    
    print(f"总推理时间: {total_time:.4f} 秒")
    print(f"平均推理时间: {avg_time:.4f} 秒")
    
    # 验证推理速度是否合理（这里设置一个宽松的阈值）
    assert avg_time < 1.0, f"推理速度过慢，平均时间: {avg_time:.4f} 秒"

def test_inference_memory_usage():
    """
    测试 AI 推理内存使用情况
    """
    # 获取初始内存使用
    initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    test_text = "刘鑫也是受害者，她当时也很害怕"
    
    # 执行推理
    result = classify_text(test_text)
    assert isinstance(result, dict)
    
    # 获取推理后的内存使用
    final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    memory_diff = final_memory - initial_memory
    
    print(f"初始内存使用: {initial_memory:.2f} MB")
    print(f"推理后内存使用: {final_memory:.2f} MB")
    print(f"内存使用差异: {memory_diff:.2f} MB")
    
    # 验证内存使用是否合理（这里设置一个宽松的阈值）
    assert memory_diff < 50.0, f"内存使用过高，差异: {memory_diff:.2f} MB"

def test_inference_stability():
    """
    测试 AI 推理的稳定性
    """
    test_text = "刘鑫也是受害者，她当时也很害怕"
    
    # 多次执行推理，验证结果的一致性
    results = []
    for i in range(5):
        result = classify_text(test_text)
        assert isinstance(result, dict)
        assert "label" in result
        assert "confidence" in result
        results.append(result)
    
    # 验证所有结果的标签是否一致
    labels = [r["label"] for r in results]
    assert all(label == labels[0] for label in labels), "推理结果标签不一致"
    
    # 验证置信度是否在合理范围内
    confidences = [r["confidence"] for r in results]
    for conf in confidences:
        assert conf >= 0.0
        assert conf <= 1.0
    
    print(f"推理结果标签: {labels[0]}")
    print(f"置信度范围: {min(confidences):.4f} - {max(confidences):.4f}")
