import unittest
import os
import shutil
from core.types import Event, JudgementVersion
from core.enums import JudgementStatus
from data.persistence import DataPersistence

class TestDataStructures(unittest.TestCase):
    """
    数据结构测试类
    """
    
    def setUp(self):
        """
        测试前的设置
        """
        # 创建临时数据目录
        self.test_data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "test_data"
        )
        
        # 清理旧的测试数据
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        
        # 创建新的测试数据目录
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # 创建数据持久化实例
        self.persistence = DataPersistence(self.test_data_dir)
    
    def tearDown(self):
        """
        测试后的清理
        """
        # 清理测试数据
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
    
    def test_event_creation(self):
        """
        测试事件创建
        """
        # 创建事件
        event = Event(
            event_id="event_1",
            title="测试事件",
            description="这是一个测试事件",
            start_time="2026-03-01",
            end_time="2026-03-02",
            judgement_ids=["judgement_1"],
            metadata={"source": "测试"},
            status=JudgementStatus.UNRESOLVED
        )
        
        # 验证事件属性
        self.assertEqual(event.event_id, "event_1")
        self.assertEqual(event.title, "测试事件")
        self.assertEqual(event.description, "这是一个测试事件")
        self.assertEqual(event.start_time, "2026-03-01")
        self.assertEqual(event.end_time, "2026-03-02")
        self.assertEqual(event.judgement_ids, ["judgement_1"])
        self.assertEqual(event.metadata, {"source": "测试"})
        self.assertEqual(event.status, JudgementStatus.UNRESOLVED)
    
    def test_event_to_dict(self):
        """
        测试事件转换为字典
        """
        # 创建事件
        event = Event(
            event_id="event_1",
            title="测试事件",
            description="这是一个测试事件",
            start_time="2026-03-01",
            status=JudgementStatus.UNRESOLVED
        )
        
        # 转换为字典
        event_dict = event.to_dict()
        
        # 验证字典属性
        self.assertEqual(event_dict["event_id"], "event_1")
        self.assertEqual(event_dict["title"], "测试事件")
        self.assertEqual(event_dict["description"], "这是一个测试事件")
        self.assertEqual(event_dict["start_time"], "2026-03-01")
        self.assertEqual(event_dict["end_time"], None)
        self.assertEqual(event_dict["judgement_ids"], [])
        self.assertEqual(event_dict["metadata"], None)
        self.assertEqual(event_dict["status"], "未结案")
    
    def test_judgement_version_creation(self):
        """
        测试判断版本创建
        """
        # 创建判断版本
        version = JudgementVersion(
            version_id="version_1",
            judgement_id="judgement_1",
            event_id="event_1",
            content={"conclusion": "测试结论"},
            status=JudgementStatus.UNRESOLVED,
            created_at="2026-03-01T12:00:00",
            previous_version_id=None,
            metadata={"source": "测试"}
        )
        
        # 验证版本属性
        self.assertEqual(version.version_id, "version_1")
        self.assertEqual(version.judgement_id, "judgement_1")
        self.assertEqual(version.event_id, "event_1")
        self.assertEqual(version.content, {"conclusion": "测试结论"})
        self.assertEqual(version.status, JudgementStatus.UNRESOLVED)
        self.assertEqual(version.created_at, "2026-03-01T12:00:00")
        self.assertEqual(version.previous_version_id, None)
        self.assertEqual(version.metadata, {"source": "测试"})
    
    def test_judgement_version_to_dict(self):
        """
        测试判断版本转换为字典
        """
        # 创建判断版本
        version = JudgementVersion(
            version_id="version_1",
            judgement_id="judgement_1",
            event_id="event_1",
            content={"conclusion": "测试结论"},
            status=JudgementStatus.UNRESOLVED,
            created_at="2026-03-01T12:00:00"
        )
        
        # 转换为字典
        version_dict = version.to_dict()
        
        # 验证字典属性
        self.assertEqual(version_dict["version_id"], "version_1")
        self.assertEqual(version_dict["judgement_id"], "judgement_1")
        self.assertEqual(version_dict["event_id"], "event_1")
        self.assertEqual(version_dict["content"], {"conclusion": "测试结论"})
        self.assertEqual(version_dict["status"], "未结案")
        self.assertEqual(version_dict["created_at"], "2026-03-01T12:00:00")
        self.assertEqual(version_dict["previous_version_id"], None)
        self.assertEqual(version_dict["metadata"], None)
    
    def test_judgement_status_transitions(self):
        """
        测试结案状态转换
        """
        # 测试未结案状态的转换
        unresolved = JudgementStatus.UNRESOLVED
        self.assertTrue(unresolved.can_transition_to(JudgementStatus.PARTIALLY_CORRECTED))
        self.assertTrue(unresolved.can_transition_to(JudgementStatus.FALSIFIED))
        self.assertTrue(unresolved.can_transition_to(JudgementStatus.CONDITIONALLY_TRUE))
        self.assertTrue(unresolved.can_transition_to(JudgementStatus.CONFIRMED))
        self.assertTrue(unresolved.can_transition_to(JudgementStatus.UNDER_REVIEW))
        
        # 测试已证伪状态的转换
        falsified = JudgementStatus.FALSIFIED
        self.assertTrue(falsified.can_transition_to(JudgementStatus.UNDER_REVIEW))
        self.assertFalse(falsified.can_transition_to(JudgementStatus.CONFIRMED))
    
    def test_event_persistence(self):
        """
        测试事件持久化
        """
        # 创建事件
        event = Event(
            event_id="event_1",
            title="测试事件",
            description="这是一个测试事件",
            start_time="2026-03-01",
            status=JudgementStatus.UNRESOLVED
        )
        
        # 保存事件
        self.assertTrue(self.persistence.save_event(event))
        
        # 加载事件
        loaded_event = self.persistence.load_event("event_1")
        self.assertIsNotNone(loaded_event)
        self.assertEqual(loaded_event.event_id, event.event_id)
        self.assertEqual(loaded_event.title, event.title)
        self.assertEqual(loaded_event.description, event.description)
        self.assertEqual(loaded_event.start_time, event.start_time)
        self.assertEqual(loaded_event.status, event.status)
    
    def test_judgement_version_persistence(self):
        """
        测试判断版本持久化
        """
        # 创建判断版本
        version = JudgementVersion(
            version_id="version_1",
            judgement_id="judgement_1",
            event_id="event_1",
            content={"conclusion": "测试结论"},
            status=JudgementStatus.UNRESOLVED,
            created_at="2026-03-01T12:00:00"
        )
        
        # 保存判断版本
        self.assertTrue(self.persistence.save_judgement_version(version))
        
        # 加载判断版本
        loaded_version = self.persistence.load_judgement_version("version_1")
        self.assertIsNotNone(loaded_version)
        self.assertEqual(loaded_version.version_id, version.version_id)
        self.assertEqual(loaded_version.judgement_id, version.judgement_id)
        self.assertEqual(loaded_version.event_id, version.event_id)
        self.assertEqual(loaded_version.content, version.content)
        self.assertEqual(loaded_version.status, version.status)
        self.assertEqual(loaded_version.created_at, version.created_at)
    
    def test_latest_judgement_version(self):
        """
        测试加载最新判断版本
        """
        # 创建第一个版本
        version1 = JudgementVersion(
            version_id="version_1",
            judgement_id="judgement_1",
            content={"conclusion": "初始结论"},
            status=JudgementStatus.UNRESOLVED,
            created_at="2026-03-01T12:00:00"
        )
        
        # 创建第二个版本
        version2 = JudgementVersion(
            version_id="version_2",
            judgement_id="judgement_1",
            content={"conclusion": "更新结论"},
            status=JudgementStatus.PARTIALLY_CORRECTED,
            created_at="2026-03-02T12:00:00",
            previous_version_id="version_1"
        )
        
        # 保存版本
        self.assertTrue(self.persistence.save_judgement_version(version1))
        self.assertTrue(self.persistence.save_judgement_version(version2))
        
        # 加载最新版本
        latest_version = self.persistence.load_latest_judgement_version("judgement_1")
        self.assertIsNotNone(latest_version)
        self.assertEqual(latest_version.version_id, "version_2")
        self.assertEqual(latest_version.content, {"conclusion": "更新结论"})
    
    def test_data_backup_restore(self):
        """
        测试数据备份和恢复
        """
        # 创建事件
        event = Event(
            event_id="event_1",
            title="测试事件",
            description="这是一个测试事件",
            start_time="2026-03-01",
            status=JudgementStatus.UNRESOLVED
        )
        
        # 保存事件
        self.assertTrue(self.persistence.save_event(event))
        
        # 备份数据
        backup_dir = os.path.join(self.test_data_dir, "backup_test")
        self.assertTrue(self.persistence.backup_data(backup_dir))
        
        # 修改事件
        event.title = "修改后的事件"
        self.assertTrue(self.persistence.save_event(event))
        
        # 恢复数据
        self.assertTrue(self.persistence.restore_data(backup_dir))
        
        # 验证恢复后的数据
        restored_event = self.persistence.load_event("event_1")
        self.assertIsNotNone(restored_event)
        self.assertEqual(restored_event.title, "测试事件")

if __name__ == "__main__":
    unittest.main()
