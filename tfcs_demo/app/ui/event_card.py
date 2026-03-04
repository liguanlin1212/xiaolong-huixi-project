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
                border-radius: 12px;
                padding: 20px;
                margin: 12px 0;
                background-color: #ffffff;
                box-shadow: 0 4px 6px rgba(0,0,0,0.08);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                opacity: 1;
                transform: translateY(0);
                cursor: pointer;
            }
            .event-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.12);
                border-color: #1890ff;
            }
            .event-card:hover .event-title {
                color: #1890ff;
            }
            .event-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 4px;
                height: 100%;
                background-color: #1890ff;
                border-radius: 12px 0 0 12px;
                transition: all 0.3s ease;
            }
            .event-card:hover::before {
                width: 8px;
            }
            .event-card.loading {
                opacity: 0.7;
                animation: pulse 1.5s ease-in-out infinite;
            }
            .event-card.refreshing {
                animation: slideIn 0.5s ease-out;
            }
            @keyframes pulse {
                0% {
                    box-shadow: 0 4px 6px rgba(0,0,0,0.08);
                }
                50% {
                    box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
                }
                100% {
                    box-shadow: 0 4px 6px rgba(0,0,0,0.08);
                }
            }
            @keyframes slideIn {
                0% {
                    opacity: 0;
                    transform: translateY(20px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .event-title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #333333;
                line-height: 1.3;
                transition: color 0.3s ease;
            }
            .event-meta {
                font-size: 14px;
                color: #666666;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                gap: 16px;
            }
            .event-meta-item {
                display: flex;
                align-items: center;
                gap: 4px;
            }
            .event-description {
                font-size: 14px;
                color: #444444;
                margin-bottom: 16px;
                line-height: 1.5;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                text-overflow: ellipsis;
                transition: all 0.3s ease;
            }
            .event-card:hover .event-description {
                -webkit-line-clamp: 3;
            }
            .event-status {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                margin-right: 10px;
                transition: all 0.3s ease;
            }
            .status-closed {
                background-color: #e6f7ee;
                color: #08974b;
            }
            .status-open {
                background-color: #fff2e8;
                color: #fa8c16;
            }
            .event-domain {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 11px;
                background-color: #f0f0f0;
                color: #666666;
                transition: all 0.3s ease;
            }
            .event-card:hover .event-domain {
                background-color: #e6f7ff;
                color: #1890ff;
            }
            .event-card-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 16px;
                padding-top: 12px;
                border-top: 1px solid #f0f0f0;
                transition: all 0.3s ease;
            }
            .event-card:hover .event-card-footer {
                border-top-color: #e6f7ff;
            }
            .event-stats {
                font-size: 12px;
                color: #999999;
                transition: color 0.3s ease;
            }
            .event-card:hover .event-stats {
                color: #666666;
            }
            .event-button {
                transition: all 0.2s ease;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                background-color: #1890ff;
                color: white;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
            }
            .event-button:hover {
                transform: scale(1.05);
                background-color: #40a9ff;
                box-shadow: 0 2px 8px rgba(24, 144, 255, 0.3);
            }
            .event-button:active {
                transform: scale(0.98);
            }
            .loading-spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 2px solid #f3f3f3;
                border-top: 2px solid #1890ff;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 8px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            </style>
            """
            , unsafe_allow_html=True)
            
            # 卡片内容
            status_class = "status-closed" if event.get('case_status', '已结案') == '已结案' else "status-open"
            status_text = event.get('case_status', '已结案')
            
            # 构建卡片内容
            domain_html = ''
            if 'domain' in event:
                domain_html = f'''
                    <div class="event-meta-item">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zm-1-9h2v3H7V5z" fill="#666666"/>
                        </svg>
                        <span>{event.get('domain', '未分类')}</span>
                    </div>
                '''
            
            domain_badge = ''
            if 'domain' in event:
                domain_badge = f'<span class="event-domain">{event.get("domain", "未分类")}</span>'
            
            # 检查事件是否有加载或刷新状态
            card_class = "event-card"
            if event.get('loading', False):
                card_class += " loading"
            if event.get('refreshing', False):
                card_class += " refreshing"
            
            card_html = f'''
            <div class="{card_class}">
                <div class="event-title">{event.get('title', '未命名事件')}</div>
                <div class="event-meta">
                    <div class="event-meta-item">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm.5 13H7v-4H5V6h2V3h1v3h2v3h-2v4z" fill="#666666"/>
                        </svg>
                        <span>{event.get('time_range', '时间未知')}</span>
                    </div>
                    {domain_html}
                </div>
                <div class="event-description">{event.get('description', '无描述')}</div>
                <div class="event-card-footer">
                    <div>
                        <span class="event-status {status_class}">{status_text}</span>
                        {domain_badge}
                    </div>
                    <div class="event-stats">
                        {len(event.get('judgment_evolution', []))} 次判断演变
                    </div>
                </div>
            </div>
            '''
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # 点击事件
            if st.button("查看详情", key=f"detail_{card_id}", use_container_width=True):
                self.show_details(event)
    
    def show_details(self, event):
        """显示事件详情"""
        # 详情页面样式
        st.markdown("""
        <style>
        .detail-container {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            animation: fadeIn 0.5s ease-out;
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
        .detail-title {
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid #1890ff;
        }
        .detail-section {
            margin-bottom: 20px;
            padding: 16px;
            background-color: #f9f9f9;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .detail-section:hover {
            background-color: #f0f8ff;
            box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1);
        }
        .detail-section-title {
            font-size: 18px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .detail-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 20px;
            font-size: 14px;
            color: #666666;
        }
        .detail-meta-item {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .detail-content {
            line-height: 1.6;
            color: #444444;
        }
        .evolution-item {
            margin-bottom: 8px;
            padding-left: 20px;
            position: relative;
        }
        .evolution-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 8px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #1890ff;
        }
        .evidence-item {
            margin-bottom: 8px;
            padding-left: 20px;
            position: relative;
        }
        .evidence-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 8px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #08974b;
        }
        .source-item {
            margin-bottom: 8px;
            padding-left: 20px;
            position: relative;
        }
        .source-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 8px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #fa8c16;
        }
        .status-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
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
        .domain-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            background-color: #f0f0f0;
            color: #666666;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 详情页面内容
        status_class = "status-closed" if event.get('case_status', '已结案') == '已结案' else "status-open"
        status_text = event.get('case_status', '已结案')
        
        # 构建详情页面内容
        domain_meta_html = ''
        if 'domain' in event:
            domain_meta_html = f'''
                <div class="detail-meta-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zm-1-9h2v3H7V5z" fill="#666666"/>
                    </svg>
                    <span>{event.get('domain', '未分类')}</span>
                </div>
            '''
        
        domain_badge_html = ''
        if 'domain' in event:
            domain_badge_html = f'''
                <div class="detail-meta-item">
                    <span class="domain-badge">{event.get("domain", "未分类")}</span>
                </div>
            '''
        
        judgment_evolution_html = ''
        if 'judgment_evolution' in event and event['judgment_evolution']:
            evolution_items = ''.join([f'<div class="evolution-item">{i+1}. {evolution}</div>' for i, evolution in enumerate(event['judgment_evolution'])])
            judgment_evolution_html = f'''
            <div class="detail-section">
                <div class="detail-section-title">
                    <svg width="18" height="18" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm1.5 11H6.5v-1h3v1zm0-2H6.5V6h3v3z" fill="#333333"/>
                    </svg>
                    判断演变过程
                </div>
                <div class="detail-content">
                    {evolution_items}
                </div>
            </div>
            '''
        
        evidence_html = ''
        if 'evidence' in event and event['evidence']:
            evidence_items = ''.join([f'<div class="evidence-item">{i+1}. {evidence}</div>' for i, evidence in enumerate(event['evidence'])])
            evidence_html = f'''
            <div class="detail-section">
                <div class="detail-section-title">
                    <svg width="18" height="18" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm-1 13h2v-2H7v2zm0-4h2V7H7v2zm0-4h2V3H7v2z" fill="#333333"/>
                    </svg>
                    关键证据
                </div>
                <div class="detail-content">
                    {evidence_items}
                </div>
            </div>
            '''
        
        final_conclusion_html = ''
        if 'final_conclusion' in event:
            final_conclusion_html = f'''
            <div class="detail-section">
                <div class="detail-section-title">
                    <svg width="18" height="18" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm-1 13h2v-2H7v2zm0-4h2V7H7v2zm0-4h2V3H7v2z" fill="#333333"/>
                    </svg>
                    最终结论
                </div>
                <div class="detail-content">{event['final_conclusion']}</div>
            </div>
            '''
        
        sources_html = ''
        if 'sources' in event and event['sources']:
            source_items = ''.join([f'<div class="source-item">{i+1}. {source}</div>' for i, source in enumerate(event['sources'])])
            sources_html = f'''
            <div class="detail-section">
                <div class="detail-section-title">
                    <svg width="18" height="18" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm-1 13h2v-2H7v2zm0-4h2V7H7v2zm0-4h2V3H7v2z" fill="#333333"/>
                    </svg>
                    信息来源
                </div>
                <div class="detail-content">
                    {source_items}
                </div>
            </div>
            '''
        
        detail_html = f'''
        <div class="detail-container">
            <div class="detail-title">{event.get('title', '未命名事件')}</div>
            
            <div class="detail-meta">
                <div class="detail-meta-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm.5 13H7v-4H5V6h2V3h1v3h2v3h-2v4z" fill="#666666"/>
                    </svg>
                    <span>{event.get('time_range', '时间未知')}</span>
                </div>
                {domain_meta_html}
                <div class="detail-meta-item">
                    <span class="status-badge {status_class}">{status_text}</span>
                </div>
                {domain_badge_html}
            </div>
            
            <div class="detail-section">
                <div class="detail-section-title">
                    <svg width="18" height="18" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zm-.5-11h1v3h-1v-3zm0 4h1v5h-1v-5z" fill="#333333"/>
                    </svg>
                    事件描述
                </div>
                <div class="detail-content">{event.get('description', '无描述')}</div>
            </div>
            
            {judgment_evolution_html}
            {evidence_html}
            {final_conclusion_html}
            {sources_html}
        </div>
        '''
        
        st.markdown(detail_html, unsafe_allow_html=True)