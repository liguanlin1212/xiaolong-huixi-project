import unittest
import os
import tempfile
from search.search_handler import SearchHandler
from search.search_prompt import SearchPromptBuilder
from search.search_analyzer import SearchAnalyzer
from search.case_status import CaseStatusChecker

class TestSearchFunctionality(unittest.TestCase):
    def setUp(self):
        self.search_handler = SearchHandler()
        self.prompt_builder = SearchPromptBuilder()
        self.search_analyzer = SearchAnalyzer()
        self.case_status_checker = CaseStatusChecker()
    
    def test_validate_query(self):
        """测试查询验证功能"""
        # 测试空查询
        is_valid, error_msg = self.search_handler.validate_query("")
        self.assertFalse(is_valid)
        self.assertEqual(error_msg, "搜索关键词至少需要2个字符")
        
        # 测试短查询
        is_valid, error_msg = self.search_handler.validate_query("a")
        self.assertFalse(is_valid)
        self.assertEqual(error_msg, "搜索关键词至少需要2个字符")
        
        # 测试长查询
        long_query = "a" * 101
        is_valid, error_msg = self.search_handler.validate_query(long_query)
        self.assertFalse(is_valid)
        self.assertEqual(error_msg, "搜索关键词不能超过100个字符")
        
        # 测试有效查询
        is_valid, error_msg = self.search_handler.validate_query("COVID-19 起源")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_cache_mechanism(self):
        """测试缓存机制"""
        # 测试缓存键生成
        query = "测试查询"
        cache_key = self.search_handler.generate_cache_key(query)
        self.assertIsInstance(cache_key, str)
        
        # 测试缓存保存和读取
        test_result = [{"title": "测试结果", "description": "测试描述"}]
        self.search_handler.save_cache_result(query, test_result)
        
        cached_result = self.search_handler.get_cached_result(query)
        self.assertEqual(cached_result, test_result)
    
    def test_prompt_builder(self):
        """测试搜索指令构建"""
        # 测试基础搜索指令
        query = "COVID-19 起源"
        prompt = self.prompt_builder.build_prompt(query)
        self.assertIn(query, prompt)
        
        # 测试精炼搜索指令
        previous_results = "测试结果"
        refine_prompt = self.prompt_builder.build_refine_prompt(query, previous_results)
        self.assertIn(query, refine_prompt)
        self.assertIn(previous_results, refine_prompt)
        
        # 测试结案状态判断指令
        event_info = "测试事件信息"
        status_prompt = self.prompt_builder.build_case_status_prompt(event_info)
        self.assertIn(event_info, status_prompt)
    
    def test_search_analyzer(self):
        """测试搜索结果分析"""
        # 测试模型响应解析
        test_response = """
## 事件概述
- 事件名称：测试事件
- 时间范围：2023-01-01 至 2023-12-31
- 事件描述：测试事件描述
- 结案状态：已结案

## 判断演变过程
1. 2023-01-01：初始判断 - 依据1
2. 2023-06-01：更新判断 - 依据2
3. 2023-12-31：最终判断 - 依据3

## 关键证据
1. 证据1
2. 证据2
3. 证据3

## 最终结论
最终结论内容

## 信息来源
来源1
来源2
来源3
"""
        
        parsed_result = self.search_analyzer.parse_model_response(test_response)
        self.assertEqual(parsed_result["title"], "测试事件")
        self.assertEqual(parsed_result["description"], "测试事件描述")
        self.assertEqual(parsed_result["time_range"], "2023-01-01 至 2023-12-31")
        self.assertEqual(parsed_result["case_status"], "已结案")
        self.assertEqual(len(parsed_result["judgment_evolution"]), 3)
        self.assertEqual(len(parsed_result["evidence"]), 3)
        self.assertEqual(parsed_result["final_conclusion"], "最终结论内容")
        self.assertEqual(len(parsed_result["sources"]), 3)
    
    def test_case_status_checker(self):
        """测试结案状态检查"""
        # 测试已结案事件
        closed_event = {
            "case_status": "已结案",
            "time_range": "2023-01-01 至 2023-12-31",
            "judgment_evolution": ["测试演变"],
            "final_conclusion": "测试结论"
        }
        is_closed, message = self.case_status_checker.check_case_status(closed_event)
        self.assertTrue(is_closed)
        self.assertEqual(message, "")
        
        # 测试未结案事件
        open_event = {
            "case_status": "未结案",
            "time_range": "2023-01-01 至 2023-12-31",
            "judgment_evolution": ["测试演变"],
            "final_conclusion": "测试结论"
        }
        is_closed, message = self.case_status_checker.check_case_status(open_event)
        self.assertFalse(is_closed)
        self.assertEqual(message, "该事件尚未结案，暂不展示")

if __name__ == "__main__":
    unittest.main()