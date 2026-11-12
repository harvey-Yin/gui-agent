# Qwen3-8B-FP8 虚拟环境部署指南

## 为什么使用虚拟环境？

- ✅ **隔离依赖**：不影响系统Python环境
- ✅ **版本管理**：精确控制包版本
- ✅ **易于清理**：出问题直接删除重建
- ✅ **多项目并存**：不同项目不同环境

## 方案1：使用venv（推荐）

### 1. 创建虚拟环境

```powershell
# 进入项目目录
cd c:\document\python\gui-agent

# 创建虚拟环境（名为venv）
python -m venv venv
```

### 2. 激活虚拟环境

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
.\venv\Scripts\activate.bat

# 激活后，命令行前会显示 (venv)
```

### 3. 升级pip

```powershell
python -m pip install --upgrade pip
```

### 4. 安装依赖

```powershell
# 安装PyTorch（CUDA 11.8）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装transformers和相关库
pip install transformers>=5.0.0 tokenizers>=0.22.0 accelerate

# 安装Web服务
pip install flask

# 安装其他依赖
pip install pillow pyautogui pyperclip requests
```

### 5. 下载模型（首次运行）

```powershell
# 运行服务会自动下载
python qwen3_local_service.py
```

### 6. 保存依赖列表

```powershell
# 导出依赖
pip freeze > requirements.txt
```

### 7. 退出虚拟环境

```powershell
deactivate
```

---

## 方案2：使用conda

### 1. 创建conda环境

```powershell
# 创建Python 3.10环境
conda create -n qwen3 python=3.10

# 激活环境
conda activate qwen3
```

### 2. 安装PyTorch

```powershell
# 使用conda安装PyTorch
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 3. 安装其他依赖

```powershell
pip install transformers>=5.0.0 tokenizers>=0.22.0 accelerate flask
pip install pillow pyautogui pyperclip requests
```

### 4. 退出环境

```powershell
conda deactivate
```

---

## 完整部署流程（venv）

### 一键部署脚本

创建 `setup_venv.ps1`：

```powershell
# 创建虚拟环境
Write-Host "创建虚拟环境..." -ForegroundColor Green
python -m venv venv

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

# 升级pip
Write-Host "升级pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# 安装PyTorch
Write-Host "安装PyTorch (CUDA 11.8)..." -ForegroundColor Green
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装transformers
Write-Host "安装transformers..." -ForegroundColor Green
pip install transformers>=5.0.0 tokenizers>=0.22.0 accelerate

# 安装其他依赖
Write-Host "安装其他依赖..." -ForegroundColor Green
pip install flask pillow pyautogui pyperclip requests

# 保存依赖列表
Write-Host "保存依赖列表..." -ForegroundColor Green
pip freeze > requirements.txt

Write-Host "✅ 虚拟环境设置完成！" -ForegroundColor Green
Write-Host "运行: python qwen3_local_service.py" -ForegroundColor Yellow
```

运行：
```powershell
powershell -ExecutionPolicy Bypass -File setup_venv.ps1
```

---

## 使用虚拟环境运行Agent

### 启动流程

```powershell
# 1. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 2. 启动Qwen3服务
python qwen3_local_service.py

# 新终端窗口
# 3. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 4. 启动MAI-UI Docker
docker-compose up -d

# 5. 运行对话Agent
python demo_chat_agent.py
```

---

## requirements.txt 示例

创建 `requirements.txt`：

```
torch==2.7.1
torchvision==0.22.1
torchaudio==2.7.1
transformers==5.0.0
tokenizers==0.22.2
accelerate==0.27.2
flask==3.0.0
pillow==10.1.0
pyautogui==0.9.54
pyperclip==1.8.2
requests==2.31.0
```

使用：
```powershell
# 激活虚拟环境后
pip install -r requirements.txt
```

---

## 常见问题

### Q1: 虚拟环境在哪里？
**A**: `c:\document\python\gui-agent\venv\`

### Q2: 如何删除虚拟环境？
**A**: 
```powershell
# 先退出
deactivate
# 直接删除文件夹
Remove-Item -Recurse -Force .\venv
```

### Q3: 如何重建虚拟环境？
**A**:
```powershell
# 删除旧环境
Remove-Item -Recurse -Force .\venv
# 重新创建
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Q4: PowerShell无法激活？
**A**: 执行策略问题
```powershell
# 临时允许
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# 然后激活
.\venv\Scripts\Activate.ps1
```

### Q5: 显存不足？
**A**: 虚拟环境不影响显存，这是硬件限制
- 关闭其他GPU程序
- 减小模型batch size
- 考虑使用更小的模型

---

## 目录结构

```
gui-agent/
├── venv/                    # 虚拟环境（不提交到git）
├── qwen3_local_service.py   # Qwen3服务
├── demo_chat_agent.py       # 对话Agent
├── rpa_tools/               # Agent模块
├── requirements.txt         # 依赖列表
├── setup_venv.ps1          # 一键部署脚本
└── .gitignore              # 忽略venv/
```

### .gitignore 配置

```
# 虚拟环境
venv/
env/
ENV/

# Python缓存
__pycache__/
*.pyc
*.pyo

# 模型缓存
.cache/
```

---

## 优势对比

| 特性 | 全局安装 | 虚拟环境 |
|------|---------|---------|
| 依赖隔离 | ❌ | ✅ |
| 版本冲突 | 易发生 | 不会 |
| 清理难度 | 困难 | 简单 |
| 多项目 | 冲突 | 独立 |
| 推荐度 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 下一步

虚拟环境设置完成后：

1. **首次运行**：`python qwen3_local_service.py`（下载模型）
2. **后续使用**：激活环境 → 运行服务
3. **开发调试**：在虚拟环境中安装新包

**记住**：每次打开新终端都要先激活虚拟环境！
