# 创建虚拟环境
Write-Host "🚀 开始设置Qwen3虚拟环境..." -ForegroundColor Cyan
Write-Host ""

# 检查Python版本
Write-Host "检查Python版本..." -ForegroundColor Green
python --version

# 创建虚拟环境
Write-Host "`n创建虚拟环境..." -ForegroundColor Green
python -m venv venv

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

# 升级pip
Write-Host "`n升级pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# 安装PyTorch
Write-Host "`n安装PyTorch (CUDA 11.8)..." -ForegroundColor Green
Write-Host "这可能需要几分钟，请耐心等待..." -ForegroundColor Yellow
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装transformers
Write-Host "`n安装transformers和tokenizers..." -ForegroundColor Green
pip install "transformers>=5.0.0" "tokenizers>=0.22.0" accelerate

# 安装Web服务
Write-Host "`n安装Flask..." -ForegroundColor Green
pip install flask

# 安装RPA依赖
Write-Host "`n安装RPA工具依赖..." -ForegroundColor Green
pip install pillow pyautogui pyperclip requests

# 保存依赖列表
Write-Host "`n保存依赖列表到requirements.txt..." -ForegroundColor Green
pip freeze > requirements.txt

# 完成
Write-Host "`n" -NoNewline
Write-Host "✅ 虚拟环境设置完成！" -ForegroundColor Green
Write-Host ""
Write-Host "下一步：" -ForegroundColor Cyan
Write-Host "  1. 运行Qwen3服务: " -NoNewline -ForegroundColor White
Write-Host "python qwen3_local_service.py" -ForegroundColor Yellow
Write-Host "  2. 运行对话Agent: " -NoNewline -ForegroundColor White
Write-Host "python demo_chat_agent.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "提示: 每次打开新终端都要先激活虚拟环境" -ForegroundColor Gray
Write-Host "      .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
