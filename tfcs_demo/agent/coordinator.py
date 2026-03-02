from typing import Dict, Any, List
from .base_agent import BaseAgent
from .search_agent import SearchAgent
from .analysis_agent import AnalysisAgent
from .organization_agent import OrganizationAgent
from .communication import communication_manager
import time

class AgentCoordinator:
    """
    Agent协调器，负责协调多个Agent的协作
    """
    
    def __init__(self):
        """
        初始化Agent协调器
        """
        self.search_agent = SearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.organization_agent = OrganizationAgent()
        
        # 注册Agent到通信管理器
        communication_manager.register_agent(self.search_agent.agent_id, self.search_agent)
        communication_manager.register_agent(self.analysis_agent.agent_id, self.analysis_agent)
        communication_manager.register_agent(self.organization_agent.agent_id, self.organization_agent)
        
        self.tasks = {}
        self.results = {}
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理任务
        
        参数:
            task: 任务数据，包含搜索关键词
            
        返回:
            Dict[str, Any]: 处理结果
        """
        task_id = task.get("task_id", str(time.time()))
        self.tasks[task_id] = task
        self.results[task_id] = {}
        
        try:
            # 1. 搜索Agent执行全网搜索
            search_result = self._execute_search(task)
            if search_result.get("status") != "success":
                return {
                    "status": "error",
                    "message": search_result.get("message", "搜索失败")
                }
            
            # 2. 分析Agent进行判断分析和时间线构建
            analysis_result = self._execute_analysis(search_result)
            if analysis_result.get("status") != "success":
                return {
                    "status": "error",
                    "message": analysis_result.get("message", "分析失败")
                }
            
            # 3. 整理Agent进行信息整理和展示
            organization_result = self._execute_organization(analysis_result)
            if organization_result.get("status") != "success":
                return {
                    "status": "error",
                    "message": organization_result.get("message", "整理失败")
                }
            
            # 4. 汇总结果
            final_result = self._summarize_results(search_result, analysis_result, organization_result)
            
            self.results[task_id] = final_result
            return final_result
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _execute_search(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行搜索任务
        
        参数:
            task: 任务数据
            
        返回:
            Dict[str, Any]: 搜索结果
        """
        keyword = task.get("keyword", "")
        return self.search_agent.process({"keyword": keyword})
    
    def _execute_analysis(self, search_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行分析任务
        
        参数:
            search_result: 搜索结果
            
        返回:
            Dict[str, Any]: 分析结果
        """
        results = search_result.get("results", [])
        return self.analysis_agent.process({"search_results": results})
    
    def _execute_organization(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行整理任务
        
        参数:
            analysis_result: 分析结果
            
        返回:
            Dict[str, Any]: 整理结果
        """
        analysis = analysis_result.get("analysis")
        timeline = analysis_result.get("timeline", [])
        return self.organization_agent.process({"analysis": analysis, "timeline": timeline})
    
    def _summarize_results(self, search_result: Dict[str, Any], analysis_result: Dict[str, Any], organization_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        汇总结果
        
        参数:
            search_result: 搜索结果
            analysis_result: 分析结果
            organization_result: 整理结果
            
        返回:
            Dict[str, Any]: 汇总结果
        """
        return {
            "status": "success",
            "search_results": search_result.get("results", []),
            "analysis": analysis_result.get("analysis"),
            "timeline": analysis_result.get("timeline", []),
            "organized_info": organization_result.get("organized_info"),
            "presentation": organization_result.get("presentation"),
            "agents": {
                "search_agent": self.search_agent.get_info(),
                "analysis_agent": self.analysis_agent.get_info(),
                "organization_agent": self.organization_agent.get_info()
            }
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        获取所有Agent的状态
        
        返回:
            Dict[str, Any]: Agent状态
        """
        return {
            "search_agent": self.search_agent.get_info(),
            "analysis_agent": self.analysis_agent.get_info(),
            "organization_agent": self.organization_agent.get_info()
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        健康检查
        
        返回:
            Dict[str, Any]: 健康检查结果
        """
        return {
            "search_agent": self.search_agent.health_check(),
            "analysis_agent": self.analysis_agent.health_check(),
            "organization_agent": self.organization_agent.health_check(),
            "all_healthy": all([
                self.search_agent.health_check(),
                self.analysis_agent.health_check(),
                self.organization_agent.health_check()
            ])
        }
