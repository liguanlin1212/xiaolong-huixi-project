import streamlit as st
import time
from search.domain_categories import DomainCategories
from app.ui.event_card import EventCard
from search.refresh_manager import RefreshManager
from search.case_status_machine import CaseStatusMachine

class ExploreUI:
    def __init__(self):
        self.domain_categories = DomainCategories()
        self.event_card = EventCard()
        self.refresh_manager = RefreshManager()
        self.case_status_machine = CaseStatusMachine()
        # 启动后台刷新线程
        self.refresh_manager.start()
    
    def display(self):
        st.title("事件探索")
        
        # 领域选择器
        categories = self.domain_categories.get_all_categories()
        selected_category = st.selectbox(
            "选择领域",
            categories,
            index=0
        )
        
        # 显示领域信息
        category_info = self.domain_categories.get_category_info(selected_category)
        if category_info:
            st.markdown(f"**领域描述：** {category_info.get('description', '无描述')}")
            if category_info.get('examples'):
                st.markdown(f"**示例：** {', '.join(category_info['examples'])}")
        
        # 刷新按钮
        refresh_clicked = st.button("刷新事件")
        
        # 事件卡片网格展示
        st.subheader(f"{selected_category}领域已结案事件")
        
        # 获取事件数据
        if refresh_clicked:
            # 用户点击刷新，强制刷新该领域事件
            with st.spinner("正在刷新事件..."):
                events = self.refresh_manager.force_refresh(selected_category)
        else:
            # 尝试从缓存获取事件
            events = self.refresh_manager.get_cached_events(selected_category)
            # 如果缓存为空，使用示例事件
            if not events:
                events = self.get_example_events(selected_category)
        
        # 使用状态机管理事件状态
        processed_events = []
        for i, event in enumerate(events):
            event_id = f"explore_{selected_category}_{i}_{int(time.time())}"
            # 获取初始状态
            status = self.case_status_machine.get_initial_status(event, event_id)
            event["case_status"] = status.value
            processed_events.append(event)
        
        # 使用列布局展示卡片
        cols = st.columns(2)
        for i, event in enumerate(processed_events):
            with cols[i % 2]:
                self.event_card.display(event, f"{selected_category}_{i}")
        
        return selected_category, refresh_clicked
    
    def get_example_events(self, category):
        """获取示例事件"""
        # 示例事件数据
        example_data = {
            "政治": [
                {
                    "title": "2024年美国总统选举结果",
                    "time_range": "2024-11-05 至 2024-11-15",
                    "description": "2024年美国总统选举结果公布，拜登成功连任",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2024-11-05：初步计票显示拜登领先",
                        "2024-11-08：主要媒体宣布拜登获胜",
                        "2024-11-15：选举结果正式确认"
                    ],
                    "evidence": [
                        "官方计票数据",
                        "媒体报道",
                        "选举委员会声明"
                    ],
                    "final_conclusion": "拜登在2024年美国总统选举中获胜，成功连任",
                    "sources": [
                        "CNN",
                        "BBC",
                        "纽约时报"
                    ]
                },
                {
                    "title": "2023年中国全国人大会议",
                    "time_range": "2023-03-05 至 2023-03-13",
                    "description": "2023年中国全国人民代表大会在北京召开",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2023-03-05：会议开幕",
                        "2023-03-10：通过重要决议",
                        "2023-03-13：会议闭幕"
                    ],
                    "evidence": [
                        "官方媒体报道",
                        "会议文件",
                        "新闻发布会"
                    ],
                    "final_conclusion": "2023年全国人大会议顺利召开，通过了多项重要决议",
                    "sources": [
                        "新华社",
                        "人民日报",
                        "中央电视台"
                    ]
                }
            ],
            "经济": [
                {
                    "title": "2023年全球经济增长预测",
                    "time_range": "2023-01-01 至 2023-12-31",
                    "description": "国际货币基金组织发布2023年全球经济增长预测",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2023-01：IMF预测全球经济增长2.9%",
                        "2023-07：IMF上调预测至3.2%",
                        "2023-10：IMF确认全年增长3.1%"
                    ],
                    "evidence": [
                        "IMF报告",
                        "全球经济数据",
                        "专家分析"
                    ],
                    "final_conclusion": "2023年全球经济增长3.1%，高于年初预期",
                    "sources": [
                        "国际货币基金组织",
                        "世界银行",
                        "经济合作与发展组织"
                    ]
                },
                {
                    "title": "2024年油价波动",
                    "time_range": "2024-01-01 至 2024-06-30",
                    "description": "2024年上半年国际油价大幅波动",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2024-01：油价突破100美元/桶",
                        "2024-03：油价回落至85美元/桶",
                        "2024-06：油价稳定在90美元/桶左右"
                    ],
                    "evidence": [
                        "国际能源署数据",
                        "石油输出国组织报告",
                        "市场分析"
                    ],
                    "final_conclusion": "2024年上半年油价经历了大幅波动，最终趋于稳定",
                    "sources": [
                        "国际能源署",
                        "石油输出国组织",
                        "彭博社"
                    ]
                }
            ],
            "科技": [
                {
                    "title": "OpenAI GPT-4发布",
                    "time_range": "2023-03-14 至 2023-03-20",
                    "description": "OpenAI发布GPT-4大型语言模型",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2023-03-14：OpenAI宣布GPT-4发布",
                        "2023-03-15：GPT-4开始向部分用户开放",
                        "2023-03-20：GPT-4全面开放"
                    ],
                    "evidence": [
                        "OpenAI官方公告",
                        "技术评测",
                        "用户反馈"
                    ],
                    "final_conclusion": "GPT-4成功发布，性能显著优于前代模型",
                    "sources": [
                        "OpenAI官网",
                        "TechCrunch",
                        "Wired"
                    ]
                },
                {
                    "title": "苹果Vision Pro上市",
                    "time_range": "2024-01-19 至 2024-01-25",
                    "description": "苹果公司首款混合现实头显Vision Pro正式上市",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2024-01-19：Vision Pro在美国正式上市",
                        "2024-01-20：首批用户收到设备",
                        "2024-01-25：市场反馈积极"
                    ],
                    "evidence": [
                        "苹果官网",
                        "用户评测",
                        "媒体报道"
                    ],
                    "final_conclusion": "苹果Vision Pro成功上市，开启混合现实新纪元",
                    "sources": [
                        "苹果官网",
                        "The Verge",
                        "CNET"
                    ]
                }
            ],
            "社会": [
                {
                    "title": "2023年全球气候变化抗议",
                    "time_range": "2023-09-20 至 2023-09-25",
                    "description": "全球多地举行气候变化抗议活动",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2023-09-20：全球多地开始抗议",
                        "2023-09-22：抗议规模达到高峰",
                        "2023-09-25：抗议活动结束"
                    ],
                    "evidence": [
                        "媒体报道",
                        "社交媒体数据",
                        "官方统计"
                    ],
                    "final_conclusion": "全球气候变化抗议活动成功举行，引起广泛关注",
                    "sources": [
                        "路透社",
                        "美联社",
                        "卫报"
                    ]
                },
                {
                    "title": "2024年东京奥运会筹备",
                    "time_range": "2023-10-01 至 2024-07-23",
                    "description": "2024年东京奥运会筹备工作进展",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2023-10：场馆建设完成",
                        "2024-03：火炬传递开始",
                        "2024-07-23：奥运会开幕"
                    ],
                    "evidence": [
                        "国际奥委会报告",
                        "东京奥组委公告",
                        "媒体报道"
                    ],
                    "final_conclusion": "2024年东京奥运会筹备工作顺利完成，成功开幕",
                    "sources": [
                        "国际奥委会",
                        "东京奥组委",
                        "共同社"
                    ]
                }
            ],
            "体育": [
                {
                    "title": "2024年欧洲杯足球赛",
                    "time_range": "2024-06-14 至 2024-07-14",
                    "description": "2024年欧洲足球锦标赛在德国举行",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2024-06-14：比赛开幕",
                        "2024-07-06：半决赛结束",
                        "2024-07-14：决赛举行，西班牙夺冠"
                    ],
                    "evidence": [
                        "欧足联官网",
                        "比赛直播",
                        "媒体报道"
                    ],
                    "final_conclusion": "2024年欧洲杯成功举行，西班牙队夺冠",
                    "sources": [
                        "欧足联官网",
                        "BBC Sport",
                        "ESPN"
                    ]
                },
                {
                    "title": "2023年NBA总决赛",
                    "time_range": "2023-06-01 至 2023-06-12",
                    "description": "2023年NBA总决赛举行",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2023-06-01：总决赛第一场",
                        "2023-06-08：系列赛3-2领先",
                        "2023-06-12：掘金队夺冠"
                    ],
                    "evidence": [
                        "NBA官网",
                        "比赛直播",
                        "媒体报道"
                    ],
                    "final_conclusion": "2023年NBA总决赛掘金队夺冠",
                    "sources": [
                        "NBA官网",
                        "ESPN",
                        "Sports Illustrated"
                    ]
                }
            ],
            "娱乐": [
                {
                    "title": "2024年奥斯卡颁奖典礼",
                    "time_range": "2024-03-10 至 2024-03-11",
                    "description": "第96届奥斯卡金像奖颁奖典礼举行",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2024-03-10：颁奖典礼开始",
                        "2024-03-11：颁奖典礼结束，获奖名单公布",
                        "2024-03-11：媒体报道和反响"
                    ],
                    "evidence": [
                        "奥斯卡官网",
                        "直播录像",
                        "媒体报道"
                    ],
                    "final_conclusion": "2024年奥斯卡颁奖典礼成功举行，《奥本海默》获得最佳影片",
                    "sources": [
                        "奥斯卡官网",
                        "Variety",
                        "Hollywood Reporter"
                    ]
                },
                {
                    "title": "2023年全球音乐流媒体数据",
                    "time_range": "2023-01-01 至 2023-12-31",
                    "description": "2023年全球音乐流媒体平台数据统计",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2023-06：Spotify用户突破5亿",
                        "2023-09：Apple Music增长放缓",
                        "2023-12：全年数据公布"
                    ],
                    "evidence": [
                        "Spotify财报",
                        "Apple Music数据",
                        "市场研究报告"
                    ],
                    "final_conclusion": "2023年全球音乐流媒体市场继续增长，Spotify保持领先",
                    "sources": [
                        "Spotify官网",
                        "Apple Music官网",
                        "IFPI报告"
                    ]
                }
            ],
            "健康": [
                {
                    "title": "2023年COVID-19疫情发展",
                    "time_range": "2023-01-01 至 2023-12-31",
                    "description": "2023年全球COVID-19疫情发展情况",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2023-01：疫情仍在全球蔓延",
                        "2023-06：疫情逐渐缓解",
                        "2023-12：疫情进入常态化阶段"
                    ],
                    "evidence": [
                        "WHO数据",
                        "各国卫生部门报告",
                        "科学研究"
                    ],
                    "final_conclusion": "2023年COVID-19疫情逐渐得到控制，进入常态化阶段",
                    "sources": [
                        "世界卫生组织",
                        "美国疾病控制与预防中心",
                        "柳叶刀"
                    ]
                },
                {
                    "title": "2024年医学突破",
                    "time_range": "2024-01-01 至 2024-06-30",
                    "description": "2024年上半年医学领域重要突破",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2024-02：AI辅助诊断技术取得突破",
                        "2024-04：基因编辑治疗成功案例",
                        "2024-06：新型疫苗研发进展"
                    ],
                    "evidence": [
                        "科学期刊论文",
                        "医学会议报告",
                        "新闻发布会"
                    ],
                    "final_conclusion": "2024年上半年医学领域取得多项重要突破",
                    "sources": [
                        "自然杂志",
                        "科学杂志",
                        "新英格兰医学杂志"
                    ]
                }
            ],
            "教育": [
                {
                    "title": "2023年全球教育改革",
                    "time_range": "2023-01-01 至 2023-12-31",
                    "description": "2023年全球教育领域改革措施",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2023-03：多个国家推出教育改革计划",
                        "2023-09：改革措施开始实施",
                        "2023-12：改革效果评估"
                    ],
                    "evidence": [
                        "各国教育部文件",
                        "教育研究报告",
                        "媒体报道"
                    ],
                    "final_conclusion": "2023年全球教育改革取得积极成效",
                    "sources": [
                        "联合国教科文组织",
                        "经济合作与发展组织",
                        "教育部门报告"
                    ]
                },
                {
                    "title": "2024年高考改革",
                    "time_range": "2024-01-01 至 2024-06-10",
                    "description": "2024年中国高考改革措施",
                    "case_status": "已结案",
                    "judgment_evolution": [
                        "2024-01：教育部发布改革方案",
                        "2024-03：改革细则公布",
                        "2024-06：高考顺利举行"
                    ],
                    "evidence": [
                        "教育部文件",
                        "考试大纲",
                        "媒体报道"
                    ],
                    "final_conclusion": "2024年高考改革顺利实施",
                    "sources": [
                        "教育部官网",
                        "人民日报",
                        "中国教育报"
                    ]
                }
            ]
        }
        
        return example_data.get(category, [])