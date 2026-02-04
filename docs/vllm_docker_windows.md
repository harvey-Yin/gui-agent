# Windows上使用Docker运行vLLM + MAI-UI-8B

## 为什么使用Docker？

**问题**: vLLM依赖uvloop，不支持Windows  
**解决**: Docker运行Linux容器 → vLLM可以正常工作 → OpenAI兼容API

---

## 前置要求

### 1. 安装Docker Desktop for Windows

**下载**: https://www.docker.com/products/docker-desktop

**安装后确认**:
```powershell
docker --version
docker-compose --version
```

### 2. 启用WSL2
Docker Desktop需要WSL2后端：
```powershell
wsl --install
wsl --set-default-version 2
```

### 3. GPU支持（可选但推荐）

**安装NVIDIA Container Toolkit**:
- Docker Desktop 4.25+ 自带GPU支持
- 确保Docker Desktop设置中启用GPU

**验证**:
```powershell
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

---

## 快速开始

### 方案A: docker-compose（推荐）

创建 `docker-compose.yml`:

```yaml
services:
  vllm-mai-ui:
    image: vllm/vllm-openai:latest
    container_name: mai-ui-8b
    ports:
      - "8001:8000"  # 映射到宿主机8001端口
    environment:
      - HF_ENDPOINT=https://hf-mirror.com  # 使用镜像加速
    volumes:
      - ~/.cache/huggingface:/root/.cache/huggingface  # 模型缓存
    command: >
      --model Tongyi-MAI/MAI-UI-8B
      --served-model-name MAI-UI-8B
      --host 0.0.0.0
      --port 8000
      --trust-remote-code
      --dtype float16
      --max-model-len 4096
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped
```

**启动**:
```powershell
cd c:\document\python\mai-ui-deploy
docker-compose up -d
```

**查看日志**:
```powershell
docker-compose logs -f
```

**停止**:
```powershell
docker-compose down
```

---

### 方案B: 直接运行容器

```powershell
docker run -d `
  --name mai-ui-8b `
  --gpus all `
  -p 8001:8000 `
  -v $HOME\.cache\huggingface:/root/.cache/huggingface `
  -e HF_ENDPOINT=https://hf-mirror.com `
  vllm/vllm-openai:latest `
  --model Tongyi-MAI/MAI-UI-8B `
  --served-model-name MAI-UI-8B `
  --host 0.0.0.0 `
  --port 8000 `
  --trust-remote-code `
  --dtype float16
```

---

## 使用方法

### 1. 启动容器后测试

```powershell
# 等待模型加载（首次下载约10-60分钟）
docker logs -f mai-ui-8b

# 看到"Uvicorn running"后测试
curl http://localhost:8001/v1/models
```

### 2. 在RPA项目中调用

```python
# 在你的项目中
import openai

client = openai.OpenAI(
    base_url="http://localhost:8001/v1",
    api_key="dummy"  # vLLM不需要真实key
)

response = client.chat.completions.create(
    model="MAI-UI-8B",
    messages=[
        {
            "role": "user",
            "content": "描述这个屏幕"
        }
    ]
)
print(response.choices[0].message.content)
```

---

## 优点

✅ **完整的vLLM功能**: OpenAI兼容API  
✅ **性能优化**: vLLM比Transformers快3-5倍  
✅ **易于管理**: 一键启停  
✅ **环境隔离**: 不污染Windows系统  
✅ **自动重启**: `restart: unless-stopped`

---

## 注意事项

### 显存管理
```yaml
# 在command中添加（如果12GB显存不够）
--gpu-memory-utilization 0.9  # 使用90%显存
--tensor-parallel-size 1      # 单GPU
```

### 模型缓存
首次启动会下载16GB模型到：
- Windows: `C:\Users\你的用户名\.cache\huggingface\`
- 容器内: `/root/.cache/huggingface/`

通过volume映射实现共享，避免重复下载。

### 网络加速
```yaml
environment:
  - HF_ENDPOINT=https://hf-mirror.com  # 国内镜像
```

---

## 故障排查

### 1. GPU不可用
```powershell
# 检查Docker GPU支持
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

如果失败，检查Docker Desktop设置 → Resources → WSL Integration → 启用GPU

### 2. 端口占用
```powershell
# 改用其他端口
ports:
  - "8002:8000"  # 改为8002
```

### 3. 内存不足
Docker Desktop默认限制内存，需要调整：
Settings → Resources → 增加Memory到16GB+

---

## 性能对比

| 方式 | 推理速度 | API | 易用性 | Windows兼容 |
|------|----------|-----|--------|-------------|
| Transformers | 慢 (~5s) | ❌ | ★★☆ | ✅ |
| vLLM (Docker) | 快 (~1-2s) | ✅ OpenAI | ★★★★ | ✅ |
| vLLM (WSL2原生) | 快 (~1-2s) | ✅ OpenAI | ★★☆ | ⚠️ 复杂 |

**推荐**: Docker方式 - 性能好且易于管理
