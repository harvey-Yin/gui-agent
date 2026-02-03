# RPA-Enhanced AI Agent

> 基于LangChain框架的本地RPA自动化智能助手，通过自然语言驱动桌面任务执行

## 🌟 项目亮点

- 🤖 **AI驱动的RPA**：使用大语言模型理解意图，自动规划和执行桌面任务
- 👁️ **视觉智能定位**：基于OpenCV和多模态LLM，无需硬编码坐标
- 🔒 **本地部署**：使用Ollama本地运行，保护数据隐私
- 📚 **知识库积累**：RAG检索历史任务，越用越智能
- 🛡️ **安全可控**：操作审计、危险操作确认、紧急停止机制

## 🏗️ 系统架构

```
用户自然语言指令
    ↓
AI Agent（LangChain）
    ↓
任务规划 + 工具调用
    ↓
┌─────────────┬─────────────┬─────────────┐
│  屏幕操作   │  视觉识别   │  知识库     │
│  PyAutoGUI  │  OpenCV     │  ChromaDB   │
└─────────────┴─────────────┴─────────────┘
```

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Windows 10/11（当前版本）
- Ollama（本地LLM引擎）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/rpa-agent.git
cd rpa-agent
```

2. **创建虚拟环境**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
copy .env.example .env
# 编辑 .env 文件，根据需要修改配置
```

5. **启动Ollama并下载模型**
```bash
# 启动Ollama服务
ollama serve

# 下载模型（另开一个终端）
ollama pull qwen2.5:7b
ollama pull llava:7b
```

6. **启动Agent服务**
```bash
python -m uvicorn backend.api.main:app --reload
```

7. **访问Web界面**
```
http://localhost:8000
```

## 📖 使用示例

```
用户：帮我打开记事本并输入"Hello World"
Agent：
  1. 🔍 使用视觉识别找到开始菜单
  2. 🖱️ 点击开始菜单
  3. ⌨️ 输入"notepad"
  4. ⏎ 按回车键
  5. ⏳ 等待记事本窗口出现
  6. ⌨️ 输入"Hello World"
  ✅ 任务完成！
```

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| AI框架 | LangChain, Ollama |
| RPA工具 | PyAutoGUI, OpenCV |
| 向量数据库 | ChromaDB |
| Web框架 | FastAPI, Uvicorn |
| 前端 | Vue.js (待开发) |

## 📁 项目结构

```
rpa-agent/
├── backend/              # 后端服务（电脑A）
│   ├── api/              # FastAPI接口
│   └── services/         # 业务逻辑
├── agent_core/           # Agent核心（电脑A）
│   ├── agent.py          # Agent主逻辑
│   ├── prompts.py        # Prompt模板
│   └── memory.py         # 记忆模块
├── rpa_tools/            # RPA工具集（电脑B）
│   ├── screen_tools.py   # 屏幕操作
│   ├── vision_tools.py   # 视觉识别
│   └── browser_tools.py  # 浏览器自动化
├── knowledge_base/       # 知识库模块（电脑A）
│   └── vector_store.py   # 向量数据库
├── web_ui/               # Web界面（电脑B）
├── configs/              # 配置文件
├── tests/                # 测试
└── examples/             # 示例场景
```

## 🔧 开发状态

- [x] Phase 1: 环境搭建 ⏳ 进行中
- [ ] Phase 2: RPA核心模块
- [ ] Phase 3: AI Agent层
- [ ] Phase 4: 知识库集成
- [ ] Phase 5: Web UI
- [ ] Phase 6: 测试优化
- [ ] Phase 7: 文档完善

## 📝 路线图

- [ ] 支持更多RPA场景（Excel、浏览器、文件操作）
- [ ] 可视化流程设计器
- [ ] 多Agent协同
- [ ] Docker一键部署
- [ ] Linux/Mac支持

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

[你的名字] - 基于真实RPA业务经验打造

---

**⭐ 如果这个项目对你有帮助，请给个Star！**
