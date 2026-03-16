# 事实校正系统代码资源包

相关代码已上传GitHub： `https://github.com/liguanlin1212/xiaolong-huixi-project`

## 资源包结构

```
tfcs_demo/
├── agent/             # 多Agent架构实现
├── ai/                # AI模型集成
│   └── inference/     # 推理引擎
├── app/               # 应用主目录
│   ├── api/           # API接口
│   ├── services/      # 业务服务
│   └── ui/            # 前端界面
├── config/            # 配置文件
├── core/              # 核心数据结构
├── data/              # 数据存储
├── docs/              # 项目文档
├── search/            # 搜索功能
├── tests/             # 测试代码
├── AI_INTEGRATION_GUIDE.md  # AI集成指南
├── app.py             # 应用主入口
├── INSTALLATION_GUIDE.md    # 安装指南
├── TECHNICAL_DOCUMENTATION.md  # 技术文档
├── CODE_PACKAGE.md    # 代码资源包说明
├── requirements.txt   # 依赖文件
└── pyinstaller.spec   # PyInstaller打包配置
```

## 资源包内容

### 核心代码文件

1. **应用主入口**
   - `app.py`：应用主入口，启动Streamlit界面

2. **AI集成**
   - `ai/inference/model_factory.py`：模型工厂，创建不同类型的AI模型运行器
   - `ai/inference/openai_runner.py`：OpenAI API集成
   - `ai/inference/ollama_runner.py`：Ollama本地模型集成
   - `ai/inference/npu_runner.py`：NPU模型集成

3. **搜索功能**
   - `search/search_handler.py`：处理搜索查询
   - `search/search_prompt.py`：构建搜索指令
   - `search/search_analyzer.py`：分析搜索结果
   - `search/case_status.py`：检查事件结案状态
   - `search/case_status_machine.py`：管理事件结案状态

4. **版本控制**
   - `search/version_manager.py`：管理判断版本
   - `search/version_storage.py`：存储版本信息
   - `search/version_history.py`：记录版本历史

5. **自查纠错**
   - `search/self_correction.py`：处理自查纠错逻辑

6. **不适感触发**
   - `search/discomfort_trigger.py`：处理用户不适感反馈

7. **前端界面**
   - `app/ui/search_ui.py`：搜索界面
   - `app/ui/explore_ui.py`：事件探索界面
   - `app/ui/timeline_view.py`：时间轴可视化
   - `app/ui/snapshot_view.py`：世界快照
   - `app/ui/false_claims_view.py`：错误说法展示
   - `app/ui/failure_archive_view.py`：认知失败档案

### 配置文件

- `config/ai_config.json`：AI模型配置

### 文档文件

- `docs/技术背景文档.md`：技术背景说明
- `docs/最终设计文档.md`：系统设计文档
- `docs/强约束实现说明文档.md`：强约束实现说明
- `docs/迭代流程.md`：迭代流程说明
- `docs/迭代流程2.0.md`：迭代流程2.0说明
- `docs/demo实现情况.md`：Demo实现情况
- `AI_INTEGRATION_GUIDE.md`：AI集成指南
- `INSTALLATION_GUIDE.md`：安装指南
- `TECHNICAL_DOCUMENTATION.md`：技术文档
- `CODE_PACKAGE.md`：代码资源包说明

### 测试文件

- `tests/unit/`：单元测试
- `tests/performance/`：性能测试
- `test_ai_integration.py`：AI集成测试
- `test_case_status.py`：结案状态测试
- `test_explore_functionality.py`：探索功能测试
- `test_imports.py`：导入测试
- `test_npu_inference.py`：NPU推理测试
- `test_ollama_integration.py`：Ollama集成测试
- `test_search_functionality.py`：搜索功能测试
- `test_system.py`：系统测试

## 创建资源包步骤

### 方法一：直接压缩项目目录

1. **确保项目完整**
   - 检查所有代码文件是否存在
   - 确保依赖文件 `requirements.txt` 已更新
   - 确保配置文件已正确设置

2. **压缩项目目录**
   - 在Windows上：右键点击 `tfcs_demo` 目录，选择 "压缩到ZIP文件"
   - 在macOS上：右键点击 `tfcs_demo` 目录，选择 "压缩"
   - 在Linux上：使用 `zip -r tfcs_demo.zip tfcs_demo/` 命令

### 方法二：使用Git归档

1. **确保项目已提交到Git**
   ```bash
   git add .
   git commit -m "Prepare code package"
   ```

2. **创建Git归档**
   ```bash
   git archive --format=zip --output=tfcs_demo.zip HEAD
   ```

### 方法三：使用Python打包工具

1. **创建setup.py文件**
   ```python
   from setuptools import setup, find_packages

   setup(
       name="tfcs_demo",
       version="1.0.0",
       packages=find_packages(),
       include_package_data=True,
       package_data={
           '': ['*.json', '*.html'],
       },
       install_requires=[
           'streamlit',
           'openai',
           'onnxruntime',
           'numpy',
           'pytest',
           'pytest-cov',
           'psutil'
       ],
       entry_points={
           'console_scripts': [
               'tfcs_demo=app:main'
           ]
       }
   )
   ```

2. **创建源码分发包**
   ```bash
   python setup.py sdist
   ```

3. **创建 wheel 包**
   ```bash
   python setup.py bdist_wheel
   ```

## 资源包使用方法

### 方法一：直接解压使用

1. **解压资源包**
   - 将 `tfcs_demo.zip` 解压到任意目录

2. **安装依赖**
   ```bash
   cd tfcs_demo
   pip install -r requirements.txt
   ```

3. **运行应用**
   ```bash
   streamlit run app.py
   ```

### 方法二：使用pip安装

1. **安装wheel包**
   ```bash
   pip install tfcs_demo-1.0.0-py3-none-any.whl
   ```

2. **运行应用**
   ```bash
   tfcs_demo
   ```

## 注意事项

1. **配置文件**
   - 解压后需要修改 `config/ai_config.json` 文件，配置API密钥

2. **依赖安装**
   - 确保Python版本为3.8或更高
   - 某些依赖可能需要额外的系统库支持

3. **AI模型**
   - 使用OpenAI模型需要有效的API密钥
   - 使用Ollama模型需要本地安装Ollama

4. **端口占用**
   - 应用默认使用8501端口，确保该端口未被占用

5. **数据存储**
   - 应用会在 `data` 目录中存储缓存和历史数据
   - 确保该目录有读写权限

## 技术支持

如果在使用过程中遇到问题，请参考以下资源：

- **安装指南**：`INSTALLATION_GUIDE.md`
- **技术文档**：`TECHNICAL_DOCUMENTATION.md`
- **AI集成指南**：`AI_INTEGRATION_GUIDE.md`

或者联系项目维护者获取支持。