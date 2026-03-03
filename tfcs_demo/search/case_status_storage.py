import os
import json
from datetime import datetime
from search.case_status_rules import CaseStatus

class CaseStatusStorage:
    """状态持久化"""
    
    def __init__(self):
        self.storage_dir = os.path.join(os.path.dirname(__file__), "..", "data", "case_status")
        os.makedirs(self.storage_dir, exist_ok=True)
        self.status_file = os.path.join(self.storage_dir, "case_status.json")
        self.status_history_file = os.path.join(self.storage_dir, "case_status_history.json")
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        # 加载状态数据
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, "r", encoding="utf-8") as f:
                    self.status_data = json.load(f)
            except Exception as e:
                print(f"加载状态数据失败: {e}")
                self.status_data = {}
        else:
            self.status_data = {}
        
        # 加载状态历史数据
        if os.path.exists(self.status_history_file):
            try:
                with open(self.status_history_file, "r", encoding="utf-8") as f:
                    self.status_history = json.load(f)
            except Exception as e:
                print(f"加载状态历史数据失败: {e}")
                self.status_history = {}
        else:
            self.status_history = {}
    
    def save_status(self, event_id, status, reason, confidence):
        """保存状态
        
        Args:
            event_id: 事件ID
            status: 状态
            reason: 转换原因
            confidence: 置信度
        """
        # 保存状态
        self.status_data[event_id] = {
            "status": status.value,
            "reason": reason,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
        
        # 保存状态历史
        if event_id not in self.status_history:
            self.status_history[event_id] = []
        
        self.status_history[event_id].append({
            "status": status.value,
            "reason": reason,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })
        
        # 保存到文件
        self._save_data()
    
    def get_status(self, event_id):
        """获取状态
        
        Args:
            event_id: 事件ID
            
        Returns:
            tuple: (CaseStatus, str, int, str) - (状态, 转换原因, 置信度, 时间戳)
        """
        if event_id in self.status_data:
            status_data = self.status_data[event_id]
            status = CaseStatus(status_data["status"])
            return status, status_data["reason"], status_data["confidence"], status_data["timestamp"]
        else:
            return None, "", 0, ""
    
    def get_status_history(self, event_id):
        """获取状态历史
        
        Args:
            event_id: 事件ID
            
        Returns:
            list: 状态历史列表
        """
        return self.status_history.get(event_id, [])
    
    def _save_data(self):
        """保存数据到文件"""
        # 保存状态数据
        try:
            with open(self.status_file, "w", encoding="utf-8") as f:
                json.dump(self.status_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存状态数据失败: {e}")
        
        # 保存状态历史数据
        try:
            with open(self.status_history_file, "w", encoding="utf-8") as f:
                json.dump(self.status_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存状态历史数据失败: {e}")
    
    def delete_status(self, event_id):
        """删除状态
        
        Args:
            event_id: 事件ID
        """
        if event_id in self.status_data:
            del self.status_data[event_id]
        
        if event_id in self.status_history:
            del self.status_history[event_id]
        
        self._save_data()
    
    def list_events(self):
        """列出所有事件
        
        Returns:
            list: 事件ID列表
        """
        return list(self.status_data.keys())