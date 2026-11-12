# 视觉引导Agent系统 - 使用指南

## 快速开始

### 1. 确保服务运行

```powershell
# 启动MAI-UI-2B Docker
cd c:\document\python\gui-agent
docker-compose up -d

# 启动Ollama（另一个终端）
ollama serve
```

### 2. 运行Agent

```powershell
cd c:\document\python\gui-agent
python demo_agent.py
```

## 系统架构

```
┌─────────────────────────────────────────────┐
│              Agent Main Loop                │
│                                             │
│  1. Perception (感知)                       │
│     └─ MAI-UI-2B视觉分析                    │
│                                             │
│  2. Reasoning (推理)                        │
│     └─ qwen决定下一步                       │
│                                             │
│  3. Action (行动)                           │
│     └─ 执行工具                             │
│                                             │
│  4. Reflection (反思)                       │
│     └─ 更新状态                             │
└─────────────────────────────────────────────┘
```

## 核心模块

### VisionModule (`rpa_tools/vision_module.py`)
- 截图当前屏幕
- 调用MAI-UI-2B分析
- 返回结构化观察结果

### ReasoningModule (`rpa_tools/reasoning_module.py`)
- 使用qwen分析状态
- 决定下一步行动
- 返回JSON格式决策

### ActionModule (`rpa_tools/action_module.py`)
- 执行具体操作
- 9个可用工具

### AgentCore (`rpa_tools/agent_core.py`)
- 主循环控制
- 状态管理
- 任务完成判断

## 可用工具

| 工具 | 功能 | 参数示例 |
|------|------|---------|
| `open_wps` | 打开WPS | `{}` |
| `click` | 点击坐标 | `{"x": 500, "y": 300}` |
| `type_text` | 输入文本 | `{"text": "Hello"}` |
| `paste_text` | 粘贴文本 | `{"text": "中文内容"}` |
| `hotkey` | 快捷键 | `{"keys": ["ctrl", "s"]}` |
| `wait` | 等待 | `{"seconds": 2}` |
| `get_weather` | 获取天气 | `{"city": "Beijing"}` |
| `generate_article` | 生成文章 | `{"prompt": "..."}` |
| `complete_task` | 完成任务 | `{}` |

## 执行流程示例

**任务**: 打开WPS并生成天气文章

1. **迭代1**: 观察桌面 → 决定打开WPS → 执行
2. **迭代2**: 观察WPS启动 → 决定等待 → 执行
3. **迭代3**: 观察WPS界面 → 决定新建文档 → 执行
4. **迭代4**: 观察空白文档 → 决定获取天气 → 执行
5. **迭代5**: 有天气数据 → 决定生成文章 → 执行
6. **迭代6**: 有文章内容 → 决定写入标题 → 执行
7. **迭代7**: 标题已写入 → 决定粘贴文章 → 执行
8. **迭代8**: 内容完整 → 决定保存 → 执行
9. **迭代9**: 文档已保存 → 决定完成任务 → 完成

## 关键优势

### vs 固定脚本
- ✅ **自适应**: 界面变化也能应对
- ✅ **智能决策**: AI自主判断
- ✅ **可解释**: 每步都有推理过程
- ✅ **容错**: 遇错能恢复

### vs 人工操作
- ⚡ **快速**: 自动化执行
- 🔄 **可重复**: 一致性高
- 📝 **可追溯**: 完整历史记录

## 调试技巧

### 查看详细日志
Agent会打印每次迭代的：
- 视觉观察结果
- 推理过程
- 执行结果
- 状态更新

### 调整参数
```python
agent = VisionGuidedAgent(
    task_description="你的任务",
    max_iterations=30  # 增加最大迭代次数
)
```

### 测试单个模块
```python
# 测试视觉模块
from rpa_tools import VisionModule
vision = VisionModule()
result = vision.analyze_screen("测试任务", "INIT")
print(result)
```

## 常见问题

### Agent一直循环
- 检查任务描述是否清晰
- 查看推理日志，看AI是否理解任务
- 可能需要优化Prompt

### 视觉识别不准确
- 确保MAI-UI-2B Docker正常运行
- 检查截图是否清晰
- 可以调整temperature参数

### 决策不合理
- 检查qwen是否正常运行
- 查看推理Prompt是否合适
- 可能需要添加Few-shot示例

## 扩展开发

### 添加新工具
在`ActionModule`中添加方法：
```python
def _action_your_tool(self, params: Dict) -> Dict:
    # 实现逻辑
    return {
        'success': True,
        'result': '描述',
        'data': None
    }
```

### 自定义任务
```python
agent = VisionGuidedAgent(
    task_description="你的自定义任务描述"
)
agent.run()
```

## 下一步

- [ ] 优化Prompt提高决策准确率
- [ ] 添加更多工具
- [ ] 实现错误恢复机制
- [ ] 支持多任务并行
