# 多机协作开发分工

## 整体架构

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

---

## 电脑A：后端服务器职责

### 硬件要求
- 内存：16GB+（Ollama需要）
- CPU：多核处理器
- GPU：可选（加速推理）

### 安装环境

```bash
# 1. 安装Ollama
# 下载：https://ollama.com/download
ollama serve

# 2. 下载模型
ollama pull qwen:7b
ollama pull llava:7b  # 多模态视觉模型

# 3. 启动向量数据库（Docker）
docker run -d -p 8001:8000 chromadb/chroma:latest
```

### 负责模块

#### 1. Agent核心层 (`agent_core/`)
```
agent_core/
├── agent.py          # Agent主逻辑（电脑A开发）
├── prompts.py        # Prompt模板
├── memory.py         # 记忆模块
└── __init__.py
```

**核心代码示例**:
```python
# agent_core/agent.py
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama

class RPAAgent:
    def __init__(self, tools, llm):
        self.llm = Ollama(model="qwen:7b")
        self.agent = create_react_agent(self.llm, tools, prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=tools)
    
    def run(self, user_input: str):
        # Agent推理执行
        return self.executor.invoke({"input": user_input})
```

#### 2. 知识库模块 (`knowledge_base/`)
```
knowledge_base/
├── vector_store.py   # 向量数据库操作（电脑A开发）
├── script_store.py   # RPA脚本存储
└── __init__.py
```

功能：
- 存储历史RPA任务
- 向量检索相似任务
- 提供few-shot examples

#### 3. 后端API (`backend/api/`)
```
backend/api/
├── main.py           # FastAPI主应用（电脑A开发）
├── routes/
│   ├── agent.py      # Agent执行接口
│   └── knowledge.py  # 知识库接口
└── __init__.py
```

**API接口示例**:
```python
# backend/api/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AgentRequest(BaseModel):
    user_input: str
    screenshot: str = None  # base64编码的截图

@app.post("/agent/execute")
async def execute_task(request: AgentRequest):
    """电脑B调用此接口，让Agent推理"""
    # 1. Agent规划任务
    plan = agent.plan(request.user_input)
    
    # 2. 返回执行指令给电脑B
    return {
        "action": "click",
        "params": {"x": 100, "y": 200},
        "reasoning": "需要点击登录按钮"
    }

@app.post("/knowledge/store")
async def store_task(task_data: dict):
    """电脑B完成任务后，存储到知识库"""
    vectordb.add(task_data)
    return {"status": "success"}
```

### 启动命令

```bash
# 在电脑A上
cd c:\document\python\gui-agent
.\venv\Scripts\activate

# 启动Ollama（如未运行）
ollama serve

# 启动FastAPI后端
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

### Git工作流

```bash
# 电脑A的分支
git checkout -b feature/agent-core

# 开发Agent核心
# 编辑 agent_core/agent.py

# 提交代码
git add agent_core/ backend/ knowledge_base/
git commit -m "feat: 实现Agent推理核心逻辑"
git push origin feature/agent-core
```

---

## 电脑B：RPA开发机职责

### 硬件要求
- Windows 10/11
- 可直接操作桌面（不在虚拟机中）
- 双显示器推荐（便于调试）

### 安装环境

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/rpa-agent.git
cd rpa-agent

# 2. 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate

# 3. 安装依赖（仅RPA相关）
pip install pyautogui opencv-python pillow pynput
pip install httpx  # 用于调用电脑A的API
```

### 负责模块

#### 1. RPA工具集 (`rpa_tools/`)
```
rpa_tools/
├── base_tool.py      # 工具基类（电脑B开发）
├── screen_tools.py   # 屏幕操作工具（电脑B开发）
├── vision_tools.py   # 视觉识别工具（电脑B开发）
├── browser_tools.py  # 浏览器自动化（电脑B开发）
└── __init__.py
```

**核心代码示例**:
```python
# rpa_tools/screen_tools.py
import pyautogui
import time

class ScreenTool:
    def click_at(self, x: int, y: int):
        """点击指定坐标"""
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        time.sleep(0.3)
        return {"status": "success", "action": f"点击({x}, {y})"}
    
    def type_text(self, text: str):
        """输入文本"""
        pyautogui.write(text, interval=0.1)
        return {"status": "success", "text": text}
    
    def screenshot(self, region=None):
        """截屏"""
        img = pyautogui.screenshot(region=region)
        # 保存或返回base64
        return img
```

#### 2. Web前端 (`web_ui/`)
```
web_ui/
├── frontend/         # Vue.js前端（电脑B开发）
│   ├── src/
│   │   ├── views/
│   │   │   ├── Chat.vue      # 对话界面
│   │   │   ├── Monitor.vue   # 执行监控
│   │   │   └── Tasks.vue     # 任务管理
│   │   └── App.vue
│   └── package.json
└── __init__.py
```

功能：
- 用户输入对话界面
- 实时显示Agent推理过程
- 展示RPA执行的截图

#### 3. RPA执行器 (`rpa_tools/executor.py`)
```python
# rpa_tools/executor.py
import httpx

class RPAExecutor:
    def __init__(self, agent_api_url="http://电脑A_IP:8000"):
        self.api_url = agent_api_url
        self.screen_tool = ScreenTool()
        self.vision_tool = VisionTool()
    
    async def execute_task(self, user_input: str):
        """调用电脑A的Agent，获取指令并执行"""
        # 1. 截图当前桌面
        screenshot = self.screen_tool.screenshot()
        
        # 2. 调用电脑A的Agent API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/agent/execute",
                json={
                    "user_input": user_input,
                    "screenshot": screenshot_to_base64(screenshot)
                }
            )
            action = response.json()
        
        # 3. 执行Agent返回的指令
        if action["action"] == "click":
            result = self.screen_tool.click_at(**action["params"])
        elif action["action"] == "type":
            result = self.screen_tool.type_text(**action["params"])
        
        # 4. 返回结果给电脑A存储
        await client.post(
            f"{self.api_url}/knowledge/store",
            json={"task": user_input, "result": result}
        )
```

### 配置文件

**`.env`** (电脑B):
```bash
# 电脑A的API地址
AGENT_API_URL=http://192.168.1.100:8000  # 替换为电脑A的实际IP

# 本地设置
SCREENSHOT_PATH=./data/screenshots
```

### Git工作流

```bash
# 电脑B的分支
git checkout -b feature/rpa-tools

# 开发RPA工具
# 编辑 rpa_tools/screen_tools.py

# 提交代码
git add rpa_tools/ web_ui/
git commit -m "feat: 实现屏幕点击和文本输入工具"
git push origin feature/rpa-tools
```

---

## 协作流程

### 工作流程示例

**场景：开发"打开记事本"功能**

#### 第1步：电脑A先行（开发Agent逻辑）
```python
# 电脑A: agent_core/agent.py
# 定义Agent如何理解"打开记事本"任务

prompt = """
用户说：{user_input}
你需要：
1. 判断需要什么工具
2. 规划执行步骤
3. 返回工具调用指令
"""
```

#### 第2步：电脑B实现工具（开发RPA工具）
```python
# 电脑B: rpa_tools/screen_tools.py
def open_notepad(self):
    # 1. 按Win键
    pyautogui.press('win')
    time.sleep(1)
    
    # 2. 输入notepad
    pyautogui.write('notepad')
    time.sleep(0.5)
    
    # 3. 按回车
    pyautogui.press('enter')
```

#### 第3步：联调测试
```bash
# 电脑A启动后端
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000

# 电脑B运行测试
python test_integration.py
```

---

## 代码合并策略

### 分支管理
```
main                    # 生产稳定版
├── dev                 # 开发主线
├── feature/agent-core       # 电脑A的功能分支
└── feature/rpa-tools        # 电脑B的功能分支
```

### 合并流程
1. 各自在feature分支开发
2. 定期合并到dev分支
3. 联合测试通过后合并到main

### 冲突处理
- **电脑A**主要修改：`agent_core/`, `backend/`, `knowledge_base/`
- **电脑B**主要修改：`rpa_tools/`, `web_ui/`
- 理论上不会有太多冲突

---

## 沟通机制

### API接口文档
- 电脑A提供Swagger文档：`http://电脑A_IP:8000/docs`
- 电脑B根据文档调用接口

### 数据格式约定

**Agent返回格式**:
```json
{
  "action": "click",
  "params": {"x": 100, "y": 200},
  "reasoning": "需要点击登录按钮",
  "next_action": "type_text"
}
```

**RPA执行结果格式**:
```json
{
  "status": "success",
  "action": "click",
  "timestamp": "2024-02-04T00:55:00",
  "screenshot_path": "./screenshots/xxx.png"
}
```

---

## 网络配置

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

## 开发时间分配

| 电脑 | 主要任务 | 预计时间 |
|------|----------|----------|
| 电脑A | Agent核心 + 知识库 + 后端API | 5-7天 |
| 电脑B | RPA工具 + Web前端 | 5-7天 |
| 联调 | 集成测试 + Bug修复 | 2-3天 |

**可并行开发**：电脑A和电脑B可以同时开发，通过Git同步代码。
