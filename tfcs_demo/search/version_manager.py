from search.version_data_structure import JudgmentVersion

class VersionManager:
    """版本管理逻辑"""
    
    def __init__(self):
        self.versions = {}  # 版本ID -> 版本实例
        self.event_versions = {}  # 事件ID -> 版本ID列表（按时间顺序）
    
    def create_version(self, event_id, content, parent_version_id=None):
        """创建新版本
        
        Args:
            event_id: 事件ID
            content: 判断内容
            parent_version_id: 父版本ID
            
        Returns:
            JudgmentVersion: 新创建的版本
        """
        # 创建新版本
        new_version = JudgmentVersion(content, parent_version_id)
        
        # 存储版本
        self.versions[new_version.version_id] = new_version
        
        # 更新事件版本列表
        if event_id not in self.event_versions:
            self.event_versions[event_id] = []
        self.event_versions[event_id].append(new_version.version_id)
        
        return new_version
    
    def get_version(self, version_id):
        """获取版本
        
        Args:
            version_id: 版本ID
            
        Returns:
            JudgmentVersion: 版本实例
        """
        return self.versions.get(version_id)
    
    def get_latest_version(self, event_id):
        """获取事件的最新版本
        
        Args:
            event_id: 事件ID
            
        Returns:
            JudgmentVersion: 最新版本实例
        """
        if event_id in self.event_versions and self.event_versions[event_id]:
            latest_version_id = self.event_versions[event_id][-1]
            return self.versions.get(latest_version_id)
        return None
    
    def get_versions(self, event_id):
        """获取事件的所有版本
        
        Args:
            event_id: 事件ID
            
        Returns:
            list: 版本实例列表
        """
        if event_id not in self.event_versions:
            return []
        
        return [self.versions[version_id] for version_id in self.event_versions[event_id]]
    
    def update_version(self, event_id, content):
        """更新版本（创建新版本，指向旧版本）
        
        Args:
            event_id: 事件ID
            content: 新的判断内容
            
        Returns:
            JudgmentVersion: 新创建的版本
        """
        # 获取最新版本作为父版本
        latest_version = self.get_latest_version(event_id)
        parent_version_id = latest_version.version_id if latest_version else None
        
        # 创建新版本
        return self.create_version(event_id, content, parent_version_id)
    
    def delete_version(self, version_id):
        """删除版本
        
        Args:
            version_id: 版本ID
            
        Returns:
            bool: 是否删除成功
        """
        if version_id in self.versions:
            # 从版本字典中删除
            del self.versions[version_id]
            
            # 从事件版本列表中删除
            for event_id, version_ids in self.event_versions.items():
                if version_id in version_ids:
                    version_ids.remove(version_id)
                    if not version_ids:
                        del self.event_versions[event_id]
            
            return True
        return False
    
    def get_version_history(self, event_id):
        """获取版本历史
        
        Args:
            event_id: 事件ID
            
        Returns:
            list: 版本实例列表（按时间顺序）
        """
        return self.get_versions(event_id)