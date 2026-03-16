# 事实校正系统技术文档

## 1. 项目概述

事实校正系统（Temporal Fact Correction System）是一个专注于记录和追踪事实判断在时间维度上演变的系统。它不以事件本身为研究对象，而是以围绕事件形成的事实判断、叙事结构、共识性认知，以及这些判断在时间中的被修正过程作为核心记录单元。

### 1.1 系统目标

- 记录"判断如何失败"
- 展示认知演变的时间轴
- 提供非个性化的世界快照
- 集中展示近期被修正的判断
- 保存具有代表性的认知失败案例

### 1.2 技术栈

- **后端**：Python 3.8+
- **前端**：Streamlit
- **AI 集成**：OpenAI API、Ollama
- **依赖管理**：pip
- **测试**：pytest

## 2. 系统架构

### 2.1 整体架构

系统分为两大层：
- **用户可见的显性板块**：包括世界快照、认知演变时间轴、近期错误说法展示、认知失败档案
- **系统级隐性板块**：包括判断版本控制系统、自查纠错机制、不适感触发机制、判断结案状态机

### 2.2 核心模块

#### 2.2.1 搜索模块
- **SearchHandler**：处理搜索查询，管理搜索缓存
- **SearchPromptBuilder**：构建大模型搜索指令
- **SearchAnalyzer**：分析搜索结果
- **CaseStatusChecker**：检查事件结案状态

#### 2.2.2 AI 集成模块
- **ModelFactory**：创建不同类型的 AI 模型运行器
- **BaseRunner**：AI 模型运行器基类
- **OpenAI_Runner**：OpenAI API 集成
- **OllamaRunner**：Ollama 本地模型集成
- **NPU_Runner**：NPU 模型集成

#### 2.2.3 版本控制模块
- **VersionManager**：管理判断版本
- **VersionStorage**：存储版本信息
- **VersionHistory**：记录版本历史

#### 2.2.4 自查纠错模块
- **SelfCorrectionMechanism**：处理自查纠错逻辑

#### 2.2.5 不适感触发模块
- **DiscomfortTrigger**：处理用户不适感反馈

#### 2.2.6 结案状态模块
- **CaseStatusMachine**：管理事件结案状态
- **CaseStatusRules**：定义结案状态规则

#### 2.2.7 前端模块
- **SearchUI**：搜索界面
- **ExploreUI**：事件探索界面
- **TimelineView**：时间轴可视化
- **SnapshotView**：世界快照
- **FalseClaimsView**：错误说法展示
- **FailureArchiveView**：认知失败档案

## 3. 核心功能

### 3.1 全网搜索
- 接收用户搜索查询
- 调用大模型进行搜索
- 分析搜索结果
- 过滤未结案事件
- 创建判断版本
- 保存搜索缓存

### 3.2 事件探索
- 按领域分类展示事件
- 提供事件详情查看

### 3.3 自查纠错
- 接收新信息输入
- 分析新信息对现有判断的影响
- 生成纠错建议
- 执行自动纠错

### 3.4 不适感反馈
- 接收用户不适感反馈
- 触发系统重新审视判断
- 提供反馈统计信息

### 3.5 时间轴可视化
- 展示事件在时间维度上的演变
- 显示判断的变化过程

### 3.6 世界快照
- 展示某一时间点的主流判断集合
- 提供当时的判断依据

### 3.7 错误说法展示
- 集中展示近期被证明是错的说法
- 提供修正依据和当前状态

### 3.8 认知失败档案
- 长期保存具有代表性的认知失败案例
- 分析错误成因和修正代价

## 4. API 设计

### 4.1 内部 API

#### 4.1.1 搜索 API
- **process_query(query)**：处理搜索查询
- **save_cache_result(query, results)**：保存搜索缓存
- **get_cache_result(query)**：获取缓存结果

#### 4.1.2 AI 模型 API
- **create_runner(model_type)**：创建 AI 模型运行器
- **classify_text(prompt)**：使用 AI 模型分类文本

#### 4.1.3 版本控制 API
- **create_version(event_id, content)**：创建判断版本
- **get_version(event_id, version_id)**：获取特定版本
- **get_all_versions(event_id)**：获取所有版本

#### 4.1.4 自查纠错 API
- **process_self_correction(new_information)**：处理自查纠错

#### 4.1.5 不适感触发 API
- **trigger_discomfort(event_id, version_id, level, reason, info)**：触发不适感
- **get_trigger_stats()**：获取触发统计信息
- **get_evaluation_stats()**：获取评估统计信息

#### 4.1.6 结案状态 API
- **get_initial_status(result, event_id)**：获取初始状态
- **get_rejection_message(result)**：获取拒绝消息

### 4.2 前端 API

#### 4.2.1 搜索 UI
- **display()**：显示搜索界面
- **display_results(results)**：显示搜索结果

#### 4.2.2 探索 UI
- **display()**：显示探索界面

#### 4.2.3 时间轴视图
- **display(data)**：显示时间轴

#### 4.2.4 快照视图
- **display()**：显示世界快照

#### 4.2.5 错误说法视图
- **display()**：显示错误说法

#### 4.2.6 失败档案视图
- **display()**：显示认知失败档案

## 5. 数据结构

### 5.1 事件数据结构

```python
{
    "title": str,  # 事件标题
    "time_range": str,  # 时间范围
    "description": str,  # 事件描述
    "final_conclusion": str,  # 最终结论
    "case_status": str  # 结案状态
}
```

### 5.2 版本数据结构

```python
{
    "version_id": str,  # 版本 ID
    "event_id": str,  # 事件 ID
    "content": str,  # 版本内容
    "timestamp": float,  # 创建时间戳
    "previous_version": str  # 前一版本 ID
}
```

### 5.3 不适感触发数据结构

```python
{
    "trigger_id": str,  # 触发 ID
    "event_id": str,  # 事件 ID
    "version_id": str,  # 版本 ID
    "level": int,  # 不适程度
    "reason": str,  # 不适原因
    "additional_info": dict,  # 附加信息
    "timestamp": float  # 触发时间戳
}
```

### 5.4 结案状态数据结构

```python
{
    "event_id": str,  # 事件 ID
    "status": str,  # 状态
    "timestamp": float,  # 状态更新时间戳
    "reason": str  # 状态更新原因
}
```

## 6. 配置管理

### 6.1 AI 配置

配置文件：`config/ai_config.json`

```json
{
  "openai": {
    "api_key": "your-openai-api-key",
    "model": "gpt-4"
  },
  "ollama": {
    "base_url": "http://localhost:11434",
    "model": "llama3"
  }
}
```

### 6.2 系统配置

系统配置通过代码中的常量和变量进行管理，主要包括：
- 缓存目录路径
- 数据存储路径
- 模型默认参数

## 7. 部署与运行

### 7.1 开发环境

1. **克隆项目**
   ```bash
   git clone <项目仓库地址>
   cd tfcs_demo
   ```

2. **创建虚拟环境**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**
   ```bash
   streamlit run app.py
   ```

### 7.2 生产环境

1. **使用 PyInstaller 打包**
   ```bash
   pyinstaller pyinstaller.spec
   ```

2. **部署可执行文件**
   将 `dist` 目录中的可执行文件部署到目标服务器。

3. **运行应用**
   双击可执行文件或在命令行中运行。

## 8. 测试策略

### 8.1 单元测试

使用 pytest 进行单元测试，测试文件位于 `tests/unit` 目录。

```bash
pytest tests/unit/
```

### 8.2 性能测试

性能测试文件位于 `tests/performance` 目录。

```bash
pytest tests/performance/
```

### 8.3 集成测试

使用 `test_system.py` 进行系统集成测试。

```bash
python test_system.py
```

## 9. 故障排除

### 9.1 常见问题

1. **依赖安装失败**
   - 确保 Python 版本正确
   - 尝试使用 `pip install --upgrade pip` 更新 pip
   - 检查网络连接

2. **应用启动失败**
   - 检查 AI 配置文件是否正确
   - 确保 AI API 密钥有效
   - 检查端口 8501 是否被占用

3. **打包失败**
   - 确保所有依赖都已正确安装
   - 检查 `pyinstaller.spec` 文件配置是否正确
   - 尝试使用 `pyinstaller app.py --onefile --add-data "app/ui/*.html:app/ui" --add-data "data/*:data" --add-data "config/*:config"` 命令

### 9.2 日志查看

应用运行时的日志会显示在命令行窗口中，可用于排查问题。

## 10. 未来规划

### 10.1 功能增强

- 支持更多 AI 模型
- 增加多语言支持
- 优化搜索算法
- 增强数据可视化

### 10.2 性能优化

- 优化缓存机制
- 提高搜索速度
- 减少内存使用

### 10.3 扩展性

- 支持插件系统
- 提供 API 接口
- 集成更多数据源

## 11. 结论

事实校正系统是一个创新的信息管理系统，它通过记录和追踪事实判断在时间维度上的演变，帮助用户理解认知的变化过程。系统采用模块化设计，具有良好的可扩展性和可维护性。通过集成 AI 技术，系统能够更有效地分析和处理信息，为用户提供更准确、更全面的认知演变视图。