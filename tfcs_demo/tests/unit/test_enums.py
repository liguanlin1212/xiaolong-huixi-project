import pytest
from core.enums import NarrativeType

def test_narrative_type_enum():
    """
    测试 NarrativeType 枚举是否正确定义
    """
    # 测试枚举成员是否存在
    assert hasattr(NarrativeType, 'EMOTIONAL')
    assert hasattr(NarrativeType, 'EVIDENCE')
    assert hasattr(NarrativeType, 'LEGAL')
    
    # 测试枚举值是否正确
    assert NarrativeType.EMOTIONAL.value == "情绪叙事"
    assert NarrativeType.EVIDENCE.value == "证据叙事"
    assert NarrativeType.LEGAL.value == "法律叙事"
    
    # 测试枚举成员数量
    assert len(NarrativeType) == 3

def test_narrative_type_members():
    """
    测试 NarrativeType 枚举成员的类型和行为
    """
    # 测试枚举成员的类型
    assert isinstance(NarrativeType.EMOTIONAL, NarrativeType)
    assert isinstance(NarrativeType.EVIDENCE, NarrativeType)
    assert isinstance(NarrativeType.LEGAL, NarrativeType)
    
    # 测试枚举成员的比较
    assert NarrativeType.EMOTIONAL != NarrativeType.EVIDENCE
    assert NarrativeType.EVIDENCE != NarrativeType.LEGAL
    assert NarrativeType.LEGAL != NarrativeType.EMOTIONAL
    
    # 测试枚举成员的字符串表示
    assert str(NarrativeType.EMOTIONAL) == "NarrativeType.EMOTIONAL"
    assert repr(NarrativeType.EMOTIONAL) == "<NarrativeType.EMOTIONAL: '情绪叙事'>"
