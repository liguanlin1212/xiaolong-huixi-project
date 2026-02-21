import pytest
from core.enums import JudgementStatus
from app.services.version_service import version_service
from app.services.judgement_service import create_versioned_judgement, transition_judgement_state, get_judgement_state, get_state_history, can_transition_to, get_available_transitions
from app.services.state_machine_service import JudgementStateMachine

class TestStateMachineService:
    def setup_method(self):
        # 重置版本服务状态
        version_service._versions = {}
        version_service._judgement_latest = {}
        # 重置状态机服务状态
        from app.services.state_machine_service import state_machine
        state_machine._state_transitions = {}
        state_machine._judgement_transitions = {}
    
    def test_transition_state(self):
        """测试状态转换功能"""
        # 创建一个判断
        judgement_id = "test-judgement-1"
        content = {
            "conclusion": "这个产品质量很好",
            "facts": ["产品通过了质量检测", "用户反馈良好"]
        }
        
        # 创建版本（初始状态为未结案）
        version1 = create_versioned_judgement(
            judgement_id=judgement_id,
            content=content,
            status=JudgementStatus.UNRESOLVED
        )
        
        # 转换到条件性成立状态
        reason = "证据充分，结论成立"
        new_version, transition = transition_judgement_state(
            judgement_id=judgement_id,
            to_state=JudgementStatus.CONDITIONALLY_TRUE,
            reason=reason
        )
        
        # 验证状态转换
        assert new_version is not None
        assert new_version.status == JudgementStatus.CONDITIONALLY_TRUE
        assert new_version.previous_version_id == version1.version_id
        assert transition is not None
        assert transition.from_state == JudgementStatus.UNRESOLVED
        assert transition.to_state == JudgementStatus.CONDITIONALLY_TRUE
        assert transition.reason == reason
    
    def test_validate_transition(self):
        """测试状态转换验证功能"""
        # 创建状态机实例
        sm = JudgementStateMachine()
        
        # 测试有效的转换
        assert sm.validate_transition(JudgementStatus.UNRESOLVED, JudgementStatus.PARTIALLY_CORRECTED) is True
        assert sm.validate_transition(JudgementStatus.UNRESOLVED, JudgementStatus.FALSIFIED) is True
        assert sm.validate_transition(JudgementStatus.PARTIALLY_CORRECTED, JudgementStatus.CONDITIONALLY_TRUE) is True
        
        # 测试无效的转换
        assert sm.validate_transition(JudgementStatus.FALSIFIED, JudgementStatus.UNRESOLVED) is False
        assert sm.validate_transition(JudgementStatus.CONDITIONALLY_TRUE, JudgementStatus.UNRESOLVED) is False
        
        # 测试同一状态转换
        assert sm.validate_transition(JudgementStatus.UNRESOLVED, JudgementStatus.UNRESOLVED) is True
    
    def test_get_judgement_state(self):
        """测试获取当前状态功能"""
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
        
        # 获取当前状态
        current_state = get_judgement_state(judgement_id)
        assert current_state == JudgementStatus.UNRESOLVED
        
        # 转换状态
        transition_judgement_state(
            judgement_id=judgement_id,
            to_state=JudgementStatus.FALSIFIED,
            reason="发现新证据，结论不成立"
        )
        
        # 再次获取当前状态
        new_state = get_judgement_state(judgement_id)
        assert new_state == JudgementStatus.FALSIFIED
    
    def test_get_state_history(self):
        """测试获取状态转换历史功能"""
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
        
        # 执行多次状态转换
        transition_judgement_state(
            judgement_id=judgement_id,
            to_state=JudgementStatus.PARTIALLY_CORRECTED,
            reason="发现部分错误"
        )
        
        transition_judgement_state(
            judgement_id=judgement_id,
            to_state=JudgementStatus.CONDITIONALLY_TRUE,
            reason="修正后结论成立"
        )
        
        # 获取状态历史
        history = get_state_history(judgement_id)
        assert len(history) == 2
        assert history[0].from_state == JudgementStatus.UNRESOLVED
        assert history[0].to_state == JudgementStatus.PARTIALLY_CORRECTED
        assert history[1].from_state == JudgementStatus.PARTIALLY_CORRECTED
        assert history[1].to_state == JudgementStatus.CONDITIONALLY_TRUE
    
    def test_can_transition_to(self):
        """测试检查是否可以转换到指定状态功能"""
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
        
        # 测试可以转换的状态
        assert can_transition_to(judgement_id, JudgementStatus.PARTIALLY_CORRECTED) is True
        assert can_transition_to(judgement_id, JudgementStatus.FALSIFIED) is True
        assert can_transition_to(judgement_id, JudgementStatus.CONDITIONALLY_TRUE) is True
        
        # 测试不可以转换的状态
        assert can_transition_to(judgement_id, JudgementStatus.UNRESOLVED) is True  # 同一状态
        
        # 转换到已证伪状态
        transition_judgement_state(
            judgement_id=judgement_id,
            to_state=JudgementStatus.FALSIFIED,
            reason="发现新证据，结论不成立"
        )
        
        # 测试已证伪状态的转换限制
        assert can_transition_to(judgement_id, JudgementStatus.UNRESOLVED) is False
        assert can_transition_to(judgement_id, JudgementStatus.PARTIALLY_CORRECTED) is False
        assert can_transition_to(judgement_id, JudgementStatus.CONDITIONALLY_TRUE) is False
        assert can_transition_to(judgement_id, JudgementStatus.FALSIFIED) is True  # 同一状态
    
    def test_get_available_transitions(self):
        """测试获取可用的状态转换目标功能"""
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
        
        # 获取可用转换
        available_transitions = get_available_transitions(judgement_id)
        assert len(available_transitions) == 3
        assert JudgementStatus.PARTIALLY_CORRECTED in available_transitions
        assert JudgementStatus.FALSIFIED in available_transitions
        assert JudgementStatus.CONDITIONALLY_TRUE in available_transitions
        
        # 转换到部分修正状态
        transition_judgement_state(
            judgement_id=judgement_id,
            to_state=JudgementStatus.PARTIALLY_CORRECTED,
            reason="发现部分错误"
        )
        
        # 获取新的可用转换
        new_available_transitions = get_available_transitions(judgement_id)
        assert len(new_available_transitions) == 2
        assert JudgementStatus.FALSIFIED in new_available_transitions
        assert JudgementStatus.CONDITIONALLY_TRUE in new_available_transitions
    
    def test_same_state_transition(self):
        """测试同一状态转换"""
        # 创建一个判断
        judgement_id = "test-judgement-6"
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
        
        # 尝试转换到同一状态
        new_version, transition = transition_judgement_state(
            judgement_id=judgement_id,
            to_state=JudgementStatus.UNRESOLVED,
            reason="状态确认"
        )
        
        # 验证结果
        assert new_version == version1  # 应该返回原版本
        assert transition is None  # 不应该创建转换记录
    
    def test_invalid_transition(self):
        """测试无效状态转换"""
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
            status=JudgementStatus.FALSIFIED
        )
        
        # 尝试从已证伪状态转换到其他状态（无效转换）
        new_version, transition = transition_judgement_state(
            judgement_id=judgement_id,
            to_state=JudgementStatus.UNRESOLVED,
            reason="尝试恢复"
        )
        
        # 验证结果
        assert new_version is None
        assert transition is None
