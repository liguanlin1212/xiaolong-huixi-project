import streamlit as st

class TimelineView:
    def __init__(self):
        # 初始化状态
        if 'selected_timeline_item' not in st.session_state:
            st.session_state.selected_timeline_item = None
        if 'timeline_zoom' not in st.session_state:
            st.session_state.timeline_zoom = 1.0
    
    def display(self, timeline_data: list, title="判断演化时间轴"):
        """
        显示现代化的时间轴
        输入：时间轴数据列表，标题
        """
        if not timeline_data:
            st.info("暂无时间轴数据")
            return
        
        # 时间范围过滤
        time_range = st.session_state.get('time_range', '全部')
        filtered_data = timeline_data
        
        # 这里可以根据实际时间格式实现过滤逻辑
        # 暂时使用全部数据，实际应用中需要根据时间字段进行过滤
        if time_range != '全部':
            # 示例：根据时间字符串进行简单过滤
            # 实际应用中需要根据具体的时间格式和数据结构进行调整
            pass
        
        # 时间轴样式
        st.markdown("""
        <style>
        .timeline-container {
            position: relative;
            padding: 20px 0;
            transform-origin: top left;
            transition: transform 0.3s ease;
            animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .timeline-line {
            position: absolute;
            left: 20px;
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: #1890ff;
            animation: drawLine 1.5s ease-out forwards;
            transform-origin: top;
            transform: scaleY(0);
        }
        @keyframes drawLine {
            0% {
                transform: scaleY(0);
            }
            100% {
                transform: scaleY(1);
            }
        }
        .timeline-item {
            position: relative;
            margin-bottom: 30px;
            padding-left: 60px;
            cursor: pointer;
            opacity: 0;
            animation: slideIn 0.6s ease-out forwards;
        }
        .timeline-item:nth-child(1) { animation-delay: 0.2s; }
        .timeline-item:nth-child(2) { animation-delay: 0.4s; }
        .timeline-item:nth-child(3) { animation-delay: 0.6s; }
        .timeline-item:nth-child(4) { animation-delay: 0.8s; }
        .timeline-item:nth-child(5) { animation-delay: 1.0s; }
        .timeline-item:nth-child(6) { animation-delay: 1.2s; }
        .timeline-item:nth-child(7) { animation-delay: 1.4s; }
        .timeline-item:nth-child(8) { animation-delay: 1.6s; }
        .timeline-item:nth-child(9) { animation-delay: 1.8s; }
        .timeline-item:nth-child(10) { animation-delay: 2.0s; }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        .timeline-item:hover {
            transform: translateX(5px);
            transition: transform 0.3s ease;
        }
        .timeline-item.selected {
            transform: translateX(10px);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(24, 144, 255, 0.4);
            }
            70% {
                box-shadow: 0 0 0 10px rgba(24, 144, 255, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(24, 144, 255, 0);
            }
        }
        .timeline-node {
            position: absolute;
            left: 11px;
            top: 5px;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background-color: #1890ff;
            border: 4px solid #e6f7ff;
            z-index: 1;
            transition: all 0.3s ease;
            animation: bounce 0.6s ease-out;
        }
        @keyframes bounce {
            0% {
                transform: scale(0);
            }
            50% {
                transform: scale(1.3);
            }
            100% {
                transform: scale(1);
            }
        }
        .timeline-item:hover .timeline-node {
            transform: scale(1.2);
            box-shadow: 0 0 0 8px rgba(24, 144, 255, 0.1);
        }
        .timeline-item.selected .timeline-node {
            transform: scale(1.3);
            box-shadow: 0 0 0 10px rgba(24, 144, 255, 0.2);
            background-color: #096dd9;
            animation: pulseNode 2s infinite;
        }
        @keyframes pulseNode {
            0% {
                box-shadow: 0 0 0 0 rgba(9, 109, 217, 0.4);
            }
            70% {
                box-shadow: 0 0 0 10px rgba(9, 109, 217, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(9, 109, 217, 0);
            }
        }
        .timeline-time {
            font-size: 14px;
            font-weight: bold;
            color: #1890ff;
            margin-bottom: 5px;
        }
        .timeline-content {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        .timeline-item:hover .timeline-content {
            box-shadow: 0 4px 8px rgba(0,0,0,0.12);
            border-color: #1890ff;
            transform: translateY(-2px);
        }
        .timeline-item.selected .timeline-content {
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            border-color: #096dd9;
            background-color: #f0f8ff;
        }
        .timeline-text {
            font-size: 14px;
            color: #444444;
            margin-bottom: 8px;
            line-height: 1.4;
        }
        .timeline-narrative {
            font-size: 12px;
            font-weight: bold;
            color: #666666;
            margin-bottom: 4px;
        }
        .timeline-confidence {
            font-size: 11px;
            color: #999999;
        }
        .timeline-title {
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #1890ff;
            animation: slideInFromLeft 0.8s ease-out;
        }
        @keyframes slideInFromLeft {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        .timeline-controls {
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
            align-items: center;
            animation: slideInFromLeft 0.8s ease-out 0.2s both;
        }
        .timeline-detail {
            margin-top: 20px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #1890ff;
            animation: fadeInUp 0.6s ease-out;
        }
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .timeline-detail-title {
            font-size: 16px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        }
        @media (max-width: 768px) {
            .timeline-item {
                padding-left: 50px;
            }
            .timeline-line {
                left: 15px;
            }
            .timeline-node {
                left: 6px;
                width: 16px;
                height: 16px;
                border-width: 3px;
            }
            .timeline-controls {
                flex-direction: column;
                align-items: flex-start;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 时间轴标题
        st.markdown(f"<div class='timeline-title'>{title}</div>", unsafe_allow_html=True)
        
        # 时间轴控制
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write("时间轴控制")
        with col2:
            # 时间范围过滤
            time_range = st.selectbox("时间范围", ["全部", "最近24小时", "最近7天", "最近30天"], key="time_range")
        with col3:
            zoom_level = st.slider("缩放级别", min_value=0.5, max_value=1.5, value=st.session_state.timeline_zoom, step=0.1, key="timeline_zoom")
            st.session_state.timeline_zoom = zoom_level
        
        # 自动播放控制
        col4, col5 = st.columns([2, 1])
        with col4:
            auto_play = st.checkbox("自动播放", key="auto_play")
        with col5:
            play_speed = st.slider("播放速度", min_value=0.5, max_value=3.0, value=1.0, step=0.5, key="play_speed")
        
        # 时间轴容器
        timeline_html = f"""
        <div class='timeline-container' id='timeline-container' style='transform: scale({st.session_state.timeline_zoom});'>
            <div class='timeline-line'></div>
        """
        
        for i, entry in enumerate(filtered_data):
            time = entry.get("time", "未知时间")
            text = entry.get("text", "无文本")
            narrative = entry.get("narrative", {}).value if hasattr(entry.get("narrative"), "value") else str(entry.get("narrative"))
            confidence = entry.get("confidence", 0)
            
            # 检查是否为选中项
            selected_class = " selected" if st.session_state.selected_timeline_item == i else ""
            
            timeline_html += f"""
            <div class='timeline-item{selected_class}' id='timeline-item-{i}'>
                <div class='timeline-node'></div>
                <div class='timeline-time'>{time}</div>
                <div class='timeline-content'>
                    <div class='timeline-text'>{text}</div>
                    <div class='timeline-narrative'>叙事类型: {narrative}</div>
                    <div class='timeline-confidence'>置信度: {confidence:.2f}</div>
                </div>
            </div>
            """
        
        timeline_html += "</div>"
        
        # 添加JavaScript代码实现缩放和交互功能
        timeline_html += """
        <script>
        function updateTimelineZoom(zoom) {
            const timeline = document.getElementById('timeline-container');
            if (timeline) {
                timeline.style.transform = `scale(${zoom})`;
            }
        }

        // 为时间轴项目添加点击事件
        document.addEventListener('DOMContentLoaded', function() {
            const timelineItems = document.querySelectorAll('.timeline-item');
            timelineItems.forEach((item, index) => {
                item.addEventListener('click', function() {
                    // 移除所有选中状态
                    timelineItems.forEach(i => i.classList.remove('selected'));
                    // 添加选中状态
                    this.classList.add('selected');
                    // 触发对应的Streamlit按钮点击
                    const button = document.querySelector(`[data-testid="stButton-${index}"] button`);
                    if (button) {
                        button.click();
                    }
                });
            });

            // 自动播放功能
            let autoplayInterval;
            const autoPlayCheckbox = document.querySelector('input[data-testid="stCheckbox-auto_play"]');
            const playSpeedSlider = document.querySelector('input[data-testid="stSlider-play_speed"]');

            function startAutoPlay() {
                let currentIndex = 0;
                autoplayInterval = setInterval(() => {
                    if (currentIndex < timelineItems.length) {
                        timelineItems.forEach(i => i.classList.remove('selected'));
                        timelineItems[currentIndex].classList.add('selected');
                        // 触发对应的Streamlit按钮点击
                        const button = document.querySelector(`[data-testid="stButton-${currentIndex}"] button`);
                        if (button) {
                            button.click();
                        }
                        // 滚动到当前项目
                        timelineItems[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
                        currentIndex++;
                    } else {
                        currentIndex = 0;
                    }
                }, 2000 / parseFloat(playSpeedSlider ? playSpeedSlider.value : 1));
            }

            function stopAutoPlay() {
                if (autoplayInterval) {
                    clearInterval(autoplayInterval);
                }
            }

            // 监听自动播放选项变化
            if (autoPlayCheckbox) {
                autoPlayCheckbox.addEventListener('change', function() {
                    if (this.checked) {
                        startAutoPlay();
                    } else {
                        stopAutoPlay();
                    }
                });
            }

            // 监听播放速度变化
            if (playSpeedSlider) {
                playSpeedSlider.addEventListener('input', function() {
                    if (autoPlayCheckbox && autoPlayCheckbox.checked) {
                        stopAutoPlay();
                        startAutoPlay();
                    }
                });
            }
        });
        </script>
        """
        
        st.markdown(timeline_html, unsafe_allow_html=True)
        
        # 时间点选择
        st.write("点击时间点查看详情:")
        for i, entry in enumerate(filtered_data):
            time = entry.get("time", "未知时间")
            text = entry.get("text", "无文本")[:50] + "..." if len(entry.get("text", "")) > 50 else entry.get("text", "无文本")
            
            if st.button(f"{time}: {text}", key=f"timeline_button_{i}"):
                st.session_state.selected_timeline_item = i
        
        # 显示选中项详情
        if st.session_state.selected_timeline_item is not None and 0 <= st.session_state.selected_timeline_item < len(filtered_data):
            selected_entry = filtered_data[st.session_state.selected_timeline_item]
            st.markdown("""
            <div class='timeline-detail'>
                <div class='timeline-detail-title'>时间点详情</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.write(f"**时间**: {selected_entry.get('time', '未知时间')}")
            st.write(f"**文本**: {selected_entry.get('text', '无文本')}")
            narrative = selected_entry.get("narrative", {}).value if hasattr(selected_entry.get("narrative"), "value") else str(selected_entry.get("narrative"))
            st.write(f"**叙事类型**: {narrative}")
            st.write(f"**置信度**: {selected_entry.get('confidence', 0):.2f}")