import uuid
from datetime import datetime
import json

class JudgmentVersion:
    """判断版本数据结构"""
    
    def __init__(self, content, parent_version_id=None, version_id=None, timestamp=None):
        """初始化判断版本
        
        Args:
            content: 判断内容
            parent_version_id: 父版本ID
            version_id: 版本ID（如果不提供，会自动生成）
            timestamp: 时间戳（如果不提供，会自动生成）
        """
        self.version_id = version_id or str(uuid.uuid4())
        self.timestamp = timestamp or datetime.now().isoformat()
        self.content = content
        self.parent_version_id = parent_version_id
    
    def to_dict(self):
        """转换为字典
        
        Returns:
            dict: 版本数据字典
        """
        return {
            "version_id": self.version_id,
            "timestamp": self.timestamp,
            "content": self.content,
            "parent_version_id": self.parent_version_id
        }
    
    def to_json(self):
        """转换为JSON字符串
        
        Returns:
            str: JSON字符串
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建版本
        
        Args:
            data: 版本数据字典
            
        Returns:
            JudgmentVersion: 版本实例
        """
        return cls(
            content=data["content"],
            parent_version_id=data.get("parent_version_id"),
            version_id=data.get("version_id"),
            timestamp=data.get("timestamp")
        )
    
    @classmethod
    def from_json(cls, json_str):
        """从JSON字符串创建版本
        
        Args:
            json_str: JSON字符串
            
        Returns:
            JudgmentVersion: 版本实例
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def __repr__(self):
        """字符串表示
        
        Returns:
            str: 字符串表示
        """
        return f"JudgmentVersion(version_id={self.version_id}, timestamp={self.timestamp}, parent_version_id={self.parent_version_id})"