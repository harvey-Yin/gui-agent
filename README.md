# GUI-Agent 项目

> 一个基于视觉识别和大语言模型的RPA智能助手实验项目

## 项目状态

⚠️ **实验性项目** - 技术验证完成，实用性有限

## 项目简介

GUI-Agent是一个探索性项目，尝试结合视觉识别（MAI-UI-2B）和大语言模型（deepseek-r1:8b）来实现智能化的RPA自动化。

### 核心功能

- 💬 **对话式交互**: 通过自然语言与AI对话，布置任务
- 👁️ **视觉识别**: 使用MAI-UI-2B理解GUI界面
- 🧠 **智能决策**: 使用LLM进行任务分解和工具选择
- 🎯 **自动化操作**: 执行鼠标、键盘、API等操作

### 技术栈

- **视觉模型**: MAI-UI-2B (Docker + vLLM)
- **语言模型**: deepseek-r1:8b (Ollama)
- **RPA工具**: PyAutoGUI, pyperclip
- **框架**: Python, Flask, Docker

## 快速开始

### 前置要求

- Python 3.10+
- Docker Desktop
- Ollama
- 12GB+ GPU显存（可选，用于视觉识别）

### 安装步骤

1. **克隆项目**
   ```powershell
   cd c:\document\python\gui-agent
   ```

2. **安装依赖**
   ```powershell
   pip install -r requirements.txt
   ```

3. **启动服务**
   ```powershell
   # 启动Ollama
   ollama serve
   
   # 下载模型
   ollama pull deepseek-r1:8b
   
   # (可选) 启动MAI-UI Docker
   docker-compose up -d
   ```

4. **运行Agent**
   ```powershell
   python demo_chat_agent.py
   ```

## 项目结构

```
gui-agent/
├── rpa_tools/              # Agent核心模块
│   ├── vision_module.py    # 视觉识别
│   ├── reasoning_module.py # 推理决策
│   ├── action_module.py    # 工具执行
│   └── conversational_agent.py  # 对话Agent
├── demo_chat_agent.py      # 对话式Demo
├── test_agent.py           # 自动化测试
├── docker-compose.yml      # MAI-UI配置
├── requirements.txt        # Python依赖
└── docs/                   # 文档目录
```

## 使用示例

### 对话式交互

```
你: 你好
Agent: 你好！我是智能RPA助手...

你: 帮我获取北京的天气
Agent: 正在查询北京的天气，请稍等...
  [执行 get_weather 工具]
  结果: 天气 15°C, Partly cloudy

你: 根据天气生成一篇文章
Agent: 好的，我来生成...
  [执行 generate_article 工具]
  结果: 文章已生成
```

## 测试结果

✅ **核心功能验证通过**:
- 对话理解和响应
- 工具调用决策
- 参数解析
- 上下文记忆

详见: [测试报告](docs/agent_test_report.md)

## 已知限制

1. **性能**: 视觉识别较慢（3-5秒/次）
2. **稳定性**: 网络依赖强，错误处理不完善
3. **实用性**: 简单任务传统RPA更快，复杂任务AI不够可靠
4. **成本**: 需要12GB+显存，推理速度慢

## 文档

- [Agent使用指南](docs/agent_usage_guide.md)
- [对话Agent指南](docs/chat_agent_guide.md)
- [虚拟环境部署](docs/venv_deployment_guide.md)
- [MAI-UI部署总结](docs/mai_ui_success_summary.md)
- [项目总结](../brain/f638ddc2-f99e-4490-b48e-a045ebff5042/project_summary.md)

## 经验教训

### ✅ 做对的
- 模块化设计
- 使用Ollama简化部署
- 详细的文档记录

### ❌ 可以改进
- 实用价值评估不足
- 性能优化不够
- 过度追求通用性

### 💡 建议
> 技术很酷 ≠ 有实用价值
> 
> 在投入大量时间前，先验证：
> 1. 是否真的解决了问题？
> 2. 是否比现有方案更好？
> 3. 成本是否可接受？

## 可复用的成果

- ✅ Ollama部署方案
- ✅ Docker配置模板
- ✅ Agent模块设计
- ✅ 部署文档和脚本

## 许可证

MIT License

## 作者

Harvey Yin

## 致谢

- MAI-UI-2B: 视觉识别模型
- deepseek-r1: 推理模型
- Ollama: 本地LLM部署工具

---

**项目状态**: 实验完成，可以收尾  
**最后更新**: 2026-02-05
