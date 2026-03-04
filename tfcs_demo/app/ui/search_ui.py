import streamlit as st
import json
import os

class SearchUI:
    def __init__(self):
        self.search_history_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "search_history.json")
        self.load_search_history()
    
    def load_search_history(self):
        try:
            if os.path.exists(self.search_history_file):
                with open(self.search_history_file, "r", encoding="utf-8") as f:
                    self.search_history = json.load(f)
            else:
                self.search_history = []
        except Exception as e:
            st.error(f"加载搜索历史失败: {e}")
            self.search_history = []
    
    def save_search_history(self):
        try:
            # 保留最近10条搜索记录
            self.search_history = self.search_history[-10:]
            with open(self.search_history_file, "w", encoding="utf-8") as f:
                json.dump(self.search_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            st.error(f"保存搜索历史失败: {e}")
    
    def add_search_history(self, query):
        if query and query not in self.search_history:
            self.search_history.append(query)
            self.save_search_history()
    
    def display(self):
        st.title("全网搜索事件")
        
        # 响应式布局 - 使用列布局
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # 搜索输入框
            search_query = st.text_input("输入事件关键词", placeholder="例如：COVID-19 起源")
        
        # 搜索历史 - 响应式显示
        if self.search_history:
            st.subheader("搜索历史")
            # 使用网格布局显示历史记录
            history_cols = st.columns(2)  # 两列布局
            for i, history in enumerate(self.search_history[::-1]):
                with history_cols[i % 2]:
                    if st.button(f"{history}", key=f"history_{i}", use_container_width=True):
                        search_query = history
        
        # 搜索按钮 - 响应式大小
        search_button = st.button("搜索", use_container_width=True)
        
        # 搜索按钮逻辑
        if search_button and search_query:
            self.add_search_history(search_query)
            return search_query
        
        # 响应式布局提示
        st.markdown("""\n\n\n**提示：** 本搜索功能使用大模型进行全网信息检索，可能需要一些时间来获取和分析结果。""")
        
        return None
    
    def display_results(self, results):
        if not results:
            st.info("未找到相关结果")
            return
        
        st.subheader("搜索结果")
        
        # 筛选和排序功能
        with st.sidebar:
            st.subheader("筛选选项")
            
            # 按结案状态筛选
            case_status_options = ['全部'] + list(set([result.get('case_status', '未知') for result in results]))
            selected_status = st.selectbox("结案状态", case_status_options)
            
            # 按时间范围筛选
            time_range_options = ['全部'] + list(set([result.get('time_range', '未知') for result in results]))
            selected_time_range = st.selectbox("时间范围", time_range_options)
            
            # 按领域筛选
            domain_options = ['全部']
            # 尝试从结果中提取领域信息
            for result in results:
                if 'domain' in result and result['domain'] not in domain_options:
                    domain_options.append(result['domain'])
            selected_domain = st.selectbox("领域", domain_options)
            
            # 排序功能
            st.subheader("排序选项")
            sort_options = [
                "默认",
                "按时间（最新）",
                "按时间（最早）"
            ]
            selected_sort = st.selectbox("排序方式", sort_options)
        
        # 应用筛选
        filtered_results = results
        if selected_status != '全部':
            filtered_results = [r for r in filtered_results if r.get('case_status') == selected_status]
        if selected_time_range != '全部':
            filtered_results = [r for r in filtered_results if r.get('time_range') == selected_time_range]
        if selected_domain != '全部':
            filtered_results = [r for r in filtered_results if r.get('domain') == selected_domain]
        
        # 应用排序
        if selected_sort == "按时间（最新）":
            # 尝试按时间范围排序（简单实现）
            def get_year(time_range):
                try:
                    if '年' in time_range:
                        return int(time_range.split('年')[0])
                except:
                    return 0
                return 0
            filtered_results.sort(key=lambda x: get_year(x.get('time_range', '未知')), reverse=True)
        elif selected_sort == "按时间（最早）":
            def get_year(time_range):
                try:
                    if '年' in time_range:
                        return int(time_range.split('年')[0])
                except:
                    return 9999
                return 9999
            filtered_results.sort(key=lambda x: get_year(x.get('time_range', '未知')))
        
        # 显示筛选结果
        if not filtered_results:
            st.info("没有符合筛选条件的结果")
            return
        
        st.write(f"找到 {len(filtered_results)} 个结果")
        
        # 改进结果卡片设计
        for i, result in enumerate(filtered_results):
            with st.expander(f"{result.get('title', f'结果 {i+1}')}"):
                # 使用列布局改善信息展示
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**描述：** {result.get('description', '无描述')}")
                    st.write(f"**时间范围：** {result.get('time_range', '未知')}")
                    st.write(f"**结案状态：** {result.get('case_status', '未知')}")
                    
                    if 'domain' in result:
                        st.write(f"**领域：** {result.get('domain', '未知')}")
                
                with col2:
                    if 'judgment_evolution' in result:
                        st.write("**判断演变过程：**")
                        for j, evolution in enumerate(result['judgment_evolution']):
                            st.write(f"{j+1}. {evolution}")
                    
                    if 'evidence' in result:
                        st.write("**证据：**")
                        for j, evidence in enumerate(result['evidence']):
                            st.write(f"{j+1}. {evidence}")