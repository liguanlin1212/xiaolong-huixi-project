import pytest
from search.version_manager import VersionManager
from search.version_history import VersionHistory
from search.case_status_machine import CaseStatusMachine
from search.self_correction import SelfCorrectionMechanism

class TestSelfCorrection:
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
        
        # 创建一些测试版本
        self.event_id = "test-event-1"
        self.version1 = self.version_manager.create_version(
            self.event_id, 
            "事件：测试事件\n时间范围：2026-03-01\n描述：这是一个测试事件\n结案状态：已结案\n最终结论：测试结论1"
        )
        self.version2 = self.version_manager.create_version(
            self.event_id, 
            "事件：测试事件\n时间范围：2026-03-01\n描述：这是一个更新的测试事件\n结案状态：已结案\n最终结论：测试结论2",
            self.version1.version_id
        )
    
    def test_analyze_new_information(self):
        """测试分析新信息"""
        new_info = "测试事件的最新信息：发生时间为2026-03-02，内容有更新"
        analysis = self.self_correction.analyze_new_information(new_info)
        
        assert "keywords" in analysis
        assert "time_info" in analysis
        assert "related_events" in analysis
        assert len(analysis["keywords"]) > 0
        assert analysis["time_info"] == "2026-03-02"
        assert self.event_id in analysis["related_events"]
    
    def test_trace_impact(self):
        """测试追踪影响"""
        new_info = "测试事件的最新信息：发生时间为2026-03-02，内容有更新"
        impact_results = self.self_correction.trace_impact(new_info)
        
        assert self.event_id in impact_results
        assert len(impact_results[self.event_id]) > 0
        
        for version_info in impact_results[self.event_id]:
            assert "version_id" in version_info
            assert "timestamp" in version_info
            assert "content" in version_info
            assert "impacted_aspects" in version_info
            assert len(version_info["impacted_aspects"]) > 0
    
    def test_generate_correction_suggestions(self):
        """测试生成纠错建议"""
        new_info = "测试事件的最新信息：发生时间为2026-03-02，内容有更新"
        impact_results = self.self_correction.trace_impact(new_info)
        suggestions = self.self_correction.generate_correction_suggestions(impact_results, new_info)
        
        assert self.event_id in suggestions
        assert len(suggestions[self.event_id]) > 0
        
        for suggestion_info in suggestions[self.event_id]:
            assert "version_id" in suggestion_info
            assert "suggestion" in suggestion_info
            assert "confidence" in suggestion_info
            assert 0 <= suggestion_info["confidence"] <= 1
    
    def test_process_self_correction(self):
        """测试处理自查纠错流程"""
        new_info = "测试事件的最新信息：发生时间为2026-03-02，内容有更新"
        correction_result = self.self_correction.process_self_correction(new_info)
        
        assert "impact_results" in correction_result
        assert "suggestions" in correction_result
        assert "correction_results" in correction_result
        
        # 验证影响分析结果
        assert self.event_id in correction_result["impact_results"]
        
        # 验证纠错建议
        assert self.event_id in correction_result["suggestions"]
    
    def test_extract_keywords(self):
        """测试提取关键词"""
        text = "测试事件的最新信息：发生时间为2026-03-02，内容有更新"
        keywords = self.self_correction._extract_keywords(text)
        
        assert isinstance(keywords, list)
        assert len(keywords) > 0
    
    def test_extract_time_info(self):
        """测试提取时间信息"""
        text = "测试事件的最新信息：发生时间为2026-03-02，内容有更新"
        time_info = self.self_correction._extract_time_info(text)
        
        assert time_info == "2026-03-02"
    
    def test_find_related_events(self):
        """测试查找相关事件"""
        keywords = ["测试", "事件"]
        related_events = self.self_correction._find_related_events(keywords)
        
        assert isinstance(related_events, list)
        assert self.event_id in related_events
    
    def test_is_version_affected(self):
        """测试判断版本是否受影响"""
        analysis = {
            "keywords": ["测试", "事件"],
            "time_info": "2026-03-01",
            "related_events": [self.event_id]
        }
        
        is_affected = self.self_correction._is_version_affected(self.version1, analysis)
        assert is_affected
    
    def test_identify_impacted_aspects(self):
        """测试识别受影响的方面"""
        analysis = {
            "keywords": ["测试", "事件"],
            "time_info": "2026-03-01",
            "related_events": [self.event_id]
        }
        
        impacted_aspects = self.self_correction._identify_impacted_aspects(self.version1, analysis)
        
        assert isinstance(impacted_aspects, list)
        assert len(impacted_aspects) > 0
        assert "事件描述" in impacted_aspects
        assert "时间信息" in impacted_aspects
        assert "结论" in impacted_aspects
    
    def test_calculate_confidence(self):
        """测试计算置信度"""
        version_info = {
            "content": "事件：测试事件\n时间范围：2026-03-01\n描述：这是一个测试事件\n结案状态：已结案\n最终结论：测试结论1"
        }
        new_information = "测试事件的最新信息：发生时间为2026-03-02，内容有更新"
        
        confidence = self.self_correction._calculate_confidence(version_info, new_information)
        
        assert 0 <= confidence <= 1
    
    def test_extract_corrected_content(self):
        """测试从建议中提取修正后的内容"""
        suggestion = """受影响的具体内容：时间信息和事件描述
错误原因分析：新信息提供了更准确的时间和内容
修正建议：更新时间信息和事件描述
修正后的内容：
事件：测试事件
时间范围：2026-03-02
描述：这是一个更新的测试事件
结案状态：已结案
最终结论：测试结论3"""
        
        corrected_content = self.self_correction._extract_corrected_content(suggestion)
        
        assert corrected_content is not None
        assert "事件：测试事件" in corrected_content
        assert "时间范围：2026-03-02" in corrected_content
