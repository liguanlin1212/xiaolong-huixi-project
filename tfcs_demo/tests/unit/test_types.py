import pytest
from core.types import TextEntry, AnalysedEntry
from core.enums import NarrativeType

def test_text_entry():
    """
    测试 TextEntry 数据类
    """
    # 测试 TextEntry 的创建
    entry = TextEntry(time="2023-01-01", text="测试文本")
    assert isinstance(entry, TextEntry)
    
    # 测试 TextEntry 的属性
    assert entry.time == "2023-01-01"
    assert entry.text == "测试文本"
    
    # 测试 TextEntry 的字符串表示
    entry_str = str(entry)
    assert "2023-01-01" in entry_str
    assert "测试文本" in entry_str

def test_analysed_entry():
    """
    测试 AnalysedEntry 数据类
    """
    # 测试 AnalysedEntry 的创建
    entry = AnalysedEntry(
        time="2023-01-01",
        text="测试文本",
        narrative=NarrativeType.EMOTIONAL,
        confidence=0.8
    )
    assert isinstance(entry, AnalysedEntry)
    
    # 测试 AnalysedEntry 的属性
    assert entry.time == "2023-01-01"
    assert entry.text == "测试文本"
    assert entry.narrative == NarrativeType.EMOTIONAL
    assert entry.confidence == 0.8
    
    # 测试 AnalysedEntry 的字符串表示
    entry_str = str(entry)
    assert "2023-01-01" in entry_str
    assert "测试文本" in entry_str
    assert "EMOTIONAL" in entry_str
    assert "0.8" in entry_str

def test_analysed_entry_with_different_narrative_types():
    """
    测试 AnalysedEntry 使用不同的 NarrativeType
    """
    # 测试使用 EVIDENCE 类型
    evidence_entry = AnalysedEntry(
        time="2023-01-02",
        text="有证据表明",
        narrative=NarrativeType.EVIDENCE,
        confidence=0.9
    )
    assert evidence_entry.narrative == NarrativeType.EVIDENCE
    
    # 测试使用 LEGAL 类型
    legal_entry = AnalysedEntry(
        time="2023-01-03",
        text="法院判决",
        narrative=NarrativeType.LEGAL,
        confidence=0.95
    )
    assert legal_entry.narrative == NarrativeType.LEGAL
