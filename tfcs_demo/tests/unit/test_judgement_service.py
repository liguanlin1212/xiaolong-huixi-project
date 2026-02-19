import pytest
from app.services.judgement_service import build_timeline

def test_build_timeline_basic():
    """
    测试 build_timeline 函数的基本功能
    """
    # 测试按时间排序的功能
    test_entries = [
        {
            "time": "2023-01-03",
            "text": "法院判决认定不构成刑事责任",
            "narrative": "LEGAL",
            "confidence": 0.95
        },
        {
            "time": "2023-01-01",
            "text": "刘鑫也是受害者，她当时也很害怕",
            "narrative": "EMOTIONAL",
            "confidence": 0.8
        },
        {
            "time": "2023-01-02",
            "text": "聊天记录显示她提前意识到危险",
            "narrative": "EVIDENCE",
            "confidence": 0.9
        }
    ]
    
    timeline = build_timeline(test_entries)
    assert isinstance(timeline, list)
    assert len(timeline) == len(test_entries)
    
    # 验证时间顺序是否正确
    assert timeline[0]["time"] == "2023-01-01"
    assert timeline[1]["time"] == "2023-01-02"
    assert timeline[2]["time"] == "2023-01-03"

def test_build_timeline_with_empty_list():
    """
    测试 build_timeline 函数处理空列表的情况
    """
    empty_entries = []
    timeline = build_timeline(empty_entries)
    assert isinstance(timeline, list)
    assert len(timeline) == 0

def test_build_timeline_with_single_entry():
    """
    测试 build_timeline 函数处理单个条目的情况
    """
    single_entry = [
        {
            "time": "2023-01-01",
            "text": "刘鑫也是受害者，她当时也很害怕",
            "narrative": "EMOTIONAL",
            "confidence": 0.8
        }
    ]
    timeline = build_timeline(single_entry)
    assert isinstance(timeline, list)
    assert len(timeline) == 1
    assert timeline[0]["time"] == "2023-01-01"

def test_build_timeline_with_duplicate_times():
    """
    测试 build_timeline 函数处理重复时间的情况
    """
    duplicate_time_entries = [
        {
            "time": "2023-01-01",
            "text": "刘鑫也是受害者，她当时也很害怕",
            "narrative": "EMOTIONAL",
            "confidence": 0.8
        },
        {
            "time": "2023-01-01",
            "text": "聊天记录显示她提前意识到危险",
            "narrative": "EVIDENCE",
            "confidence": 0.9
        }
    ]
    
    timeline = build_timeline(duplicate_time_entries)
    assert isinstance(timeline, list)
    assert len(timeline) == len(duplicate_time_entries)
    # 重复时间的条目应该保持原始顺序
    assert timeline[0]["text"] == "刘鑫也是受害者，她当时也很害怕"
    assert timeline[1]["text"] == "聊天记录显示她提前意识到危险"
