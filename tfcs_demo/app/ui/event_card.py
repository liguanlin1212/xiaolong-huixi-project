import streamlit as st

class EventCard:
    def __init__(self):
        pass
    
    def display(self, event, card_id):
        """显示事件卡片"""
        with st.container():
            # 卡片样式
            st.markdown("""
            <style>
            .event-card {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
                margin: 8px 0;
                background-color: #ffffff;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .event-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }
            .event-title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 8px;
                color: #333333;
            }
            .event-meta {
                font-size: 14px;
                color: #666666;
                margin-bottom: 8px;
            }
            .event-description {
                font-size: 14px;
                color: #444444;
                margin-bottom: 12px;
                line-height: 1.4;
            }
            .event-status {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            .status-closed {
                background-color: #e6f7ee;
                color: #08974b;
            }
            .status-open {
                background-color: #fff2e8;
                color: #fa8c16;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # 卡片内容
            st.markdown(f"""
            <div class="event-card">
                <div class="event-title">{event.get('title', '未命名事件')}</div>
                <div class="event-meta">{event.get('time_range', '时间未知')}</div>
                <div class="event-description">{event.get('description', '无描述')}</div>
                <div class="event-status status-closed">已结案</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 点击事件
            if st.button("查看详情", key=f"detail_{card_id}"):
                self.show_details(event)
    
    def show_details(self, event):
        """显示事件详情"""
        st.subheader(event.get('title', '未命名事件'))
        st.write(f"**时间范围：** {event.get('time_range', '时间未知')}")
        st.write(f"**描述：** {event.get('description', '无描述')}")
        st.write(f"**结案状态：** {event.get('case_status', '未知')}")
        
        if 'judgment_evolution' in event:
            st.write("**判断演变过程：**")
            for i, evolution in enumerate(event['judgment_evolution']):
                st.write(f"{i+1}. {evolution}")
        
        if 'evidence' in event:
            st.write("**证据：**")
            for i, evidence in enumerate(event['evidence']):
                st.write(f"{i+1}. {evidence}")
        
        if 'final_conclusion' in event:
            st.write("**最终结论：**")
            st.write(event['final_conclusion'])
        
        if 'sources' in event:
            st.write("**信息来源：**")
            for i, source in enumerate(event['sources']):
                st.write(f"{i+1}. {source}")