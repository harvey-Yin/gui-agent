# MAI-UI-8B 手动部署步骤
# 如果PowerShell脚本无法运行，请按照以下步骤手动执行

## 解决方案：逐条执行命令

### Step 1: 创建项目目录
```powershell
cd c:\document\python
mkdir mai-ui-deploy -ErrorAction SilentlyContinue
cd mai-ui-deploy
```

### Step 2: 创建虚拟环境
```powershell
python -m venv venv_mai
```

### Step 3: 激活虚拟环境
```powershell
.\venv_mai\Scripts\activate
```

### Step 4: 升级pip
```powershell
python -m pip install --upgrade pip
```

### Step 5: 安装vLLM（约5-10分钟）
```powershell
pip install vllm>=0.11.0
```

### Step 6: 安装transformers
```powershell
pip install transformers>=4.57.0
```

### Step 7: 安装PyTorch（选择合适的CUDA版本）
```powershell
# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 如果CUDA 11.8，使用：
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Step 8: 克隆MAI-UI代码库
```powershell
git clone https://github.com/Tongyi-MAI/MAI-UI.git
cd MAI-UI
pip install -r requirements.txt
```

### Step 9: 启动vLLM服务（首次会下载16GB模型）
```powershell
python -m vllm.entrypoints.openai.api_server --model Tongyi-MAI/MAI-UI-8B --served-model-name MAI-UI-8B --host 0.0.0.0 --port 8001 --tensor-parallel-size 1 --trust-remote-code
```

---

## 测试API（新开终端）
```powershell
# 查看模型
curl http://localhost:8001/v1/models

# 测试推理
curl http://localhost:8001/v1/chat/completions -H "Content-Type: application/json" -d '{\"model\": \"MAI-UI-8B\", \"messages\": [{\"role\": \"user\", \"content\": \"你好\"}]}'
```

---

## 注意事项
- 确保有NVIDIA GPU（16GB+显存）
- 确保安装了CUDA驱动
- 首次运行会下载约16GB模型文件
- 下载时间取决于网络速度（可能10-60分钟）
