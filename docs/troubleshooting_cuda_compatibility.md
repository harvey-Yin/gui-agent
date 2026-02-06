# Docker CUDA兼容性问题解决方案

## 🔍 问题分析

**错误信息**:
```
nvidia-container-cli: requirement error: unsatisfied condition: cuda>=12.9
```

**原因**:
- 您的GPU驱动支持CUDA 12.4
- 最新的vLLM镜像 (`vllm/vllm-openai:latest`) 要求CUDA 12.9+
- 版本不兼容导致容器无法启动

**您的环境**:
- GPU: NVIDIA GeForce GTX 1650 Ti (4GB显存)
- CUDA Version: 12.4
- Driver Version: 551.23

---

## ✅ 解决方案

### 方案1: 使用兼容的vLLM镜像版本（推荐）

**已应用**: 修改`docker-compose.yml`使用`v0.6.0`版本

```yaml
services:
  vllm-mai-ui:
    image: vllm/vllm-openai:v0.6.0  # 兼容CUDA 12.4
```

**优势**:
- ✅ 无需升级驱动
- ✅ 稳定版本
- ✅ 兼容CUDA 12.1+

### 方案2: 升级NVIDIA驱动（备选）

如果方案1不行，可以升级驱动：

1. 访问 https://www.nvidia.com/Download/index.aspx
2. 选择GTX 1650 Ti
3. 下载最新驱动（支持CUDA 12.9+）
4. 安装后重启

---

## ⚠️ 显存限制警告

**重要**: GTX 1650 Ti只有4GB显存，可能无法运行MAI-UI-2B（需要4-6GB）

### 建议配置调整

```yaml
command: >
  --model Tongyi-MAI/MAI-UI-2B
  --gpu-memory-utilization 0.7      # 降低到70%
  --max-model-len 2048               # 减少上下文长度
  --enforce-eager                    # 节省显存
  --dtype float16
```

### 备选方案

如果4GB显存不够，考虑：

1. **使用量化模型**:
```yaml
command: >
  --model Tongyi-MAI/MAI-UI-2B
  --quantization int8  # INT8量化，显存需求~2-3GB
```

2. **使用CPU模式**（不推荐，很慢）:
```yaml
# 移除GPU相关配置，使用CPU
```

3. **使用其他轻量级视觉模型**:
- LLaVA-1.5-7B
- MiniGPT-4
- Qwen-VL-Chat

---

## 🚀 下一步操作

```powershell
# 1. 拉取新镜像
docker pull vllm/vllm-openai:v0.6.0

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

---

## 📊 预期结果

**成功标志**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**可能的警告**（可忽略）:
```
WARNING: GPU memory may be insufficient
```

如果仍然显存不足，请使用上述"建议配置调整"。
