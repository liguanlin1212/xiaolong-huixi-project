import streamlit as st

class FailureArchiveView:
    def __init__(self):
        # 初始化状态
        if 'selected_archive' not in st.session_state:
            st.session_state.selected_archive = None
        if 'search_query' not in st.session_state:
            st.session_state.search_query = ""
        if 'filter_category' not in st.session_state:
            st.session_state.filter_category = "全部"
    
    def display(self):
        """
        显示认知失败档案
        """
        # 页面标题
        st.markdown("""
        <div style='text-align: center; margin-bottom: 40px; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h1 style='color: #2c3e50; margin-bottom: 10px;'>认知失败档案查看</h1>
            <p style='color: #7f8c8d; font-size: 1.1em;'>分析过去的认知失败案例，从中学习以避免未来的错误</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 应用样式
        st.markdown("""
        <style>
        .archive-card {
            background-color: #fff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 4px solid #9b59b6;
            margin-bottom: 20px;
            cursor: pointer;
        }
        .archive-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .archive-card h3 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        .archive-card p {
            color: #555;
            margin-bottom: 15px;
        }
        .archive-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9em;
            color: #7f8c8d;
            margin-bottom: 15px;
        }
        .lifecycle-timeline {
            position: relative;
            padding: 20px 0;
            margin: 20px 0;
        }
        .lifecycle-line {
            position: absolute;
            left: 50%;
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: #9b59b6;
            transform: translateX(-50%);
        }
        .lifecycle-item {
            position: relative;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
        }
        .lifecycle-item:nth-child(odd) {
            flex-direction: row;
        }
        .lifecycle-item:nth-child(even) {
            flex-direction: row-reverse;
        }
        .lifecycle-content {
            width: 45%;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .lifecycle-content h4 {
            color: #2c3e50;
            margin-bottom: 8px;
            font-size: 1em;
        }
        .lifecycle-content p {
            color: #555;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        .lifecycle-node {
            position: absolute;
            left: 50%;
            top: 20px;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background-color: #9b59b6;
            border: 3px solid #e6e6fa;
            transform: translateX(-50%);
            z-index: 1;
        }
        .analysis-section {
            margin-top: 30px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
        }
        .analysis-section h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.1em;
        }
        .cause-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        .cause-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: #9b59b6;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
            flex-shrink: 0;
        }
        .cause-content {
            flex: 1;
        }
        .cause-content h4 {
            color: #2c3e50;
            margin-bottom: 5px;
            font-size: 1em;
        }
        .cause-content p {
            color: #555;
            font-size: 0.9em;
        }
        .cost-item {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .cost-label {
            width: 120px;
            font-weight: bold;
            color: #555;
        }
        .cost-bar {
            flex: 1;
            height: 8px;
            background-color: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin: 0 10px;
        }
        .cost-fill {
            height: 100%;
            background-color: #e74c3c;
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        .cost-value {
            width: 50px;
            text-align: right;
            color: #7f8c8d;
        }
        .search-filter {
            background-color: #f9f9f9;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 搜索和筛选功能
        st.markdown("""
        <div class='search-filter'>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            search_query = st.text_input("搜索档案", value=st.session_state.search_query, key="search_query")
            st.session_state.search_query = search_query
        with col2:
            filter_category = st.selectbox(
                "筛选类别",
                ["全部", "信息获取错误", "逻辑推理错误", "认知偏见", "情绪影响"],
                index=["全部", "信息获取错误", "逻辑推理错误", "认知偏见", "情绪影响"].index(st.session_state.filter_category),
                key="filter_category"
            )
            st.session_state.filter_category = filter_category
        
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
        
        # 模拟认知失败档案数据
        failure_archives = [
            {
                "id": 1,
                "title": "刘鑫锁门事件认知错误",
                "category": "信息获取错误",
                "date": "2023-06-15",
                "summary": "公众对刘鑫在案发时是否锁门的认知存在错误，直到法院判决才澄清事实。",
                "lifecycle": [
                    {
                        "stage": "初始判断",
                        "date": "2016-11-04",
                        "description": "根据媒体报道和江歌母亲的说法，公众普遍认为刘鑫在案发时锁门。"
                    },
                    {
                        "stage": "质疑阶段",
                        "date": "2017-12-18",
                        "description": "刘鑫在庭审中否认锁门，其证词与其他证据存在矛盾。"
                    },
                    {
                        "stage": "重新评估",
                        "date": "2022-12-30",
                        "description": "民事判决认定刘鑫未采取有效措施救助江歌。"
                    },
                    {
                        "stage": "最终结论",
                        "date": "2023-06-15",
                        "description": "二审维持原判，确认刘鑫对江歌的死亡存在过错。"
                    }
                ],
                "causes": [
                    {
                        "id": 1,
                        "title": "信息来源单一",
                        "description": "公众主要依赖江歌母亲的陈述和部分媒体报道，缺乏对其他信息来源的核实。"
                    },
                    {
                        "id": 2,
                        "title": "情绪影响",
                        "description": "公众对江歌的同情和对刘鑫的不满情绪影响了客观判断。"
                    },
                    {
                        "id": 3,
                        "title": "缺乏专业分析",
                        "description": "大多数公众缺乏法律专业知识，难以准确理解案件细节和法律责任。"
                    }
                ],
                "costs": {
                    "公众信任损失": 0.8,
                    "社会分化": 0.7,
                    "法律资源消耗": 0.9,
                    "个人声誉损害": 0.95
                }
            },
            {
                "id": 2,
                "title": "陈世峰正当防卫认知错误",
                "category": "逻辑推理错误",
                "date": "2023-06-10",
                "summary": "部分公众认为陈世峰的行为属于正当防卫，实际上法院认定其构成故意杀人罪。",
                "lifecycle": [
                    {
                        "stage": "初始判断",
                        "date": "2016-11-04",
                        "description": "案发后，部分人根据有限信息认为陈世峰可能是正当防卫。"
                    },
                    {
                        "stage": "证据披露",
                        "date": "2017-12-18",
                        "description": "庭审中披露的证据显示陈世峰携带刀具前往现场，有预谋伤害的意图。"
                    },
                    {
                        "stage": "法院判决",
                        "date": "2017-12-20",
                        "description": "东京地方裁判所认定陈世峰构成故意杀人罪，判处有期徒刑20年。"
                    },
                    {
                        "stage": "最终结论",
                        "date": "2023-06-10",
                        "description": "法律专家再次确认陈世峰的行为不属于正当防卫。"
                    }
                ],
                "causes": [
                    {
                        "id": 1,
                        "title": "法律知识缺乏",
                        "description": "公众对正当防卫的法律定义和适用条件缺乏准确理解。"
                    },
                    {
                        "id": 2,
                        "title": "信息误读",
                        "description": "部分人误读了案件细节，错误地认为陈世峰是在受到攻击时还手。"
                    },
                    {
                        "id": 3,
                        "title": "媒体误导",
                        "description": "部分媒体早期报道对案件细节描述不准确，导致公众产生误解。"
                    }
                ],
                "costs": {
                    "司法公信力影响": 0.6,
                    "公众法律意识混淆": 0.8,
                    "受害者家属二次伤害": 0.9,
                    "社会舆论分裂": 0.7
                }
            },
            {
                "id": 3,
                "title": "江歌母亲炒作案件认知错误",
                "category": "认知偏见",
                "date": "2023-06-15",
                "summary": "部分公众认为江歌母亲是在炒作案件，实际上她是在寻求法律公正。",
                "lifecycle": [
                    {
                        "stage": "初始判断",
                        "date": "2016-11-05",
                        "description": "江歌母亲开始通过媒体寻求帮助，部分人认为她是在炒作。"
                    },
                    {
                        "stage": "持续行动",
                        "date": "2017-12-20",
                        "description": "江歌母亲持续关注案件进展，推动司法程序。"
                    },
                    {
                        "stage": "法律行动",
                        "date": "2022-12-30",
                        "description": "江歌母亲提起民事诉讼并获得胜诉。"
                    },
                    {
                        "stage": "最终结论",
                        "date": "2023-06-15",
                        "description": "二审维持原判，证明江歌母亲的诉求具有法律依据。"
                    }
                ],
                "causes": [
                    {
                        "id": 1,
                        "title": "刻板印象",
                        "description": "部分人对受害者家属通过媒体发声存在刻板印象，认为是在炒作。"
                    },
                    {
                        "id": 2,
                        "title": "信息不对称",
                        "description": "公众对江歌母亲为案件所做的努力和面临的困难缺乏了解。"
                    },
                    {
                        "id": 3,
                        "title": "网络暴力",
                        "description": "部分网络言论基于偏见和误解，进一步强化了错误认知。"
                    }
                ],
                "costs": {
                    "受害者家属精神伤害": 0.95,
                    "社会同情心减弱": 0.6,
                    "网络环境恶化": 0.8,
                    "公众信任危机": 0.7
                }
            }
        ]
        
        # 应用搜索和筛选
        filtered_archives = failure_archives
        if search_query:
            filtered_archives = [archive for archive in filtered_archives if search_query.lower() in archive['title'].lower() or search_query.lower() in archive['summary'].lower()]
        if filter_category != "全部":
            filtered_archives = [archive for archive in filtered_archives if archive['category'] == filter_category]
        
        # 档案列表页面
        st.markdown("## 认知失败档案列表")
        
        if not filtered_archives:
            st.info("未找到符合条件的档案")
        else:
            for archive in filtered_archives:
                # 显示档案卡片
                st.markdown(f"""
                <div class='archive-card'>
                    <div class='archive-meta'>
                        <span>日期: {archive['date']}</span>
                        <span>类别: {archive['category']}</span>
                    </div>
                    <h3>{archive['title']}</h3>
                    <p>{archive['summary']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 选择档案按钮
                if st.button(f"查看详情", key=f"archive-{archive['id']}"):
                    st.session_state.selected_archive = archive['id']
                
                # 展开详情
                if st.session_state.selected_archive == archive['id']:
                    # 判断生命周期展示
                    st.markdown("### 判断生命周期")
                    st.markdown("""
                    <div class='lifecycle-timeline'>
                        <div class='lifecycle-line'></div>
                    """, unsafe_allow_html=True)
                    
                    for i, stage in enumerate(archive['lifecycle']):
                        st.markdown(f"""
                        <div class='lifecycle-item'>
                            <div class='lifecycle-node'></div>
                            <div class='lifecycle-content'>
                                <h4>{stage['stage']}</h4>
                                <p><strong>日期:</strong> {stage['date']}</p>
                                <p>{stage['description']}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 错误成因分析
                    st.markdown("### 错误成因分析")
                    st.markdown("""
                    <div class='analysis-section'>
                    """, unsafe_allow_html=True)
                    
                    for cause in archive['causes']:
                        st.markdown(f"""
                        <div class='cause-item'>
                            <div class='cause-icon'>{cause['id']}</div>
                            <div class='cause-content'>
                                <h4>{cause['title']}</h4>
                                <p>{cause['description']}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 修正代价展示
                    st.markdown("### 修正代价")
                    st.markdown("""
                    <div class='analysis-section'>
                    """, unsafe_allow_html=True)
                    
                    for cost_name, cost_value in archive['costs'].items():
                        st.markdown(f"""
                        <div class='cost-item'>
                            <span class='cost-label'>{cost_name}</span>
                            <div class='cost-bar'>
                                <div class='cost-fill' style='width: {cost_value * 100}%'></div>
                            </div>
                            <span class='cost-value'>{int(cost_value * 100)}%</span>
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
            st.metric("总档案数", len(failure_archives))
        with col2:
            st.metric("当前显示", len(filtered_archives))
        with col3:
            categories = set(archive['category'] for archive in failure_archives)
            st.metric("类别数量", len(categories))
