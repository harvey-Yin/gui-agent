# 🔧 Docker镜像下载问题快速解决方案

## 问题现象
```
unexpected end of JSON input
failed to connect to the docker API
```

## 解决步骤

### Step 1: 重启Docker Desktop
**最重要的一步！**

1. 完全退出Docker Desktop（右键托盘图标 → Quit）
2. 等待10秒
3. 重新启动Docker Desktop
4. 等待Docker完全启动（托盘图标变绿）

### Step 2: 清理损坏的镜像

```powershell
# 等Docker启动后执行
docker system prune -a -f
```

### Step 3: 使用更稳定的镜像版本

已更新`docker-compose.yml`使用 **v0.5.4**（更稳定，体积更小）

### Step 4: 启动服务

```powershell
docker-compose up -d
```

---

## 🎯 为什么选择v0.5.4？

| 版本 | 镜像大小 | CUDA要求 | 稳定性 |
|------|---------|---------|--------|
| latest | 6-7GB | 12.9+ | ⚠️ 不稳定 |
| v0.6.0 | 5.1GB | 12.6+ | ⚠️ 下载易失败 |
| **v0.5.4** | **3.8GB** | **12.1+** | **✅ 稳定** |

---

## ⚠️ 如果仍然失败

### 方案A: 手动下载镜像（推荐）

```powershell
# 1. 重启Docker Desktop后
docker pull vllm/vllm-openai:v0.5.4

# 2. 等待下载完成（约10-20分钟）

# 3. 启动服务
docker-compose up -d
```

### 方案B: 使用Transformers直接运行（不用Docker）

如果Docker一直有问题，可以不用Docker：

```powershell
# 1. 激活虚拟环境
.\venv\Scripts\activate

# 2. 安装依赖
pip install transformers torch pillow

# 3. 直接用Python运行MAI-UI
python -c "
from transformers import AutoModel, AutoTokenizer
model = AutoModel.from_pretrained('Tongyi-MAI/MAI-UI-2B', trust_remote_code=True)
print('模型加载成功')
"
```

**缺点**: 
- 没有OpenAI兼容API
- 需要自己写代码调用
- 显存占用更高（~6-8GB）

### 方案C: 暂时跳过MAI-UI

MAI-UI是增强功能，不是必需的。您可以：

1. 先继续开发RPA核心功能
2. 使用传统的OpenCV图像识别（已在`vision_tools.py`中实现）
3. 等Docker问题解决后再集成MAI-UI

---

## 📝 当前建议

**立即操作**:
1. ✅ 重启Docker Desktop（最重要！）
2. ✅ 等待Docker完全启动
3. ✅ 运行 `docker-compose up -d`

**如果还是失败**:
- 使用方案B（Transformers）或方案C（暂时跳过）
- MAI-UI不是必需的，RPA工具已经很强大了

---

## 🎯 GTX 1650 Ti的现实情况

**坦白说**: 您的4GB显存可能真的不够运行MAI-UI-2B

**更实际的选择**:
1. 使用传统OpenCV图像识别（已实现）
2. 调用在线API（如GPT-4V、Claude）
3. 等有更好的GPU再尝试本地视觉模型

**RPA项目完全可以不依赖MAI-UI运行！**
