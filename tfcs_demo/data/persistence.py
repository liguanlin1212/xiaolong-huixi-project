import os
import json
import shutil
from typing import Dict, Any, List, Optional
from datetime import datetime
from core.types import Event, JudgementVersion
from core.enums import JudgementStatus

class DataPersistence:
    """
    数据持久化类，负责数据的保存和加载
    """
    
    def __init__(self, data_dir: str = None):
        """
        初始化数据持久化
        
        参数:
            data_dir: 数据存储目录
        """
        if data_dir is None:
            self.data_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "data"
            )
        else:
            self.data_dir = data_dir
        
        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 数据文件路径
        self.events_file = os.path.join(self.data_dir, "events.json")
        self.judgements_file = os.path.join(self.data_dir, "judgements.json")
        self.versions_file = os.path.join(self.data_dir, "versions.json")
        
        # 初始化数据文件
        self._initialize_files()
    
    def _initialize_files(self):
        """
        初始化数据文件
        """
        for file_path in [self.events_file, self.judgements_file, self.versions_file]:
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
    
    def save_event(self, event: Event) -> bool:
        """
        保存事件
        
        参数:
            event: 事件对象
            
        返回:
            bool: 是否保存成功
        """
        try:
            # 读取现有事件
            with open(self.events_file, "r", encoding="utf-8") as f:
                events = json.load(f)
            
            # 保存事件
            events[event.event_id] = event.to_dict()
            
            # 写回文件
            with open(self.events_file, "w", encoding="utf-8") as f:
                json.dump(events, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存事件失败: {e}")
            return False
    
    def load_event(self, event_id: str) -> Optional[Event]:
        """
        加载事件
        
        参数:
            event_id: 事件ID
            
        返回:
            Optional[Event]: 事件对象
        """
        try:
            with open(self.events_file, "r", encoding="utf-8") as f:
                events = json.load(f)
            
            if event_id in events:
                event_data = events[event_id]
                # 转换状态
                status = None
                if event_data.get("status"):
                    status = JudgementStatus(event_data["status"])
                
                return Event(
                    event_id=event_data["event_id"],
                    title=event_data["title"],
                    description=event_data["description"],
                    start_time=event_data["start_time"],
                    end_time=event_data.get("end_time"),
                    judgement_ids=event_data.get("judgement_ids", []),
                    metadata=event_data.get("metadata"),
                    status=status
                )
            return None
        except Exception as e:
            print(f"加载事件失败: {e}")
            return None
    
    def load_all_events(self) -> List[Event]:
        """
        加载所有事件
        
        返回:
            List[Event]: 事件列表
        """
        try:
            with open(self.events_file, "r", encoding="utf-8") as f:
                events = json.load(f)
            
            event_list = []
            for event_data in events.values():
                # 转换状态
                status = None
                if event_data.get("status"):
                    status = JudgementStatus(event_data["status"])
                
                event = Event(
                    event_id=event_data["event_id"],
                    title=event_data["title"],
                    description=event_data["description"],
                    start_time=event_data["start_time"],
                    end_time=event_data.get("end_time"),
                    judgement_ids=event_data.get("judgement_ids", []),
                    metadata=event_data.get("metadata"),
                    status=status
                )
                event_list.append(event)
            
            return event_list
        except Exception as e:
            print(f"加载所有事件失败: {e}")
            return []
    
    def save_judgement_version(self, version: JudgementVersion) -> bool:
        """
        保存判断版本
        
        参数:
            version: 判断版本对象
            
        返回:
            bool: 是否保存成功
        """
        try:
            # 读取现有版本
            with open(self.versions_file, "r", encoding="utf-8") as f:
                versions = json.load(f)
            
            # 保存版本
            versions[version.version_id] = version.to_dict()
            
            # 写回文件
            with open(self.versions_file, "w", encoding="utf-8") as f:
                json.dump(versions, f, ensure_ascii=False, indent=2)
            
            # 更新判断ID到版本ID的映射
            self._update_judgement_mapping(version)
            
            return True
        except Exception as e:
            print(f"保存判断版本失败: {e}")
            return False
    
    def _update_judgement_mapping(self, version: JudgementVersion):
        """
        更新判断ID到版本ID的映射
        
        参数:
            version: 判断版本对象
        """
        try:
            with open(self.judgements_file, "r", encoding="utf-8") as f:
                judgements = json.load(f)
            
            if version.judgement_id not in judgements:
                judgements[version.judgement_id] = {
                    "version_ids": [],
                    "latest_version": version.version_id
                }
            else:
                if version.version_id not in judgements[version.judgement_id]["version_ids"]:
                    judgements[version.judgement_id]["version_ids"].append(version.version_id)
                judgements[version.judgement_id]["latest_version"] = version.version_id
            
            with open(self.judgements_file, "w", encoding="utf-8") as f:
                json.dump(judgements, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"更新判断映射失败: {e}")
    
    def load_judgement_version(self, version_id: str) -> Optional[JudgementVersion]:
        """
        加载判断版本
        
        参数:
            version_id: 版本ID
            
        返回:
            Optional[JudgementVersion]: 判断版本对象
        """
        try:
            with open(self.versions_file, "r", encoding="utf-8") as f:
                versions = json.load(f)
            
            if version_id in versions:
                version_data = versions[version_id]
                # 转换状态
                status = JudgementStatus(version_data["status"])
                
                return JudgementVersion(
                    version_id=version_data["version_id"],
                    judgement_id=version_data["judgement_id"],
                    event_id=version_data.get("event_id"),
                    content=version_data["content"],
                    status=status,
                    created_at=version_data["created_at"],
                    previous_version_id=version_data.get("previous_version_id"),
                    metadata=version_data.get("metadata")
                )
            return None
        except Exception as e:
            print(f"加载判断版本失败: {e}")
            return None
    
    def load_latest_judgement_version(self, judgement_id: str) -> Optional[JudgementVersion]:
        """
        加载最新的判断版本
        
        参数:
            judgement_id: 判断ID
            
        返回:
            Optional[JudgementVersion]: 判断版本对象
        """
        try:
            with open(self.judgements_file, "r", encoding="utf-8") as f:
                judgements = json.load(f)
            
            if judgement_id in judgements:
                latest_version_id = judgements[judgement_id]["latest_version"]
                return self.load_judgement_version(latest_version_id)
            return None
        except Exception as e:
            print(f"加载最新判断版本失败: {e}")
            return None
    
    def load_all_judgement_versions(self, judgement_id: str) -> List[JudgementVersion]:
        """
        加载判断的所有版本
        
        参数:
            judgement_id: 判断ID
            
        返回:
            List[JudgementVersion]: 版本列表
        """
        try:
            with open(self.judgements_file, "r", encoding="utf-8") as f:
                judgements = json.load(f)
            
            if judgement_id in judgements:
                version_ids = judgements[judgement_id]["version_ids"]
                versions = []
                for version_id in version_ids:
                    version = self.load_judgement_version(version_id)
                    if version:
                        versions.append(version)
                return versions
            return []
        except Exception as e:
            print(f"加载所有判断版本失败: {e}")
            return []
    
    def backup_data(self, backup_dir: str = None) -> bool:
        """
        备份数据
        
        参数:
            backup_dir: 备份目录
            
        返回:
            bool: 是否备份成功
        """
        try:
            if backup_dir is None:
                # 生成备份目录名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_dir = os.path.join(self.data_dir, f"backup_{timestamp}")
            
            # 确保备份目录存在
            os.makedirs(backup_dir, exist_ok=True)
            
            # 备份文件
            for file_path in [self.events_file, self.judgements_file, self.versions_file]:
                if os.path.exists(file_path):
                    backup_file = os.path.join(backup_dir, os.path.basename(file_path))
                    shutil.copy2(file_path, backup_file)
            
            print(f"数据备份成功: {backup_dir}")
            return True
        except Exception as e:
            print(f"备份数据失败: {e}")
            return False
    
    def restore_data(self, backup_dir: str) -> bool:
        """
        恢复数据
        
        参数:
            backup_dir: 备份目录
            
        返回:
            bool: 是否恢复成功
        """
        try:
            # 验证备份目录是否存在
            if not os.path.exists(backup_dir):
                print(f"备份目录不存在: {backup_dir}")
                return False
            
            # 恢复文件
            for file_name in ["events.json", "judgements.json", "versions.json"]:
                backup_file = os.path.join(backup_dir, file_name)
                target_file = os.path.join(self.data_dir, file_name)
                
                if os.path.exists(backup_file):
                    shutil.copy2(backup_file, target_file)
                else:
                    print(f"备份文件不存在: {backup_file}")
                    return False
            
            print(f"数据恢复成功: {backup_dir}")
            return True
        except Exception as e:
            print(f"恢复数据失败: {e}")
            return False

# 全局数据持久化实例
data_persistence = DataPersistence()
