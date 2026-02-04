# MAI-UI 启动服务脚本
# 用于启动已安装的MAI-UI-8B服务

$ErrorActionPreference = "Stop"

$MAI_DIR = "c:\document\python\mai-ui-deploy"

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "启动 MAI-UI-8B vLLM 服务" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

Write-Host "`nAPI地址: http://localhost:8001/v1" -ForegroundColor Green
Write-Host "按 Ctrl+C 停止服务`n" -ForegroundColor Yellow

Set-Location $MAI_DIR

# 启动vLLM服务器
& "$MAI_DIR\venv_mai\Scripts\python.exe" -m vllm.entrypoints.openai.api_server `
  --model Tongyi-MAI/MAI-UI-8B `
  --served-model-name MAI-UI-8B `
  --host 0.0.0.0 `
  --port 8001 `
  --tensor-parallel-size 1 `
  --trust-remote-code
