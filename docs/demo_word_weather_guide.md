# Word天气文章自动化Demo使用说明

## 功能介绍

这个Demo展示了完整的AI + RPA自动化流程：

1. **获取实时天气** - 调用wttr.in API获取北京天气
2. **AI生成文章** - 使用Ollama qwen:7b生成天气播报文章
3. **自动打开Word** - 自动启动Microsoft Word
4. **写入内容** - 使用pyautogui自动输入标题和文章
5. **保存文档** - 自动保存为Word文档

## 运行前准备

### 1. 确保Ollama运行
```powershell
# 检查Ollama是否运行
curl http://localhost:11434/api/tags

# 如果没运行，启动Ollama
ollama serve
```

### 2. 确保已安装Word
- Microsoft Word 2016/2019/365

### 3. 安装依赖
```powershell
pip install requests pyautogui pyperclip
```

## 运行Demo

```powershell
cd c:\document\python\gui-agent
python demo_word_weather.py
```

## 运行流程

1. **获取天气** (~2秒)
   - 调用免费天气API
   - 显示当前温度、天气状况、湿度等

2. **AI生成文章** (~10-20秒)
   - 使用qwen:7b生成200字天气播报
   - 包含出行建议

3. **打开Word** (~3秒)
   - 自动启动Word应用
   - 等待完全加载

4. **写入内容** (~5秒)
   - 输入标题：YYYY年MM月DD日 北京天气播报
   - 粘贴AI生成的文章内容

5. **保存文档** (~2秒)
   - 自动保存为：天气播报_YYYYMMDD_HHMMSS.docx
   - 保存到"我的文档"

## 注意事项

### 屏幕分辨率
- 脚本中的点击坐标 `(500, 300)` 是针对常见分辨率
- 如果Word窗口位置不同，可能需要调整坐标

### Word版本
- 支持Word 2016/2019/365
- 如果路径不同，脚本会尝试用系统命令启动

### 网络问题
- 如果天气API失败，会使用模拟数据
- 如果Ollama失败，会使用模板文章

## 自定义修改

### 修改城市
```python
# 第33行
response = requests.get(
    "https://wttr.in/Shanghai?format=j1",  # 改为Shanghai
    timeout=10
)
```

### 修改文章长度
```python
# 第71行
要求：
1. 语言生动，适合播报
2. 包含出行建议
3. 字数500字左右  # 改为500字
```

### 修改保存位置
```python
# 第175行，在输入文件名前添加路径
pyautogui.write(r"C:\Users\YourName\Desktop\weather.docx", interval=0.05)
```

## 故障排查

### Word没有打开
- 检查Word安装路径
- 手动运行 `start winword` 测试

### 内容没有写入
- 确保Word窗口在前台
- 调整点击坐标 `(500, 300)`

### 中文乱码
- 确保安装了 `pyperclip`
- 使用剪贴板方式写入中文

### Ollama连接失败
```powershell
# 检查Ollama服务
curl http://localhost:11434/api/tags

# 重启Ollama
ollama serve
```

## 扩展建议

1. **添加MAI-UI视觉识别**
   - 截图识别Word界面
   - 智能定位输入位置

2. **支持更多城市**
   - 从命令行参数读取城市
   - 支持多个城市批量生成

3. **美化Word格式**
   - 使用python-docx库直接操作Word
   - 添加标题样式、字体、颜色

4. **定时任务**
   - 使用Windows任务计划程序
   - 每天早上自动生成天气播报
