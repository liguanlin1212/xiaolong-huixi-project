import pytest
from app.services.narrative_service import analyse_text_entry
from core.enums import NarrativeType

def test_analyse_text_entry_basic():
    """
    测试 analyse_text_entry 函数的基本功能
    """
    # 测试情绪叙事文本
    emotional_entry = {
        "time": "2023-01-01",
        "text": "刘鑫也是受害者，她当时也很害怕"
    }
    emotional_result = analyse_text_entry(emotional_entry)
    assert isinstance(emotional_result, dict)
    assert "time" in emotional_result
    assert "text" in emotional_result
    assert "narrative" in emotional_result
    assert "confidence" in emotional_result
    assert emotional_result["time"] == emotional_entry["time"]
    assert emotional_result["text"] == emotional_entry["text"]
    assert isinstance(emotional_result["narrative"], NarrativeType)
    assert isinstance(emotional_result["confidence"], float)
    assert emotional_result["confidence"] >= 0.0
    assert emotional_result["confidence"] <= 1.0
    
    # 测试证据叙事文本
    evidence_entry = {
        "time": "2023-01-02",
        "text": "聊天记录显示她提前意识到危险"
    }
    evidence_result = analyse_text_entry(evidence_entry)
    assert isinstance(evidence_result, dict)
    assert "time" in evidence_result
    assert "text" in evidence_result
    assert "narrative" in evidence_result
    assert "confidence" in evidence_result
    
    # 测试法律叙事文本
    legal_entry = {
        "time": "2023-01-03",
        "text": "法院判决认定不构成刑事责任"
    }
    legal_result = analyse_text_entry(legal_entry)
    assert isinstance(legal_result, dict)
    assert "time" in legal_result
    assert "text" in legal_result
    assert "narrative" in legal_result
    assert "confidence" in legal_result

def test_analyse_text_entry_with_missing_fields():
    """
    测试 analyse_text_entry 函数处理缺少字段的情况
    """
    # 测试缺少 time 字段
    entry_without_time = {
        "text": "刘鑫也是受害者，她当时也很害怕"
    }
    with pytest.raises(Exception):
        analyse_text_entry(entry_without_time)
    
    # 测试缺少 text 字段
    entry_without_text = {
        "time": "2023-01-01"
    }
    with pytest.raises(Exception):
        analyse_text_entry(entry_without_text)

def test_analyse_text_entry_with_empty_text():
    """
    测试 analyse_text_entry 函数处理空文本的情况
    """
    empty_text_entry = {
        "time": "2023-01-01",
        "text": ""
    }
    result = analyse_text_entry(empty_text_entry)
    assert isinstance(result, dict)
    assert "time" in result
    assert "text" in result
    assert "narrative" in result
    assert "confidence" in result
