from datetime import datetime

class VersionHistory:
    """版本历史查询功能"""
    
    def __init__(self, version_manager):
        """初始化版本历史
        
        Args:
            version_manager: 版本管理器实例
        """
        self.version_manager = version_manager
    
    def get_history_by_time(self, event_id):
        """按时间顺序获取版本历史
        
        Args:
            event_id: 事件ID
            
        Returns:
            list: 版本实例列表（按时间顺序）
        """
        versions = self.version_manager.get_versions(event_id)
        # 按时间戳排序
        versions.sort(key=lambda v: v.timestamp)
        return versions
    
    def get_history_by_version(self, event_id):
        """按版本顺序获取版本历史
        
        Args:
            event_id: 事件ID
            
        Returns:
            list: 版本实例列表（按版本顺序）
        """
        # 版本顺序与时间顺序一致
        return self.get_history_by_time(event_id)
    
    def get_version_chain(self, version_id):
        """获取版本链
        
        Args:
            version_id: 版本ID
            
        Returns:
            list: 版本实例列表（从当前版本到根版本）
        """
        version_chain = []
        current_version = self.version_manager.get_version(version_id)
        
        while current_version:
            version_chain.append(current_version)
            if not current_version.parent_version_id:
                break
            current_version = self.version_manager.get_version(current_version.parent_version_id)
        
        return version_chain
    
    def get_version_diff(self, version_id1, version_id2):
        """获取两个版本的差异
        
        Args:
            version_id1: 版本1的ID
            version_id2: 版本2的ID
            
        Returns:
            dict: 版本差异
        """
        version1 = self.version_manager.get_version(version_id1)
        version2 = self.version_manager.get_version(version_id2)
        
        if not version1 or not version2:
            return {}
        
        return {
            "version1": {
                "version_id": version1.version_id,
                "timestamp": version1.timestamp,
                "content": version1.content
            },
            "version2": {
                "version_id": version2.version_id,
                "timestamp": version2.timestamp,
                "content": version2.content
            }
        }
    
    def format_history(self, event_id):
        """格式化版本历史
        
        Args:
            event_id: 事件ID
            
        Returns:
            str: 格式化的版本历史
        """
        versions = self.get_history_by_time(event_id)
        if not versions:
            return "暂无版本历史"
        
        history_str = f"事件 {event_id} 的版本历史：\n"
        for i, version in enumerate(versions, 1):
            history_str += f"\n版本 {i} ({version.timestamp}):\n"
            history_str += f"  版本ID: {version.version_id}\n"
            history_str += f"  父版本ID: {version.parent_version_id or '无'}\n"
            history_str += f"  内容: {version.content}\n"
        
        return history_str