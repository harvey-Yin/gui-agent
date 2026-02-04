# RPA工具集文档

## 📚 概述

基于您现有的18个RPA项目提取和整理的Agent可用工具集，包含6大类核心功能模块。

## 🗂️ 项目结构

```
rpa_tools/
├── __init__.py              # 包初始化
├── base_tool.py             # 工具基类
├── screen_tools.py          # 屏幕操作工具
├── vision_tools.py          # 视觉识别工具
├── excel_tools.py           # Excel处理工具
├── word_tools.py            # Word处理工具
├── data_tools.py            # 数据处理工具
└── tool_registry.py         # 工具注册系统
```

## 🛠️ 核心工具模块

### 1. ScreenTool - 屏幕操作工具

**功能来源**: `catch_number.py`, `message_push/auto_click.py`, `green.py`

**主要功能**:
- ✅ 鼠标点击 (`click_at`, `double_click_at`, `right_click_at`)
- ✅ 键盘输入 (`type_text`, `press_key`, `hotkey`)
- ✅ 拖拽操作 (`drag_to`)
- ✅ 滚动操作 (`scroll`)
- ✅ 截图功能 (`screenshot`)
- ✅ 剪贴板操作 (`copy_to_clipboard`, `paste_from_clipboard`)

**使用示例**:
```python
from rpa_tools import ScreenTool

screen = ScreenTool()
screen.click_at(100, 200)
screen.type_text("你好世界")
screen.hotkey('ctrl', 'c')
```

---

### 2. VisionTool - 视觉识别工具

**功能来源**: `catch_number.py`, `green.py`, `deal_86.py`

**主要功能**:
- ✅ 图像查找 (`find_image`, `find_all_images`)
- ✅ 多尺度匹配 (`find_image_multiscale`) - 适应不同DPI
- ✅ 等待元素 (`wait_for_element`)
- ✅ 点击图像 (`click_image`)
- ✅ 相对定位点击 (`click_relative`) - 基于锚点偏移

**技术特点**:
- 支持PyAutoGUI精确匹配
- 支持OpenCV多尺度匹配（解决DPI缩放问题）
- 自动缓存最佳缩放比例

**使用示例**:
```python
from rpa_tools import VisionTool

vision = VisionTool(image_dir="picture")
vision.click_image("submit_button.png", timeout=10)
vision.click_relative("anchor.png", offset_x=50, offset_y=20)
```

---

### 3. ExcelTool - Excel处理工具

**功能来源**: `daily_report/daily_notice_v2.py`, `assess_all.py`, `class_work/catch_data.py`

**主要功能**:
- ✅ 文件读写 (`read_excel`, `write_excel`)
- ✅ 工作簿操作 (`open_workbook`, `select_sheet`, `save_workbook`)
- ✅ 单元格操作 (`read_cell`, `write_cell`)
- ✅ 数据过滤 (`filter_data`)
- ✅ 数据合并 (`merge_data`)
- ✅ 分组聚合 (`group_aggregate`)
- ✅ 查找表头 (`find_header_row`)
- ✅ 写入日期数据 (`write_daily_data`) - 自动匹配或追加

**使用示例**:
```python
from rpa_tools import ExcelTool

excel = ExcelTool()
result = excel.read_excel("data.xlsx")
df = result['data']
excel.filter_data(df, column="状态", condition="==", value="完成")
```

---

### 4. WordTool - Word处理工具

**功能来源**: `word_process/word_process_v4.py`

**主要功能**:
- ✅ 文档读写 (`open_document`, `save_document`)
- ✅ 文本提取 (`extract_text`)
- ✅ 正则提取 (`extract_info_by_regex`)
- ✅ 模板渲染 (`render_template`)
- ✅ 内容添加 (`add_paragraph`, `add_heading`, `add_table`)
- ✅ 批量生成 (`batch_generate_from_template`)

**使用示例**:
```python
from rpa_tools import WordTool

word = WordTool()
patterns = {"编号": r"GD-\d+", "姓名": r"姓名[:：]\s*([^\s]+)"}
result = word.extract_info_by_regex("doc.docx", patterns)

data = {"客户姓名": "张三", "申诉号码": "13800138000"}
word.render_template("template.docx", data, "output.docx")
```

---

### 5. DataTool - 数据处理工具

**功能来源**: `class_work/catch_data.py`, `deal_86.py`

**主要功能**:
- ✅ 正则提取 (`extract_by_regex`, `parse_structured_text`)
- ✅ 日期处理 (`parse_date`, `calculate_date_offset`)
- ✅ 数据转换 (`convert_to_json`, `parse_json`)
- ✅ 文本处理 (`clean_text`, `split_text`, `replace_text`)
- ✅ 数据验证 (`validate_phone`, `validate_email`)

**使用示例**:
```python
from rpa_tools import DataTool

data_tool = DataTool()
result = data_tool.extract_by_regex(text, r"GD-\d+-\d+")
result = data_tool.calculate_date_offset("2024-02-04", offset_days=7)
result = data_tool.validate_phone("13800138000")
```

---

### 6. ToolRegistry - 工具注册系统

**主要功能**:
- ✅ 自动发现和注册所有RPA工具
- ✅ 转换为LangChain Tool格式
- ✅ 提供统一的工具访问接口

**使用示例**:
```python
from rpa_tools import get_rpa_tools

# 获取所有LangChain工具（供Agent使用）
tools = get_rpa_tools()

# 在LangChain Agent中使用
from langchain.agents import create_react_agent
agent = create_react_agent(llm, tools, prompt)
```

---

## 📊 从现有项目提取的功能映射

| 原项目 | 提取的核心功能 | 对应工具模块 |
|--------|---------------|-------------|
| `catch_number.py` | 图像识别点击、SQL自动化 | VisionTool, ScreenTool |
| `message_push/auto_click.py` | 批量点击、剪贴板操作 | ScreenTool |
| `word_process_v4.py` | Word模板渲染、正则提取 | WordTool |
| `daily_notice_v2.py` | Excel日期数据写入 | ExcelTool |
| `assess_all.py` | Excel数据分组统计 | ExcelTool |
| `green.py` | 图像查找重试机制 | VisionTool |
| `deal_86.py` | 多尺度图像匹配、相对定位 | VisionTool |
| `class_work/catch_data.py` | 正则解析、GUI配置 | DataTool |

---

## 🚀 快速开始

### 安装依赖

```bash
pip install pyautogui pydirectinput pyperclip opencv-python
pip install pandas openpyxl python-docx docxtpl
pip install langchain
```

### 基础使用

```python
# 1. 导入工具
from rpa_tools import ScreenTool, VisionTool, ExcelTool

# 2. 创建工具实例
screen = ScreenTool()
vision = VisionTool(image_dir="picture")
excel = ExcelTool()

# 3. 使用工具
screen.click_at(100, 200)
vision.click_image("button.png")
result = excel.read_excel("data.xlsx")
```

### Agent集成

```python
from rpa_tools import get_rpa_tools
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama

# 获取所有RPA工具
tools = get_rpa_tools()

# 创建Agent
llm = Ollama(model="qwen:7b")
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

# 执行任务
result = executor.invoke({"input": "打开Excel文件data.xlsx并读取第一行"})
```

---

## 🎯 设计特点

### 1. 统一的接口设计
所有工具继承自`RPAToolBase`，提供一致的调用方式：
- `execute(**kwargs)` - 核心执行方法
- `pre_check()` - 前置安全检查
- `post_process()` - 后处理
- `log_execution()` - 自动日志记录

### 2. 安全机制
- ✅ 操作延迟（避免误操作）
- ✅ 执行历史记录
- ✅ 异常捕获和错误处理
- ✅ PyAutoGUI FAILSAFE（鼠标移到左上角紧急停止）

### 3. 兼容性
- ✅ 支持中文输入（使用剪贴板）
- ✅ 多尺度图像匹配（适应不同DPI）
- ✅ 灵活的参数配置

### 4. 可扩展性
- ✅ 模块化设计，易于添加新工具
- ✅ 工具注册系统自动发现新工具
- ✅ 与LangChain无缝集成

---

## 📝 注意事项

1. **图像识别**：需要提前准备模板图片，放在`picture`目录
2. **屏幕操作**：确保目标窗口在前台且可见
3. **文件路径**：建议使用绝对路径
4. **安全性**：危险操作（如删除文件）需要额外确认

---

## 🔧 后续扩展方向

- [ ] OCR文字识别（集成paddleocr或tesseract）
- [ ] 浏览器自动化（集成Selenium/Playwright）
- [ ] 文件操作工具（复制、移动、重命名）
- [ ] 数据库操作工具
- [ ] API调用工具
- [ ] 邮件发送工具

---

## 📄 许可证

基于现有RPA项目提取，供内部使用。
