# 事实校正系统安装指南

## 环境要求

- Python 3.8 或更高版本
- pip 包管理器
- 操作系统：Windows 10/11、macOS、Linux

## 依赖安装

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

## 应用打包

### 使用 PyInstaller 打包为可执行文件

1. **安装 PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **创建打包配置文件**
   创建 `pyinstaller.spec` 文件：
   ```python
   # -*- mode: python ; coding: utf-8 -*-

   block_cipher = None

   a = Analysis(
       ['app.py'],
       pathex=[],
       binaries=[],
       datas=[
           ('app/ui/*.html', 'app/ui'),
           ('data/*', 'data'),
           ('config/*', 'config')
       ],
       hiddenimports=['streamlit'],
       hookspath=[],
       hooksconfig={},
       runtime_hooks=[],
       excludes=[],
       win_no_prefer_redirects=False,
       win_private_assemblies=False,
       cipher=block_cipher,
       noarchive=False,
   )
   pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

   exe = EXE(
       pyz,
       a.scripts,
       a.binaries,
       a.zipfiles,
       a.datas,
       [],
       name='fact-checking-system',
       debug=False,
       bootloader_ignore_signals=False,
       strip=False,
       upx=True,
       upx_exclude=[],
       runtime_tmpdir=None,
       console=True,
       disable_windowed_traceback=False,
       argv_emulation=False,
       target_arch=None,
       codesign_identity=None,
       entitlements_file=None,
   )
   ```

3. **执行打包命令**
   ```bash
   pyinstaller pyinstaller.spec
   ```

4. **打包结果**
   打包完成后，可执行文件将位于 `dist` 目录中。

## 运行应用

### 方法一：直接运行 Python 脚本

1. **激活虚拟环境**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **启动应用**
   ```bash
   streamlit run app.py
   ```

3. **访问应用**
   打开浏览器，访问输出中显示的 URL（通常是 `http://localhost:8501`）。

### 方法二：运行打包后的可执行文件

1. **定位可执行文件**
   进入 `dist` 目录，找到 `fact-checking-system.exe`（Windows）或 `fact-checking-system`（macOS/Linux）。

2. **运行应用**
   双击可执行文件，或在命令行中运行：
   ```bash
   # Windows
   .\fact-checking-system.exe
   
   # macOS/Linux
   ./fact-checking-system
   ```

3. **访问应用**
   打开浏览器，访问 `http://localhost:8501`。

## 配置说明

### AI 模型配置

1. **修改 AI 配置文件**
   编辑 `config/ai_config.json` 文件，配置 API 密钥和模型参数：
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

2. **选择 AI 模型**
   在 `app.py` 文件中，修改以下代码选择使用的 AI 模型：
   ```python
   self.ai_model = self.model_factory.create_runner("OPENAI")  # 或 "OLLAMA"
   ```

## 故障排除

### 常见问题

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

### 日志查看

应用运行时的日志会显示在命令行窗口中，可用于排查问题。

## 联系支持

如果遇到无法解决的问题，请联系项目维护者获取支持。