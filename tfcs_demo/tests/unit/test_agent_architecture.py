import unittest
from agent.base_agent import BaseAgent
from agent.search_agent import SearchAgent
from agent.analysis_agent import AnalysisAgent
from agent.organization_agent import OrganizationAgent
from agent.coordinator import AgentCoordinator
from agent.communication import communication_manager, Message

class TestAgentArchitecture(unittest.TestCase):
    """
    多Agent架构测试类
    """
    
    def setUp(self):
        """
        测试前的设置
        """
        self.search_agent = SearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.organization_agent = OrganizationAgent()
        self.coordinator = AgentCoordinator()
    
    def test_agent_initialization(self):
        """
        测试Agent初始化
        """
        self.assertIsNotNone(self.search_agent)
        self.assertIsNotNone(self.analysis_agent)
        self.assertIsNotNone(self.organization_agent)
        self.assertIsNotNone(self.coordinator)
        
        # 测试Agent ID
        self.assertIsInstance(self.search_agent.agent_id, str)
        self.assertIsInstance(self.analysis_agent.agent_id, str)
        self.assertIsInstance(self.organization_agent.agent_id, str)
        
        # 测试Agent状态
        self.assertEqual(self.search_agent.status, "IDLE")
        self.assertEqual(self.analysis_agent.status, "IDLE")
        self.assertEqual(self.organization_agent.status, "IDLE")
    
    def test_search_agent(self):
        """
        测试搜索Agent
        """
        # 测试搜索功能
        result = self.search_agent.process({"keyword": "测试事件"})
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("results", result)
        self.assertIsInstance(result["results"], list)
    
    def test_analysis_agent(self):
        """
        测试分析Agent
        """
        # 模拟搜索结果
        mock_search_results = [
            {"title": "测试结果1", "content": "测试内容1"},
            {"title": "测试结果2", "content": "测试内容2"}
        ]
        
        # 测试分析功能
        result = self.analysis_agent.process({"search_results": mock_search_results})
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("analysis", result)
        self.assertIn("timeline", result)
        self.assertIsInstance(result["timeline"], list)
    
    def test_organization_agent(self):
        """
        测试整理Agent
        """
        # 模拟分析结果
        mock_analysis = {
            "initial_judgment": "初始判断",
            "evolved_judgment": "演变后的判断",
            "key_factors": ["因素1", "因素2"],
            "confidence": 0.85
        }
        
        # 模拟时间线
        mock_timeline = [
            {"timestamp": "2026-02-20", "event": "事件发生", "judgment": "初始判断"},
            {"timestamp": "2026-03-01", "event": "最终结论", "judgment": "最终判断"}
        ]
        
        # 测试整理功能
        result = self.organization_agent.process({"analysis": mock_analysis, "timeline": mock_timeline})
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("organized_info", result)
        self.assertIn("presentation", result)
    
    def test_agent_coordinator(self):
        """
        测试Agent协调器
        """
        # 测试完整的协作流程
        result = self.coordinator.process_task({"keyword": "测试事件"})
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("search_results", result)
        self.assertIn("analysis", result)
        self.assertIn("timeline", result)
        self.assertIn("organized_info", result)
        self.assertIn("presentation", result)
    
    def test_agent_health_check(self):
        """
        测试Agent健康检查
        """
        # 测试单个Agent的健康检查
        self.assertTrue(self.search_agent.health_check())
        self.assertTrue(self.analysis_agent.health_check())
        self.assertTrue(self.organization_agent.health_check())
        
        # 测试协调器的健康检查
        health_status = self.coordinator.health_check()
        self.assertTrue(health_status["search_agent"])
        self.assertTrue(health_status["analysis_agent"])
        self.assertTrue(health_status["organization_agent"])
        self.assertTrue(health_status["all_healthy"])
    
    def test_agent_status(self):
        """
        测试Agent状态
        """
        status = self.coordinator.get_agent_status()
        self.assertIn("search_agent", status)
        self.assertIn("analysis_agent", status)
        self.assertIn("organization_agent", status)
        
        # 检查状态信息的结构
        for agent_name, agent_info in status.items():
            self.assertIn("agent_id", agent_info)
            self.assertIn("status", agent_info)
            self.assertIn("created_at", agent_info)
            self.assertIn("last_activity", agent_info)
            self.assertIn("context", agent_info)

if __name__ == "__main__":
    unittest.main()
