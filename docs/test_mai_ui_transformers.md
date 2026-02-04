# MAI-UI-8B Transformers测试指南

## 步骤说明

### 1. 安装依赖（正在进行中）

```powershell
cd c:\document\python\mai-ui-deploy
.\venv_mai\Scripts\activate
pip install accelerate bitsandbytes scipy
```

### 2. 运行测试脚本

```powershell
.\venv_mai\Scripts\python.exe test_mai_ui.py
```

### 3. 预期过程

**首次运行**：
- 下载模型文件（约16GB，10-60分钟）
- 下载到：`C:\Users\你的用户名\.cache\huggingface\hub\`
- 显示下载进度条

**模型加载**：
- INT8量化处理
- 加载到GPU（约8-10GB显存）
- 耗时约30-60秒

**测试推理**：
- 询问模型自我介绍
- 检查显存占用

### 4. 可能遇到的问题

#### 问题1：显存不足

**解决**：降低量化精度
编辑 `test_mai_ui.py`，将：
```python
load_in_8bit=True
```
改为：
```python
load_in_4bit=True  # 4bit量化，显存需求更低
```

#### 问题2：下载失败

**解决**：使用镜像
```powershell
$env:HF_ENDPOINT = "https://hf-mirror.com"
# 然后重新运行
```

#### 问题3：CUDA错误

检查CUDA：
```powershell
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

### 5. 成功标志

看到以下输出：
```
[OK] Tokenizer加载成功
[OK] 模型加载成功
  设备: cuda:0
[OK] 模型响应:
你好！我是MAI-UI...
  GPU: NVIDIA GeForce RTX...
  已用显存: 8.23 GB
```

### 6. 下一步：GUI识别测试

创建GUI识别测试脚本（需要截图输入）。

---

## 性能对比

| 方式 | 优点 | 缺点 |
|------|------|------|
| vLLM | 速度快、API接口 | ❌ 不支持Windows |
| Transformers | ✅ Windows兼容 | 速度较慢、无API |

**当前方案**：Transformers（唯一可用）
