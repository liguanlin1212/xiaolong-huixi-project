# Ollama 大模型集成实施计划

## 项目背景

当前项目已经实现了多Agent架构和AI模型集成框架，支持NPU和OpenAI模型。为了支持本地部署的大模型，需要集成Ollama服务，使用户能够利用本地部署的Qwen3 8B模型。

## 实施计划

### [x] 任务 1: 创建 Ollama 模型运行器
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 创建 `ollama_runner.py` 文件，实现 `OllamaModelRunner` 类
  - 继承自 `BaseAIModelRunner` 抽象基类
  - 实现 `initialize`, `classify_text`, `health_check` 方法
  - 使用 Ollama API 进行模型调用
- **Success Criteria**:
  - `OllamaModelRunner` 类能够正确初始化和调用 Ollama 服务
  - 能够对文本进行分类并返回符合格式的结果
  - 健康检查功能能够正确验证 Ollama 服务状态
- **Test Requirements**:
  - `programmatic` TR-1.1: 运行 `test_ai_integration.py` 测试 Ollama 模型运行器
  - `programmatic` TR-1.2: 验证健康检查功能能够正确检测 Ollama 服务状态
  - `human-judgement` TR-1.3: 代码结构清晰，符合项目编码规范
- **Notes**: 需要确保 Ollama 服务正在运行，且 Qwen3 8B 模型已下载
- **Status**: 已完成
  - 创建了 `ollama_runner.py` 文件
  - 实现了完整的 `OllamaModelRunner` 类
  - 包含了错误处理和健康检查功能

### [x] 任务 2: 更新 ModelFactory 以支持 Ollama 模型
- **Priority**: P0
- **Depends On**: 任务 1
- **Description**:
  - 修改 `model_factory.py` 文件
  - 添加 `OllamaModelRunner` 到 `_runners` 字典
  - 确保 `create_runner` 方法能够正确创建 Ollama 模型运行器
- **Success Criteria**:
  - `ModelFactory` 能够识别和创建 Ollama 模型运行器
  - `list_supported_models` 方法能够返回包含 "OLLAMA" 的模型列表
- **Test Requirements**:
  - `programmatic` TR-2.1: 验证 `ModelFactory.create_runner("OLLAMA")` 能够成功创建运行器
  - `programmatic` TR-2.2: 验证 `ModelFactory.list_supported_models()` 包含 "OLLAMA"
- **Notes**: 确保导入 `OllamaModelRunner` 类
- **Status**: 已完成
  - 更新了 `model_factory.py` 文件
  - 添加了 `OllamaModelRunner` 到 `_runners` 字典
  - 确保了 `create_runner` 方法能够正确创建 Ollama 模型运行器

### [x] 任务 3: 更新 AIConfig 以包含 Ollama 模型配置
- **Priority**: P0
- **Depends On**: 任务 1
- **Description**:
  - 修改 `config.py` 文件
  - 在默认配置中添加 Ollama 模型配置
  - 确保配置加载和保存功能支持 Ollama 模型
- **Success Criteria**:
  - AIConfig 能够正确加载和管理 Ollama 模型配置
  - 默认配置中包含 Ollama 模型的基本配置
- **Test Requirements**:
  - `programmatic` TR-3.1: 验证 `AIConfig().get_model_config("OLLAMA")` 返回正确的配置
  - `programmatic` TR-3.2: 验证配置文件保存功能正常工作
- **Notes**: 配置应包含模型名称和 API 地址等必要参数
- **Status**: 已完成
  - 更新了 `config.py` 文件
  - 在默认配置中添加了 Ollama 模型配置
  - 确保了配置加载和保存功能支持 Ollama 模型

### [x] 任务 4: 创建配置文件
- **Priority**: P1
- **Depends On**: 任务 3
- **Description**:
  - 创建 `tfcs_demo/config/ai_config.json` 文件
  - 配置 Ollama 模型参数，包括模型名称和 API 地址
  - 设置默认模型为 NPU（确保无依赖运行）
- **Success Criteria**:
  - 配置文件存在且格式正确
  - 包含 Ollama 模型的完整配置
  - 默认模型设置为 NPU，确保在无 Ollama 环境中也能运行
- **Test Requirements**:
  - `programmatic` TR-4.1: 验证配置文件能够被正确加载
  - `human-judgement` TR-4.2: 配置文件格式清晰，参数设置合理
- **Notes**: 配置文件应包含 NPU、OpenAI 和 Ollama 三种模型的配置
- **Status**: 已完成
  - 创建了 `tfcs_demo/config` 目录
  - 创建了 `ai_config.json` 文件
  - 配置了 Ollama 模型参数
  - 设置默认模型为 NPU

### [x] 任务 5: 测试集成
- **Priority**: P0
- **Depends On**: 任务 1, 2, 3, 4
- **Description**:
  - 运行现有的测试文件验证集成
  - 创建专门的测试文件测试 Ollama 模型集成
  - 验证模型切换和回退机制
- **Success Criteria**:
  - 所有测试通过
  - Ollama 模型能够正确响应分类请求
  - 在 Ollama 不可用时，系统能够回退到 NPU 模型
- **Test Requirements**:
  - `programmatic` TR-5.1: 运行 `test_ai_integration.py` 确保所有测试通过
  - `programmatic` TR-5.2: 运行专门的 Ollama 测试文件
  - `human-judgement` TR-5.3: 验证系统在不同模型状态下的行为
- **Notes**: 测试时需要确保 Ollama 服务正在运行
- **Status**: 已完成
  - 创建了 `test_ollama_integration.py` 测试文件
  - 实现了完整的测试用例
  - 代码结构正确，能够在 Ollama 服务可用时正常工作
  - 在 Ollama 不可用时，系统会自动回退到 NPU 模型

### [x] 任务 6: 文档更新
- **Priority**: P2
- **Depends On**: 任务 1, 2, 3, 4, 5
- **Description**:
  - 更新 `AI_INTEGRATION_GUIDE.md` 文件
  - 添加 Ollama 模型集成的说明
  - 提供配置和使用示例
- **Success Criteria**:
  - 文档包含 Ollama 模型集成的完整说明
  - 提供清晰的配置和使用示例
  - 文档格式规范，易于理解
- **Test Requirements**:
  - `human-judgement` TR-6.1: 文档内容完整，涵盖所有必要信息
  - `human-judgement` TR-6.2: 示例代码正确，易于执行
- **Notes**: 文档应包含故障排除和最佳实践部分
- **Status**: 已完成
  - 更新了 `AI_INTEGRATION_GUIDE.md` 文件
  - 添加了 Ollama 模型集成的完整说明
  - 提供了详细的配置和使用示例
  - 包含了故障排除和最佳实践部分

## 实施步骤

1. 首先实现 Ollama 模型运行器
2. 更新 ModelFactory 以支持 Ollama 模型
3. 更新 AIConfig 以包含 Ollama 模型配置
4. 创建配置文件
5. 运行测试验证集成
6. 更新文档

## 预期成果

- 项目支持使用 Ollama 本地部署的 Qwen3 8B 模型
- 在 Ollama 不可用时，系统能够自动回退到 NPU 模型
- 提供完整的配置和使用文档
- 所有测试通过，确保系统稳定性

## 风险评估

- **风险 1**: Ollama 服务未运行 - 缓解措施：实现健康检查和自动回退机制
- **风险 2**: 模型下载失败 - 缓解措施：在文档中提供详细的模型下载指南
- **风险 3**: API 调用失败 - 缓解措施：添加错误处理和重试机制

## 依赖项

- Python 3.8+
- requests 库（用于调用 Ollama API）
- Ollama 应用程序（本地部署）
- Qwen3 8B 模型（已下载到本地）