import uuid
from typing import List, Optional, Dict, Any
from core.types import JudgementVersion
from core.enums import JudgementStatus

class VersionService:
    def __init__(self):
        self._versions: Dict[str, JudgementVersion] = {}
        self._judgement_latest: Dict[str, str] = {}
    
    def create_new_version(
        self,
        judgement_id: str,
        content: Dict[str, Any],
        status: JudgementStatus,
        previous_version: Optional[JudgementVersion] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> JudgementVersion:
        """
        创建新版本，确保新版本指向旧版本
        """
        version_id = str(uuid.uuid4())
        created_at = "2026-02-19T" + str(uuid.uuid4())[:8] + ".000Z"
        
        previous_version_id = previous_version.version_id if previous_version else None
        
        new_version = JudgementVersion(
            version_id=version_id,
            judgement_id=judgement_id,
            content=content,
            status=status,
            created_at=created_at,
            previous_version_id=previous_version_id,
            metadata=metadata
        )
        
        # 存储版本
        self._versions[version_id] = new_version
        
        # 更新最新版本记录
        self._judgement_latest[judgement_id] = version_id
        
        return new_version
    
    def get_version_history(self, judgement_id: str) -> List[JudgementVersion]:
        """
        获取判断的完整版本历史，按时间倒序排列
        """
        if judgement_id not in self._judgement_latest:
            return []
        
        history = []
        current_version_id = self._judgement_latest[judgement_id]
        
        while current_version_id:
            if current_version_id not in self._versions:
                break
            
            version = self._versions[current_version_id]
            history.append(version)
            
            current_version_id = version.previous_version_id
        
        return history
    
    def get_latest_version(self, judgement_id: str) -> Optional[JudgementVersion]:
        """
        获取判断的最新版本
        """
        if judgement_id not in self._judgement_latest:
            return None
        
        latest_version_id = self._judgement_latest[judgement_id]
        return self._versions.get(latest_version_id)
    
    def validate_version_chain(self, version: JudgementVersion) -> bool:
        """
        验证版本链的完整性
        """
        seen_versions = set()
        current_version = version
        
        while current_version:
            if current_version.version_id in seen_versions:
                return False  # 循环引用
            
            seen_versions.add(current_version.version_id)
            
            if not current_version.previous_version_id:
                break
            
            next_version = self._versions.get(current_version.previous_version_id)
            if not next_version:
                return False  # 版本链断裂
            
            current_version = next_version
        
        return True
    
    def get_version(self, version_id: str) -> Optional[JudgementVersion]:
        """
        根据版本ID获取特定版本
        """
        return self._versions.get(version_id)

# 全局版本服务实例
version_service = VersionService()
