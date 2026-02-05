# 🎉 MAI-UI-2B Docker部署成功总结

## 部署成果

**日期**: 2026-02-05  
**环境**: Windows 11 + Docker Desktop + WSL2 + RTX 4070 (12GB)

### ✅ 成功部署MAI-UI-2B
- **模型**: Tongyi-MAI/MAI-UI-2B
- **框架**: vLLM 0.15.0 (Docker)
- **显存**: 4.24 GB / 12 GB
- **上下文**: 4096 tokens
- **API**: OpenAI兼容 (http://localhost:8001)

---

## 关键配置

### docker-compose.yml
```yaml
services:
  vllm-mai-ui:
    image: vllm/vllm-openai:latest
    container_name: mai-ui-2b-agent
    ports:
      - "8001:8000"
    environment:
      - HF_ENDPOINT=https://hf-mirror.com
      - CUDA_VISIBLE_DEVICES=0
    volumes:
      - ${USERPROFILE}/.cache/huggingface:/root/.cache/huggingface
    command: >
      --model Tongyi-MAI/MAI-UI-2B
      --served-model-name MAI-UI-2B
      --host 0.0.0.0
      --port 8000
      --trust-remote-code
      --dtype float16
      --gpu-memory-utilization 0.85
      --max-model-len 4096
      --enforce-eager
```

**关键参数说明**：
- `max-model-len 4096`: 支持视觉语言输入（图片+文本）
- `gpu-memory-utilization 0.85`: 适配12GB显存
- `enforce-eager`: 禁用CUDA Graphs，节省显存

---

## GUI识别测试结果

### 测试脚本
`test_mai_ui_api.py` - 使用OpenAI兼容API调用MAI-UI

### 识别能力
✅ **成功识别**：
- IDE类型（VS Code）
- 当前文件名（test_mai_ui_api.py）
- 文件列表（requirements.txt, docker-compose.yml等）
- Source Control面板
- Docker配置详情
- 文件修改状态

### 性能指标
- **模型加载时间**: ~45秒
- **推理速度**: ~5-10秒/请求
- **并发能力**: 9.23x (4096 tokens/request)

---

## 与MAI-UI-8B对比

| 指标 | MAI-UI-8B | MAI-UI-2B |
|------|-----------|-----------|
| 显存占用 | 16.64 GB | 4.24 GB |
| 12GB GPU兼容 | ❌ 需要量化或失败 | ✅ 完美运行 |
| 加载时间 | ~140秒 | ~45秒 |
| 识别准确度 | 更高 | 足够用 |
| 推荐场景 | 24GB+ GPU | 12GB GPU |

---

## 使用方法

### 1. 启动服务
```powershell
cd c:\document\python\gui-agent
docker-compose up -d
```

### 2. 查看日志
```powershell
docker-compose logs -f
```

### 3. 测试API
```powershell
# 检查服务状态
curl http://localhost:8001/v1/models

# 运行GUI识别测试
python test_mai_ui_api.py
```

### 4. 停止服务
```powershell
docker-compose down
```

---

## 集成到RPA项目

### 方式1：直接使用OpenAI SDK
```python
import openai
import base64

client = openai.OpenAI(
    base_url="http://localhost:8001/v1",
    api_key="dummy"
)

# 编码截图
with open("screenshot.png", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

# 调用MAI-UI
response = client.chat.completions.create(
    model="MAI-UI-2B",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
            {"type": "text", "text": "找到登录按钮的位置"}
        ]
    }]
)

print(response.choices[0].message.content)
```

### 方式2：封装为RPA工具
```python
# rpa_tools/vision_tools.py
class MAIUIVisionTool:
    def __init__(self, api_base="http://localhost:8001/v1"):
        self.client = openai.OpenAI(base_url=api_base, api_key="dummy")
    
    def locate_element(self, screenshot_path, element_description):
        """使用MAI-UI定位UI元素"""
        # 实现逻辑...
```

---

## 优势总结

### vs Transformers方式
| 特性 | Docker + vLLM | Transformers |
|------|---------------|--------------|
| 推理速度 | ⚡ 快 (~5s) | 🐌 慢 (~10s) |
| API接口 | ✅ OpenAI兼容 | ❌ 需要自己封装 |
| 易用性 | ✅ 一键启停 | ⚠️ 需要管理环境 |
| 显存占用 | 4.24 GB | ~9 GB (INT8) |

### vs MAI-UI-8B
- ✅ 显存需求低（4GB vs 17GB）
- ✅ 加载速度快（45s vs 140s）
- ✅ 12GB GPU完美运行
- ⚠️ 识别准确度略低（但足够用）

---

## 简历描述模板

> "成功在Windows环境通过Docker部署MAI-UI-2B视觉语言模型，实现GUI自动化的智能识别能力。针对12GB显存限制，优化了vLLM配置参数（gpu-memory-utilization、max-model-len、enforce-eager），将显存占用控制在4.24GB。集成OpenAI兼容API，为RPA项目提供了高性能的视觉理解能力。"

**体现能力**：
- ✅ 容器化部署经验
- ✅ GPU资源优化
- ✅ 视觉语言模型应用
- ✅ API集成能力

---

## 下一步

### 选项A：继续深入MAI-UI
- [ ] 测试更多GUI识别场景
- [ ] 优化prompt提高准确率
- [ ] 封装为RPA工具类

### 选项B：回归RPA项目主线
- [ ] Phase 2: 开发RPA核心工具
- [ ] 集成qwen:7b（已验证）
- [ ] 实现第一个Agent Demo

**推荐**：选B，MAI-UI已验证可用，可作为高级特性后期集成。
