import pytest
import os
import tempfile
from search.version_data_structure import JudgmentVersion
from search.version_manager import VersionManager
from search.version_storage import VersionStorage
from search.version_history import VersionHistory

class TestVersionControl:
    def setup_method(self):
        # 初始化版本控制组件
        self.version_manager = VersionManager()
        self.version_storage = VersionStorage()
        self.version_history = VersionHistory(self.version_manager)
    
    def teardown_method(self):
        # 清理版本数据
        self.version_storage.delete_versions()
    
    def test_judgment_version_creation(self):
        """测试创建判断版本实例"""
        content = "Test judgment content"
        parent_version_id = "parent-123"
        
        # 创建版本
        version = JudgmentVersion(content, parent_version_id)
        
        # 验证属性
        assert version.content == content
        assert version.parent_version_id == parent_version_id
        assert version.version_id is not None
        assert version.timestamp is not None
    
    def test_version_manager_create_version(self):
        """测试版本管理器创建版本"""
        event_id = "event-1"
        content = "Initial version"
        
        # 创建版本
        version = self.version_manager.create_version(event_id, content)
        
        # 验证版本创建
        assert version is not None
        assert version.content == content
        assert version.parent_version_id is None
        
        # 验证版本被存储
        versions = self.version_manager.get_versions(event_id)
        assert len(versions) == 1
        assert versions[0].version_id == version.version_id
    
    def test_version_manager_update_version(self):
        """测试版本管理器更新版本（创建新版本）"""
        event_id = "event-2"
        content1 = "Version 1"
        content2 = "Version 2"
        
        # 创建第一个版本
        version1 = self.version_manager.create_version(event_id, content1)
        
        # 更新版本（创建第二个版本）
        version2 = self.version_manager.update_version(event_id, content2)
        
        # 验证新版本指向旧版本
        assert version2.parent_version_id == version1.version_id
        assert version2.content == content2
        
        # 验证两个版本都存在
        versions = self.version_manager.get_versions(event_id)
        assert len(versions) == 2
    
    def test_version_manager_get_latest_version(self):
        """测试获取最新版本"""
        event_id = "event-3"
        content1 = "Version 1"
        content2 = "Version 2"
        
        # 创建两个版本
        version1 = self.version_manager.create_version(event_id, content1)
        version2 = self.version_manager.create_version(event_id, content2, version1.version_id)
        
        # 获取最新版本
        latest_version = self.version_manager.get_latest_version(event_id)
        
        # 验证最新版本是第二个版本
        assert latest_version.version_id == version2.version_id
    
    def test_version_storage_save_and_load(self):
        """测试版本存储和加载"""
        event_id = "event-4"
        content = "Test content"
        
        # 创建版本
        version = self.version_manager.create_version(event_id, content)
        
        # 保存版本
        self.version_storage.save_versions(self.version_manager)
        
        # 创建新的版本管理器并加载
        new_version_manager = VersionManager()
        self.version_storage.load_versions(new_version_manager)
        
        # 验证加载成功
        loaded_versions = new_version_manager.get_versions(event_id)
        assert len(loaded_versions) == 1
        assert loaded_versions[0].version_id == version.version_id
        assert loaded_versions[0].content == content
    
    def test_version_history_get_history_by_time(self):
        """测试按时间获取版本历史"""
        event_id = "event-5"
        
        # 创建多个版本
        version1 = self.version_manager.create_version(event_id, "Version 1")
        # 等待一点时间确保时间戳不同
        import time
        time.sleep(0.1)
        version2 = self.version_manager.create_version(event_id, "Version 2", version1.version_id)
        time.sleep(0.1)
        version3 = self.version_manager.create_version(event_id, "Version 3", version2.version_id)
        
        # 按时间获取历史
        history = self.version_history.get_history_by_time(event_id)
        
        # 验证历史顺序（从旧到新）
        assert len(history) == 3
        assert history[0].version_id == version1.version_id
        assert history[1].version_id == version2.version_id
        assert history[2].version_id == version3.version_id
    
    def test_version_history_get_version_chain(self):
        """测试获取版本链"""
        event_id = "event-6"
        
        # 创建版本链
        version1 = self.version_manager.create_version(event_id, "Version 1")
        version2 = self.version_manager.create_version(event_id, "Version 2", version1.version_id)
        version3 = self.version_manager.create_version(event_id, "Version 3", version2.version_id)
        
        # 获取版本链
        chain = self.version_history.get_version_chain(version3.version_id)
        
        # 验证版本链顺序（从新到旧）
        assert len(chain) == 3
        assert chain[0].version_id == version3.version_id
        assert chain[1].version_id == version2.version_id
        assert chain[2].version_id == version1.version_id
    
    def test_version_history_get_version_diff(self):
        """测试获取版本差异"""
        event_id = "event-7"
        content1 = "Version 1: Initial content"
        content2 = "Version 2: Updated content"
        
        # 创建两个版本
        version1 = self.version_manager.create_version(event_id, content1)
        version2 = self.version_manager.create_version(event_id, content2, version1.version_id)
        
        # 获取差异
        diff = self.version_history.get_version_diff(version1.version_id, version2.version_id)
        
        # 验证差异字典结构
        assert "version1" in diff
        assert "version2" in diff
        assert diff["version1"]["content"] == content1
        assert diff["version2"]["content"] == content2
