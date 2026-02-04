# MAI-UI 快速部署脚本
# 自动化安装和启动MAI-UI-8B

# 设置错误时停止
$ErrorActionPreference = "Stop"

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "MAI-UI-8B 自动部署脚本" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Step 1: 检查环境
Write-Host "`n[Step 1] 检查环境..." -ForegroundColor Yellow
python --version
nvidia-smi

# Step 2: 创建项目目录
Write-Host "`n[Step 2] 创建项目目录..." -ForegroundColor Yellow
$MAI_DIR = "c:\document\python\mai-ui-deploy"
if (-not (Test-Path $MAI_DIR)) {
    New-Item -ItemType Directory -Path $MAI_DIR
}
Set-Location $MAI_DIR

# Step 3: 创建虚拟环境
Write-Host "`n[Step 3] 创建虚拟环境..." -ForegroundColor Yellow
if (-not (Test-Path "venv_mai")) {
    python -m venv venv_mai
}

# Step 4: 激活虚拟环境并安装依赖
Write-Host "`n[Step 4] 安装依赖（这可能需要5-10分钟）..." -ForegroundColor Yellow
& "$MAI_DIR\venv_mai\Scripts\python.exe" -m pip install --upgrade pip
& "$MAI_DIR\venv_mai\Scripts\python.exe" -m pip install vllm>=0.11.0
& "$MAI_DIR\venv_mai\Scripts\python.exe" -m pip install transformers>=4.57.0
& "$MAI_DIR\venv_mai\Scripts\python.exe" -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Step 5: 克隆MAI-UI代码库
Write-Host "`n[Step 5] 克隆MAI-UI代码库..." -ForegroundColor Yellow
if (-not (Test-Path "MAI-UI")) {
    git clone https://github.com/Tongyi-MAI/MAI-UI.git
}
Set-Location MAI-UI
& "$MAI_DIR\venv_mai\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host "`n=======================================" -ForegroundColor Green
Write-Host "✓ 安装完成！" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

Write-Host "`n下一步：启动vLLM服务" -ForegroundColor Cyan
Write-Host "运行以下命令：" -ForegroundColor White
Write-Host "cd $MAI_DIR" -ForegroundColor Yellow
Write-Host ".\venv_mai\Scripts\activate" -ForegroundColor Yellow
Write-Host "python -m vllm.entrypoints.openai.api_server --model Tongyi-MAI/MAI-UI-8B --served-model-name MAI-UI-8B --host 0.0.0.0 --port 8001 --tensor-parallel-size 1 --trust-remote-code" -ForegroundColor Yellow
