"""
RPA工具注册系统
自动发现和注册所有RPA工具，转换为LangChain Tool格式
"""
from typing import List, Dict, Any
from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field
import logging

# 导入所有工具类
from .screen_tools import ScreenTool
from .vision_tools import VisionTool
from .excel_tools import ExcelTool
from .word_tools import WordTool
from .data_tools import DataTool


logger = logging.getLogger(__name__)


class RPAToolRegistry:
    """RPA工具注册中心"""
    
    def __init__(self):
        self.tools = {}
        self.langchain_tools = []
        
        # 初始化所有工具实例
        self.screen_tool = ScreenTool()
        self.vision_tool = VisionTool()
        self.excel_tool = ExcelTool()
        self.word_tool = WordTool()
        self.data_tool = DataTool()
        
        # 注册工具
        self._register_all_tools()
    
    def _register_all_tools(self):
        """注册所有RPA工具"""
        
        # ========== 屏幕操作工具 ==========
        self._register_tool(
            name="click_at",
            description="点击屏幕指定坐标位置。参数: x(int), y(int), clicks(int, 默认1), button(str, 默认'left')",
            func=self.screen_tool.click_at
        )
        
        self._register_tool(
            name="type_text",
            description="在当前焦点位置输入文本（支持中文）。参数: text(str)",
            func=self.screen_tool.type_text
        )
        
        self._register_tool(
            name="press_key",
            description="按下键盘按键。参数: key(str, 如'enter', 'backspace'), presses(int, 默认1)",
            func=self.screen_tool.press_key
        )
        
        self._register_tool(
            name="hotkey",
            description="执行组合键操作。参数: *keys(可变参数, 如'ctrl', 'c')",
            func=self.screen_tool.hotkey
        )
        
        self._register_tool(
            name="screenshot",
            description="截取屏幕。参数: region(tuple, 可选), save_path(str, 可选)",
            func=self.screen_tool.screenshot
        )
        
        self._register_tool(
            name="scroll",
            description="滚动鼠标滚轮。参数: clicks(int, 正数向上负数向下)",
            func=self.screen_tool.scroll
        )
        
        # ========== 视觉识别工具 ==========
        self._register_tool(
            name="find_image",
            description="在屏幕上查找图像。参数: template_name(str), confidence(float, 可选)",
            func=self.vision_tool.find_image
        )
        
        self._register_tool(
            name="click_image",
            description="查找并点击图像。参数: template_name(str), clicks(int, 默认1), timeout(float, 默认10)",
            func=self.vision_tool.click_image
        )
        
        self._register_tool(
            name="wait_for_element",
            description="等待图像元素出现。参数: template_name(str), timeout(float, 默认10)",
            func=self.vision_tool.wait_for_element
        )
        
        self._register_tool(
            name="click_relative",
            description="基于锚点图像的相对位置点击。参数: anchor_template(str), offset_x(int), offset_y(int)",
            func=self.vision_tool.click_relative
        )
        
        # ========== Excel工具 ==========
        self._register_tool(
            name="read_excel",
            description="读取Excel文件。参数: file_path(str), sheet_name(str, 可选)",
            func=self.excel_tool.read_excel
        )
        
        self._register_tool(
            name="write_excel",
            description="写入Excel文件。参数: data(DataFrame), file_path(str)",
            func=self.excel_tool.write_excel
        )
        
        self._register_tool(
            name="filter_excel_data",
            description="过滤Excel数据。参数: data(DataFrame), column(str), condition(str), value(Any)",
            func=self.excel_tool.filter_data
        )
        
        # ========== Word工具 ==========
        self._register_tool(
            name="extract_word_text",
            description="提取Word文档文本。参数: file_path(str)",
            func=self.word_tool.extract_text
        )
        
        self._register_tool(
            name="render_word_template",
            description="渲染Word模板。参数: template_path(str), data(dict), output_path(str)",
            func=self.word_tool.render_template
        )
        
        self._register_tool(
            name="extract_word_info_regex",
            description="使用正则表达式从Word提取信息。参数: file_path(str), patterns(dict)",
            func=self.word_tool.extract_info_by_regex
        )
        
        # ========== 数据处理工具 ==========
        self._register_tool(
            name="extract_by_regex",
            description="使用正则表达式提取文本。参数: text(str), pattern(str)",
            func=self.data_tool.extract_by_regex
        )
        
        self._register_tool(
            name="parse_date",
            description="解析日期字符串。参数: date_str(str), format(str, 默认'%Y-%m-%d')",
            func=self.data_tool.parse_date
        )
        
        self._register_tool(
            name="calculate_date_offset",
            description="计算日期偏移。参数: base_date(str), offset_days(int)",
            func=self.data_tool.calculate_date_offset
        )
        
        logger.info(f"已注册 {len(self.tools)} 个RPA工具")
    
    def _register_tool(self, name: str, description: str, func):
        """注册单个工具"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "func": func
        }
        
        # 转换为LangChain Tool
        langchain_tool = Tool(
            name=name,
            description=description,
            func=lambda **kwargs: func(**kwargs)
        )
        self.langchain_tools.append(langchain_tool)
    
    def get_tool(self, name: str):
        """获取指定工具"""
        return self.tools.get(name)
    
    def get_all_tools(self) -> List[Tool]:
        """获取所有LangChain工具"""
        return self.langchain_tools
    
    def list_tools(self) -> List[str]:
        """列出所有工具名称"""
        return list(self.tools.keys())
    
    def get_tool_description(self, name: str) -> str:
        """获取工具描述"""
        tool = self.tools.get(name)
        return tool["description"] if tool else "工具不存在"


# 全局工具注册实例
tool_registry = RPAToolRegistry()


def get_rpa_tools() -> List[Tool]:
    """获取所有RPA工具（供Agent使用）"""
    return tool_registry.get_all_tools()


def get_tool_by_name(name: str):
    """根据名称获取工具"""
    return tool_registry.get_tool(name)
