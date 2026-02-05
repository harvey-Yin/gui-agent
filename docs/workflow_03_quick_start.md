# 工作流程报告3: 快速启动与常用命令

## 📋 流程概述

本报告整合了项目的快速启动脚本、常用命令和日常操作流程。

---

## 🚀 快速启动命令

### 启动MAI-UI服务（Docker方式）

**PowerShell脚本**: `start_mai_ui.ps1`

```powershell
# MAI-UI Docker服务快速启动脚本

Write-Host "=== MAI-UI-2B 启动脚本 ===" -ForegroundColor Green

# 检查Docker是否运行
$dockerRunning = docker info 2>$null
if (-not $dockerRunning) {
    Write-Host "错误: Docker Desktop未运行，请先启动Docker Desktop" -ForegroundColor Red
    exit 1
}

# 进入项目目录
cd c:\document\python\gui-agent\gui-agent

# 启动服务
Write-Host "正在启动MAI-UI-2B服务..." -ForegroundColor Yellow
docker-compose up -d

# 等待服务启动
Write-Host "等待服务启动（约45秒）..." -ForegroundColor Yellow
Start-Sleep -Seconds 50

# 检查服务状态
Write-Host "检查服务状态..." -ForegroundColor Yellow
$response = Invoke-WebRequest -Uri "http://localhost:8001/v1/models" -UseBasicParsing -ErrorAction SilentlyContinue

if ($response.StatusCode -eq 200) {
    Write-Host "✅ MAI-UI-2B服务启动成功！" -ForegroundColor Green
    Write-Host "API地址: http://localhost:8001" -ForegroundColor Cyan
} else {
    Write-Host "⚠️ 服务可能还在启动中，请查看日志" -ForegroundColor Yellow
    Write-Host "运行命令查看日志: docker-compose logs -f" -ForegroundColor Cyan
}
```

**使用方法**:
```powershell
# 直接运行
.\docs\start_mai_ui.ps1

# 或者手动命令
cd c:\document\python\gui-agent\gui-agent
docker-compose up -d
```

---

## 🛠️ 常用Docker命令

### 服务管理

```powershell
# 启动服务（后台运行）
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 查看最近100行日志
docker-compose logs --tail=100
```

### 容器管理

```powershell
# 进入容器内部
docker exec -it mai-ui-2b-agent /bin/bash

# 查看容器资源占用
docker stats mai-ui-2b-agent

# 查看容器详细信息
docker inspect mai-ui-2b-agent

# 删除容器（需要先停止）
docker rm mai-ui-2b-agent
```

### GPU监控

```powershell
# 查看GPU使用情况
nvidia-smi

# 持续监控GPU（每2秒刷新）
nvidia-smi -l 2

# 查看特定进程的GPU占用
nvidia-smi pmon
```

---

## 🧪 测试与验证

### API测试命令

```powershell
# 1. 检查模型列表
curl http://localhost:8001/v1/models

# 2. 简单文本测试
curl http://localhost:8001/v1/chat/completions `
  -H "Content-Type: application/json" `
  -d '{
    "model": "MAI-UI-2B",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 100
  }'

# 3. 健康检查
curl http://localhost:8001/health
```

### Python测试脚本

**运行GUI识别测试**:
```powershell
# 确保已安装依赖
pip install openai pillow

# 运行测试
python test_mai_ui_api.py
```

---

## 📁 项目目录导航

### 核心目录结构

```
gui-agent/
├── rpa_tools/              # ✅ RPA工具集（已完成）
│   ├── base_tool.py        # 工具基类
│   ├── screen_tools.py     # 屏幕操作
│   ├── vision_tools.py     # 视觉识别
│   ├── excel_tools.py      # Excel处理
│   ├── word_tools.py       # Word处理
│   ├── data_tools.py       # 数据处理
│   └── tool_registry.py    # 工具注册
│
├── examples/               # 示例代码
│   └── rpa_tools_example.py
│
├── docs/                   # 📚 文档目录
│   ├── workflow_01_project_setup.md        # 项目搭建流程
│   ├── workflow_02_mai_ui_deployment.md    # MAI-UI部署流程
│   └── workflow_03_quick_start.md          # 本文档
│
├── docker-compose.yml      # Docker配置
├── test_mai_ui_api.py      # MAI-UI测试脚本
└── requirements.txt        # Python依赖
```

### 快速访问

```powershell
# 进入项目根目录
cd c:\document\python\gui-agent\gui-agent

# 查看RPA工具
cd rpa_tools

# 查看文档
cd docs

# 查看示例
cd examples
```

---

## 🔄 日常开发流程

### 开发RPA工具

```powershell
# 1. 激活虚拟环境
.\venv\Scripts\activate

# 2. 编辑工具代码
code rpa_tools/screen_tools.py

# 3. 运行测试
python examples/rpa_tools_example.py

# 4. 提交代码
git add rpa_tools/
git commit -m "feat: 添加新的RPA工具"
git push
```

### 测试MAI-UI集成

```powershell
# 1. 启动MAI-UI服务
docker-compose up -d

# 2. 等待服务就绪
Start-Sleep -Seconds 50

# 3. 运行测试
python test_mai_ui_api.py

# 4. 查看日志（如有问题）
docker-compose logs -f
```

### 调试问题

```powershell
# 1. 查看容器日志
docker-compose logs --tail=100

# 2. 检查GPU状态
nvidia-smi

# 3. 进入容器调试
docker exec -it mai-ui-2b-agent /bin/bash

# 4. 重启服务
docker-compose restart
```

---

## 📊 性能监控

### 实时监控脚本

**PowerShell监控**:
```powershell
# 创建监控脚本 monitor.ps1
while ($true) {
    Clear-Host
    Write-Host "=== MAI-UI 性能监控 ===" -ForegroundColor Green
    Write-Host ""
    
    # Docker状态
    Write-Host "Docker容器状态:" -ForegroundColor Yellow
    docker-compose ps
    Write-Host ""
    
    # GPU状态
    Write-Host "GPU使用情况:" -ForegroundColor Yellow
    nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv
    Write-Host ""
    
    # API状态
    Write-Host "API健康检查:" -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8001/v1/models" -UseBasicParsing -TimeoutSec 5
        Write-Host "✅ API正常" -ForegroundColor Green
    } catch {
        Write-Host "❌ API异常" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds 5
}
```

### 日志分析

```powershell
# 查看错误日志
docker-compose logs | Select-String "ERROR"

# 查看警告日志
docker-compose logs | Select-String "WARNING"

# 导出日志到文件
docker-compose logs > mai_ui_logs.txt
```

---

## 🔧 故障快速修复

### 常见问题速查

| 问题 | 快速修复命令 |
|------|-------------|
| 服务无响应 | `docker-compose restart` |
| 显存不足 | `docker-compose down` 然后修改配置 |
| 端口被占用 | `netstat -ano \| findstr :8001` 查找占用进程 |
| 容器无法启动 | `docker-compose down` → `docker-compose up -d` |
| GPU不可用 | 重启Docker Desktop |

### 一键重置

```powershell
# 完全重置MAI-UI服务
docker-compose down
docker system prune -f
docker-compose up -d
```

---

## 📝 配置文件快速编辑

### 修改Docker配置

```powershell
# 编辑docker-compose.yml
code docker-compose.yml

# 应用更改
docker-compose down
docker-compose up -d
```

### 常用配置调整

**降低显存占用**:
```yaml
command: >
  --gpu-memory-utilization 0.75  # 从0.85降到0.75
```

**提高推理速度**（需要更多显存）:
```yaml
command: >
  # 移除 --enforce-eager
```

**切换到8B模型**:
```yaml
command: >
  --model Tongyi-MAI/MAI-UI-8B  # 从2B改为8B
```

---

## 🎯 下一步操作建议

### 立即可做

1. **启动MAI-UI服务**
   ```powershell
   cd c:\document\python\gui-agent\gui-agent
   docker-compose up -d
   ```

2. **测试RPA工具**
   ```powershell
   python examples/rpa_tools_example.py
   ```

3. **查看文档**
   ```powershell
   code docs/workflow_01_project_setup.md
   code docs/workflow_02_mai_ui_deployment.md
   ```

### 后续开发

1. **开发Agent核心** (电脑A)
   - 实现Agent主逻辑
   - 集成LangChain
   - 连接知识库

2. **开发Web前端** (电脑B)
   - Vue.js界面
   - 对话功能
   - 任务监控

3. **集成测试**
   - 端到端测试
   - 性能优化
   - Bug修复

---

## 📚 相关文档

- [工作流程报告1: 项目环境搭建](workflow_01_project_setup.md)
- [工作流程报告2: MAI-UI部署调试](workflow_02_mai_ui_deployment.md)
- [RPA工具集文档](../rpa_tools/README.md)
- [RPA工具提取总结](../../.gemini/antigravity/brain/.../rpa_tools_summary.md)

---

## 🆘 获取帮助

### 问题排查顺序

1. 查看本文档的"故障快速修复"部分
2. 查看Docker日志: `docker-compose logs -f`
3. 查看GPU状态: `nvidia-smi`
4. 查看详细部署文档: `workflow_02_mai_ui_deployment.md`

### 联系方式

- GitHub Issues
- 项目文档
- 团队协作平台

---

**快速启动指南完成！现在可以高效地管理和使用MAI-UI服务了！** 🚀
