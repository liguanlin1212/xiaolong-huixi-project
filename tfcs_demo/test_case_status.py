import unittest
from search.case_status_rules import CaseStatus, CaseStatusRules
from search.case_status_judge import CaseStatusJudge
from search.case_status_machine import CaseStatusMachine
from search.case_status_storage import CaseStatusStorage

class TestCaseStatus(unittest.TestCase):
    def setUp(self):
        self.case_status_rules = CaseStatusRules
        self.case_status_judge = CaseStatusJudge()
        self.case_status_machine = CaseStatusMachine()
        self.case_status_storage = CaseStatusStorage()
    
    def test_case_status_rules(self):
        """测试状态判定规则"""
        # 测试已结案事件
        closed_event = {
            "title": "测试已结案事件",
            "time_range": "2023-01-01 至 2023-12-31",
            "description": "测试已结案事件描述",
            "case_status": "已结案",
            "judgment_evolution": ["测试演变1", "测试演变2", "测试演变3"],
            "evidence": ["证据1", "证据2", "证据3"],
            "final_conclusion": "测试结论",
            "sources": ["官方来源1", "官方来源2", "官方来源3"]
        }
        is_closed, reason = self.case_status_rules.is_closed(closed_event)
        self.assertTrue(is_closed)
        
        # 测试未结案事件
        open_event = {
            "title": "测试未结案事件",
            "time_range": "2024-01-01 至 2024-12-31",
            "description": "测试未结案事件描述",
            "case_status": "未结案",
            "judgment_evolution": ["测试演变1", "测试演变2"],
            "evidence": ["证据1", "证据2"],
            "final_conclusion": "",
            "sources": ["非官方来源1", "非官方来源2"]
        }
        is_closed, reason = self.case_status_rules.is_closed(open_event)
        self.assertFalse(is_closed)
        
        # 测试状态转换规则
        self.assertTrue(self.case_status_rules.can_transition(CaseStatus.PENDING, CaseStatus.OPEN))
        self.assertTrue(self.case_status_rules.can_transition(CaseStatus.PENDING, CaseStatus.CLOSED))
        self.assertTrue(self.case_status_rules.can_transition(CaseStatus.OPEN, CaseStatus.CLOSED))
        self.assertFalse(self.case_status_rules.can_transition(CaseStatus.CLOSED, CaseStatus.OPEN))
    
    def test_case_status_judge(self):
        """测试大模型辅助判断逻辑"""
        # 测试事件信息
        test_event = {
            "title": "测试事件",
            "time_range": "2023-01-01 至 2023-12-31",
            "description": "测试事件描述",
            "judgment_evolution": ["测试演变1", "测试演变2", "测试演变3"],
            "evidence": ["证据1", "证据2", "证据3"],
            "final_conclusion": "测试结论",
            "sources": ["官方来源1", "官方来源2", "官方来源3"]
        }
        
        # 测试判断逻辑
        status, reason, confidence = self.case_status_judge.judge_case_status(test_event)
        self.assertIsInstance(status, CaseStatus)
        self.assertIsInstance(reason, str)
        self.assertIsInstance(confidence, int)
        self.assertGreaterEqual(confidence, 0)
        self.assertLessEqual(confidence, 100)
    
    def test_case_status_machine(self):
        """测试状态转换机制"""
        # 测试事件信息
        test_event = {
            "title": "测试事件",
            "time_range": "2023-01-01 至 2023-12-31",
            "description": "测试事件描述",
            "judgment_evolution": ["测试演变1", "测试演变2", "测试演变3"],
            "evidence": ["证据1", "证据2", "证据3"],
            "final_conclusion": "测试结论",
            "sources": ["官方来源1", "官方来源2", "官方来源3"]
        }
        
        event_id = "test_event_1"
        
        # 测试获取初始状态
        initial_status = self.case_status_machine.get_initial_status(test_event, event_id)
        self.assertIsInstance(initial_status, CaseStatus)
        
        # 测试状态转换
        new_status, reason, confidence = self.case_status_machine.transition(event_id, initial_status, test_event)
        self.assertIsInstance(new_status, CaseStatus)
        self.assertIsInstance(reason, str)
        self.assertIsInstance(confidence, int)
        
        # 测试获取当前状态
        current_status, reason, confidence, timestamp = self.case_status_machine.get_current_status(event_id)
        self.assertIsInstance(current_status, CaseStatus)
        
        # 测试获取状态历史
        history = self.case_status_machine.get_status_history(event_id)
        self.assertIsInstance(history, list)
        self.assertTrue(len(history) > 0)
    
    def test_case_status_storage(self):
        """测试状态持久化"""
        # 测试事件信息
        test_event = {
            "title": "测试事件",
            "time_range": "2023-01-01 至 2023-12-31",
            "description": "测试事件描述",
            "judgment_evolution": ["测试演变1", "测试演变2", "测试演变3"],
            "evidence": ["证据1", "证据2", "证据3"],
            "final_conclusion": "测试结论",
            "sources": ["官方来源1", "官方来源2", "官方来源3"]
        }
        
        event_id = "test_event_2"
        
        # 测试保存状态
        status = CaseStatus.CLOSED
        reason = "测试保存状态"
        confidence = 90
        self.case_status_storage.save_status(event_id, status, reason, confidence)
        
        # 测试获取状态
        saved_status, saved_reason, saved_confidence, timestamp = self.case_status_storage.get_status(event_id)
        self.assertEqual(saved_status, status)
        self.assertEqual(saved_reason, reason)
        self.assertEqual(saved_confidence, confidence)
        
        # 测试获取状态历史
        history = self.case_status_storage.get_status_history(event_id)
        self.assertIsInstance(history, list)
        self.assertTrue(len(history) > 0)
        
        # 测试列出所有事件
        events = self.case_status_storage.list_events()
        self.assertIsInstance(events, list)
        self.assertIn(event_id, events)
        
        # 测试删除状态
        self.case_status_storage.delete_status(event_id)
        deleted_status, _, _, _ = self.case_status_storage.get_status(event_id)
        self.assertIsNone(deleted_status)

if __name__ == "__main__":
    unittest.main()