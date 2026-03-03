class DomainCategories:
    def __init__(self):
        self.categories = {
            "政治": {
                "description": "政治领域事件，包括政策变化、政治事件等",
                "examples": ["政府政策变更", "国际政治事件", "选举结果"]
            },
            "经济": {
                "description": "经济领域事件，包括经济政策、市场变化等",
                "examples": ["经济政策调整", "市场波动", "企业并购"]
            },
            "科技": {
                "description": "科技领域事件，包括技术突破、产品发布等",
                "examples": ["新技术发布", "科技公司动态", "技术争议"]
            },
            "社会": {
                "description": "社会领域事件，包括社会现象、民生问题等",
                "examples": ["社会热点事件", "民生问题讨论", "社会改革"]
            },
            "体育": {
                "description": "体育领域事件，包括比赛结果、运动员动态等",
                "examples": ["体育比赛结果", "运动员争议", "体育政策变化"]
            },
            "娱乐": {
                "description": "娱乐领域事件，包括明星动态、影视新闻等",
                "examples": ["明星绯闻", "影视节目争议", "娱乐产业动态"]
            },
            "健康": {
                "description": "健康领域事件，包括疾病防控、医疗突破等",
                "examples": ["疾病疫情", "医疗技术突破", "健康政策"]
            },
            "教育": {
                "description": "教育领域事件，包括教育政策、学术争议等",
                "examples": ["教育政策改革", "学术造假事件", "教育热点讨论"]
            }
        }
    
    def get_all_categories(self):
        """获取所有领域分类"""
        return list(self.categories.keys())
    
    def get_category_info(self, category):
        """获取领域信息"""
        return self.categories.get(category, {})
    
    def is_valid_category(self, category):
        """检查领域是否有效"""
        return category in self.categories