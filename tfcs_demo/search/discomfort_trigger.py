import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from search.version_manager import VersionManager
from search.version_history import VersionHistory
from search.case_status_machine import CaseStatusMachine
from search.self_correction import SelfCorrectionMechanism

class DiscomfortTrigger:
    """不适感触发机制"""
    
    def __init__(self, version_manager: VersionManager, version_history: VersionHistory, 
                 case_status_machine: CaseStatusMachine, self_correction: SelfCorrectionMechanism):
        """初始化不适感触发机制
        
        Args:
            version_manager: 版本管理器实例
            version_history: 版本历史实例
            case_status_machine: 案件状态机实例
            self_correction: 自查纠错机制实例
        """
        self.version_manager = version_manager
        self.version_history = version_history
        self.case_status_machine = case_status_machine
        self.self_correction = self_correction
        self.storage_dir = os.path.join(os.path.dirname(__file__), "..", "data", "discomfort")
        os.makedirs(self.storage_dir, exist_ok=True)
        self.triggers_file = os.path.join(self.storage_dir, "triggers.json")
        self.evaluations_file = os.path.join(self.storage_dir, "evaluations.json")
        self._load_triggers()
        self._load_evaluations()
    
    def _load_triggers(self):
        """加载触发记录"""
        if os.path.exists(self.triggers_file):
            try:
                with open(self.triggers_file, "r", encoding="utf-8") as f:
                    self.triggers = json.load(f)
            except Exception as e:
                print(f"加载触发记录失败: {e}")
                self.triggers = {}
        else:
            self.triggers = {}
    
    def _load_evaluations(self):
        """加载评估记录"""
        if os.path.exists(self.evaluations_file):
            try:
                with open(self.evaluations_file, "r", encoding="utf-8") as f:
                    self.evaluations = json.load(f)
            except Exception as e:
                print(f"加载评估记录失败: {e}")
                self.evaluations = {}
        else:
            self.evaluations = {}
    
    def _save_triggers(self):
        """保存触发记录"""
        try:
            with open(self.triggers_file, "w", encoding="utf-8") as f:
                json.dump(self.triggers, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存触发记录失败: {e}")
            return False
    
    def _save_evaluations(self):
        """保存评估记录"""
        try:
            with open(self.evaluations_file, "w", encoding="utf-8") as f:
                json.dump(self.evaluations, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存评估记录失败: {e}")
            return False
    
    def trigger_discomfort(self, event_id: str, version_id: str, 
                         discomfort_level: int, reason: str, 
                         additional_info: Optional[Dict] = None) -> str:
        """触发不适感
        
        Args:
            event_id: 事件ID
            version_id: 版本ID
            discomfort_level: 不适程度 (1-5)
            reason: 不适原因
            additional_info: 附加信息
            
        Returns:
            str: 触发ID
        """
        trigger_id = f"trigger_{datetime.now().isoformat().replace(':', '-')}"
        timestamp = datetime.now().isoformat()
        
        trigger_data = {
            "trigger_id": trigger_id,
            "event_id": event_id,
            "version_id": version_id,
            "timestamp": timestamp,
            "discomfort_level": discomfort_level,
            "reason": reason,
            "additional_info": additional_info or {},
            "status": "pending",  # pending, processing, resolved
            "processed_at": None
        }
        
        if event_id not in self.triggers:
            self.triggers[event_id] = []
        
        self.triggers[event_id].append(trigger_data)
        self._save_triggers()
        
        # 处理触发信号
        self._process_trigger(trigger_id, event_id, version_id, discomfort_level, reason, additional_info)
        
        return trigger_id
    
    def _process_trigger(self, trigger_id: str, event_id: str, version_id: str, 
                        discomfort_level: int, reason: str, additional_info: Optional[Dict] = None):
        """处理触发信号
        
        Args:
            trigger_id: 触发ID
            event_id: 事件ID
            version_id: 版本ID
            discomfort_level: 不适程度
            reason: 不适原因
            additional_info: 附加信息
        """
        # 更新触发状态为处理中
        for trigger in self.triggers.get(event_id, []):
            if trigger["trigger_id"] == trigger_id:
                trigger["status"] = "processing"
                trigger["processed_at"] = datetime.now().isoformat()
                break
        self._save_triggers()
        
        # 重新审视判断
        self._reexamine_judgment(event_id, version_id, reason, additional_info)
        
        # 更新触发状态为已解决
        for trigger in self.triggers.get(event_id, []):
            if trigger["trigger_id"] == trigger_id:
                trigger["status"] = "resolved"
                break
        self._save_triggers()
    
    def _reexamine_judgment(self, event_id: str, version_id: str, 
                           reason: str, additional_info: Optional[Dict] = None):
        """重新审视判断
        
        Args:
            event_id: 事件ID
            version_id: 版本ID
            reason: 不适原因
            additional_info: 附加信息
        """
        # 获取当前版本
        current_version = self.version_manager.get_version(version_id)
        if not current_version:
            return
        
        # 分析不适原因，生成新的信息
        new_information = self._generate_new_information(reason, additional_info, current_version)
        
        # 使用自查纠错机制处理新信息
        if new_information:
            self.self_correction.process_self_correction(new_information)
        
        # 更新案件状态
        latest_version = self.version_manager.get_latest_version(event_id)
        if latest_version:
            # 重新评估案件状态
            self.case_status_machine.get_initial_status({"content": latest_version.content}, event_id)
    
    def _generate_new_information(self, reason: str, additional_info: Optional[Dict], 
                                 current_version: object) -> str:
        """根据不适原因生成新信息
        
        Args:
            reason: 不适原因
            additional_info: 附加信息
            current_version: 当前版本
            
        Returns:
            str: 新信息
        """
        # 简单的新信息生成逻辑
        new_info_parts = [f"用户反馈不适：{reason}"]
        
        if additional_info:
            for key, value in additional_info.items():
                new_info_parts.append(f"{key}：{value}")
        
        new_info_parts.append(f"当前版本内容：{current_version.content}")
        
        return "\n".join(new_info_parts)
    
    def evaluate_trigger_effect(self, trigger_id: str, event_id: str, 
                              effectiveness: int, comments: Optional[str] = None) -> bool:
        """评估触发效果
        
        Args:
            trigger_id: 触发ID
            event_id: 事件ID
            effectiveness: 效果评估 (1-5)
            comments: 评估评论
            
        Returns:
            bool: 是否评估成功
        """
        evaluation_id = f"eval_{datetime.now().isoformat().replace(':', '-')}"
        timestamp = datetime.now().isoformat()
        
        evaluation_data = {
            "evaluation_id": evaluation_id,
            "trigger_id": trigger_id,
            "event_id": event_id,
            "timestamp": timestamp,
            "effectiveness": effectiveness,
            "comments": comments or ""
        }
        
        if event_id not in self.evaluations:
            self.evaluations[event_id] = []
        
        self.evaluations[event_id].append(evaluation_data)
        return self._save_evaluations()
    
    def get_triggers(self, event_id: Optional[str] = None) -> List[Dict]:
        """获取触发记录
        
        Args:
            event_id: 事件ID，不提供则获取所有触发记录
            
        Returns:
            list: 触发记录列表
        """
        if event_id:
            return self.triggers.get(event_id, [])
        else:
            all_triggers = []
            for event_triggers in self.triggers.values():
                all_triggers.extend(event_triggers)
            return all_triggers
    
    def get_evaluations(self, event_id: Optional[str] = None) -> List[Dict]:
        """获取评估记录
        
        Args:
            event_id: 事件ID，不提供则获取所有评估记录
            
        Returns:
            list: 评估记录列表
        """
        if event_id:
            return self.evaluations.get(event_id, [])
        else:
            all_evaluations = []
            for event_evaluations in self.evaluations.values():
                all_evaluations.extend(event_evaluations)
            return all_evaluations
    
    def get_trigger_stats(self) -> Dict:
        """获取触发统计信息
        
        Returns:
            dict: 统计信息
        """
        total_triggers = 0
        resolved_triggers = 0
        discomfort_levels = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for event_triggers in self.triggers.values():
            for trigger in event_triggers:
                total_triggers += 1
                if trigger["status"] == "resolved":
                    resolved_triggers += 1
                discomfort_level = trigger.get("discomfort_level", 0)
                if 1 <= discomfort_level <= 5:
                    discomfort_levels[discomfort_level] += 1
        
        return {
            "total_triggers": total_triggers,
            "resolved_triggers": resolved_triggers,
            "resolution_rate": resolved_triggers / total_triggers if total_triggers > 0 else 0,
            "discomfort_levels": discomfort_levels
        }
    
    def get_evaluation_stats(self) -> Dict:
        """获取评估统计信息
        
        Returns:
            dict: 统计信息
        """
        total_evaluations = 0
        total_effectiveness = 0
        effectiveness_levels = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for event_evaluations in self.evaluations.values():
            for evaluation in event_evaluations:
                total_evaluations += 1
                effectiveness = evaluation.get("effectiveness", 0)
                total_effectiveness += effectiveness
                if 1 <= effectiveness <= 5:
                    effectiveness_levels[effectiveness] += 1
        
        return {
            "total_evaluations": total_evaluations,
            "average_effectiveness": total_effectiveness / total_evaluations if total_evaluations > 0 else 0,
            "effectiveness_levels": effectiveness_levels
        }
