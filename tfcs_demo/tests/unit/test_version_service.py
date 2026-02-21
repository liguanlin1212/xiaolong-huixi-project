import pytest
from core.enums import JudgementStatus
from app.services.version_service import version_service
from app.services.judgement_service import create_versioned_judgement, get_judgement_history, get_latest_judgement, validate_judgement_versions

class TestVersionService:
    def setup_method(self):
        # 重置版本服务状态
        version_service._versions = {}
        version_service._judgement_latest = {}
    
    def test_create_new_version(self):
        """测试创建新版本"""
        judgement_id = "test-judgement-1"
        content = {"conclusion": "Initial judgement"}
        status = JudgementStatus.UNRESOLVED
        
        # 创建第一个版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=status
        )
        
        assert version1.judgement_id == judgement_id
        assert version1.content == content
        assert version1.status == status
        assert version1.previous_version_id is None
        
        # 创建第二个版本
        content2 = {"conclusion": "Updated judgement"}
        status2 = JudgementStatus.PARTIALLY_CORRECTED
        
        version2 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content2,
            status=status2,
            previous_version=version1
        )
        
        assert version2.judgement_id == judgement_id
        assert version2.content == content2
        assert version2.status == status2
        assert version2.previous_version_id == version1.version_id
    
    def test_get_version_history(self):
        """测试获取版本历史"""
        judgement_id = "test-judgement-2"
        
        # 创建多个版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content={"conclusion": "V1"},
            status=JudgementStatus.UNRESOLVED
        )
        
        version2 = create_versioned_judgement(
            judgement_id=judgement_id,
            content={"conclusion": "V2"},
            status=JudgementStatus.PARTIALLY_CORRECTED,
            previous_version=version1
        )
        
        version3 = create_versioned_judgement(
            judgement_id=judgement_id,
            content={"conclusion": "V3"},
            status=JudgementStatus.CONDITIONALLY_TRUE,
            previous_version=version2
        )
        
        # 获取版本历史
        history = get_judgement_history(judgement_id)
        assert len(history) == 3
        assert history[0].version_id == version3.version_id  # 最新版本在前
        assert history[1].version_id == version2.version_id
        assert history[2].version_id == version1.version_id
    
    def test_get_latest_version(self):
        """测试获取最新版本"""
        judgement_id = "test-judgement-3"
        
        # 创建多个版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content={"conclusion": "V1"},
            status=JudgementStatus.UNRESOLVED
        )
        
        version2 = create_versioned_judgement(
            judgement_id=judgement_id,
            content={"conclusion": "V2"},
            status=JudgementStatus.PARTIALLY_CORRECTED,
            previous_version=version1
        )
        
        # 获取最新版本
        latest_version = get_latest_judgement(judgement_id)
        assert latest_version is not None
        assert latest_version.version_id == version2.version_id
    
    def test_validate_version_chain(self):
        """测试验证版本链"""
        judgement_id = "test-judgement-4"
        
        # 创建有效的版本链
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content={"conclusion": "V1"},
            status=JudgementStatus.UNRESOLVED
        )
        
        version2 = create_versioned_judgement(
            judgement_id=judgement_id,
            content={"conclusion": "V2"},
            status=JudgementStatus.PARTIALLY_CORRECTED,
            previous_version=version1
        )
        
        # 验证版本链
        assert validate_judgement_versions(version2) is True
    
    def test_get_nonexistent_judgement(self):
        """测试获取不存在的判断"""
        non_existent_id = "non-existent-judgement"
        
        history = get_judgement_history(non_existent_id)
        assert len(history) == 0
        
        latest_version = get_latest_judgement(non_existent_id)
        assert latest_version is None
