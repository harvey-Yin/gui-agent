# Windows上运行MAI-UI-8B的解决方案

## 问题说明
vLLM依赖uvloop，而**uvloop不支持Windows**。这是vLLM的已知限制。

---

## 解决方案（3选1）

### 方案A：使用Transformers直接加载（推荐给Windows用户⭐）

不使用vLLM，直接用transformers库加载模型：

```powershell
cd c:\document\python\mai-ui-deploy
.\venv_mai\Scripts\activate

# 安装额外依赖
pip install accelerate bitsandbytes

# Python交互式测试
python
```

然后在Python中运行：
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 加载模型（会自动下载）
model_name = "Tongyi-MAI/MAI-UI-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# INT8量化加载
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_8bit=True,  # INT8量化
    device_map="auto",
    trust_remote_code=True
)

# 测试推理
messages = [{"role": "user", "content": "你好"}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer([text], return_tensors="pt").to(model.device)

outputs = model.generate(**inputs, max_new_tokens=100)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

---

### 方案B：WSL2 + vLLM（完整但复杂）

在WSL2（Windows Subsystem for Linux）中运行vLLM：

#### 步骤：
1. 启用WSL2
   ```powershell
   wsl --install
   ```

2. 在WSL2中安装Ubuntu
3. 在WSL2中重新安装vLLM和MAI-UI
4. WSL2可以访问Windows的GPU（需要NVIDIA驱动支持）

**优点**：完整的vLLM功能
**缺点**：配置复杂，需要重新安装

---

### 方案C：使用MAI-UI-2B + Ollama（最简单⭐⭐）

既然你已经有Ollama在运行，可以：

1. **下载MAI-UI-2B到Ollama格式**（如果有Modelfile）
2. **或者直接用现有的qwen:7b + OpenCV方案**

这是**最实用的方案**，因为：
- ✅ 12GB显存足够
- ✅ Windows原生支持
- ✅ 已验证成功
- ✅ 更容易集成到你的RPA项目

---

## 推荐行动

考虑到你的情况（Windows + 12GB显存 + RPA项目），我**强烈推荐方案C**：

### 回归原计划：qwen:7b + OpenCV + llava

你的测试已经通过了：
```
[OK] Ollama响应: 你好，我是一名具备语言处理能力的AI助手。
[OK] LangChain响应: 作为RPA自动化助手...
[OK] PyAutoGUI可用 - 屏幕尺寸: Size(width=2560, height=1440)
[OK] OpenCV可用 - 版本: 4.10.0
```

**这套方案**：
- Windows原生支持
- 显存需求低（4-6GB）
- 已经验证工作
- 容易调试和定制
- 简历同样有亮点

---

## 实际建议

MAI-UI虽然性能强，但在Windows上部署复杂度太高。对于你的简历项目：

**现在可以做的**：
1. 继续用qwen:7b + OpenCV开发RPA Agent
2. 完成Phase 2-3的核心功能
3. 后期如果需要，可以添加MAI-UI作为**可选的高级特性**

**简历可以这样写**：
> "研究并对比了阿里MAI-UI等业界SOTA方案，最终采用轻量化的qwen+OpenCV架构，在保证性能的同时降低了部署复杂度和资源需求"

---

你觉得呢？想继续折腾Windows上的MAI-UI，还是**回归原计划**继续开发RPA项目？
