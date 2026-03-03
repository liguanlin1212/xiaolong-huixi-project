import os
import json
import threading
import time
from datetime import datetime
from search.explore_prompt import ExplorePromptBuilder
from search.search_analyzer import SearchAnalyzer
from ai.inference.model_factory import ModelFactory

class RefreshManager:
    def __init__(self):
        self.cache_dir = os.path.join(os.path.dirname(__file__), "..", "data", "explore_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.prompt_builder = ExplorePromptBuilder()
        self.search_analyzer = SearchAnalyzer()
        self.model_factory = ModelFactory()
        self.ai_model = self.model_factory.create_runner("OPENAI")
        self.cache = {}
        self.refresh_thread = None
        self.running = False
    
    def start(self):
        """启动后台刷新线程"""
        if not self.running:
            self.running = True
            self.refresh_thread = threading.Thread(target=self._refresh_loop, daemon=True)
            self.refresh_thread.start()
    
    def stop(self):
        """停止后台刷新线程"""
        self.running = False
        if self.refresh_thread:
            self.refresh_thread.join()
    
    def _refresh_loop(self):
        """后台刷新循环"""
        while self.running:
            # 每小时刷新一次
            self.refresh_all_domains()
            for i in range(3600):
                if not self.running:
                    break
                time.sleep(1)
    
    def refresh_all_domains(self):
        """刷新所有领域的事件"""
        from search.domain_categories import DomainCategories
        domain_categories = DomainCategories()
        categories = domain_categories.get_all_categories()
        
        for domain in categories:
            self.refresh_domain(domain)
    
    def refresh_domain(self, domain):
        """刷新特定领域的事件"""
        try:
            # 构建prompt
            prompt = self.prompt_builder.build_prompt(domain)
            
            # 调用大模型
            raw_results = self.ai_model.classify_text(prompt)
            
            # 分析结果
            results = self.search_analyzer.analyze_results(raw_results)
            
            # 缓存结果
            self.cache[domain] = {
                "events": results,
                "timestamp": datetime.now().isoformat()
            }
            
            # 保存到文件
            self._save_cache(domain)
            
            print(f"刷新{domain}领域事件成功")
        except Exception as e:
            print(f"刷新{domain}领域事件失败: {e}")
    
    def get_cached_events(self, domain):
        """获取缓存的事件"""
        # 先尝试从内存缓存获取
        if domain in self.cache:
            return self.cache[domain]["events"]
        
        # 再尝试从文件缓存获取
        cached_data = self._load_cache(domain)
        if cached_data:
            self.cache[domain] = cached_data
            return cached_data["events"]
        
        return []
    
    def _save_cache(self, domain):
        """保存缓存到文件"""
        cache_path = os.path.join(self.cache_dir, f"{domain}.json")
        if domain in self.cache:
            try:
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(self.cache[domain], f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"保存缓存失败: {e}")
    
    def _load_cache(self, domain):
        """从文件加载缓存"""
        cache_path = os.path.join(self.cache_dir, f"{domain}.json")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载缓存失败: {e}")
        return None
    
    def is_cache_valid(self, domain):
        """检查缓存是否有效（24小时内）"""
        cached_data = self._load_cache(domain)
        if not cached_data:
            return False
        
        try:
            timestamp = datetime.fromisoformat(cached_data["timestamp"])
            return (datetime.now() - timestamp).total_seconds() < 24 * 60 * 60
        except Exception as e:
            print(f"检查缓存有效性失败: {e}")
            return False
    
    def force_refresh(self, domain):
        """强制刷新特定领域的事件"""
        self.refresh_domain(domain)
        return self.get_cached_events(domain)