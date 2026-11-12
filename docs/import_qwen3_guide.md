# 从ModelScope导入Qwen3-8B-FP8到Ollama

## 方法1：使用ModelScope CLI（推荐）

### 1. 安装ModelScope CLI
```powershell
pip install modelscope
```

### 2. 下载模型
```powershell
# 创建模型目录
mkdir C:\models\qwen3-8b-fp8
cd C:\models\qwen3-8b-fp8

# 使用Python下载
python -c "from modelscope import snapshot_download; snapshot_download('Qwen/Qwen3-8B-FP8', cache_dir='.')"
```

### 3. 创建Ollama Modelfile
在 `C:\models\qwen3-8b-fp8` 目录创建文件 `Modelfile`：

```
FROM ./Qwen3-8B-FP8

TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
"""

PARAMETER stop "<|im_start|>"
PARAMETER stop "<|im_end|>"
PARAMETER temperature 0.7
PARAMETER top_p 0.8
PARAMETER top_k 20
```

### 4. 导入到Ollama
```powershell
cd C:\models\qwen3-8b-fp8
ollama create Qwen3-8B-FP8 -f Modelfile
```

### 5. 验证
```powershell
ollama list
ollama run Qwen3-8B-FP8 "你好"
```

---

## 方法2：直接使用已有的qwen:7b（最简单）

如果下载太慢或遇到问题，建议先用你已有的 `qwen:7b`：

```powershell
# 不需要任何操作，qwen:7b已经可用
ollama run qwen:7b "你好"
```

然后我把代码改回 `qwen:7b` 即可。

---

## 方法3：使用Ollama官方的Qwen2模型

Ollama官方支持的Qwen模型：

```powershell
# 安装Qwen2 7B
ollama pull qwen2:7b

# 或者更大的版本
ollama pull qwen2:14b
```

---

## 推荐方案

**如果你想快速开始**：
- 用现有的 `qwen:7b`（我改回代码）

**如果你想要新模型但不想等太久**：
- 用 `ollama pull qwen2:7b`（官方支持，下载快）

**如果你一定要用Qwen3-8B-FP8**：
- 按方法1操作，但需要：
  1. 下载时间较长（~8GB）
  2. 需要配置Modelfile
  3. 可能遇到兼容性问题

你想用哪个方案？
