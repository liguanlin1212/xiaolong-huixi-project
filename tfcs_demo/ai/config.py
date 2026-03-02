import os
import json
from typing import Dict, Any, Optional

class AIConfig:
    """
    AI配置管理类，支持从环境变量和配置文件加载配置
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化AI配置管理
        
        参数:
            config_file: 配置文件路径，默认使用默认路径
        """
        if config_file is None:
            self.config_file = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "config", "ai_config.json"
            )
        else:
            self.config_file = config_file
        
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置
        
        返回:
            Dict[str, Any]: 配置字典
        """
        # 默认配置
        default_config = {
            "default_model": "NPU",
            "models": {
                "NPU": {
                    "type": "NPU"
                },
                "OPENAI": {
                    "type": "OPENAI",
                    "api_key": os.environ.get("OPENAI_API_KEY", ""),
                    "model_name": "gpt-4o"
                }
            }
        }
        
        # 尝试从配置文件加载
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                # 合并配置
                default_config.update(file_config)
                # 从环境变量覆盖API密钥
                if "OPENAI" in default_config.get("models", {}):
                    env_api_key = os.environ.get("OPENAI_API_KEY")
                    if env_api_key:
                        default_config["models"]["OPENAI"]["api_key"] = env_api_key
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                print("使用默认配置")
        else:
            # 配置文件不存在，使用默认配置
            print(f"配置文件不存在: {self.config_file}")
            print("使用默认配置")
        
        return default_config
    
    def get_default_model(self) -> str:
        """
        获取默认模型
        
        返回:
            str: 默认模型名称
        """
        return self._config.get("default_model", "NPU")
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """
        获取指定模型的配置
        
        参数:
            model_name: 模型名称
            
        返回:
            Dict[str, Any]: 模型配置
        """
        return self._config.get("models", {}).get(model_name, {})
    
    def set_default_model(self, model_name: str) -> None:
        """
        设置默认模型
        
        参数:
            model_name: 模型名称
        """
        self._config["default_model"] = model_name
        self._save_config()
    
    def update_model_config(self, model_name: str, config: Dict[str, Any]) -> None:
        """
        更新模型配置
        
        参数:
            model_name: 模型名称
            config: 模型配置
        """
        if "models" not in self._config:
            self._config["models"] = {}
        self._config["models"][model_name] = config
        self._save_config()
    
    def _save_config(self) -> None:
        """
        保存配置到文件
        """
        try:
            # 确保配置目录存在
            config_dir = os.path.dirname(self.config_file)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
            
            # 保存配置
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def list_models(self) -> list:
        """
        列出所有支持的模型
        
        返回:
            list: 模型名称列表
        """
        return list(self._config.get("models", {}).keys())
    
    def has_api_key(self, model_name: str) -> bool:
        """
        检查模型是否配置了API密钥
        
        参数:
            model_name: 模型名称
            
        返回:
            bool: 是否配置了API密钥
        """
        model_config = self.get_model_config(model_name)
        api_key = model_config.get("api_key", "")
        return bool(api_key)
