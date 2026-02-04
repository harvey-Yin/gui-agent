"""
RPA工具使用示例
演示如何使用提取的RPA工具集
"""
import sys
sys.path.append('c:\\document\\python\\gui-agent\\gui-agent')

from rpa_tools import (
    ScreenTool,
    VisionTool,
    ExcelTool,
    WordTool,
    DataTool,
    get_rpa_tools
)


def example_screen_operations():
    """示例1: 屏幕操作"""
    print("=== 示例1: 屏幕操作 ===")
    
    screen = ScreenTool()
    
    # 点击坐标
    result = screen.click_at(100, 200)
    print(f"点击结果: {result['message']}")
    
    # 输入文本
    result = screen.type_text("你好，这是测试文本")
    print(f"输入结果: {result['message']}")
    
    # 组合键
    result = screen.hotkey('ctrl', 'c')
    print(f"组合键结果: {result['message']}")
    
    # 截图
    result = screen.screenshot(save_path="screenshot.png")
    print(f"截图结果: {result['message']}")


def example_vision_operations():
    """示例2: 视觉识别"""
    print("\n=== 示例2: 视觉识别 ===")
    
    vision = VisionTool(image_dir="picture")
    
    # 查找图像
    result = vision.find_image("button.png")
    if result['found']:
        print(f"找到图像位置: {result['position']}")
    
    # 点击图像
    result = vision.click_image("submit_button.png", timeout=10)
    print(f"点击图像结果: {result['message']}")
    
    # 相对定位点击
    result = vision.click_relative("anchor.png", offset_x=50, offset_y=20)
    print(f"相对点击结果: {result['message']}")


def example_excel_operations():
    """示例3: Excel处理"""
    print("\n=== 示例3: Excel处理 ===")
    
    excel = ExcelTool()
    
    # 读取Excel
    result = excel.read_excel("input.xlsx", sheet_name="Sheet1")
    if result['status'] == 'success':
        df = result['data']
        print(f"读取Excel: {result['shape']} 行列")
        print(f"列名: {result['columns']}")
    
    # 过滤数据
    result = excel.filter_data(df, column="状态", condition="==", value="完成")
    if result['status'] == 'success':
        print(f"过滤结果: {result['filtered_count']} 行")
    
    # 写入Excel
    result = excel.write_excel(df, "output.xlsx")
    print(f"写入结果: {result['message']}")


def example_word_operations():
    """示例4: Word处理"""
    print("\n=== 示例4: Word处理 ===")
    
    word = WordTool()
    
    # 提取文本
    result = word.extract_text("document.docx")
    if result['status'] == 'success':
        print(f"提取文本: {result['length']} 字符")
    
    # 使用正则提取信息
    patterns = {
        "编号": r"GD-\d+",
        "姓名": r"姓名[:：]\s*([^\s]+)",
        "电话": r"1[3-9]\d{9}"
    }
    result = word.extract_info_by_regex("document.docx", patterns)
    if result['status'] == 'success':
        print(f"提取信息: {result['data']}")
    
    # 渲染模板
    data = {
        "客户姓名": "张三",
        "申诉号码": "13800138000",
        "处理结果": "已解决"
    }
    result = word.render_template("template.docx", data, "output.docx")
    print(f"模板渲染: {result['message']}")


def example_data_operations():
    """示例5: 数据处理"""
    print("\n=== 示例5: 数据处理 ===")
    
    data_tool = DataTool()
    
    # 正则提取
    text = "订单号: GD-20240204-001, 日期: 2024-02-04"
    result = data_tool.extract_by_regex(text, r"GD-\d+-\d+")
    print(f"提取订单号: {result['match']}")
    
    # 日期计算
    result = data_tool.calculate_date_offset("2024-02-04", offset_days=7)
    print(f"日期计算: {result['message']}")
    
    # 手机号验证
    result = data_tool.validate_phone("13800138000")
    print(f"手机号验证: {result['message']}")


def example_integrated_workflow():
    """示例6: 综合工作流（模拟真实场景）"""
    print("\n=== 示例6: 综合工作流 ===")
    
    # 场景: 从Excel读取数据，填写到Word模板，保存结果
    
    excel = ExcelTool()
    word = WordTool()
    
    # 1. 读取Excel数据
    print("步骤1: 读取Excel数据...")
    result = excel.read_excel("客户信息.xlsx")
    if result['status'] == 'success':
        df = result['data']
        print(f"  读取 {len(df)} 条记录")
        
        # 2. 批量生成Word文档
        print("步骤2: 批量生成Word文档...")
        data_list = df.to_dict('records')
        result = word.batch_generate_from_template(
            template_path="客户报告模板.docx",
            data_list=data_list,
            output_dir="output_reports",
            filename_pattern="报告_{客户姓名}_{申诉号码}.docx"
        )
        print(f"  生成 {result['count']} 个文档")


def example_langchain_integration():
    """示例7: LangChain Agent集成"""
    print("\n=== 示例7: LangChain Agent集成 ===")
    
    # 获取所有工具
    tools = get_rpa_tools()
    print(f"可用工具数量: {len(tools)}")
    
    # 列出所有工具
    print("\n可用的RPA工具:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")


if __name__ == "__main__":
    print("RPA工具集使用示例\n")
    print("=" * 60)
    
    # 运行示例（注释掉需要实际文件的示例）
    # example_screen_operations()
    # example_vision_operations()
    # example_excel_operations()
    # example_word_operations()
    # example_data_operations()
    # example_integrated_workflow()
    example_langchain_integration()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
