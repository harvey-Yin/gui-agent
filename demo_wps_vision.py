"""
AI视觉引导的WPS自动化Demo
功能：
1. 获取天气数据
2. AI生成文章（流式显示思考过程）
3. 打开WPS
4. 使用MAI-UI-2B视觉识别WPS界面
5. 智能定位输入区域
6. 写入内容并保存
"""

import requests
import pyautogui
import time
from datetime import datetime
import subprocess
import os
import base64
from PIL import ImageGrab
import pyperclip

print("=" * 70)
print("AI视觉引导的WPS自动化Demo")
print("=" * 70)

# ==================== 配置 ====================
MAI_UI_API = "http://localhost:8001/v1"
OLLAMA_API = "http://localhost:11434/api/generate"

# ==================== Step 1: 获取天气信息 ====================
print("\n[Step 1] 获取当前天气信息...")

def get_weather():
    """获取北京天气"""
    try:
        response = requests.get("https://wttr.in/Beijing?format=j1", timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            weather_info = {
                'city': '北京',
                'temperature': current['temp_C'],
                'weather': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'wind_speed': current['windspeedKmph'],
                'feels_like': current['FeelsLikeC']
            }
            print(f"  [OK] 天气: {weather_info['temperature']}°C, {weather_info['weather']}")
            return weather_info
        else:
            raise Exception("API error")
    except:
        print(f"  [WARN] 使用模拟数据")
        return {'city': '北京', 'temperature': '15', 'weather': 'Partly cloudy', 
                'humidity': '65', 'wind_speed': '12', 'feels_like': '14'}

weather = get_weather()

# ==================== Step 2: AI生成文章（流式输出）====================
print("\n[Step 2] AI生成天气文章...")

def generate_article_stream(weather_info):
    """使用qwen生成文章，流式显示思考过程"""
    prompt = f"""请根据以下天气信息，写一篇200字左右的天气播报文章：

城市：{weather_info['city']}
温度：{weather_info['temperature']}°C
天气：{weather_info['weather']}
湿度：{weather_info['humidity']}%

要求：语言生动，包含出行建议，200字左右，不要标题。"""

    try:
        print(f"\n  [AI思考中...]\n")
        print("-" * 70)
        
        response = requests.post(
            OLLAMA_API,
            json={"model": "qwen:7b", "prompt": prompt, "stream": True},
            stream=True,
            timeout=120
        )
        
        article = ""
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    import json
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        text = chunk['response']
                        print(text, end='', flush=True)
                        article += text
            
            print("\n" + "-" * 70)
            print(f"\n  [OK] 文章生成完成 ({len(article)} 字)")
            return article
        else:
            return f"今天{weather_info['city']}的天气{weather_info['weather']}，温度{weather_info['temperature']}°C。"
    except Exception as e:
        print(f"\n  [FAIL] AI失败: {e}")
        return f"今天{weather_info['city']}的天气{weather_info['weather']}，温度{weather_info['temperature']}°C。"

article = generate_article_stream(weather)

# ==================== Step 3: 打开WPS ====================
print("\n[Step 3] 打开WPS文字...")

def open_wps():
    """打开WPS"""
    try:
        wps_paths = [
            r"C:\Program Files (x86)\Kingsoft\WPS Office\ksolaunch.exe",
            r"C:\Program Files\Kingsoft\WPS Office\ksolaunch.exe",
        ]
        
        for path in wps_paths:
            if os.path.exists(path):
                subprocess.Popen([path, "/w"])
                print(f"  [OK] WPS启动成功")
                time.sleep(4)
                return True
        
        os.system("start wps")
        print(f"  [OK] WPS启动（系统命令）")
        time.sleep(4)
        return True
    except Exception as e:
        print(f"  [FAIL] WPS启动失败: {e}")
        return False

if not open_wps():
    print("\n[ERROR] 无法启动WPS")
    exit(1)

# 创建新文档
print("\n[Step 3.5] 创建新文档...")
pyautogui.hotkey('ctrl', 'n')
time.sleep(2)
print(f"  [OK] 新文档已创建")

# ==================== Step 4: 使用MAI-UI视觉识别WPS界面 ====================
print("\n[Step 4] 使用MAI-UI-2B视觉识别WPS界面...")

def capture_and_analyze_screen():
    """截图并使用MAI-UI分析"""
    # 截图
    screenshot = ImageGrab.grab()
    screenshot.save("wps_screen.png")
    print(f"  [OK] 截图已保存")
    
    # 编码为base64
    with open("wps_screen.png", "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()
    
    # 调用MAI-UI-2B分析
    print(f"  [MAI-UI分析中...]")
    
    try:
        payload = {
            "model": "MAI-UI-2B",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
                    {"type": "text", "text": """请分析这个WPS文字界面：
1. 文档编辑区域在屏幕的哪个位置？（用百分比描述，如"屏幕中央偏上，约占屏幕40%-90%的区域"）
2. 当前光标是否在文档中？
3. 是否有工具栏、菜单栏遮挡？
4. 建议点击哪个位置开始输入？（用屏幕百分比，如"50%宽度，30%高度"）

请简洁回答。"""}
                ]
            }],
            "max_tokens": 300,
            "temperature": 0.3
        }
        
        response = requests.post(
            f"{MAI_UI_API}/chat/completions",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis = result['choices'][0]['message']['content']
            
            print("\n" + "=" * 70)
            print("MAI-UI视觉分析结果:")
            print("=" * 70)
            print(analysis)
            print("=" * 70)
            
            return analysis
        else:
            print(f"  [FAIL] MAI-UI调用失败: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  [FAIL] 视觉分析失败: {e}")
        return None

vision_analysis = capture_and_analyze_screen()

# ==================== Step 5: 智能定位输入区域 ====================
print("\n[Step 5] 根据视觉分析定位输入区域...")

def smart_click_input_area(analysis):
    """根据MAI-UI分析结果智能点击"""
    screen_width, screen_height = pyautogui.size()
    
    # 默认点击位置（屏幕中央偏上）
    click_x = int(screen_width * 0.5)
    click_y = int(screen_height * 0.35)
    
    if analysis:
        # 尝试从分析结果中提取位置信息
        # 这里简化处理，实际可以用更复杂的解析
        if "50%" in analysis and "30%" in analysis:
            # 提取百分比（这里简化，实际需要更精确的解析）
            click_x = int(screen_width * 0.5)
            click_y = int(screen_height * 0.3)
        elif "中央" in analysis or "center" in analysis.lower():
            click_x = int(screen_width * 0.5)
            click_y = int(screen_height * 0.4)
    
    print(f"  [OK] 智能定位: ({click_x}, {click_y})")
    pyautogui.click(x=click_x, y=click_y)
    time.sleep(0.5)
    return True

smart_click_input_area(vision_analysis)

# ==================== Step 6: 写入内容 ====================
print("\n[Step 6] 写入文章到WPS...")

def write_content(title, content):
    """写入标题和内容"""
    try:
        # 写入标题
        pyautogui.write(title, interval=0.05)
        pyautogui.press('enter')
        pyautogui.press('enter')
        
        # 写入内容（使用剪贴板处理中文）
        pyperclip.copy(content)
        pyautogui.hotkey('ctrl', 'v')
        
        print(f"  [OK] 内容写入成功")
        return True
    except Exception as e:
        print(f"  [FAIL] 写入失败: {e}")
        return False

today = datetime.now().strftime("%Y年%m月%d日")
title = f"{today} {weather['city']}天气播报"

write_content(title, article)

# ==================== Step 7: 保存文档 ====================
print("\n[Step 7] 保存文档...")

def save_document():
    """保存文档"""
    try:
        time.sleep(1)
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)
        
        filename = f"天气播报_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        pyautogui.write(filename, interval=0.05)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1)
        
        print(f"  [OK] 文档已保存: {filename}")
        return True
    except Exception as e:
        print(f"  [FAIL] 保存失败: {e}")
        return False

save_document()

# ==================== 完成 ====================
print("\n" + "=" * 70)
print("✅ AI视觉引导自动化任务完成！")
print("=" * 70)
print(f"\n关键技术：")
print(f"  1. ☁️  天气API获取实时数据")
print(f"  2. 🤖 qwen:7b流式生成文章")
print(f"  3. 👁️  MAI-UI-2B视觉识别界面")
print(f"  4. 🎯 智能定位输入区域")
print(f"  5. ⌨️  自动化输入和保存")
print(f"\n生成的文档：{title}")
print(f"文章长度：{len(article)} 字")
print("\n按任意键关闭...")
input()
