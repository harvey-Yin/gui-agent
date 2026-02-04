# MAI-UI 依赖问题解决方案

## 问题原因
- MAI-UI的requirements.txt要求 `numpy==2.3.5`
- numpy 2.3.5需要Python 3.11+
- 你的系统是Python 3.10.6

## 解决方案（3选1）

---

### 方案1：放宽numpy版本要求（推荐⭐）

修改MAI-UI的requirements.txt，不强制特定numpy版本：

```powershell
cd c:\document\python\mai-ui-deploy\MAI-UI

# 编辑requirements.txt，将 numpy==2.3.5 改为 numpy>=1.24.0,<3.0

# 然后重新安装
c:\document\python\mai-ui-deploy\venv_mai\Scripts\python.exe -m pip install -r requirements.txt
```

**手动修改步骤**：
1. 打开 `c:\document\python\mai-ui-deploy\MAI-UI\requirements.txt`
2. 找到 `numpy==2.3.5`
3. 改为 `numpy>=1.24.0,<3.0`
4. 保存文件
5. 重新运行安装命令

---

### 方案2：升级Python到3.11+（彻底解决）

```powershell
# 1. 下载Python 3.11或3.12
# 访问 https://www.python.org/downloads/

# 2. 安装后，重新创建虚拟环境
cd c:\document\python\mai-ui-deploy
Remove-Item -Recurse -Force venv_mai  # 删除旧环境

# 使用新Python创建环境
python3.11 -m venv venv_mai

# 重新安装依赖
.\venv_mai\Scripts\python.exe -m pip install vllm>=0.11.0 transformers>=4.57.0
cd MAI-UI
..\venv_mai\Scripts\python.exe -m pip install -r requirements.txt
```

---

### 方案3：跳过MAI-UI依赖，只安装vLLM（简化方案）

如果只是想运行MAI-UI模型推理，不需要完整的MAI-UI工具包：

```powershell
# 已经安装了vLLM和transformers，就可以直接启动模型服务
cd c:\document\python\mai-ui-deploy

.\venv_mai\Scripts\python.exe -m vllm.entrypoints.openai.api_server --model Tongyi-MAI/MAI-UI-8B --served-model-name MAI-UI-8B --host 0.0.0.0 --port 8001 --tensor-parallel-size 1 --trust-remote-code
```

---

## 推荐行动

**我推荐方案1或方案3**：

### 立即可执行（方案3）
既然vLLM已安装成功，可以直接启动模型服务，不管MAI-UI工具包的依赖问题：

```powershell
cd c:\document\python\mai-ui-deploy
.\venv_mai\Scripts\python.exe -m vllm.entrypoints.openai.api_server --model Tongyi-MAI/MAI-UI-8B --served-model-name MAI-UI-8B --host 0.0.0.0 --port 8001 --tensor-parallel-size 1 --trust-remote-code
```

**首次运行会下载约16GB模型**，请确保：
1. 有足够硬盘空间
2. 网络稳定
3. 有合适的GPU

---

## 检查GPU

在启动vLLM前，先检查GPU：

```powershell
nvidia-smi
```

需要看到：
- NVIDIA驱动正常
- CUDA版本显示
- GPU显存>=16GB（用于8B模型）

如果显存不足，可以改用MAI-UI-2B模型（只需4-6GB显存）。
