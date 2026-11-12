# Qwen3-8B-FP8 本地部署指南

## 方案：使用transformers直接加载（不用Ollama）

### 1. 安装依赖

```powershell
pip install transformers torch flask accelerate
```

### 2. 下载模型（首次运行会自动下载）

模型会自动从ModelScope下载到：
`C:\Users\你的用户名\.cache\huggingface\hub\`

大小约8GB，需要等待下载。

### 3. 启动本地服务

```powershell
cd c:\document\python\gui-agent
python qwen3_local_service.py
```

**首次启动**：
- 会自动下载模型（~8GB）
- 下载完成后加载到GPU
- 看到"服务启动"后即可使用

**后续启动**：
- 直接加载本地模型
- 约30秒-1分钟启动

### 4. 测试服务

```powershell
# 测试API
curl http://localhost:11434/api/generate -d '{"prompt":"你好","stream":false}'
```

### 5. Agent自动使用

Agent代码已经配置为使用 `http://localhost:11434/api/generate`，无需修改！

启动服务后直接运行：
```powershell
python demo_chat_agent.py
```

## 优势

### vs Ollama
- ✅ **直接控制**：完全控制模型加载和推理
- ✅ **无需额外软件**：不依赖Ollama
- ✅ **灵活配置**：可以自定义参数

### vs 云API
- ✅ **本地运行**：数据不出本地
- ✅ **无限制**：不受API限制
- ✅ **免费**：无调用费用

## 配置说明

### 修改模型参数

在 `qwen3_local_service.py` 中：

```python
# 修改最大生成长度
max_new_tokens=2048  # 改为4096或更大

# 修改温度
temperature=0.7  # 0.1-1.0之间

# 启用思考模式
enable_thinking=True  # 更强推理，但更慢
```

### 内存要求

- **最小**: 12GB GPU显存
- **推荐**: 16GB GPU显存
- **CPU模式**: 可用但很慢（不推荐）

## 故障排查

### 显存不足
```
OutOfMemoryError: CUDA out of memory
```

**解决**：
1. 关闭其他GPU程序
2. 减小 `max_new_tokens`
3. 使用CPU模式（很慢）

### 下载失败
```
Connection error
```

**解决**：
```python
# 在代码开头添加镜像
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
```

### 模型加载慢
- 首次下载：正常，需要等待
- 后续加载：约30秒-1分钟

## 与Agent集成

Agent的三个模块已配置为使用本地服务：
- `ReasoningModule` - 决策推理
- `ActionModule` - 文章生成  
- `ConversationalAgent` - 对话

**完整流程**：
1. 启动Qwen3服务：`python qwen3_local_service.py`
2. 启动MAI-UI Docker：`docker-compose up -d`
3. 运行Agent：`python demo_chat_agent.py`

## 性能对比

| 指标 | Ollama qwen:7b | Qwen3-8B-FP8 |
|------|----------------|--------------|
| 模型大小 | 4.5GB | 8.2GB |
| 推理速度 | 快 | 中等 |
| 推理质量 | 好 | 更好 |
| 启动时间 | 快 | 慢（首次） |

## 下一步

模型启动后，可以：
1. 测试对话Agent
2. 测试视觉识别
3. 执行完整的RPA任务
