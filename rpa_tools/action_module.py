"""
行动模块 - 执行具体操作
"""

import pyautogui
import pyperclip
import requests
import subprocess
import os
import time
from typing import Dict, Any


class ActionModule:
    """行动执行模块"""
    
    def __init__(self):
        self.ollama_api = "http://localhost:11434/api/generate"
        
    def execute(self, action: str, params: Dict[str, Any]) -> Dict:
        """
        执行行动
        
        Args:
            action: 行动名称
            params: 参数字典
        
        Returns:
            {
                'success': True/False,
                'result': '执行结果描述',
                'data': 返回数据（如果有）
            }
        """
        try:
            # 根据action调用对应方法
            method = getattr(self, f"_action_{action}", None)
            
            if method:
                return method(params)
            else:
                return {
                    'success': False,
                    'result': f"未知操作: {action}",
                    'data': None
                }
        except Exception as e:
            return {
                'success': False,
                'result': f"执行失败: {e}",
                'data': None
            }
    
    # ==================== 工具方法 ====================
    
    def _action_open_wps(self, params: Dict) -> Dict:
        """打开WPS"""
        try:
            wps_paths = [
                r"C:\Program Files (x86)\Kingsoft\WPS Office\ksolaunch.exe",
                r"C:\Program Files\Kingsoft\WPS Office\ksolaunch.exe",
            ]
            
            for path in wps_paths:
                if os.path.exists(path):
                    subprocess.Popen([path, "/w"])
                    time.sleep(4)
                    return {
                        'success': True,
                        'result': 'WPS已启动',
                        'data': None
                    }
            
            # 备用方案
            os.system("start wps")
            time.sleep(4)
            return {
                'success': True,
                'result': 'WPS已启动（系统命令）',
                'data': None
            }
        except Exception as e:
            return {
                'success': False,
                'result': f'WPS启动失败: {e}',
                'data': None
            }
    
    def _action_click(self, params: Dict) -> Dict:
        """点击"""
        x = params.get('x', 500)
        y = params.get('y', 300)
        
        try:
            pyautogui.click(x=x, y=y)
            time.sleep(0.5)
            return {
                'success': True,
                'result': f'已点击 ({x}, {y})',
                'data': None
            }
        except Exception as e:
            return {
                'success': False,
                'result': f'点击失败: {e}',
                'data': None
            }
    
    def _action_type_text(self, params: Dict) -> Dict:
        """输入文本（英文/数字）"""
        text = params.get('text', '')
        interval = params.get('interval', 0.05)
        
        try:
            pyautogui.write(text, interval=interval)
            time.sleep(0.3)
            return {
                'success': True,
                'result': f'已输入文本: {text[:20]}...',
                'data': None
            }
        except Exception as e:
            return {
                'success': False,
                'result': f'输入失败: {e}',
                'data': None
            }
    
    def _action_paste_text(self, params: Dict) -> Dict:
        """粘贴文本（适合中文）"""
        text = params.get('text', '')
        
        try:
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            return {
                'success': True,
                'result': f'已粘贴文本 ({len(text)} 字)',
                'data': None
            }
        except Exception as e:
            return {
                'success': False,
                'result': f'粘贴失败: {e}',
                'data': None
            }
    
    def _action_hotkey(self, params: Dict) -> Dict:
        """按快捷键"""
        keys = params.get('keys', [])
        
        if not keys:
            return {
                'success': False,
                'result': '未指定按键',
                'data': None
            }
        
        try:
            pyautogui.hotkey(*keys)
            time.sleep(0.5)
            return {
                'success': True,
                'result': f'已按快捷键: {"+".join(keys)}',
                'data': None
            }
        except Exception as e:
            return {
                'success': False,
                'result': f'快捷键失败: {e}',
                'data': None
            }
    
    def _action_wait(self, params: Dict) -> Dict:
        """等待"""
        seconds = params.get('seconds', 1)
        
        try:
            time.sleep(seconds)
            return {
                'success': True,
                'result': f'已等待 {seconds} 秒',
                'data': None
            }
        except Exception as e:
            return {
                'success': False,
                'result': f'等待失败: {e}',
                'data': None
            }
    
    def _action_get_weather(self, params: Dict) -> Dict:
        """获取天气"""
        city = params.get('city', 'Beijing')
        
        try:
            response = requests.get(
                f"https://wttr.in/{city}?format=j1",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                
                weather_info = {
                    'city': city,
                    'temperature': current['temp_C'],
                    'weather': current['weatherDesc'][0]['value'],
                    'humidity': current['humidity'],
                    'wind_speed': current['windspeedKmph'],
                    'feels_like': current['FeelsLikeC']
                }
                
                return {
                    'success': True,
                    'result': f'天气: {weather_info["temperature"]}°C, {weather_info["weather"]}',
                    'data': weather_info
                }
            else:
                # 模拟数据
                return {
                    'success': True,
                    'result': '使用模拟天气数据',
                    'data': {
                        'city': city,
                        'temperature': '15',
                        'weather': 'Partly cloudy',
                        'humidity': '65',
                        'wind_speed': '12',
                        'feels_like': '14'
                    }
                }
        except Exception as e:
            return {
                'success': False,
                'result': f'获取天气失败: {e}',
                'data': None
            }
    
    def _action_generate_article(self, params: Dict) -> Dict:
        """生成文章"""
        prompt = params.get('prompt', '')
        stream = params.get('stream', False)
        
        if not prompt:
            return {
                'success': False,
                'result': '未提供prompt',
                'data': None
            }
        
        try:
            response = requests.post(
                self.ollama_api,
                json={
                    "model": "deepseek-r1:8b",
                    "prompt": prompt,
                    "stream": stream
                },
                timeout=120
            )
            
            if response.status_code == 200:
                if stream:
                    # 流式输出
                    article = ""
                    for line in response.iter_lines():
                        if line:
                            import json
                            chunk = json.loads(line)
                            if 'response' in chunk:
                                text = chunk['response']
                                print(text, end='', flush=True)
                                article += text
                    print()  # 换行
                else:
                    result = response.json()
                    article = result['response']
                
                return {
                    'success': True,
                    'result': f'文章已生成 ({len(article)} 字)',
                    'data': article
                }
            else:
                return {
                    'success': False,
                    'result': 'AI生成失败',
                    'data': None
                }
        except Exception as e:
            return {
                'success': False,
                'result': f'生成失败: {e}',
                'data': None
            }
    
    def _action_complete_task(self, params: Dict) -> Dict:
        """标记任务完成"""
        return {
            'success': True,
            'result': '任务已完成',
            'data': 'TASK_COMPLETED'
        }


if __name__ == "__main__":
    # 测试
    action_module = ActionModule()
    
    # 测试等待
    result = action_module.execute('wait', {'seconds': 1})
    print(f"等待测试: {result}")
    
    # 测试获取天气
    result = action_module.execute('get_weather', {'city': 'Beijing'})
    print(f"天气测试: {result}")
