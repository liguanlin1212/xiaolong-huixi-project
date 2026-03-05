import streamlit as st

class SnapshotView:
    def __init__(self):
        # 初始化状态
        if 'current_snapshot_date' not in st.session_state:
            st.session_state.current_snapshot_date = '2023-06-15'
        if 'current_evidence_tab' not in st.session_state:
            st.session_state.current_evidence_tab = 'official'
    
    def display(self):
        """
        显示非个性化世界快照
        """
        # 页面标题
        st.markdown("""
        <div style='text-align: center; margin-bottom: 40px; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h1 style='color: #2c3e50; margin-bottom: 10px;'>非个性化世界快照</h1>
            <p style='color: #7f8c8d; font-size: 1.1em;'>还原当时世界如何看待事件的主流判断</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 时间锚点选择区域
        st.markdown("## 时间锚点选择")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            selected_date = st.date_input(
                "选择时间点",
                value=st.session_state.current_snapshot_date,
                key="snapshot_date"
            )
            st.session_state.current_snapshot_date = str(selected_date)
        
        with col2:
            if st.button("加载快照", key="load_snapshot"):
                pass
        
        with col3:
            if st.button("重置", key="reset_snapshot"):
                st.session_state.current_snapshot_date = '2023-06-15'
                st.session_state.current_evidence_tab = 'official'
                st.experimental_rerun()
        
        # 预设日期按钮
        st.markdown("### 关键时间点")
        preset_dates = {
            "案件发生": "2016-11-03",
            "舆论发酵": "2016-11-10",
            "一审判决": "2017-12-20",
            "民事判决": "2022-12-30",
            "二审判决": "2023-06-15"
        }
        
        preset_buttons = st.columns(len(preset_dates))
        for i, (label, date) in enumerate(preset_dates.items()):
            with preset_buttons[i]:
                if st.button(label, key=f"preset_{date}"):
                    st.session_state.current_snapshot_date = date
                    st.experimental_rerun()
        
        # 模拟世界快照数据
        snapshot_data = {
            "2016-11-03": {
                "consensus": [
                    {
                        "id": 1,
                        "title": "江歌在东京寓所外遇害",
                        "summary": "中国留学生江歌在日本东京住所外被杀害，其室友刘鑫幸存。",
                        "strength": 0.95,
                        "sourceCount": 24
                    },
                    {
                        "id": 2,
                        "title": "嫌疑人陈世峰被警方控制",
                        "summary": "警方锁定嫌疑人陈世峰，与刘鑫曾为恋人关系。",
                        "strength": 0.90,
                        "sourceCount": 18
                    }
                ],
                "evidence": {
                    "official": [
                        {
                            "id": 1,
                            "title": "日本警视厅通报",
                            "content": "警方确认江歌因颈部刺伤导致失血过多死亡，已控制嫌疑人陈世峰。",
                            "source": "日本警视厅",
                            "date": "2016-11-04"
                        }
                    ],
                    "media": [
                        {
                            "id": 1,
                            "title": "媒体初步报道",
                            "content": "据日媒报道，案发当晚刘鑫先回到公寓，随后江歌被尾随的陈世峰杀害。",
                            "source": "日本时事通讯社",
                            "date": "2016-11-04"
                        }
                    ],
                    "public": [],
                    "expert": []
                }
            },
            "2016-11-10": {
                "consensus": [
                    {
                        "id": 1,
                        "title": "刘鑫被质疑锁门",
                        "summary": "网络舆论质疑刘鑫在案发时锁门，导致江歌无法进入公寓避险。",
                        "strength": 0.75,
                        "sourceCount": 45
                    },
                    {
                        "id": 2,
                        "title": "陈世峰被指控故意杀人",
                        "summary": "检方以故意杀人罪对陈世峰提起公诉。",
                        "strength": 0.90,
                        "sourceCount": 22
                    }
                ],
                "evidence": {
                    "official": [
                        {
                            "id": 1,
                            "title": "检方起诉书",
                            "content": "检方指控陈世峰携带刀具前往江歌公寓，对江歌实施了故意杀人行为。",
                            "source": "东京地方检察厅",
                            "date": "2016-11-09"
                        }
                    ],
                    "media": [
                        {
                            "id": 1,
                            "title": "江歌母亲采访",
                            "content": "江歌母亲通过媒体表示，刘鑫在案发时可能锁上了公寓门，导致江歌无法逃生。",
                            "source": "中国新闻周刊",
                            "date": "2016-11-08"
                        }
                    ],
                    "public": [
                        {
                            "id": 1,
                            "title": "网络舆论反应",
                            "content": "大量网友在社交媒体上质疑刘鑫的行为，认为她对江歌的死亡负有责任。",
                            "source": "微博热门话题",
                            "date": "2016-11-10"
                        }
                    ],
                    "expert": []
                }
            },
            "2017-12-20": {
                "consensus": [
                    {
                        "id": 1,
                        "title": "陈世峰被判有期徒刑20年",
                        "summary": "东京地方裁判所认定陈世峰故意杀人罪成立，判处有期徒刑20年。",
                        "strength": 0.98,
                        "sourceCount": 67
                    },
                    {
                        "id": 2,
                        "title": "刘鑫证词存在矛盾",
                        "summary": "法院审理过程中发现刘鑫的部分证词存在前后矛盾之处。",
                        "strength": 0.85,
                        "sourceCount": 38
                    }
                ],
                "evidence": {
                    "official": [
                        {
                            "id": 1,
                            "title": "法院判决书",
                            "content": "法院认定陈世峰犯故意杀人罪，考虑到其自首情节但犯罪情节恶劣，判处有期徒刑20年。",
                            "source": "东京地方裁判所",
                            "date": "2017-12-20"
                        }
                    ],
                    "media": [
                        {
                            "id": 1,
                            "title": "庭审报道",
                            "content": "庭审过程中，刘鑫的证词与物证存在多处矛盾，引发公众质疑。",
                            "source": "朝日新闻",
                            "date": "2017-12-18"
                        }
                    ],
                    "public": [
                        {
                            "id": 1,
                            "title": "公众反应",
                            "content": "公众对判决结果基本认可，但对刘鑫的行为仍存在广泛质疑。",
                            "source": "网络舆情分析",
                            "date": "2017-12-21"
                        }
                    ],
                    "expert": [
                        {
                            "id": 1,
                            "title": "法律专家解读",
                            "content": "专家认为判决结果符合日本刑法规定，考虑了案件的具体情节。",
                            "source": "东京大学法学部",
                            "date": "2017-12-22"
                        }
                    ]
                }
            },
            "2022-12-30": {
                "consensus": [
                    {
                        "id": 1,
                        "title": "刘鑫被判赔偿69.6万元",
                        "summary": "青岛市城阳区人民法院判决刘鑫赔偿江秋莲各项损失及精神损害抚慰金共计69.6万元。",
                        "strength": 0.95,
                        "sourceCount": 89
                    },
                    {
                        "id": 2,
                        "title": "刘鑫行为存在过错",
                        "summary": "法院认定刘鑫对江歌的死亡存在过错，应当承担相应的民事赔偿责任。",
                        "strength": 0.90,
                        "sourceCount": 64
                    }
                ],
                "evidence": {
                    "official": [
                        {
                            "id": 1,
                            "title": "民事判决书",
                            "content": "法院认定刘鑫在案发前未将陈世峰的威胁告知江歌，案发时未采取有效措施救助，存在过错。",
                            "source": "青岛市城阳区人民法院",
                            "date": "2022-12-30"
                        }
                    ],
                    "media": [
                        {
                            "id": 1,
                            "title": "判决报道",
                            "content": "法院认为刘鑫的行为与江歌的死亡之间存在因果关系，应当承担民事赔偿责任。",
                            "source": "人民日报",
                            "date": "2022-12-31"
                        }
                    ],
                    "public": [
                        {
                            "id": 1,
                            "title": "公众反应",
                            "content": "多数公众认为判决结果公平合理，体现了法律对正义的维护。",
                            "source": "网络舆情监测",
                            "date": "2023-01-01"
                        }
                    ],
                    "expert": [
                        {
                            "id": 1,
                            "title": "法律专家解读",
                            "content": "专家认为判决结果符合民法关于过错责任的规定，对类似案件具有参考意义。",
                            "source": "中国政法大学",
                            "date": "2023-01-02"
                        }
                    ]
                }
            },
            "2023-06-15": {
                "consensus": [
                    {
                        "id": 1,
                        "title": "二审维持原判",
                        "summary": "山东省青岛市中级人民法院二审维持原判，刘鑫需赔偿江秋莲69.6万元。",
                        "strength": 0.98,
                        "sourceCount": 95
                    },
                    {
                        "id": 2,
                        "title": "刘鑫改名引发争议",
                        "summary": "刘鑫改名为刘暖曦，引发公众对其逃避责任的质疑。",
                        "strength": 0.85,
                        "sourceCount": 56
                    }
                ],
                "evidence": {
                    "official": [
                        {
                            "id": 1,
                            "title": "二审判决书",
                            "content": "二审法院认为一审判决认定事实清楚，适用法律正确，判决驳回上诉，维持原判。",
                            "source": "山东省青岛市中级人民法院",
                            "date": "2023-06-15"
                        }
                    ],
                    "media": [
                        {
                            "id": 1,
                            "title": "二审报道",
                            "content": "二审法院经审理认为，刘鑫的行为确实存在过错，应当承担相应的民事责任。",
                            "source": "新华社",
                            "date": "2023-06-15"
                        }
                    ],
                    "public": [
                        {
                            "id": 1,
                            "title": "公众反应",
                            "content": "公众对二审维持原判的结果表示认可，认为法律最终维护了公平正义。",
                            "source": "社交媒体分析",
                            "date": "2023-06-16"
                        }
                    ],
                    "expert": [
                        {
                            "id": 1,
                            "title": "法律专家解读",
                            "content": "专家认为二审判决体现了法律的稳定性和公正性，对社会具有积极的引导作用。",
                            "source": "北京大学法学院",
                            "date": "2023-06-17"
                        }
                    ]
                }
            }
        }
        
        # 加载当前日期的快照数据
        current_date = st.session_state.current_snapshot_date
        if current_date in snapshot_data:
            data = snapshot_data[current_date]
            
            # 主流判断摘要区域
            st.markdown("## 主流判断摘要")
            
            # 应用样式
            st.markdown("""
            <style>
            .consensus-card {
                background-color: #f9f9f9;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                border-left: 4px solid #3498db;
                margin-bottom: 20px;
            }
            .consensus-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }
            .consensus-card h3 {
                color: #2c3e50;
                margin-bottom: 10px;
                font-size: 1.1em;
            }
            .consensus-card p {
                color: #555;
                margin-bottom: 15px;
            }
            .consensus-meta {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.9em;
                color: #7f8c8d;
            }
            .consensus-strength {
                display: flex;
                align-items: center;
                gap: 5px;
            }
            .strength-bar {
                width: 60px;
                height: 4px;
                background-color: #e0e0e0;
                border-radius: 2px;
                overflow: hidden;
            }
            .strength-fill {
                height: 100%;
                background-color: #27ae60;
                border-radius: 2px;
                transition: width 0.5s ease;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # 显示主流判断卡片
            for item in data['consensus']:
                st.markdown(f"""
                <div class='consensus-card'>
                    <h3>{item['title']}</h3>
                    <p>{item['summary']}</p>
                    <div class='consensus-meta'>
                        <span>信息源: {item['sourceCount']}个</span>
                        <div class='consensus-strength'>
                            <span>共识强度:</span>
                            <div class='strength-bar'>
                                <div class='strength-fill' style='width: {item['strength'] * 100}%'></div>
                            </div>
                            <span>{(item['strength'] * 100):.0f}%</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # 判断依据展示区域
            st.markdown("## 判断依据")
            
            # 证据标签页
            evidence_tabs = st.tabs(["官方信息", "媒体报道", "公众意见", "专家观点"])
            tab_keys = ['official', 'media', 'public', 'expert']
            tab_names = ['官方信息', '媒体报道', '公众意见', '专家观点']
            
            for i, tab in enumerate(evidence_tabs):
                with tab:
                    st.session_state.current_evidence_tab = tab_keys[i]
                    evidence_data = data['evidence'][tab_keys[i]]
                    
                    if not evidence_data:
                        st.info(f"该时间点暂无{tab_names[i]}数据")
                    else:
                        for item in evidence_data:
                            st.markdown(f"""
                            <div style='background-color: #f9f9f9; border-radius: 8px; padding: 20px; margin-bottom: 10px; border-left: 3px solid #3498db;'>
                                <h4 style='color: #2c3e50; margin-bottom: 8px; font-size: 1em;'>{item['title']}</h4>
                                <p style='color: #555; font-size: 0.95em; margin-bottom: 10px;'>{item['content']}</p>
                                <div style='display: flex; justify-content: space-between; font-size: 0.85em; color: #7f8c8d;'>
                                    <span>来源: {item['source']}</span>
                                    <span>日期: {item['date']}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.warning("该时间点暂无快照数据")
        
        # 快照分享功能
        st.markdown("## 快照分享")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("复制快照链接", key="copy_link"):
                st.success("快照链接已复制到剪贴板")
        with col2:
            if st.button("下载快照报告", key="download_report"):
                st.success("快照报告下载中...")
