import os
import json
import hashlib
from datetime import datetime, timedelta

class SearchHandler:
    def __init__(self):
        self.cache_dir = os.path.join(os.path.dirname(__file__), "..", "data", "search_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def validate_query(self, query):
        """验证搜索查询"""
        if not query or len(query.strip()) < 2:
            return False, "搜索关键词至少需要2个字符"
        if len(query) > 100:
            return False, "搜索关键词不能超过100个字符"
        return True, ""
    
    def generate_cache_key(self, query):
        """生成缓存键"""
        return hashlib.md5(query.encode()).hexdigest()
    
    def get_cache_path(self, query):
        """获取缓存文件路径"""
        cache_key = self.generate_cache_key(query)
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def is_cache_valid(self, cache_path):
        """检查缓存是否有效（24小时内）"""
        if not os.path.exists(cache_path):
            return False
        
        file_time = os.path.getmtime(cache_path)
        current_time = datetime.now().timestamp()
        return (current_time - file_time) < 24 * 60 * 60
    
    def get_cached_result(self, query):
        """获取缓存结果"""
        cache_path = self.get_cache_path(query)
        if self.is_cache_valid(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"读取缓存失败: {e}")
        return None
    
    def save_cache_result(self, query, result):
        """保存缓存结果"""
        cache_path = self.get_cache_path(query)
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存缓存失败: {e}")
    
    def process_query(self, query):
        """处理搜索查询"""
        # 验证查询
        is_valid, error_msg = self.validate_query(query)
        if not is_valid:
            return None, error_msg
        
        # 检查缓存
        cached_result = self.get_cached_result(query)
        if cached_result:
            return cached_result, ""
        
        # 这里将在后续步骤中集成大模型搜索
        # 目前返回空结果，等待后续实现
        return [], ""