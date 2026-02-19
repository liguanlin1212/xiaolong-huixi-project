import pytest
from ai.inference.npu_runner import classify_text, batch_classify_text, NPURunner

def test_classify_text_basic():
    """
    测试 classify_text 函数的基本功能
    """
    # 测试情绪叙事文本
    emotional_text = "刘鑫也是受害者，她当时也很害怕"
    emotional_result = classify_text(emotional_text)
    assert isinstance(emotional_result, dict)
    assert "label" in emotional_result
    assert "confidence" in emotional_result
    assert isinstance(emotional_result["label"], str)
    assert isinstance(emotional_result["confidence"], float)
    assert emotional_result["confidence"] >= 0.0
    assert emotional_result["confidence"] <= 1.0
    
    # 测试证据叙事文本
    evidence_text = "聊天记录显示她提前意识到危险"
    evidence_result = classify_text(evidence_text)
    assert isinstance(evidence_result, dict)
    assert "label" in evidence_result
    assert "confidence" in evidence_result
    
    # 测试法律叙事文本
    legal_text = "法院判决认定不构成刑事责任"
    legal_result = classify_text(legal_text)
    assert isinstance(legal_result, dict)
    assert "label" in legal_result
    assert "confidence" in legal_result

def test_classify_text_with_empty_string():
    """
    测试 classify_text 函数处理空字符串的情况
    """
    empty_text = ""
    result = classify_text(empty_text)
    assert isinstance(result, dict)
    assert "label" in result
    assert "confidence" in result
    assert isinstance(result["label"], str)
    assert isinstance(result["confidence"], float)

def test_classify_text_with_special_characters():
    """
    测试 classify_text 函数处理包含特殊字符的文本
    """
    special_text = "刘鑫！！！她当时也很害怕..."
    result = classify_text(special_text)
    assert isinstance(result, dict)
    assert "label" in result
    assert "confidence" in result

def test_batch_classify_text():
    """
    测试 batch_classify_text 函数的功能
    """
    test_texts = [
        "刘鑫也是受害者，她当时也很害怕",
        "聊天记录显示她提前意识到危险",
        "法院判决认定不构成刑事责任"
    ]
    
    results = batch_classify_text(test_texts)
    assert isinstance(results, list)
    assert len(results) == len(test_texts)
    
    for result in results:
        assert isinstance(result, dict)
        assert "label" in result
        assert "confidence" in result
        assert isinstance(result["label"], str)
        assert isinstance(result["confidence"], float)
        assert result["confidence"] >= 0.0
        assert result["confidence"] <= 1.0

def test_batch_classify_text_with_empty_list():
    """
    测试 batch_classify_text 函数处理空列表的情况
    """
    empty_list = []
    results = batch_classify_text(empty_list)
    assert isinstance(results, list)
    assert len(results) == 0

def test_npu_runner_initialization():
    """
    测试 NPURunner 类的初始化
    """
    runner = NPURunner()
    assert isinstance(runner, NPURunner)
    # 测试 runner 具有必要的属性
    assert hasattr(runner, 'model_path')
    assert hasattr(runner, 'session')

def test_npu_runner_classify_text():
    """
    测试 NPURunner 类的 classify_text 方法
    """
    runner = NPURunner()
    test_text = "刘鑫也是受害者，她当时也很害怕"
    result = runner.classify_text(test_text)
    assert isinstance(result, dict)
    assert "label" in result
    assert "confidence" in result
    assert isinstance(result["label"], str)
    assert isinstance(result["confidence"], float)
    assert result["confidence"] >= 0.0
    assert result["confidence"] <= 1.0
