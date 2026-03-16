# AI调用和大模型接入指南

## 项目结构

```
tfcs_demo/
  ai/
    inference/
      __init__.py
      base_runner.py      # AI模型运行器抽象基类
      npu_runner.py       # 基于规则的NPU运行器
      openai_runner.py    # OpenAI模型运行器
      model_factory.py    # 模型工厂类
    config.py             # AI配置管理
    schema.py             # AI数据结构定义
    __init__.py
  app/
    services/
      narrative_service.py  # 叙事服务
  test_ai_integration.py  # AI集成测试
  requirements.txt        # 依赖项
```

## 功能说明

### 1. AI调用抽象接口

创建了`BaseAIModelRunner`抽象基类，定义了统一的接口规范，包括：
- `classify_text(text: str)`: 对文本进行分类
- `initialize(**kwargs)`: 初始化模型运行器
- `health_check()`: 健康检查，验证模型是否可以正常工作

### 2. 大模型接入

实现了`OpenAIModelRunner`类，支持使用OpenAI的大模型进行文本分类：
- 支持配置API密钥和模型名称
- 使用OpenAI的Chat Completions API进行文本分类
- 提供健康检查功能，验证模型是否可以正常工作

### 3. 配置管理

创建了`AIConfig`类，支持加载、保存和管理不同大模型的配置：
- 支持从配置文件加载配置
- 支持从环境变量加载API密钥
- 支持设置默认模型
- 支持更新和保存配置

### 4. 模型工厂

创建了`ModelFactory`类，用于根据配置选择不同的AI模型运行器：
- 支持创建NPU模型运行器
- 支持创建OpenAI模型运行器
- 支持列出所有支持的模型类型

### 5. 向后兼容

修改了现有的`classify_text`函数，使其：
- 支持根据配置选择不同的AI模型运行器
- 保持向后兼容，默认使用NPU模型
- 在发生错误时使用NPU作为备用

## 安装和配置

### 1. 安装依赖项

```bash
pip install -r requirements.txt
```

### 2. 配置OpenAI API密钥

有两种方式配置OpenAI API密钥：

#### 方式1：环境变量

```bash
# Windows
setset OPENAI_API_KEY=your_api_key

# Linux/Mac
export OPENAI_API_KEY=your_api_key
```

#### 方式2：配置文件

创建`tfcs_demo/config/ai_config.json`文件，内容如下：

```json
{
  "default_model": "OPENAI",
  "models": {
    "NPU": {
      "type": "NPU"
    },
    "OPENAI": {
      "type": "OPENAI",
      "api_key": "your_api_key",
      "model_name": "gpt-4o"
    }
  }
}
```

## 使用示例

### 1. 使用默认模型

```python
from ai.inference.npu_runner import classify_text

# 使用默认模型（配置中的default_model）
result = classify_text("我真的很可怜，失去了妈妈")
print(result)  # 输出: {"label": "EMOTIONAL", "confidence": 1.0}
```

### 2. 指定模型

```python
from ai.inference.npu_runner import classify_text

# 使用NPU模型
npu_result = classify_text("有聊天记录作为证据", model_name="NPU")
print(npu_result)  # 输出: {"label": "EVIDENCE", "confidence": 1.0}

# 使用OpenAI模型（如果配置了API密钥）
openai_result = classify_text("法院判决他承担刑事责任", model_name="OPENAI")
print(openai_result)  # 输出: {"label": "LEGAL", "confidence": 0.95}
```

### 3. 使用模型工厂

```python
from ai.inference.model_factory import ModelFactory
from ai.config import AIConfig

config = AIConfig()

# 创建NPU模型
npu_runner = ModelFactory.create_runner("NPU")
npu_result = npu_runner.classify_text("我真的很可怜，失去了妈妈")
print(npu_result)  # 输出: {"label": "EMOTIONAL", "confidence": 1.0}

# 创建OpenAI模型（如果配置了API密钥）
openai_config = config.get_model_config("OPENAI")
if openai_config.get("api_key"):
    openai_runner = ModelFactory.create_runner("OPENAI", **openai_config)
    openai_result = openai_runner.classify_text("法院判决他承担刑事责任")
    print(openai_result)  # 输出: {"label": "LEGAL", "confidence": 0.95}
```

## 测试

运行测试文件：

```bash
python test_ai_integration.py
```

测试文件会验证以下功能：
1. 默认模型（NPU）的分类功能
2. 配置管理功能
3. 模型工厂的创建和管理功能
4. 不同模型的分类结果比较

## 故障排除

### 1. OpenAI API密钥错误

如果收到OpenAI API密钥错误，请确保：
- 已正确配置API密钥
- API密钥有效且有足够的配额
- 网络连接正常

### 2. 模型创建失败

如果模型创建失败，请检查：
- 模型类型是否正确
- 配置参数是否完整
- 依赖项是否已安装

### 3. 分类结果不准确

如果分类结果不准确，可以：
- 调整OpenAI模型的提示词
- 尝试使用不同的OpenAI模型（如gpt-4-turbo）
- 增加训练数据，改进NPU模型的规则

## 扩展

### 添加新的大模型

要添加新的大模型，需要：
1. 创建一个新的模型运行器类，继承自`BaseAIModelRunner`
2. 实现`classify_text`、`initialize`和`health_check`方法
3. 在`ModelFactory`中注册新模型
4. 在配置文件中添加新模型的配置

### Ollama模型集成

本项目已集成Ollama模型支持，使用本地部署的大模型进行文本分类：

#### 配置Ollama模型

在`tfcs_demo/config/ai_config.json`文件中添加Ollama模型配置：

```json
{
  "default_model": "NPU",
  "models": {
    "NPU": {
      "type": "NPU"
    },
    "OPENAI": {
      "type": "OPENAI",
      "api_key": "your_api_key",
      "model_name": "gpt-4o"
    },
    "OLLAMA": {
      "type": "OLLAMA",
      "model_name": "qwen3:8b",
      "base_url": "http://localhost:11434/api",
      "timeout": 30
    }
  }
}
```

#### 使用Ollama模型

```python
from ai.inference.npu_runner import classify_text

# 使用Ollama模型
ollama_result = classify_text("法院判决他承担刑事责任", model_name="OLLAMA")
print(ollama_result)  # 输出: {"label": "LEGAL", "confidence": 0.85}
```

#### 使用模型工厂

```python
from ai.inference.model_factory import ModelFactory
from ai.config import AIConfig

config = AIConfig()

# 创建Ollama模型
ollama_config = config.get_model_config("OLLAMA")
ollama_runner = ModelFactory.create_runner("OLLAMA", **ollama_config)
ollama_result = ollama_runner.classify_text("法院判决他承担刑事责任")
print(ollama_result)  # 输出: {"label": "LEGAL", "confidence": 0.85}
```

#### 前提条件

使用Ollama模型需要：
1. 安装并运行Ollama应用程序
2. 下载所需的模型（如qwen3:8b）
3. 确保Ollama服务在http://localhost:11434/api可用

#### 故障排除

如果Ollama模型调用失败：
1. 确保Ollama应用程序正在运行
2. 验证模型名称是否正确
3. 检查网络连接和API地址
4. 查看Ollama应用程序日志

### 添加其他模型

例如，添加Anthropic模型：

```python
# ai/inference/anthropic_runner.py
from typing import Dict, Any
from .base_runner import BaseAIModelRunner

class AnthropicModelRunner(BaseAIModelRunner):
    def initialize(self, **kwargs) -> None:
        # 初始化Anthropic模型
        pass
    
    def classify_text(self, text: str) -> Dict[str, Any]:
        # 使用Anthropic模型进行分类
        pass
    
    def health_check(self) -> bool:
        # 健康检查
        pass

# ai/inference/model_factory.py
from .anthropic_runner import AnthropicModelRunner

class ModelFactory:
    _runners = {
        "NPU": NPURunner,
        "OPENAI": OpenAIModelRunner,
        "OLLAMA": OllamaModelRunner,
        "ANTHROPIC": AnthropicModelRunner
    }
    # 其他代码不变
```

### 调整分类逻辑

要调整分类逻辑，可以：
1. 修改OpenAI模型的提示词，提高分类准确性
2. 调整NPU模型的关键词规则
3. 添加新的分类特征和算法

## 总结

本项目实现了AI调用和大模型接入的核心功能，包括：
- 统一的AI调用抽象接口
- OpenAI模型的接入
- 配置管理和模型工厂
- 向后兼容的API设计

这些功能为项目提供了灵活、可扩展的AI能力，支持不同场景下的文本分类需求。