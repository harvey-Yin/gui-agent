# RPA-Enhanced AI Agent 项目实施计划

## 项目概述

基于langchain-chatchat架构，开发具有RPA能力的本地AI Agent助手。

**核心价值**: 通过自然语言指令，让AI Agent自动执行桌面自动化任务，降低RPA开发门槛。

**技术栈**: LangChain + Ollama (qwen:7b) + PyAutoGUI + OpenCV + ChromaDB + FastAPI

---

## Phase 1: 项目基础设施搭建 ✅ 已完成

### 已完成工作
- [x] Python虚拟环境创建
- [x] 完整项目目录结构
- [x] 依赖包安装（LangChain, Ollama, PyAutoGUI, OpenCV等）
- [x] 配置文件准备（.env, requirements.txt, README.md）
- [x] Ollama + LangChain集成验证

### 验证结果
- Ollama (qwen:7b) 正常响应
- LangChain能够规划简单任务
- RPA工具（PyAutoGUI, OpenCV）可用

---

## Phase 2: RPA核心能力模块开发（预计3-5天）

### 2.1 设计RPA工具抽象基类

**文件**: `rpa_tools/base_tool.py`

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class RPAToolBase(ABC):
    """RPA工具基类"""
    name: str
    description: str
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """执行工具逻辑"""
        pass
    
    def pre_check(self) -> bool:
        """执行前安全检查"""
        return True
    
    def log_execution(self, params: dict, result: dict):
        """记录执行日志"""
        pass
```

### 2.2 实现屏幕操作工具

**文件**: `rpa_tools/screen_tools.py`

核心功能：
- `click_at(x, y)` - 点击指定坐标
- `type_text(text)` - 输入文本
- `press_key(key)` - 按键操作
- `screenshot(region=None)` - 截屏
- `drag_to(x1, y1, x2, y2)` - 拖拽操作

安全机制：
- 操作前延迟（避免误操作）
- 操作日志记录
- 紧急停止热键监听

### 2.3 实现视觉识别工具

**文件**: `rpa_tools/vision_tools.py`

核心功能：
- `find_image(template_path, confidence=0.8)` - 模板匹配定位
- `wait_for_element(template_path, timeout=10)` - 等待元素出现
- `ocr_text(region=None)` - OCR文字识别
- `detect_element_llm(description)` - 使用多模态LLM识别UI元素

技术方案：
- 优先使用OpenCV模板匹配（速度快）
- 复杂场景调用llava多模态模型（理解能力强）

### 2.4 开发工具注册系统

**文件**: `rpa_tools/tool_registry.py`

功能：
- 自动发现所有RPA工具
- 转换为LangChain Tool格式
- 权限控制（标记危险操作）

---

## Phase 3: AI Agent智能层开发（预计3-4天）

### 3.1 设计Agent Prompt

**文件**: `agent_core/prompts.py`

核心Prompt模板：
```
你是一个RPA自动化助手，擅长通过屏幕操作和视觉识别完成桌面任务。

可用工具：
{tools}

工作流程：
1. 理解用户意图
2. 拆解为具体步骤
3. 使用视觉工具定位元素
4. 执行操作
5. 验证结果

注意事项：
- 操作前先截图确认当前状态
- 使用视觉识别而非硬编码坐标
- 操作失败时尝试备选方案
```

### 3.2 实现Agent核心

**文件**: `agent_core/agent.py`

基于LangChain的ReAct Agent：
```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama

class RPAAgent:
    def __init__(self, tools, llm):
        self.agent = create_react_agent(llm, tools, prompt)
        self.executor = AgentExecutor(
            agent=self.agent, 
            tools=tools,
            max_iterations=10,
            verbose=True
        )
    
    def run(self, user_input: str):
        return self.executor.invoke({"input": user_input})
```

### 3.3 实现记忆模块

**文件**: `agent_core/memory.py`

- 对话历史（ConversationBufferMemory）
- 任务历史（SQLite存储）
- 上下文维护（记住上次操作的窗口、位置）

---

## Phase 4: 知识库和RAG能力（预计2-3天）

### 4.1 构建RPA脚本知识库

**文件**: `knowledge_base/vector_store.py`

功能：
- 存储用户成功执行的RPA任务
- 向量化任务描述（使用sentence-transformers）
- 检索相似任务作为参考

### 4.2 预置常见场景

**目录**: `examples/`

示例场景：
1. 批量重命名文件
2. Excel数据填写
3. 浏览器自动化（填表单）
4. 应用程序操作

---

## Phase 5: Web UI开发（预计2-3天）

### 5.1 后端API设计

**文件**: `backend/api/main.py`

核心接口：
- `POST /agent/execute` - 执行Agent任务
- `POST /knowledge/store` - 存储任务到知识库
- `GET /task/history` - 获取任务历史
- `WS /agent/stream` - WebSocket实时推送

### 5.2 前端界面

**目录**: `web_ui/`

核心页面：
1. 对话界面 - 消息列表、工具调用展示
2. 执行监控 - 实时截图、操作日志
3. 任务管理 - 历史任务、保存模板
4. 知识库管理 - 上传脚本、查看任务

---

## Phase 6: 测试和优化（预计2天）

### 安全机制
- 危险操作确认（删除文件、系统设置）
- 操作审计日志
- 紧急停止热键（Ctrl+Shift+Q）
- 沙盒模式（测试环境）

### 测试用例
1. 单元测试 - 每个RPA工具独立测试
2. 集成测试 - 完整Agent任务执行
3. 场景测试 - 真实业务场景模拟

---

## Phase 7: 文档与展示（预计1-2天）

### 7.1 项目文档

- README.md（已完成）
- API文档（FastAPI自动生成）
- 用户手册
- 开发者指南

### 7.2 演示材料

演示视频（3个场景）：
1. 简单任务：打开记事本输入文字
2. 中等任务：批量重命名100个文件
3. 复杂任务：从网页抓取数据填入Excel

### 7.3 简历描述模板

```
【独立项目】RPA-Enhanced AI Agent
- 技术栈：LangChain, Ollama, PyAutoGUI, OpenCV, FastAPI, Vue.js
- 项目描述：开发了一个基于大语言模型的本地RPA自动化Agent，
  通过自然语言指令驱动桌面自动化任务执行
- 核心亮点：
  1. 设计了LLM + RPA的融合架构，实现智能任务规划与可靠执行
  2. 基于opencv实现视觉智能定位，避免传统RPA硬编码坐标问题
  3. 构建知识库系统，支持历史任务检索和最佳实践复用
  4. 实现完整的安全控制机制（操作审计、权限管理、紧急停止）
- 项目成果：成功应用于Excel批处理、表单填写、数据采集等10+场景
```

---

## 时间估算

| 阶段 | 预计时间 | 状态 |
|------|----------|------|
| Phase 1: 环境搭建 | 2-3天 | ✅ 已完成 |
| Phase 2: RPA模块 | 3-5天 | ⏳ 待开始 |
| Phase 3: Agent层 | 3-4天 | ⏳ 待开始 |
| Phase 4: 知识库 | 2-3天 | ⏳ 待开始 |
| Phase 5: Web UI | 2-3天 | ⏳ 待开始 |
| Phase 6: 测试 | 2天 | ⏳ 待开始 |
| Phase 7: 文档 | 1-2天 | ⏳ 待开始 |
| **总计** | **15-23天** | **MVP版本** |

---

## 技术决策

### 为什么选择本地LLM（Ollama）？
1. **数据隐私** - RPA涉及企业内部系统，不能上传云端
2. **成本控制** - 高频RPA调用，API成本过高
3. **响应速度** - 本地推理延迟更低

### 视觉识别方案选择

| 方案 | 优点 | 缺点 | 使用场景 |
|------|------|------|----------|
| OpenCV模板匹配 | 速度快、无需额外模型 | 对界面变化敏感 | ✅ 主方案 |
| 多模态LLM（llava） | 理解能力强、泛化好 | 速度较慢 | ✅ 复杂场景 |
| OCR + 规则 | 文字定位准确 | 仅适用于文本 | ✅ 辅助方案 |

### Agent架构选择
- **ReAct模式**（当前使用）- 思考-行动-观察循环，适合多步骤RPA
- Plan-and-Execute（未来扩展）- 适合复杂长任务

---

## 后续扩展方向

1. **多模态增强** - 集成语音输入/输出
2. **协作能力** - 多Agent协同工作
3. **低代码编辑器** - 可视化RPA流程设计
4. **Docker部署** - 一键安装包
5. **跨平台支持** - Linux/Mac兼容
