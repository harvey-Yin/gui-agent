# MAI-UI-8B 量化版启动指南

## 启动步骤

### 1. 打开PowerShell终端

### 2. 运行启动命令

```powershell
cd c:\document\python\mai-ui-deploy

.\venv_mai\Scripts\python.exe -m vllm.entrypoints.openai.api_server --model Tongyi-MAI/MAI-UI-8B --served-model-name MAI-UI-8B --quantization int8 --host 0.0.0.0 --port 8001 --tensor-parallel-size 1 --trust-remote-code --gpu-memory-utilization 0.9
```

### 3. 等待模型加载

**首次运行**：
- 会从HuggingFace下载约16GB模型文件
- 下载到：`C:\Users\你的用户名\.cache\huggingface\hub\`
- 下载时间：10-60分钟（取决于网络）

**后续运行**：
- 使用已下载的模型
- 加载时间：约30-60秒

### 4. 成功标志

看到以下输出说明启动成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### 5. 测试API（新开终端）

```powershell
# 查看模型列表
curl http://localhost:8001/v1/models

# 测试推理
curl http://localhost:8001/v1/chat/completions -H "Content-Type: application/json" -d '{\"model\": \"MAI-UI-8B\", \"messages\": [{\"role\": \"user\", \"content\": \"你好\"}]}'
```

---

## 监控显存使用

在另一个终端运行：
```powershell
nvidia-smi -l 1
```

会实时显示显存占用，预期：
- 加载中：逐渐增加到8-10GB
- 运行中：稳定在8-10GB
- 推理时：可能短暂升高

---

## 如果启动失败

### 情况1：显存不足（OOM错误）

**降低显存使用**：
```powershell
# 减少GPU利用率到80%
--gpu-memory-utilization 0.8
```

**或者换用2B模型**：
```powershell
.\venv_mai\Scripts\python.exe -m vllm.entrypoints.openai.api_server --model Tongyi-MAI/MAI-UI-2B --port 8001 --trust-remote-code
```

### 情况2：下载失败

**使用镜像加速**：
```powershell
$env:HF_ENDPOINT = "https://hf-mirror.com"
# 然后重新运行启动命令
```

### 情况3：CUDA错误

检查CUDA驱动：
```powershell
nvidia-smi
```

确保显示CUDA版本（如CUDA 12.1或11.8）

---

## 停止服务

在vLLM运行的终端按：`Ctrl+C`

---

## 下一步

启动成功后，可以：
1. 测试GUI识别能力（通过API调用）
2. 集成到你的RPA项目中
3. 对比与qwen:7b的效果差异
