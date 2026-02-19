import pytest
import os
import sys
import json
from unittest import mock

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.services.narrative_service import analyse_text_entry
from app.services.judgement_service import build_timeline

def test_analyse_api_integration():
    """
    测试 API 层的集成功能
    """
    # 模拟测试数据
    mock_raw_entries = [
        {
            "time": "2023-01-01",
            "text": "刘鑫也是受害者，她当时也很害怕"
        },
        {
            "time": "2023-01-02",
            "text": "聊天记录显示她提前意识到危险"
        },
        {
            "time": "2023-01-03",
            "text": "法院判决认定不构成刑事责任"
        }
    ]
    
    # 测试 analyse_text_entry 函数
    analysed_entries = []
    for entry in mock_raw_entries:
        analysed_entry = analyse_text_entry(entry)
        analysed_entries.append(analysed_entry)
        assert isinstance(analysed_entry, dict)
        assert "time" in analysed_entry
        assert "text" in analysed_entry
        assert "narrative" in analysed_entry
        assert "confidence" in analysed_entry
    
    # 测试 build_timeline 函数
    timeline = build_timeline(analysed_entries)
    assert isinstance(timeline, list)
    assert len(timeline) == len(mock_raw_entries)
    
    # 验证时间顺序是否正确
    assert timeline[0]["time"] == "2023-01-01"
    assert timeline[1]["time"] == "2023-01-02"
    assert timeline[2]["time"] == "2023-01-03"

def test_analyse_api_end_to_end():
    """
    测试 API 层的端到端功能
    """
    # 创建临时测试数据文件
    test_data = [
        {
            "time": "2023-01-01",
            "text": "刘鑫也是受害者，她当时也很害怕"
        }
    ]
    
    test_data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "test_raw_texts.json")
    
    try:
        # 写入测试数据
        with open(test_data_path, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # 导入并测试 analyse.py 的核心逻辑
        from app.api import analyse
        
        # 模拟文件读取
        with mock.patch('app.api.analyse.open', mock.mock_open(read_data=json.dumps(test_data))):
            # 模拟显示函数
            with mock.patch('app.api.analyse.display_timeline') as mock_display:
                # 执行 main 函数
                analyse.main()
                # 验证 display_timeline 被调用
                mock_display.assert_called_once()
                # 验证调用参数
                args, kwargs = mock_display.call_args
                timeline = args[0]
                assert isinstance(timeline, list)
                assert len(timeline) == 1
                assert timeline[0]["time"] == "2023-01-01"
    finally:
        # 清理临时文件
        if os.path.exists(test_data_path):
            os.remove(test_data_path)
