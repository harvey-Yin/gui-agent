"""
AI自动化WPS文档生成Demo
功能：获取天气 → AI生成文章（流式显示思考过程）→ 自动打开WPS → 写入内容 → 保存文档
"""

import requests
import pyautogui
import time
from datetime import datetime
import subprocess
import os

print("=" * 60)
print("AI自动化Word文档生成Demo")
print("=" * 60)

# ==================== Step 1: 获取天气信息 ====================
print("\n[Step 1] 获取当前天气信息...")

def get_weather():
    """获取北京天气（使用免费API）"""
    try:
        # 使用wttr.in免费天气API
        response = requests.get(
            "https://wttr.in/Beijing?format=j1",
            timeout=10
        )
        
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
            
            print(f"  [OK] 天气获取成功")
            print(f"  城市: {weather_info['city']}")
            print(f"  温度: {weather_info['temperature']}°C")
            print(f"  天气: {weather_info['weather']}")
            print(f"  湿度: {weather_info['humidity']}%")
            
            return weather_info
        else:
            print(f"  [WARN] API返回错误，使用模拟数据")
            return {
                'city': '北京',
                'temperature': '15',
                'weather': 'Partly cloudy',
                'humidity': '65',
                'wind_speed': '12',
                'feels_like': '14'
            }
    except Exception as e:
        print(f"  [WARN] 获取天气失败: {e}，使用模拟数据")
        return {
            'city': '北京',
            'temperature': '15',
            'weather': 'Partly cloudy',
            'humidity': '65',
            'wind_speed': '12',
            'feels_like': '14'
        }

weather = get_weather()

# ==================== Step 2: AI生成文章 ====================
print("\n[Step 2] 使用AI生成天气文章...")

def generate_article(weather_info):
    """使用Ollama生成文章（流式输出，显示思考过程）"""
    try:
        prompt = f"""请根据以下天气信息，写一篇200字左右的天气播报文章：

城市：{weather_info['city']}
温度：{weather_info['temperature']}°C
天气：{weather_info['weather']}
湿度：{weather_info['humidity']}%
风速：{weather_info['wind_speed']} km/h
体感温度：{weather_info['feels_like']}°C

要求：
1. 语言生动，适合播报
2. 包含出行建议
3. 字数200字左右
4. 不要包含标题
"""
        
        print(f"  [AI思考中...]\n")
        print("-" * 60)
        
        # 使用流式API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen:7b",
                "prompt": prompt,
                "stream": True  # 启用流式输出
            },
            stream=True,
            timeout=120
        )
        
        article = ""
        if response.status_code == 200:
            # 逐字显示AI生成过程
            for line in response.iter_lines():
                if line:
                    import json
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        text = chunk['response']
                        print(text, end='', flush=True)
                        article += text
            
            print("\n" + "-" * 60)
            print(f"\n  [OK] 文章生成完成")
            print(f"  文章长度: {len(article)} 字")
            return article
        else:
            print(f"  [FAIL] AI生成失败，使用模板")
            return f"""今天{weather_info['city']}的天气{weather_info['weather']}，当前温度{weather_info['temperature']}°C，体感温度{weather_info['feels_like']}°C。空气湿度为{weather_info['humidity']}%，风速{weather_info['wind_speed']}公里每小时。建议出行时根据体感温度适当增减衣物，注意保暖。"""
            
    except Exception as e:
        print(f"\n  [FAIL] AI调用失败: {e}")
        return f"""今天{weather_info['city']}的天气{weather_info['weather']}，当前温度{weather_info['temperature']}°C，体感温度{weather_info['feels_like']}°C。空气湿度为{weather_info['humidity']}%，风速{weather_info['wind_speed']}公里每小时。建议出行时根据体感温度适当增减衣物，注意保暖。"""

article = generate_article(weather)

print("\n生成的文章预览：")
print("-" * 60)
print(article)
print("-" * 60)

# ==================== Step 3: 打开WPS文字 ====================
print("\n[Step 3] 打开WPS文字...")

def open_wps():
    """打开WPS文字应用"""
    try:
        # WPS文字的常见路径
        wps_paths = [
            r"C:\Program Files (x86)\Kingsoft\WPS Office\ksolaunch.exe",
            r"C:\Program Files\Kingsoft\WPS Office\ksolaunch.exe",
            r"C:\Users\{}\AppData\Local\Kingsoft\WPS Office\ksolaunch.exe".format(os.getenv('USERNAME')),
        ]
        
        for path in wps_paths:
            if os.path.exists(path):
                # 启动WPS文字 (参数 /w 表示打开Writer)
                subprocess.Popen([path, "/w"])
                print(f"  [OK] WPS文字启动成功")
                time.sleep(4)  # 等待WPS启动
                return True
        
        # 如果找不到，尝试用start命令
        os.system("start wps")
        print(f"  [OK] WPS启动成功（使用系统命令）")
        time.sleep(4)
        return True
        
    except Exception as e:
        print(f"  [FAIL] WPS启动失败: {e}")
        return False

if not open_wps():
    print("\n[ERROR] 无法启动WPS，请确保已安装WPS Office")
    exit(1)

# ==================== Step 4: 等待WPS完全加载 ====================
print("\n[Step 4] 等待WPS加载...")
time.sleep(3)

# 创建新文档
print("\n[Step 4.5] 创建新文档...")
try:
    pyautogui.hotkey('ctrl', 'n')  # Ctrl+N 新建文档
    time.sleep(2)  # 等待新文档创建
    print(f"  [OK] 新文档创建成功")
except Exception as e:
    print(f"  [WARN] 新建文档可能失败: {e}")
    time.sleep(1)

# ==================== Step 5: 写入内容到WPS ====================
print("\n[Step 5] 写入文章到WPS...")

def write_to_wps(title, content):
    """使用pyautogui写入内容到WPS"""
    try:
        # 确保WPS窗口激活
        pyautogui.click(x=500, y=300)  # 点击WPS窗口中心
        time.sleep(0.5)
        
        # 写入标题
        pyautogui.write(title, interval=0.05)
        pyautogui.press('enter')
        pyautogui.press('enter')
        
        # 写入内容（中文需要用typewrite或剪贴板）
        # 使用剪贴板方式写入中文
        import pyperclip
        pyperclip.copy(content)
        pyautogui.hotkey('ctrl', 'v')
        
        print(f"  [OK] 内容写入成功")
        return True
        
    except Exception as e:
        print(f"  [FAIL] 写入失败: {e}")
        return False

# 生成标题
today = datetime.now().strftime("%Y年%m月%d日")
title = f"{today} {weather['city']}天气播报"

write_to_wps(title, article)

# ==================== Step 6: 保存WPS文档 ====================
print("\n[Step 6] 保存WPS文档...")

def save_word_document():
    """保存WPS文档"""
    try:
        time.sleep(1)
        
        # 使用Ctrl+S保存
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)
        
        # 输入文件名
        filename = f"天气播报_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        pyautogui.write(filename, interval=0.05)
        time.sleep(0.5)
        
        # 按Enter确认保存
        pyautogui.press('enter')
        time.sleep(1)
        
        print(f"  [OK] 文档已保存: {filename}")
        return True
        
    except Exception as e:
        print(f"  [FAIL] 保存失败: {e}")
        return False

save_word_document()

# ==================== 完成 ====================
print("\n" + "=" * 60)
print("✅ 自动化任务完成！")
print("=" * 60)
print(f"\n生成的文档：")
print(f"  标题: {title}")
print(f"  内容: {len(article)} 字")
print(f"  保存位置: 我的文档")
print("\n按任意键关闭...")
input()
