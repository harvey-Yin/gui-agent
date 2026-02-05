# 工作流程报告2: MAI-UI视觉模型部署调试

## 📋 流程概述

本报告整合了MAI-UI-2B/8B模型的Docker部署、调试和集成的完整流程。

---

## 🎯 MAI-UI模型介绍

**MAI-UI** 是阿里巴巴通义实验室开源的GUI智能体模型，可以通过自然语言+截图理解并操作用户界面。

- **HuggingFace**: https://huggingface.co/Tongyi-MAI/MAI-UI-8B
- **GitHub**: https://github.com/Tongyi-MAI/MAI-UI
- **推理引擎**: vLLM（高性能推理）
- **API方式**: OpenAI兼容接口

### 模型对比

| 指标 | MAI-UI-8B | MAI-UI-2B |
|------|-----------|-----------|
| 参数量 | 8B | 2B |
| 显存占用 | 16.64 GB | 4.24 GB |
| 12GB GPU兼容 | ❌ 需要量化 | ✅ 完美运行 |
| 加载时间 | ~140秒 | ~45秒 |
| 识别准确度 | 更高 | 足够用 |
| 推荐场景 | 24GB+ GPU | 12GB GPU |

**结论**: 对于12GB显存（如RTX 4070），推荐使用MAI-UI-2B。

---

## 🚀 Docker部署流程（推荐方式）

### Step 1: 环境准备

**系统要求**:
- Windows 11 + Docker Desktop
- WSL2已启用
- NVIDIA GPU（12GB+显存）
- CUDA支持

**检查环境**:
```powershell
# 检查Docker
docker --version

# 检查GPU
nvidia-smi

# 检查WSL2
wsl --list --verbose
```

### Step 2: 创建docker-compose.yml

**位置**: `c:\document\python\gui-agent\gui-agent\docker-compose.yml`

```yaml
version: '3.8'

services:
  vllm-mai-ui:
    image: vllm/vllm-openai:latest
    container_name: mai-ui-2b-agent
    ports:
      - "8001:8000"
    environment:
      - HF_ENDPOINT=https://hf-mirror.com  # 国内镜像
      - CUDA_VISIBLE_DEVICES=0
    volumes:
      - ${USERPROFILE}/.cache/huggingface:/root/.cache/huggingface
    command: >
      --model Tongyi-MAI/MAI-UI-2B
      --served-model-name MAI-UI-2B
      --host 0.0.0.0
      --port 8000
      --trust-remote-code
      --dtype float16
      --gpu-memory-utilization 0.85
      --max-model-len 4096
      --enforce-eager
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/v1/models"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Step 3: 启动服务

```powershell
# 进入项目目录
cd c:\document\python\gui-agent\gui-agent

# 启动服务（首次会下载模型，需要10-30分钟）
docker-compose up -d

# 查看日志
docker-compose logs -f
```

**首次启动日志**:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: 验证服务

```powershell
# 检查模型列表
curl http://localhost:8001/v1/models

# 测试简单推理
curl http://localhost:8001/v1/chat/completions `
  -H "Content-Type: application/json" `
  -d '{
    "model": "MAI-UI-2B",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 100
  }'
```

**预期输出**:
```json
{
  "id": "cmpl-xxx",
  "model": "MAI-UI-2B",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "你好！我是MAI-UI..."
    }
  }]
}
```

---

## 🧪 GUI识别测试

### 测试脚本

**文件**: `test_mai_ui_api.py`

```python
import openai
import base64
from pathlib import Path

# 配置API
client = openai.OpenAI(
    base_url="http://localhost:8001/v1",
    api_key="dummy"  # vLLM不需要真实key
)

# 读取截图
screenshot_path = "screenshot.png"
with open(screenshot_path, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

# 调用MAI-UI
response = client.chat.completions.create(
    model="MAI-UI-2B",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_base64}"
                }
            },
            {
                "type": "text",
                "text": "请描述这个界面上有什么元素"
            }
        ]
    }],
    max_tokens=512
)

print(response.choices[0].message.content)
```

### 测试结果

**识别能力** ✅:
- IDE类型（VS Code）
- 当前文件名
- 文件列表
- Source Control面板
- Docker配置详情
- 文件修改状态

**性能指标**:
- 模型加载时间: ~45秒
- 推理速度: ~5-10秒/请求
- 显存占用: 4.24 GB / 12 GB

---

## 🔧 常见问题与解决方案

### 问题1: 显存不足 (OOM)

**症状**: 
```
torch.cuda.OutOfMemoryError: CUDA out of memory
```

**解决方案**:

**方案A: 降低显存利用率**
```yaml
command: >
  --gpu-memory-utilization 0.75  # 从0.85降到0.75
```

**方案B: 减少上下文长度**
```yaml
command: >
  --max-model-len 2048  # 从4096降到2048
```

**方案C: 使用MAI-UI-2B代替8B**
```yaml
command: >
  --model Tongyi-MAI/MAI-UI-2B  # 显存需求4GB vs 17GB
```

### 问题2: 模型下载失败

**症状**:
```
HTTPSConnectionPool: Max retries exceeded
```

**解决方案**:

**方案A: 使用国内镜像**
```yaml
environment:
  - HF_ENDPOINT=https://hf-mirror.com
```

**方案B: 手动预下载**
```powershell
# 安装huggingface-cli
pip install huggingface-hub

# 下载模型
huggingface-cli download Tongyi-MAI/MAI-UI-2B --local-dir ./models/MAI-UI-2B

# 修改docker-compose.yml使用本地路径
command: >
  --model /models/MAI-UI-2B
```

### 问题3: Docker容器启动失败

**症状**:
```
Error response from daemon: could not select device driver "nvidia"
```

**解决方案**:

1. **安装NVIDIA Container Toolkit**
```powershell
# 在WSL2中安装
wsl
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

2. **检查Docker Desktop设置**
- 打开Docker Desktop
- Settings → Resources → WSL Integration
- 启用WSL2集成

3. **验证GPU可用性**
```powershell
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### 问题4: API响应慢

**症状**: 推理时间超过30秒

**解决方案**:

**方案A: 启用CUDA Graphs**（需要更多显存）
```yaml
command: >
  # 移除 --enforce-eager
```

**方案B: 增加tensor并行**（多GPU）
```yaml
command: >
  --tensor-parallel-size 2  # 使用2个GPU
```

**方案C: 减少max_tokens**
```python
response = client.chat.completions.create(
    max_tokens=256  # 从512降到256
)
```

---

## 🔗 集成到RPA项目

### 方式1: 封装为RPA工具

**文件**: `rpa_tools/mai_ui_vision.py`

```python
import openai
import base64
from typing import Dict, Any
from .base_tool import RPAToolBase

class MAIUIVisionTool(RPAToolBase):
    """MAI-UI视觉识别工具"""
    
    def __init__(self, api_base="http://localhost:8001/v1"):
        super().__init__()
        self.description = "使用MAI-UI模型识别GUI元素"
        self.client = openai.OpenAI(base_url=api_base, api_key="dummy")
    
    def execute(self, screenshot_path: str, instruction: str) -> Dict[str, Any]:
        """
        使用MAI-UI识别GUI元素
        
        Args:
            screenshot_path: 截图文件路径
            instruction: 识别指令（如"找到登录按钮"）
        """
        try:
            # 读取截图
            with open(screenshot_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode()
            
            # 调用MAI-UI
            response = self.client.chat.completions.create(
                model="MAI-UI-2B",
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        },
                        {"type": "text", "text": instruction}
                    ]
                }],
                max_tokens=512
            )
            
            result_text = response.choices[0].message.content
            
            return {
                "status": "success",
                "result": result_text,
                "message": f"MAI-UI识别完成: {result_text[:100]}..."
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
```

### 方式2: 在Agent中使用

```python
from rpa_tools import get_rpa_tools, MAIUIVisionTool

# 注册MAI-UI工具
mai_ui_tool = MAIUIVisionTool()
tools = get_rpa_tools() + [mai_ui_tool]

# 在Agent中使用
agent = create_react_agent(llm, tools, prompt)
result = agent.invoke({
    "input": "截图当前屏幕，然后找到登录按钮并点击"
})
```

---

## 📊 性能优化建议

### 针对12GB显存的最佳配置

```yaml
command: >
  --model Tongyi-MAI/MAI-UI-2B
  --gpu-memory-utilization 0.85
  --max-model-len 4096
  --enforce-eager
  --dtype float16
```

**关键参数说明**:
- `max-model-len 4096`: 支持视觉语言输入
- `gpu-memory-utilization 0.85`: 留15%给系统
- `enforce-eager`: 禁用CUDA Graphs节省显存

### 性能对比

| 配置 | 显存占用 | 加载时间 | 推理速度 |
|------|---------|---------|---------|
| 默认配置 | 9.2 GB | ~60s | ~8s |
| 优化配置 | 4.24 GB | ~45s | ~5s |
| 量化INT8 | 2.8 GB | ~50s | ~12s |

---

## ✅ 部署成功标志

1. **Docker容器运行中**
```powershell
docker ps
# 应该看到 mai-ui-2b-agent 容器
```

2. **API响应正常**
```powershell
curl http://localhost:8001/v1/models
# 返回模型列表
```

3. **GUI识别测试通过**
```powershell
python test_mai_ui_api.py
# 成功识别截图内容
```

4. **显存占用合理**
```powershell
nvidia-smi
# GPU显存占用 < 6GB
```

---

## 📝 下一步

### 选项A: 深入MAI-UI应用
- [ ] 测试更多GUI识别场景
- [ ] 优化prompt提高准确率
- [ ] 封装为完整的RPA工具类
- [ ] 集成到Agent工作流

### 选项B: 回归RPA项目主线
- [ ] Phase 2: 开发Agent核心
- [ ] 集成qwen:7b（已验证）
- [ ] 实现第一个Agent Demo
- [ ] MAI-UI作为高级特性后期集成

**推荐**: 选B，MAI-UI已验证可用，可作为增强功能后期集成。

---

## 🆘 故障排查清单

| 问题 | 检查项 | 解决方案 |
|------|--------|---------|
| 容器无法启动 | Docker Desktop运行？ | 启动Docker Desktop |
| GPU不可用 | nvidia-smi正常？ | 安装NVIDIA驱动 |
| 显存不足 | 显存占用？ | 降低gpu-memory-utilization |
| 下载失败 | 网络连接？ | 使用HF镜像 |
| API无响应 | 端口冲突？ | 检查8001端口占用 |

---

**部署完成！现在可以在RPA项目中使用MAI-UI的强大视觉识别能力了！** 🎉
