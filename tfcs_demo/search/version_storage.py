import os
import json
from search.version_data_structure import JudgmentVersion
from search.version_manager import VersionManager

class VersionStorage:
    """版本持久化"""
    
    def __init__(self):
        self.storage_dir = os.path.join(os.path.dirname(__file__), "..", "data", "versions")
        os.makedirs(self.storage_dir, exist_ok=True)
        self.versions_file = os.path.join(self.storage_dir, "versions.json")
        self.event_versions_file = os.path.join(self.storage_dir, "event_versions.json")
    
    def save_versions(self, version_manager):
        """保存版本
        
        Args:
            version_manager: 版本管理器实例
        """
        # 保存版本数据
        versions_data = {}
        for version_id, version in version_manager.versions.items():
            versions_data[version_id] = version.to_dict()
        
        # 保存事件版本映射
        event_versions_data = version_manager.event_versions
        
        # 写入文件
        try:
            with open(self.versions_file, "w", encoding="utf-8") as f:
                json.dump(versions_data, f, ensure_ascii=False, indent=2)
            
            with open(self.event_versions_file, "w", encoding="utf-8") as f:
                json.dump(event_versions_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存版本失败: {e}")
            return False
    
    def load_versions(self, version_manager):
        """加载版本
        
        Args:
            version_manager: 版本管理器实例
            
        Returns:
            bool: 是否加载成功
        """
        try:
            # 加载版本数据
            if os.path.exists(self.versions_file):
                with open(self.versions_file, "r", encoding="utf-8") as f:
                    versions_data = json.load(f)
                
                # 恢复版本
                for version_id, version_data in versions_data.items():
                    version = JudgmentVersion.from_dict(version_data)
                    version_manager.versions[version_id] = version
            
            # 加载事件版本映射
            if os.path.exists(self.event_versions_file):
                with open(self.event_versions_file, "r", encoding="utf-8") as f:
                    event_versions_data = json.load(f)
                
                # 恢复事件版本映射
                version_manager.event_versions = event_versions_data
            
            return True
        except Exception as e:
            print(f"加载版本失败: {e}")
            return False
    
    def delete_versions(self):
        """删除所有版本
        
        Returns:
            bool: 是否删除成功
        """
        try:
            if os.path.exists(self.versions_file):
                os.remove(self.versions_file)
            
            if os.path.exists(self.event_versions_file):
                os.remove(self.event_versions_file)
            
            return True
        except Exception as e:
            print(f"删除版本失败: {e}")
            return False