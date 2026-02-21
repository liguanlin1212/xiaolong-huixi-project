import pytest
from core.enums import JudgementStatus
from core.types import JudgementVersion

class TestJudgementVersion:
    def test_judgement_version_creation(self):
        """测试创建判断版本实例"""
        version_id = "test-version-1"
        judgement_id = "test-judgement-1"
        content = {"conclusion": "Test conclusion"}
        status = JudgementStatus.UNRESOLVED
        created_at = "2026-02-19T12:00:00.000Z"
        previous_version_id = "test-version-0"
        metadata = {"source": "manual"}
        
        # 创建 JudgementVersion 实例
        version = JudgementVersion(
            version_id=version_id,
            judgement_id=judgement_id,
            content=content,
            status=status,
            created_at=created_at,
            previous_version_id=previous_version_id,
            metadata=metadata
        )
        
        # 验证属性
        assert version.version_id == version_id
        assert version.judgement_id == judgement_id
        assert version.content == content
        assert version.status == status
        assert version.created_at == created_at
        assert version.previous_version_id == previous_version_id
        assert version.metadata == metadata
    
    def test_judgement_version_without_optional_fields(self):
        """测试创建不带可选字段的判断版本实例"""
        version_id = "test-version-2"
        judgement_id = "test-judgement-2"
        content = {"conclusion": "Test conclusion"}
        status = JudgementStatus.UNRESOLVED
        created_at = "2026-02-19T12:00:00.000Z"
        
        # 创建 JudgementVersion 实例（不带可选字段）
        version = JudgementVersion(
            version_id=version_id,
            judgement_id=judgement_id,
            content=content,
            status=status,
            created_at=created_at
        )
        
        # 验证属性
        assert version.version_id == version_id
        assert version.judgement_id == judgement_id
        assert version.content == content
        assert version.status == status
        assert version.created_at == created_at
        assert version.previous_version_id is None
        assert version.metadata is None
    
    def test_to_dict_method(self):
        """测试 to_dict 方法"""
        version_id = "test-version-3"
        judgement_id = "test-judgement-3"
        content = {"conclusion": "Test conclusion"}
        status = JudgementStatus.UNRESOLVED
        created_at = "2026-02-19T12:00:00.000Z"
        previous_version_id = "test-version-2"
        metadata = {"source": "manual"}
        
        # 创建 JudgementVersion 实例
        version = JudgementVersion(
            version_id=version_id,
            judgement_id=judgement_id,
            content=content,
            status=status,
            created_at=created_at,
            previous_version_id=previous_version_id,
            metadata=metadata
        )
        
        # 调用 to_dict 方法
        version_dict = version.to_dict()
        
        # 验证字典内容
        assert version_dict["version_id"] == version_id
        assert version_dict["judgement_id"] == judgement_id
        assert version_dict["content"] == content
        assert version_dict["status"] == status.value  # 应该返回枚举值
        assert version_dict["created_at"] == created_at
        assert version_dict["previous_version_id"] == previous_version_id
        assert version_dict["metadata"] == metadata
    
    def test_to_dict_method_without_optional_fields(self):
        """测试不带可选字段的 to_dict 方法"""
        version_id = "test-version-4"
        judgement_id = "test-judgement-4"
        content = {"conclusion": "Test conclusion"}
        status = JudgementStatus.UNRESOLVED
        created_at = "2026-02-19T12:00:00.000Z"
        
        # 创建 JudgementVersion 实例（不带可选字段）
        version = JudgementVersion(
            version_id=version_id,
            judgement_id=judgement_id,
            content=content,
            status=status,
            created_at=created_at
        )
        
        # 调用 to_dict 方法
        version_dict = version.to_dict()
        
        # 验证字典内容
        assert version_dict["version_id"] == version_id
        assert version_dict["judgement_id"] == judgement_id
        assert version_dict["content"] == content
        assert version_dict["status"] == status.value
        assert version_dict["created_at"] == created_at
        assert version_dict["previous_version_id"] is None
        assert version_dict["metadata"] is None
