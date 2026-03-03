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
        
        # 搜索输入框
        search_query = st.text_input("输入事件关键词", placeholder="例如：COVID-19 起源")
        
        # 搜索历史
        if self.search_history:
            st.subheader("搜索历史")
            for i, history in enumerate(self.search_history[::-1]):
                if st.button(f"{history}", key=f"history_{i}"):
                    search_query = history
        
        # 搜索按钮
        if st.button("搜索") and search_query:
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
        
        for i, result in enumerate(results):
            with st.expander(f"{result.get('title', f'结果 {i+1}')}"):
                st.write(f"**描述：** {result.get('description', '无描述')}")
                st.write(f"**时间范围：** {result.get('time_range', '未知')}")
                st.write(f"**结案状态：** {result.get('case_status', '未知')}")
                
                if 'judgment_evolution' in result:
                    st.write("**判断演变过程：**")
                    for j, evolution in enumerate(result['judgment_evolution']):
                        st.write(f"{j+1}. {evolution}")
                
                if 'evidence' in result:
                    st.write("**证据：**")
                    for j, evidence in enumerate(result['evidence']):
                        st.write(f"{j+1}. {evidence}")