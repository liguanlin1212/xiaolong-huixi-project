import pytest
import os
import tempfile
from search.version_manager import VersionManager
from search.version_history import VersionHistory
from search.case_status_machine import CaseStatusMachine
from search.self_correction import SelfCorrectionMechanism
from search.discomfort_trigger import DiscomfortTrigger

class TestDiscomfortTrigger:
    def setup_method(self):
        # 初始化测试环境
        self.version_manager = VersionManager()
        self.version_history = VersionHistory(self.version_manager)
        self.case_status_machine = CaseStatusMachine()
        self.self_correction = SelfCorrectionMechanism(
            self.version_manager, 
            self.version_history, 
            self.case_status_machine
        )
        
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建测试版本
        self.event_id = "test-event-1"
        self.version1 = self.version_manager.create_version(
            self.event_id, 
            "事件：测试事件\n时间范围：2026-03-01\n描述：这是一个测试事件\n结案状态：已结案\n最终结论：测试结论1"
        )
        
        # 初始化不适感触发机制
        self.discomfort_trigger = DiscomfortTrigger(
            self.version_manager, 
            self.version_history, 
            self.case_status_machine, 
            self.self_correction
        )
    
    def teardown_method(self):
        # 清理临时目录
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_trigger_discomfort(self):
        """测试触发不适感"""
        discomfort_level = 3
        reason = "测试不适原因"
        additional_info = {"具体问题": "测试问题", "建议": "测试建议"}
        
        # 触发不适感
        trigger_id = self.discomfort_trigger.trigger_discomfort(
            self.event_id, 
            self.version1.version_id, 
            discomfort_level, 
            reason, 
            additional_info
        )
        
        # 验证触发成功
        assert trigger_id is not None
        assert isinstance(trigger_id, str)
        
        # 获取触发记录
        triggers = self.discomfort_trigger.get_triggers(self.event_id)
        assert len(triggers) > 0
        
        # 验证触发记录
        trigger = triggers[-1]
        assert trigger["trigger_id"] == trigger_id
        assert trigger["event_id"] == self.event_id
        assert trigger["version_id"] == self.version1.version_id
        assert trigger["discomfort_level"] == discomfort_level
        assert trigger["reason"] == reason
        assert trigger["additional_info"] == additional_info
        assert trigger["status"] == "resolved"
    
    def test_evaluate_trigger_effect(self):
        """测试评估触发效果"""
        # 先触发不适感
        trigger_id = self.discomfort_trigger.trigger_discomfort(
            self.event_id, 
            self.version1.version_id, 
            3, 
            "测试不适原因"
        )
        
        # 评估触发效果
        effectiveness = 4
        comments = "测试评估评论"
        result = self.discomfort_trigger.evaluate_trigger_effect(
            trigger_id, 
            self.event_id, 
            effectiveness, 
            comments
        )
        
        # 验证评估成功
        assert result is True
        
        # 获取评估记录
        evaluations = self.discomfort_trigger.get_evaluations(self.event_id)
        assert len(evaluations) > 0
        
        # 验证评估记录
        evaluation = evaluations[-1]
        assert evaluation["trigger_id"] == trigger_id
        assert evaluation["event_id"] == self.event_id
        assert evaluation["effectiveness"] == effectiveness
        assert evaluation["comments"] == comments
    
    def test_get_triggers(self):
        """测试获取触发记录"""
        # 触发多次不适感
        for i in range(3):
            self.discomfort_trigger.trigger_discomfort(
                self.event_id, 
                self.version1.version_id, 
                3, 
                f"测试不适原因{i}"
            )
        
        # 获取所有触发记录
        all_triggers = self.discomfort_trigger.get_triggers()
        assert len(all_triggers) >= 3
        
        # 获取特定事件的触发记录
        event_triggers = self.discomfort_trigger.get_triggers(self.event_id)
        assert len(event_triggers) >= 3
    
    def test_get_evaluations(self):
        """测试获取评估记录"""
        # 触发并评估多次
        for i in range(3):
            trigger_id = self.discomfort_trigger.trigger_discomfort(
                self.event_id, 
                self.version1.version_id, 
                3, 
                f"测试不适原因{i}"
            )
            self.discomfort_trigger.evaluate_trigger_effect(
                trigger_id, 
                self.event_id, 
                4, 
                f"测试评估评论{i}"
            )
        
        # 获取所有评估记录
        all_evaluations = self.discomfort_trigger.get_evaluations()
        assert len(all_evaluations) >= 3
        
        # 获取特定事件的评估记录
        event_evaluations = self.discomfort_trigger.get_evaluations(self.event_id)
        assert len(event_evaluations) >= 3
    
    def test_get_trigger_stats(self):
        """测试获取触发统计信息"""
        # 触发多次不适感
        for i in range(5):
            self.discomfort_trigger.trigger_discomfort(
                self.event_id, 
                self.version1.version_id, 
                i + 1, 
                f"测试不适原因{i}"
            )
        
        # 获取统计信息
        stats = self.discomfort_trigger.get_trigger_stats()
        
        # 验证统计信息
        assert stats["total_triggers"] >= 5
        assert stats["resolved_triggers"] >= 5
        assert stats["resolution_rate"] >= 0.5
        assert sum(stats["discomfort_levels"].values()) >= 5
    
    def test_get_evaluation_stats(self):
        """测试获取评估统计信息"""
        # 触发并评估多次
        for i in range(5):
            trigger_id = self.discomfort_trigger.trigger_discomfort(
                self.event_id, 
                self.version1.version_id, 
                3, 
                f"测试不适原因{i}"
            )
            self.discomfort_trigger.evaluate_trigger_effect(
                trigger_id, 
                self.event_id, 
                i + 1, 
                f"测试评估评论{i}"
            )
        
        # 获取统计信息
        stats = self.discomfort_trigger.get_evaluation_stats()
        
        # 验证统计信息
        assert stats["total_evaluations"] >= 5
        assert stats["average_effectiveness"] >= 1.0
        assert sum(stats["effectiveness_levels"].values()) >= 5
