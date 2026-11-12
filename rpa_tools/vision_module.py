"""
视觉模块 - 使用MAI-UI-2B分析屏幕
"""

import base64
import requests
from PIL import ImageGrab
from typing import Dict, Optional


class VisionModule:
    """视觉感知模块"""
    
    def __init__(self, api_base: str = "http://localhost:8001/v1"):
        self.api_base = api_base
        self.model_name = "MAI-UI-2B"
        
    def capture_screen(self, save_path: str = "agent_screen.png") -> str:
        """截取屏幕并保存"""
        screenshot = ImageGrab.grab()
        screenshot.save(save_path)
        return save_path
    
    def encode_image(self, image_path: str) -> str:
        """将图片编码为base64"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    def analyze_screen(self, 
                      task_description: str,
                      current_state: str = "UNKNOWN",
                      specific_question: Optional[str] = None) -> Dict:
        """
        分析当前屏幕
        
        Args:
            task_description: 当前任务描述
            current_state: 当前状态
            specific_question: 特定问题（可选）
        
        Returns:
            {
                'description': '屏幕描述',
                'current_app': '当前应用',
                'key_elements': ['元素1', '元素2'],
                'task_status': '任务状态评估',
                'suggestion': '建议的下一步操作',
                'raw_response': '原始响应'
            }
        """
        # 截图
        image_path = self.capture_screen()
        image_base64 = self.encode_image(image_path)
        
        # 构建分析提示
        prompt = self._build_analysis_prompt(
            task_description, 
            current_state, 
            specific_question
        )
        
        # 调用MAI-UI-2B
        try:
            payload = {
                "model": self.model_name,
                "messages": [{
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
                            "text": prompt
                        }
                    ]
                }],
                "max_tokens": 400,
                "temperature": 0.2  # 低温度，更准确
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                raw_response = result['choices'][0]['message']['content']
                
                # 解析响应
                parsed = self._parse_response(raw_response)
                parsed['raw_response'] = raw_response
                
                return parsed
            else:
                return self._error_response(f"API错误: {response.status_code}")
                
        except Exception as e:
            return self._error_response(f"视觉分析失败: {e}")
    
    def _build_analysis_prompt(self, 
                               task: str, 
                               state: str,
                               question: Optional[str]) -> str:
        """构建分析提示"""
        base_prompt = f"""请分析这个屏幕截图。

当前任务：{task}
当前状态：{state}

请回答：
1. 当前显示的是什么应用/界面？
2. 主要的UI元素有哪些？（列出3-5个关键元素）
3. 光标或焦点在哪里？
4. 是否有弹窗、错误提示或需要交互的元素？
5. 根据任务，当前进度如何？（未开始/进行中/接近完成/已完成）
6. 建议的下一步操作是什么？

请简洁回答，重点关注与任务相关的信息。"""

        if question:
            base_prompt += f"\n\n特别问题：{question}"
        
        return base_prompt
    
    def _parse_response(self, response: str) -> Dict:
        """解析MAI-UI响应（简单解析）"""
        # 这里做简单的关键词提取
        # 实际项目中可以用更复杂的NLP或让AI返回JSON
        
        return {
            'description': response[:200],  # 前200字作为描述
            'current_app': self._extract_app_name(response),
            'key_elements': self._extract_elements(response),
            'task_status': self._extract_status(response),
            'suggestion': self._extract_suggestion(response),
        }
    
    def _extract_app_name(self, text: str) -> str:
        """提取应用名称"""
        keywords = ['WPS', 'Word', '桌面', 'Desktop', '浏览器', 'Chrome']
        for keyword in keywords:
            if keyword in text:
                return keyword
        return "未知应用"
    
    def _extract_elements(self, text: str) -> list:
        """提取UI元素（简化版）"""
        elements = []
        element_keywords = ['按钮', '输入框', '菜单', '工具栏', '文档', '编辑区']
        for keyword in element_keywords:
            if keyword in text:
                elements.append(keyword)
        return elements[:5]
    
    def _extract_status(self, text: str) -> str:
        """提取任务状态"""
        if '已完成' in text or '完成' in text:
            return "COMPLETED"
        elif '进行中' in text or '正在' in text:
            return "IN_PROGRESS"
        elif '未开始' in text or '需要' in text:
            return "NOT_STARTED"
        else:
            return "UNKNOWN"
    
    def _extract_suggestion(self, text: str) -> str:
        """提取建议"""
        # 查找"建议"后的内容
        if '建议' in text:
            idx = text.find('建议')
            return text[idx:idx+100].strip()
        return "继续观察"
    
    def _error_response(self, error_msg: str) -> Dict:
        """错误响应"""
        return {
            'description': f"错误: {error_msg}",
            'current_app': "ERROR",
            'key_elements': [],
            'task_status': "ERROR",
            'suggestion': "重试或人工介入",
            'raw_response': error_msg
        }


if __name__ == "__main__":
    # 测试
    vision = VisionModule()
    result = vision.analyze_screen(
        task_description="打开WPS并创建文档",
        current_state="INIT"
    )
    
    print("视觉分析结果：")
    print(f"当前应用: {result['current_app']}")
    print(f"任务状态: {result['task_status']}")
    print(f"建议: {result['suggestion']}")
    print(f"\n完整响应:\n{result['raw_response']}")
