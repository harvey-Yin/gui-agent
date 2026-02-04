# MAI-UI-8B 本地部署完整指南

## 📋 部署概述

**MAI-UI-8B** 是阿里巴巴通义实验室开源的GUI智能体模型，可以通过自然语言+截图理解并操作用户界面。

- **模型大小**: 8B参数
- **推理引擎**: vLLM（高性能推理）
- **API方式**: OpenAI兼容接口
- **HuggingFace**: https://huggingface.co/Tongyi-MAI/MAI-UI-8B

---

## ⚙️ 系统要求

### 硬件要求
- **GPU**: 推荐NVIDIA GPU（显存16GB+）
  - RTX 3090 / RTX 4090 / A100等
  - 支持CUDA
- **内存**: 32GB+
- **硬盘**: 20GB+（存储模型）

### 软件要求
- Python 3.10+
- CUDA 11.8+ / 12.1+
- Git

---

## 🚀 完整部署步骤

### Step 1: 检查环境

```bash
# 检查Python版本
python --version  # 应该是 3.10+

# 检查CUDA（如有GPU）
nvidia-smi

# 检查Git
git --version
```

### Step 2: 创建独立虚拟环境

**为什么独立环境？** MAI-UI需要特定版本的依赖，避免与现有RPA项目冲突。

```bash
# 在合适的位置创建MAI-UI项目目录
cd c:\document\python
mkdir mai-ui-deploy
cd mai-ui-deploy

# 创建虚拟环境
python -m venv venv_mai

# 激活虚拟环境
venv_mai\Scripts\activate
```

### Step 3: 安装vLLM和依赖

vLLM是高性能LLM推理引擎，支持OpenAI兼容API。

```bash
# 升级pip
python -m pip install --upgrade pip

# 安装vLLM（需要时间，约5-10分钟）
pip install vllm>=0.11.0

# 安装transformers
pip install transformers>=4.57.0

# 安装其他依赖
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**注意**：
- 如果没有GPU，vLLM可能无法使用，需要使用CPU版本（性能较差）
- CUDA版本根据你的GPU驱动选择（cu118或cu121）

### Step 4: 下载MAI-UI-8B模型

**方式A：自动下载（推荐）**

vLLM会在首次运行时自动从HuggingFace下载模型。

**方式B：手动预下载（可选）**

```bash
# 安装huggingface-cli
pip install huggingface-hub

# 登录（如需访问私有模型）
huggingface-cli login

# 下载模型（约16GB，需要时间）
huggingface-cli download Tongyi-MAI/MAI-UI-8B --local-dir ./models/MAI-UI-8B
```

### Step 5: 启动vLLM API服务器

```bash
# 确保虚拟环境已激活
venv_mai\Scripts\activate

# 启动vLLM服务（自动下载模式）
python -m vllm.entrypoints.openai.api_server \
  --model Tongyi-MAI/MAI-UI-8B \
  --served-model-name MAI-UI-8B \
  --host 0.0.0.0 \
  --port 8001 \
  --tensor-parallel-size 1 \
  --trust-remote-code
```

**参数说明**：
- `--model`: 模型路径（HuggingFace ID或本地路径）
- `--port 8001`: API端口（避免与现有项目的8000冲突）
- `--tensor-parallel-size 1`: 单GPU推理（多GPU改为2、4、8等）
- `--trust-remote-code`: 允许执行模型自定义代码

**首次运行**：
- vLLM会自动下载模型到 `~/.cache/huggingface/`
- 下载过程可能需要10-30分钟（取决于网络）
- 下载完成后会加载模型到GPU

**成功标志**：
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### Step 6: 测试API服务

**新开一个终端**，测试API是否正常：

```bash
# 查看模型列表
curl http://localhost:8001/v1/models

# 测试简单推理
curl http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MAI-UI-8B",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 100
  }'
```

预期输出：
```json
{
  "id": "...",
  "model": "MAI-UI-8B",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "你好！我是MAI-UI..."
      }
    }
  ]
}
```

---

## 🧪 第一次运行：GUI识别测试

### 安装MAI-UI工具包

```bash
# 克隆MAI-UI官方代码库
git clone https://github.com/Tongyi-MAI/MAI-UI.git
cd MAI-UI

# 安装依赖
pip install -r requirements.txt

# 启动Jupyter
pip install jupyter
jupyter notebook
```

### 运行Grounding Demo

1. 打开 `cookbook/grounding.ipynb`
2. 修改API地址：
   ```python
   agent = MAIGroundingAgent(
       llm_base_url="http://localhost:8001/v1",  # 你的vLLM地址
       model_name="MAI-UI-8B",
       runtime_conf={
           "history_n": 3,
           "temperature": 0.0,
           "max_tokens": 2048,
       },
   )
   ```
3. 运行所有单元格
4. 提供一张截图 + 自然语言指令（如"点击登录按钮"）
5. 模型会返回UI元素的位置坐标

---

## 🔧 常见问题

### Q1: 显存不够怎么办？

**方案1：量化模型**
```bash
# 使用INT8量化
python -m vllm.entrypoints.openai.api_server \
  --model Tongyi-MAI/MAI-UI-8B \
  --quantization int8 \
  --port 8001
```

**方案2：使用MAI-UI-2B**
```bash
# 使用更小的2B模型（显存需求约4-6GB）
python -m vllm.entrypoints.openai.api_server \
  --model Tongyi-MAI/MAI-UI-2B \
  --port 8001
```

### Q2: 下载速度慢？

**使用国内镜像**：
```bash
# 设置HuggingFace镜像（可选）
export HF_ENDPOINT=https://hf-mirror.com
```

### Q3: 没有GPU能用吗？

**CPU模式**（速度非常慢，不推荐）：
```bash
pip install vllm-cpu
# 或使用transformers直接加载
```

### Q4: 如何停止服务？

在vLLM服务器终端按 `Ctrl+C`

---

## 📊 性能预期

| 硬件 | 首次加载 | 单次推理 | 显存占用 |
|------|----------|----------|----------|
| RTX 4090 | ~30秒 | ~2-5秒 | ~15GB |
| RTX 3090 | ~40秒 | ~3-7秒 | ~16GB |
| A100 | ~20秒 | ~1-3秒 | ~15GB |

---

## 🎯 与你的RPA项目集成

部署成功后，可以在你的RPA Agent中调用MAI-UI：

```python
# 在你的项目中
import httpx
import base64

class MAIUIVisionTool:
    def __init__(self):
        self.api_url = "http://localhost:8001/v1"
    
    async def locate_element(self, screenshot_path: str, instruction: str):
        """使用MAI-UI定位UI元素"""
        
        # 读取截图并转为base64
        with open(screenshot_path, 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode()
        
        # 调用MAI-UI API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/chat/completions",
                json={
                    "model": "MAI-UI-8B",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": instruction},
                                {"type": "image_url", "image_url": f"data:image/png;base64,{img_base64}"}
                            ]
                        }
                    ],
                    "max_tokens": 512
                }
            )
            result = response.json()
            # 解析返回的坐标
            return result
```

---

## 📝 下一步

1. **测试Grounding功能**：识别UI元素位置
2. **测试Navigation功能**：完整任务执行
3. **集成到RPA项目**：作为视觉识别的增强方案
4. **性能优化**：调整batch_size、temperature等参数

---

## 🆘 获取帮助

- GitHub Issue: https://github.com/Tongyi-MAI/MAI-UI/issues
- HuggingFace讨论: https://huggingface.co/Tongyi-MAI/MAI-UI-8B/discussions
- 官方文档: 查看README.md

---

**部署完成后告诉我，我们可以一起测试第一个GUI识别任务！** 🎉
