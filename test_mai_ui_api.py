"""
测试MAI-UI-2B Docker API
演示如何通过OpenAI兼容API调用MAI-UI
"""

import requests
import base64
from pathlib import Path
from PIL import ImageGrab

# API配置
API_BASE = "http://localhost:8001/v1"
MODEL_NAME = "MAI-UI-2B"

print("=" * 50)
print("MAI-UI-2B Docker API 测试")
print("=" * 50)

# Step 1: 检查API状态
print("\n[Step 1] 检查API状态...")
try:
    response = requests.get(f"{API_BASE}/models")
    if response.status_code == 200:
        models = response.json()
        print(f"  [OK] API运行正常")
        print(f"  可用模型: {models['data'][0]['id']}")
    else:
        print(f"  [FAIL] API返回错误: {response.status_code}")
        exit(1)
except Exception as e:
    print(f"  [FAIL] 无法连接API: {e}")
    exit(1)

# Step 2: 截取屏幕
print("\n[Step 2] 截取当前屏幕...")
screenshot = ImageGrab.grab()
screenshot_path = "current_screen.png"
screenshot.save(screenshot_path)
print(f"  [OK] 截图保存: {screenshot_path}")

# Step 3: 编码图片为base64
print("\n[Step 3] 编码图片...")
with open(screenshot_path, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')
print(f"  [OK] 图片编码完成")

# Step 4: 调用API进行GUI识别
print("\n[Step 4] 调用MAI-UI识别屏幕内容...")
try:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "请描述这个屏幕上有什么内容，包括主要的UI元素。"
                    }
                ]
            }
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }
    
    response = requests.post(
        f"{API_BASE}/chat/completions",
        json=payload,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        answer = result['choices'][0]['message']['content']
        
        print("\n" + "=" * 50)
        print("识别结果:")
        print("=" * 50)
        print(answer)
        print("=" * 50)
    else:
        print(f"  [FAIL] API调用失败: {response.status_code}")
        print(f"  错误信息: {response.text}")
        
except Exception as e:
    print(f"  [FAIL] 调用失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成！")
print("\n可以尝试的任务：")
print("1. 修改prompt为: '找到屏幕上的开始按钮'")
print("2. 修改prompt为: '列出所有可见的图标'")
print("3. 修改prompt为: '屏幕左上角有什么？'")
