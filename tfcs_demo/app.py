import streamlit as st
import time
from app.ui.search_ui import SearchUI
from app.ui.explore_ui import ExploreUI
from search.search_handler import SearchHandler
from search.search_prompt import SearchPromptBuilder
from search.search_analyzer import SearchAnalyzer
from search.case_status import CaseStatusChecker
from search.case_status_machine import CaseStatusMachine
from search.version_manager import VersionManager
from search.version_storage import VersionStorage
from search.version_history import VersionHistory
from search.self_correction import SelfCorrectionMechanism
from search.discomfort_trigger import DiscomfortTrigger
from ai.inference.model_factory import ModelFactory

class MainApp:
    def __init__(self):
        # 搜索功能组件
        self.search_ui = SearchUI()
        self.search_handler = SearchHandler()
        self.prompt_builder = SearchPromptBuilder()
        self.search_analyzer = SearchAnalyzer()
        self.case_status_checker = CaseStatusChecker()
        self.model_factory = ModelFactory()
        self.ai_model = self.model_factory.create_runner("OPENAI")
        
        # 结案状态判断机制
        self.case_status_machine = CaseStatusMachine()
        
        # 版本控制系统
        self.version_manager = VersionManager()
        self.version_storage = VersionStorage()
        self.version_history = VersionHistory(self.version_manager)
        # 加载已保存的版本
        self.version_storage.load_versions(self.version_manager)
        
        # 自查纠错机制
        self.self_correction = SelfCorrectionMechanism(self.version_manager, self.version_history, self.case_status_machine)
        
        # 不适感触发机制
        self.discomfort_trigger = DiscomfortTrigger(self.version_manager, self.version_history, self.case_status_machine, self.self_correction)
        
        # 探索功能组件
        self.explore_ui = ExploreUI()
    
    def run(self):
        st.set_page_config(
            page_title="事实校正系统",
            page_icon="🔍",
            layout="wide"
        )
        
        # 导航菜单
        tab1, tab2, tab3, tab4 = st.tabs(["全网搜索", "事件探索", "自查纠错", "不适感反馈"])
        
        with tab1:
            # 显示搜索界面
            search_query = self.search_ui.display()
            
            if search_query:
                # 处理搜索查询
                results, error_msg = self.search_handler.process_query(search_query)
                
                if error_msg:
                    st.error(error_msg)
                else:
                    # 如果没有缓存结果，使用大模型搜索
                    if not results:
                        with st.spinner("正在搜索..."):
                            # 构建搜索指令
                            prompt = self.prompt_builder.build_prompt(search_query)
                            
                            # 调用大模型
                            try:
                                raw_results = self.ai_model.classify_text(prompt)
                                
                                # 分析搜索结果
                                results = self.search_analyzer.analyze_results(raw_results)
                                
                                # 过滤未结案事件并使用状态机管理状态，同时创建判断版本
                                filtered_results = []
                                for i, result in enumerate(results):
                                    event_id = f"search_{i}_{int(time.time())}"
                                    # 获取初始状态
                                    status = self.case_status_machine.get_initial_status(result, event_id)
                                    if status.value == "已结案":
                                        result["case_status"] = status.value
                                        filtered_results.append(result)
                                        
                                        # 创建判断版本
                                        content = f"事件：{result.get('title', '未命名事件')}\n" \
                                                f"时间范围：{result.get('time_range', '未知')}\n" \
                                                f"描述：{result.get('description', '无描述')}\n" \
                                                f"结案状态：{status.value}\n" \
                                                f"最终结论：{result.get('final_conclusion', '无')}"
                                        self.version_manager.create_version(event_id, content)
                                    else:
                                        rejection_message = self.case_status_checker.get_rejection_message(result)
                                        st.warning(rejection_message)
                                
                                # 保存缓存
                                self.search_handler.save_cache_result(search_query, filtered_results)
                                
                                # 显示结果
                                self.search_ui.display_results(filtered_results)
                            except Exception as e:
                                st.error(f"搜索失败: {e}")
                    else:
                        # 显示缓存结果
                        self.search_ui.display_results(results)
        
        with tab2:
            # 显示探索界面
            self.explore_ui.display()
        
        with tab3:
            # 显示自查纠错界面
            st.header("自查纠错机制")
            st.write("输入新信息，系统将自动分析其对现有判断的影响并生成纠错建议")
            
            new_information = st.text_area("输入新信息", height=200)
            
            if st.button("分析影响并纠错"):
                if new_information:
                    with st.spinner("正在分析新信息..."):
                        # 处理自查纠错
                        correction_result = self.self_correction.process_self_correction(new_information)
                        
                        # 显示影响分析结果
                        st.subheader("影响分析结果")
                        if correction_result["impact_results"]:
                            for event_id, affected_versions in correction_result["impact_results"].items():
                                st.write(f"**事件 ID: {event_id}**")
                                for version_info in affected_versions:
                                    st.write(f"- 版本 ID: {version_info['version_id']}")
                                    st.write(f"  受影响方面: {', '.join(version_info['impacted_aspects'])}")
                                    st.write(f"  内容: {version_info['content'][:100]}...")
                        else:
                            st.info("未发现受影响的判断")
                        
                        # 显示纠错建议
                        st.subheader("纠错建议")
                        if correction_result["suggestions"]:
                            for event_id, suggestions in correction_result["suggestions"].items():
                                st.write(f"**事件 ID: {event_id}**")
                                for suggestion_info in suggestions:
                                    st.write(f"- 版本 ID: {suggestion_info['version_id']}")
                                    st.write(f"  置信度: {suggestion_info['confidence']:.2f}")
                                    st.write(f"  建议: {suggestion_info['suggestion'][:200]}...")
                        else:
                            st.info("未生成纠错建议")
                        
                        # 显示纠错结果
                        st.subheader("纠错结果")
                        if correction_result["correction_results"]:
                            for event_id, corrections in correction_result["correction_results"].items():
                                st.write(f"**事件 ID: {event_id}**")
                                for correction in corrections:
                                    st.write(f"- 旧版本 ID: {correction['old_version_id']}")
                                    st.write(f"  新版本 ID: {correction['new_version_id']}")
                                    st.write(f"  置信度: {correction['confidence']:.2f}")
                        else:
                            st.info("未执行自动纠错")
                else:
                    st.error("请输入新信息")
        
        with tab4:
            # 显示不适感反馈界面
            st.header("不适感触发机制")
            st.write("如果您对某个判断感到不适，请提交反馈，系统将重新审视该判断")
            
            # 事件ID和版本ID输入
            event_id = st.text_input("事件 ID")
            version_id = st.text_input("版本 ID")
            
            # 不适程度选择
            discomfort_level = st.slider("不适程度", 1, 5, 3, help="1=轻微不适，5=严重不适")
            
            # 不适原因输入
            reason = st.text_area("不适原因", height=100)
            
            # 附加信息
            additional_info = {}
            additional_info["具体问题"] = st.text_input("具体问题")
            additional_info["建议"] = st.text_input("您的建议")
            
            if st.button("提交反馈"):
                if event_id and version_id and reason:
                    with st.spinner("正在处理反馈..."):
                        # 触发不适感
                        trigger_id = self.discomfort_trigger.trigger_discomfort(
                            event_id, version_id, discomfort_level, reason, additional_info
                        )
                        
                        st.success(f"反馈提交成功！触发ID: {trigger_id}")
                        st.info("系统已开始重新审视该判断")
                else:
                    st.error("请填写事件ID、版本ID和不适原因")
            
            # 显示触发统计信息
            st.subheader("反馈统计")
            trigger_stats = self.discomfort_trigger.get_trigger_stats()
            evaluation_stats = self.discomfort_trigger.get_evaluation_stats()
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("触发统计")
                st.write(f"总触发次数: {trigger_stats['total_triggers']}")
                st.write(f"已解决次数: {trigger_stats['resolved_triggers']}")
                st.write(f"解决率: {trigger_stats['resolution_rate']:.2f}")
            
            with col2:
                st.write("评估统计")
                st.write(f"总评估次数: {evaluation_stats['total_evaluations']}")
                st.write(f"平均效果: {evaluation_stats['average_effectiveness']:.2f}")

if __name__ == "__main__":
    app = MainApp()
    app.run()