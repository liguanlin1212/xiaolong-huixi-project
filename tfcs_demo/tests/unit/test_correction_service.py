import pytest
from core.enums import JudgementStatus
from app.services.version_service import version_service
from app.services.judgement_service import create_versioned_judgement, analyse_information_impact, create_correction
from app.services.correction_service import CorrectionService

class TestCorrectionService:
    def setup_method(self):
        # 重置版本服务状态
        version_service._versions = {}
        version_service._judgement_latest = {}
    
    def test_analyse_impact_with_conflicting_information(self):
        """测试分析具有冲突信息的影响"""
        # 创建一个判断
        judgement_id = "test-judgement-1"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测", "用户反馈良好"],
            "assumptions": ["生产过程符合标准"]
        }
        
        # 创建版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 准备冲突的新信息
        conflicting_info = {
            "conclusion": "这个产品质量有问题",
            "facts": ["产品未通过最新质量检测"],
            "evidence": ["检测报告显示存在缺陷"]
        }
        
        # 分析影响
        impact_analysis = analyse_information_impact(conflicting_info)
        
        # 验证影响分析结果
        assert len(impact_analysis.affected_judgements) > 0
        assert judgement_id in impact_analysis.affected_conclusions
        assert len(impact_analysis.affected_conclusions[judgement_id]) > 0
        assert impact_analysis.impact_scores[judgement_id] > 0
    
    def test_analyse_impact_without_conflict(self):
        """测试分析无冲突信息的影响"""
        # 创建一个判断
        judgement_id = "test-judgement-2"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测", "用户反馈良好"]
        }
        
        # 创建版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 准备无冲突的新信息
        non_conflicting_info = {
            "facts": ["产品获得了行业奖项"]
        }
        
        # 分析影响
        impact_analysis = analyse_information_impact(non_conflicting_info)
        
        # 验证影响分析结果
        assert len(impact_analysis.affected_judgements) == 0
        assert judgement_id not in impact_analysis.affected_conclusions
    
    def test_create_correction_version(self):
        """测试创建修正版本"""
        # 创建一个判断
        judgement_id = "test-judgement-3"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测", "用户反馈良好"],
            "assumptions": ["生产过程符合标准"]
        }
        
        # 创建版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 准备冲突的新信息
        conflicting_info = {
            "conclusion": "这个产品质量有问题",
            "facts": ["产品未通过最新质量检测"],
            "evidence": ["检测报告显示存在缺陷"]
        }
        
        # 分析影响
        impact_analysis = analyse_information_impact(conflicting_info)
        
        # 创建修正版本
        correction_version = create_correction(
            judgement_id=judgement_id,
            new_information=conflicting_info,
            impact_analysis=impact_analysis
        )
        
        # 验证修正版本
        assert correction_version is not None
        assert correction_version.judgement_id == judgement_id
        assert correction_version.content["conclusion"] == conflicting_info["conclusion"]
        assert len(correction_version.content["facts"]) == 3  # 原有2个事实 + 新增1个
        assert correction_version.previous_version_id == version1.version_id
        assert correction_version.status == JudgementStatus.PARTIALLY_CORRECTED
    
    def test_conflict_detection(self):
        """测试冲突检测功能"""
        service = CorrectionService()
        
        # 测试直接矛盾
        new_content = "这个产品不是好的"
        old_contents = ["这个产品是好的"]
        assert service._detect_conflict(new_content, old_contents) is True
        
        # 测试无冲突
        new_content = "这个产品很好"
        old_contents = ["这个产品是好的"]
        assert service._detect_conflict(new_content, old_contents) is False
    
    def test_assumption_failure_detection(self):
        """测试假设失效检测功能"""
        service = CorrectionService()
        
        # 测试假设失效
        assumption = "生产过程符合标准"
        new_evidence = ["证据显示生产过程不符合标准"]
        assert service._assumption_failed(assumption, new_evidence) is True
        
        # 测试假设未失效
        assumption = "生产过程符合标准"
        new_evidence = ["生产过程符合标准"]
        assert service._assumption_failed(assumption, new_evidence) is False
    
    def test_impact_calculation(self):
        """测试影响计算功能"""
        service = CorrectionService()
        
        # 创建一个判断版本
        judgement_id = "test-judgement-4"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测", "用户反馈良好"],
            "assumptions": ["生产过程符合标准"]
        }
        
        version = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 准备冲突信息
        conflicting_info = {
            "conclusion": "这个产品质量有问题",
            "facts": ["产品未通过最新质量检测"],
            "evidence": ["检测报告显示存在缺陷"]
        }
        
        # 计算影响
        impact_score, affected_conclusions, failed_assumptions = service._calculate_impact(
            conflicting_info, version
        )
        
        # 验证影响计算结果
        assert impact_score > 0
        assert len(affected_conclusions) > 0
        assert len(failed_assumptions) > 0
