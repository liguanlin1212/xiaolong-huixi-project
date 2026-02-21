import pytest
from core.enums import JudgementStatus
from app.services.version_service import version_service
from app.services.judgement_service import create_versioned_judgement, report_discomfort, get_discomfort_history, get_discomfort_summary
from app.services.discomfort_service import DiscomfortService

class TestDiscomfortService:
    def setup_method(self):
        # 重置版本服务状态
        version_service._versions = {}
        version_service._judgement_latest = {}
        # 重置不适感服务状态
        from app.services.discomfort_service import discomfort_service
        discomfort_service._discomfort_signals = {}
        discomfort_service._judgement_discomforts = {}
    
    def test_report_discomfort(self):
        """测试报告不适感"""
        # 创建一个判断
        judgement_id = "test-judgement-1"
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
        
        # 报告不适感
        discomfort_type = "逻辑冲突"
        severity = 0.8
        description = "结论与事实不匹配"
        
        signal = report_discomfort(
            judgement_id=judgement_id,
            discomfort_type=discomfort_type,
            severity=severity,
            description=description,
            user_id="test-user-1"
        )
        
        # 验证信号创建
        assert signal is not None
        assert signal.judgement_id == judgement_id
        assert signal.discomfort_type == discomfort_type
        assert signal.severity == severity
        assert signal.description == description
        assert signal.user_id == "test-user-1"
    
    def test_process_discomfort_signal(self):
        """测试处理触发信号"""
        # 创建一个判断
        judgement_id = "test-judgement-2"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测"]
        }
        
        # 创建版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 报告高严重度的不适感
        signal = report_discomfort(
            judgement_id=judgement_id,
            discomfort_type="证据不足",
            severity=0.9,
            description="只有一个事实支持结论"
        )
        
        # 验证信号被处理
        from app.services.discomfort_service import discomfort_service
        assert judgement_id in discomfort_service._judgement_discomforts
        assert len(discomfort_service._judgement_discomforts[judgement_id]) > 0
    
    def test_trigger_review(self):
        """测试触发重新审视流程"""
        # 创建一个判断
        judgement_id = "test-judgement-3"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测"]
        }
        
        # 创建版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 报告高严重度的不适感（应该触发重新审视）
        signal = report_discomfort(
            judgement_id=judgement_id,
            discomfort_type="证据不足",
            severity=0.9,
            description="只有一个事实支持结论"
        )
        
        # 验证创建了重新审视版本
        from app.services.discomfort_service import discomfort_service
        service = DiscomfortService()
        review_result = service.trigger_review(judgement_id, signal)
        
        assert review_result["reviewed"] is True
        assert "created_review_version" in review_result["actions"]
        assert "review_version_id" in review_result
    
    def test_get_discomfort_history(self):
        """测试获取不适感历史"""
        # 创建一个判断
        judgement_id = "test-judgement-4"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测"]
        }
        
        # 创建版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 报告多个不适感
        for i in range(3):
            signal = report_discomfort(
                judgement_id=judgement_id,
                discomfort_type=f"测试类型{i}",
                severity=0.5 + i * 0.1,
                description=f"测试描述{i}"
            )
        
        # 获取历史
        history = get_discomfort_history(judgement_id)
        assert len(history) == 3
        
        # 获取所有历史
        all_history = get_discomfort_history()
        assert len(all_history) >= 3
    
    def test_get_discomfort_summary(self):
        """测试获取不适感摘要"""
        # 创建一个判断
        judgement_id = "test-judgement-5"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测"]
        }
        
        # 创建版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 报告多个不适感
        report_discomfort(
            judgement_id=judgement_id,
            discomfort_type="逻辑冲突",
            severity=0.8,
            description="结论与事实不匹配"
        )
        
        report_discomfort(
            judgement_id=judgement_id,
            discomfort_type="证据不足",
            severity=0.6,
            description="支持证据不足"
        )
        
        # 获取摘要
        summary = get_discomfort_summary(judgement_id)
        
        assert summary["judgement_id"] == judgement_id
        assert summary["total_signals"] == 2
        assert summary["average_severity"] == 0.7  # (0.8 + 0.6) / 2
        assert "逻辑冲突" in summary["discomfort_types"]
        assert "证据不足" in summary["discomfort_types"]
        assert len(summary["recent_signals"]) == 2
    
    def test_identify_issues(self):
        """测试识别问题功能"""
        # 创建一个判断
        judgement_id = "test-judgement-6"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测"],
            "assumptions": ["用户反馈良好"]
        }
        
        # 创建版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 创建服务实例
        service = DiscomfortService()
        
        # 创建信号
        from app.services.discomfort_service import DiscomfortSignal
        signal = DiscomfortSignal(
            signal_id="test-signal-1",
            judgement_id=judgement_id,
            discomfort_type="逻辑冲突",
            severity=0.8,
            description="测试"
        )
        
        # 识别问题
        issues = service._identify_issues(version1, signal)
        assert len(issues) > 0
    
    def test_create_review_version(self):
        """测试创建重新审视版本"""
        # 创建一个判断
        judgement_id = "test-judgement-7"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测"]
        }
        
        # 创建版本
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 创建服务实例
        service = DiscomfortService()
        
        # 创建信号
        from app.services.discomfort_service import DiscomfortSignal
        signal = DiscomfortSignal(
            signal_id="test-signal-2",
            judgement_id=judgement_id,
            discomfort_type="证据不足",
            severity=0.8,
            description="测试"
        )
        
        # 识别问题
        issues = ["证据不足，需要补充"]
        
        # 创建重新审视版本
        review_version = service._create_review_version(version1, issues, signal)
        
        assert review_version is not None
        assert review_version.judgement_id == judgement_id
        assert review_version.previous_version_id == version1.version_id
        assert review_version.status == JudgementStatus.PARTIALLY_CORRECTED
        assert "review_notes" in review_version.content
        assert "review_trigger" in review_version.content
