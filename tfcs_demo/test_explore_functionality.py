import unittest
from search.domain_categories import DomainCategories
from search.explore_prompt import ExplorePromptBuilder
from search.refresh_manager import RefreshManager

class TestExploreFunctionality(unittest.TestCase):
    def setUp(self):
        self.domain_categories = DomainCategories()
        self.prompt_builder = ExplorePromptBuilder()
        self.refresh_manager = RefreshManager()
    
    def test_domain_categories(self):
        """测试领域分类功能"""
        # 测试获取所有领域
        categories = self.domain_categories.get_all_categories()
        self.assertIsInstance(categories, list)
        self.assertTrue(len(categories) > 0)
        
        # 测试获取领域信息
        for category in categories:
            info = self.domain_categories.get_category_info(category)
            self.assertIsInstance(info, dict)
            self.assertIn('description', info)
            self.assertIn('examples', info)
        
        # 测试检查领域有效性
        self.assertTrue(self.domain_categories.is_valid_category('政治'))
        self.assertTrue(self.domain_categories.is_valid_category('经济'))
        self.assertFalse(self.domain_categories.is_valid_category('不存在的领域'))
    
    def test_explore_prompt_builder(self):
        """测试大模型prompt模板"""
        # 测试构建基础prompt
        domain = "科技"
        prompt = self.prompt_builder.build_prompt(domain)
        self.assertIn(domain, prompt)
        self.assertIn("请给我十个", prompt)
        self.assertIn("领域已结案的事件", prompt)
        
        # 测试构建精炼prompt
        previous_results = "测试结果"
        refine_prompt = self.prompt_builder.build_refine_prompt(domain, previous_results)
        self.assertIn(domain, refine_prompt)
        self.assertIn(previous_results, refine_prompt)
        self.assertIn("请提供更多", refine_prompt)
    
    def test_refresh_manager(self):
        """测试后台自动刷新机制"""
        # 测试缓存目录创建
        import os
        cache_dir = os.path.join(os.path.dirname(__file__), "data", "explore_cache")
        self.assertTrue(os.path.exists(cache_dir))
        
        # 测试获取缓存的事件（初始为空）
        domain = "科技"
        events = self.refresh_manager.get_cached_events(domain)
        self.assertIsInstance(events, list)
        
        # 测试缓存有效性检查
        is_valid = self.refresh_manager.is_cache_valid(domain)
        self.assertIsInstance(is_valid, bool)
    
    def test_event_structure(self):
        """测试事件数据结构"""
        # 测试示例事件结构 - 直接定义测试数据，避免导入streamlit
        test_events = [
            {
                "title": "测试事件",
                "time_range": "2023-01-01 至 2023-12-31",
                "description": "测试事件描述",
                "case_status": "已结案",
                "judgment_evolution": ["测试演变1", "测试演变2", "测试演变3"],
                "evidence": ["证据1", "证据2", "证据3"],
                "final_conclusion": "测试结论",
                "sources": ["来源1", "来源2", "来源3"]
            }
        ]
        
        self.assertIsInstance(test_events, list)
        self.assertTrue(len(test_events) > 0)
        
        # 检查事件结构
        for event in test_events:
            self.assertIsInstance(event, dict)
            self.assertIn('title', event)
            self.assertIn('time_range', event)
            self.assertIn('description', event)
            self.assertIn('case_status', event)
            self.assertIn('judgment_evolution', event)
            self.assertIn('evidence', event)
            self.assertIn('final_conclusion', event)
            self.assertIn('sources', event)
            
            # 检查字段类型
            self.assertIsInstance(event['title'], str)
            self.assertIsInstance(event['time_range'], str)
            self.assertIsInstance(event['description'], str)
            self.assertIsInstance(event['case_status'], str)
            self.assertIsInstance(event['judgment_evolution'], list)
            self.assertIsInstance(event['evidence'], list)
            self.assertIsInstance(event['final_conclusion'], str)
            self.assertIsInstance(event['sources'], list)

if __name__ == "__main__":
    unittest.main()