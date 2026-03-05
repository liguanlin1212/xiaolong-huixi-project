import streamlit as st

class FalseClaimsView:
    def __init__(self):
        # 初始化状态
        if 'selected_claim' not in st.session_state:
            st.session_state.selected_claim = None
    
    def display(self):
        """
        显示过去30天被证明是错的说法
        """
        # 页面标题
        st.markdown("""
        <div style='text-align: center; margin-bottom: 40px; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h1 style='color: #2c3e50; margin-bottom: 10px;'>过去30天被证明是错的说法</h1>
            <p style='color: #7f8c8d; font-size: 1.1em;'>追踪并展示近期被证伪的说法及其影响</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 应用样式
        st.markdown("""
        <style>
        .claim-card {
            background-color: #fff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 4px solid #e74c3c;
            margin-bottom: 20px;
        }
        .claim-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .claim-card h3 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        .claim-card p {
            color: #555;
            margin-bottom: 15px;
        }
        .claim-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9em;
            color: #7f8c8d;
            margin-bottom: 15px;
        }
        .impact-section {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
        }
        .impact-item {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }
        .impact-label {
            width: 100px;
            font-weight: bold;
            color: #555;
        }
        .impact-bar {
            flex: 1;
            height: 8px;
            background-color: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin: 0 10px;
        }
        .impact-fill {
            height: 100%;
            background-color: #e74c3c;
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        .impact-value {
            width: 50px;
            text-align: right;
            color: #7f8c8d;
        }
        .evidence-section {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
        }
        .evidence-item {
            background-color: #f9f9f9;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 8px;
            border-left: 3px solid #3498db;
        }
        .evidence-item h4 {
            color: #2c3e50;
            margin-bottom: 5px;
            font-size: 1em;
        }
        .evidence-item p {
            color: #555;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        .evidence-meta {
            font-size: 0.85em;
            color: #7f8c8d;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .status-corrected {
            background-color: #d4edda;
            color: #155724;
        }
        .status-investigating {
            background-color: #fff3cd;
            color: #856404;
        }
        .status-confirmed {
            background-color: #f8d7da;
            color: #721c24;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 模拟错误说法数据
        false_claims_data = [
            {
                "id": 1,
                "claim": "刘鑫在案发时没有锁门",
                "date_made": "2023-05-20",
                "date_falsified": "2023-06-05",
                "source": "刘鑫个人声明",
                "impact": {
                    "media_coverage": 0.8,
                    "public_belief": 0.6,
                    "social_discussion": 0.9
                },
                "evidence": [
                    {
                        "id": 1,
                        "title": "法院判决书",
                        "content": "二审法院认定刘鑫在案发时未采取有效措施救助江歌，间接导致其死亡。",
                        "source": "山东省青岛市中级人民法院",
                        "date": "2023-06-15"
                    },
                    {
                        "id": 2,
                        "title": "证人证言",
                        "content": "邻居证词显示案发时听到江歌的呼救声和门铃声，但刘鑫未及时开门。",
                        "source": "东京地方裁判所庭审记录",
                        "date": "2017-12-18"
                    }
                ],
                "status": "corrected"
            },
            {
                "id": 2,
                "claim": "陈世峰是正当防卫",
                "date_made": "2023-05-10",
                "date_falsified": "2023-06-10",
                "source": "陈世峰辩护律师",
                "impact": {
                    "media_coverage": 0.7,
                    "public_belief": 0.3,
                    "social_discussion": 0.8
                },
                "evidence": [
                    {
                        "id": 1,
                        "title": "法院判决书",
                        "content": "法院认定陈世峰的行为构成故意杀人罪，不属于正当防卫。",
                        "source": "东京地方裁判所",
                        "date": "2017-12-20"
                    },
                    {
                        "id": 2,
                        "title": "法医鉴定",
                        "content": "江歌身上多处刺伤，其中致命伤位于颈部，不符合正当防卫的特征。",
                        "source": "东京警视厅法医报告",
                        "date": "2016-11-10"
                    }
                ],
                "status": "corrected"
            },
            {
                "id": 3,
                "claim": "江歌母亲炒作案件",
                "date_made": "2023-06-01",
                "date_falsified": "2023-06-15",
                "source": "网络言论",
                "impact": {
                    "media_coverage": 0.6,
                    "public_belief": 0.4,
                    "social_discussion": 0.9
                },
                "evidence": [
                    {
                        "id": 1,
                        "title": "法院判决",
                        "content": "法院判决支持江秋莲的诉讼请求，表明其诉求具有法律依据。",
                        "source": "山东省青岛市中级人民法院",
                        "date": "2023-06-15"
                    },
                    {
                        "id": 2,
                        "title": "媒体报道",
                        "content": "多家媒体报道江秋莲为案件奔波多年，始终坚持寻求真相。",
                        "source": "人民日报",
                        "date": "2023-06-16"
                    }
                ],
                "status": "corrected"
            }
        ]
        
        # 错误说法列表
        st.markdown("## 错误说法列表")
        
        for claim in false_claims_data:
            # 状态标签
            status_map = {
                "corrected": "已修正",
                "investigating": "调查中",
                "confirmed": "已确认"
            }
            status_class = f"status-{claim['status']}"
            
            # 显示错误说法卡片
            st.markdown(f"""
            <div class='claim-card'>
                <div class='claim-meta'>
                    <span>发布日期: {claim['date_made']}</span>
                    <span>证伪日期: {claim['date_falsified']}</span>
                    <span class='status-badge {status_class}'>{status_map[claim['status']]}</span>
                </div>
                <h3>{claim['claim']}</h3>
                <p>来源: {claim['source']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 影响范围展示
            st.markdown("### 影响范围")
            st.markdown(f"""
            <div class='impact-section'>
                <div class='impact-item'>
                    <span class='impact-label'>媒体报道</span>
                    <div class='impact-bar'>
                        <div class='impact-fill' style='width: {claim['impact']['media_coverage'] * 100}%'></div>
                    </div>
                    <span class='impact-value'>{int(claim['impact']['media_coverage'] * 100)}%</span>
                </div>
                <div class='impact-item'>
                    <span class='impact-label'>公众相信</span>
                    <div class='impact-bar'>
                        <div class='impact-fill' style='width: {claim['impact']['public_belief'] * 100}%'></div>
                    </div>
                    <span class='impact-value'>{int(claim['impact']['public_belief'] * 100)}%</span>
                </div>
                <div class='impact-item'>
                    <span class='impact-label'>社会讨论</span>
                    <div class='impact-bar'>
                        <div class='impact-fill' style='width: {claim['impact']['social_discussion'] * 100}%'></div>
                    </div>
                    <span class='impact-value'>{int(claim['impact']['social_discussion'] * 100)}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 修正依据展示
            st.markdown("### 修正依据")
            st.markdown("""
            <div class='evidence-section'>
            """, unsafe_allow_html=True)
            
            for evidence in claim['evidence']:
                st.markdown(f"""
                <div class='evidence-item'>
                    <h4>{evidence['title']}</h4>
                    <p>{evidence['content']}</p>
                    <div class='evidence-meta'>
                        <span>来源: {evidence['source']} | 日期: {evidence['date']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
        
        # 统计信息
        st.markdown("## 统计信息")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总错误说法", len(false_claims_data))
        with col2:
            st.metric("已修正", sum(1 for claim in false_claims_data if claim['status'] == 'corrected'))
        with col3:
            st.metric("平均影响范围", f"{sum(claim['impact']['social_discussion'] for claim in false_claims_data) / len(false_claims_data):.2f}")
