import time
import psutil
import pytest
from ai.inference.npu_runner import batch_classify_text, classify_text

def test_batch_processing_throughput():
    """
    测试批量处理的吞吐量
    """
    # 创建测试文本列表
    test_texts = [
        "刘鑫也是受害者，她当时也很害怕",
        "聊天记录显示她提前意识到危险",
        "法院判决认定不构成刑事责任",
        "刘鑫在案发时是否锁门",
        "江歌母亲的诉求"
    ]
    
    # 测试批量处理
    start_time_batch = time.time()
    batch_results = batch_classify_text(test_texts)
    end_time_batch = time.time()
    batch_time = end_time_batch - start_time_batch
    
    # 测试逐个处理（作为对比）
    start_time_single = time.time()
    single_results = []
    for text in test_texts:
        result = classify_text(text)
        single_results.append(result)
    end_time_single = time.time()
    single_time = end_time_single - start_time_single
    
    print(f"批量处理时间: {batch_time:.4f} 秒")
    print(f"逐个处理时间: {single_time:.4f} 秒")
    print(f"批量处理速度提升: {(single_time - batch_time) / single_time * 100:.2f}%")
    
    # 验证结果数量
    assert len(batch_results) == len(test_texts)
    assert len(single_results) == len(test_texts)
    
    # 验证结果格式
    for result in batch_results:
        assert isinstance(result, dict)
        assert "label" in result
        assert "confidence" in result
    
    for result in single_results:
        assert isinstance(result, dict)
        assert "label" in result
        assert "confidence" in result

def test_batch_processing_memory_usage():
    """
    测试批量处理内存使用情况
    """
    # 获取初始内存使用
    initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    test_texts = [
        "刘鑫也是受害者，她当时也很害怕",
        "聊天记录显示她提前意识到危险",
        "法院判决认定不构成刑事责任"
    ]
    
    # 执行批量处理
    results = batch_classify_text(test_texts)
    assert isinstance(results, list)
    assert len(results) == len(test_texts)
    
    # 获取处理后的内存使用
    final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    memory_diff = final_memory - initial_memory
    
    print(f"初始内存使用: {initial_memory:.2f} MB")
    print(f"批量处理后内存使用: {final_memory:.2f} MB")
    print(f"内存使用差异: {memory_diff:.2f} MB")
    
    # 验证内存使用是否合理（这里设置一个宽松的阈值）
    assert memory_diff < 100.0, f"内存使用过高，差异: {memory_diff:.2f} MB"

def test_batch_processing_large_input():
    """
    测试批量处理大输入的情况
    """
    # 创建较大的测试文本列表
    test_texts = ["测试文本 " * 10 for _ in range(10)]
    
    start_time = time.time()
    results = batch_classify_text(test_texts)
    end_time = time.time()
    
    processing_time = end_time - start_time
    avg_time_per_text = processing_time / len(test_texts)
    
    print(f"处理 {len(test_texts)} 个文本的总时间: {processing_time:.4f} 秒")
    print(f"平均每个文本处理时间: {avg_time_per_text:.4f} 秒")
    
    # 验证结果
    assert isinstance(results, list)
    assert len(results) == len(test_texts)
    
    for result in results:
        assert isinstance(result, dict)
        assert "label" in result
        assert "confidence" in result
