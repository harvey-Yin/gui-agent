# 工作流程报告1: 项目环境搭建与配置

## 📋 流程概述

本报告整合了项目初始化、环境配置和多机协作的完整流程。

---

## 🎯 Phase 1: 项目基础设施搭建

### 1.1 项目结构创建

**状态**: ✅ 已完成

```
gui-agent/
├── backend/              # 后端API服务
├── agent_core/           # Agent核心逻辑
├── rpa_tools/            # RPA工具集 (已完成)
├── knowledge_base/       # 知识库模块
├── web_ui/               # Web界面
├── configs/              # 配置文件
├── tests/                # 测试目录
├── examples/             # 示例场景
├── data/                 # 数据存储
│   ├── screenshots/      # 截图存储
│   └── vectordb/         # 向量数据库
├── logs/                 # 日志目录
└── docs/                 # 文档目录
```

### 1.2 虚拟环境配置

```powershell
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 1.3 核心依赖包

**LLM框架**:
- langchain==0.3.0
- langchain-community==0.3.0
- langchain-core==0.3.0
- ollama==0.4.0

**RPA工具**:
- pyautogui==0.9.54
- opencv-python==4.10.0.84
- pillow==10.4.0
- pynput==1.7.7

**向量数据库**:
- chromadb==0.5.0
- sentence-transformers==3.0.1

**Web框架**:
- fastapi==0.115.0
- uvicorn==0.30.6
- websockets==13.1

---

## 🖥️ 多机协作架构

### 整体架构图

```
┌─────────────────────────────────────────┐
│         电脑A（后端服务器）              │
│  - Ollama (qwen:7b)                     │
│  - Agent核心（LangChain）                │
│  - 向量数据库（ChromaDB）                │
│  - FastAPI后端服务                       │
└─────────────┬───────────────────────────┘
              │ HTTP API
              │ (http://电脑A_IP:8000)
              │
┌─────────────┴───────────────────────────┐
│         电脑B（RPA开发机）               │
│  - RPA工具开发（PyAutoGUI + OpenCV）     │
│  - Web前端（Vue.js）                     │
│  - 直接操作Windows桌面                   │
└─────────────────────────────────────────┘
```

### 电脑A职责

**硬件要求**:
- 内存：16GB+
- CPU：多核处理器
- GPU：可选（加速推理）

**负责模块**:
1. **Agent核心层** (`agent_core/`)
   - `agent.py` - Agent主逻辑
   - `prompts.py` - Prompt模板
   - `memory.py` - 记忆模块

2. **知识库模块** (`knowledge_base/`)
   - `vector_store.py` - 向量数据库操作
   - `script_store.py` - RPA脚本存储

3. **后端API** (`backend/api/`)
   - `main.py` - FastAPI主应用
   - `routes/agent.py` - Agent执行接口
   - `routes/knowledge.py` - 知识库接口

**启动命令**:
```bash
# 启动Ollama
ollama serve

# 启动向量数据库
docker run -d -p 8001:8000 chromadb/chroma:latest

# 启动FastAPI后端
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

### 电脑B职责

**硬件要求**:
- Windows 10/11
- 可直接操作桌面
- 双显示器推荐

**负责模块**:
1. **RPA工具集** (`rpa_tools/`) - ✅ 已完成
   - `base_tool.py` - 工具基类
   - `screen_tools.py` - 屏幕操作
   - `vision_tools.py` - 视觉识别
   - `excel_tools.py` - Excel处理
   - `word_tools.py` - Word处理
   - `data_tools.py` - 数据处理
   - `tool_registry.py` - 工具注册

2. **Web前端** (`web_ui/`)
   - Vue.js前端界面
   - 对话界面、执行监控、任务管理

3. **RPA执行器** (`rpa_tools/executor.py`)
   - 调用电脑A的API
   - 执行RPA指令

**配置文件** (`.env`):
```bash
# 电脑A的API地址
AGENT_API_URL=http://192.168.1.100:8000

# 本地设置
SCREENSHOT_PATH=./data/screenshots
```

---

## 🔄 Git工作流

### 分支管理

```
main                    # 生产稳定版
├── dev                 # 开发主线
├── feature/agent-core       # 电脑A的功能分支
└── feature/rpa-tools        # 电脑B的功能分支
```

### 提交规范

- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更新
- `test:` 测试相关

### 合并流程

1. 各自在feature分支开发
2. 定期合并到dev分支
3. 联合测试通过后合并到main

---

## ✅ 已完成工作

- [x] Python虚拟环境创建
- [x] 完整项目目录结构
- [x] 依赖包安装
- [x] 配置文件准备
- [x] **RPA工具集开发完成** (6个模块，60+方法)
- [x] Ollama + LangChain集成验证

---

## 📋 下一步计划

### 电脑A任务

1. **Agent核心开发**
   - 实现Agent主逻辑
   - 设计Prompt模板
   - 开发记忆模块

2. **知识库开发**
   - 向量数据库集成
   - RPA脚本存储
   - 相似任务检索

3. **后端API开发**
   - FastAPI接口实现
   - WebSocket实时通信
   - 任务执行管理

### 电脑B任务

1. **Web前端开发**
   - Vue.js项目搭建
   - 对话界面开发
   - 执行监控界面

2. **RPA执行器**
   - 实现与电脑A的通信
   - 指令解析和执行
   - 结果反馈机制

3. **集成测试**
   - 端到端测试
   - 性能测试
   - Bug修复

---

## 🌐 网络配置

### 确保电脑B能访问电脑A

```bash
# 在电脑A上查看IP
ipconfig

# 在电脑B上测试连接
curl http://192.168.1.100:8000/docs
```

### 防火墙设置

- 电脑A开放8000端口（FastAPI）
- 可选：开放8001端口（ChromaDB）

---

## 📊 开发时间估算

| 电脑 | 主要任务 | 预计时间 | 状态 |
|------|----------|----------|------|
| 电脑A | Agent核心 + 知识库 + 后端API | 5-7天 | ⏳ 进行中 |
| 电脑B | RPA工具 + Web前端 | 5-7天 | ✅ 工具完成 |
| 联调 | 集成测试 + Bug修复 | 2-3天 | ⏳ 待开始 |

---

## 🎯 项目目标

**核心价值**: 通过自然语言指令，让AI Agent自动执行桌面自动化任务，降低RPA开发门槛。

**技术栈**: LangChain + Ollama (qwen:7b) + PyAutoGUI + OpenCV + ChromaDB + FastAPI

**预期成果**: 
- 可通过自然语言控制的RPA Agent
- 支持Excel、Word、屏幕操作等多种任务
- 具备任务学习和知识积累能力
