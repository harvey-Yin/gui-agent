"""
对话式Agent - 可以聊天并执行任务
"""

import json
from typing import List, Dict, Optional
from .vision_module import VisionModule
from .action_module import ActionModule
import requests


class ConversationalAgent:
    """对话式智能Agent"""
    
    def __init__(self):
        self.vision = VisionModule()
        self.action = ActionModule()
        self.ollama_api = "http://localhost:11434/api/generate"
        
        # 对话历史
        self.conversation_history = []
        
        # 任务执行状态
        self.current_task = None
        self.task_context = {}  # 存储任务相关数据
        
        # System Prompt
        self.system_prompt = """你是一个智能RPA助手，可以帮助用户完成电脑操作任务。

你的能力：
1. 对话交流：理解用户需求，回答问题
2. 视觉感知：通过MAI-UI-2B查看屏幕内容
3. 执行操作：控制鼠标、键盘，打开应用，调用API等

可用工具：
- look_screen: 查看当前屏幕（使用MAI-UI-2B）
- open_wps: 打开WPS文字
- click(x, y): 点击坐标
- type_text(text): 输入文本
- paste_text(text): 粘贴文本（适合中文）
- hotkey(*keys): 按快捷键
- get_weather(city): 获取天气
- generate_article(prompt): 生成文章
- wait(seconds): 等待

交互规则：
1. 如果用户只是聊天，正常对话
2. 如果用户要求执行任务，先确认理解，然后逐步执行
3. 执行任务时，主动使用look_screen观察屏幕
4. 每次只执行一个操作，然后报告结果
5. 遇到问题，主动询问用户

回复格式：
- 如果只是对话：直接回复文本
- 如果需要执行操作：返回JSON格式
  {
    "type": "action",
    "thought": "你的思考",
    "tool": "工具名",
    "params": {...},
    "message": "告诉用户你在做什么"
  }
"""
    
    def chat(self, user_message: str) -> Dict:
        """
        与用户对话
        
        Returns:
            {
                'type': 'text' | 'action',
                'content': '回复内容',
                'action': {...}  # 如果type是action
            }
        """
        # 添加到历史
        self.conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # 构建完整对话上下文
        prompt = self._build_chat_prompt(user_message)
        
        # 调用qwen
        try:
            response = requests.post(
                self.ollama_api,
                json={
                    "model": "deepseek-r1:8b",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['response']
                
                # 解析响应
                parsed = self._parse_response(ai_response)
                
                # 添加到历史
                self.conversation_history.append({
                    'role': 'assistant',
                    'content': ai_response
                })
                
                return parsed
            else:
                return {
                    'type': 'text',
                    'content': '抱歉，我遇到了一些问题，请稍后再试。'
                }
        except Exception as e:
            return {
                'type': 'text',
                'content': f'抱歉，出现错误: {e}'
            }
    
    def execute_action(self, action_info: Dict) -> Dict:
        """执行操作"""
        tool = action_info.get('tool')
        params = action_info.get('params', {})
        
        # 特殊处理：look_screen
        if tool == 'look_screen':
            question = params.get('question', '')
            result = self.vision.analyze_screen(
                task_description=self.current_task or "观察屏幕",
                current_state="OBSERVING",
                specific_question=question
            )
            return {
                'success': True,
                'result': f"屏幕分析完成",
                'data': result
            }
        else:
            # 使用ActionModule执行
            return self.action.execute(tool, params)
    
    def _build_chat_prompt(self, user_message: str) -> str:
        """构建对话提示"""
        # 历史对话（最近5轮）
        recent_history = self.conversation_history[-10:]
        history_text = ""
        for msg in recent_history:
            role = "用户" if msg['role'] == 'user' else "助手"
            history_text += f"{role}: {msg['content']}\n"
        
        # 任务上下文
        context_text = ""
        if self.current_task:
            context_text = f"\n当前任务: {self.current_task}\n"
        
        if self.task_context:
            context_text += "任务数据:\n"
            for key, value in self.task_context.items():
                if isinstance(value, str):
                    context_text += f"  {key}: {value[:50]}...\n"
                else:
                    context_text += f"  {key}: {value}\n"
        
        prompt = f"""{self.system_prompt}

{context_text}

对话历史:
{history_text}

用户: {user_message}

助手:"""
        
        return prompt
    
    def _parse_response(self, response: str) -> Dict:
        """解析AI响应"""
        # 尝试提取JSON
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = response[start:end]
                action_data = json.loads(json_str)
                
                if action_data.get('type') == 'action':
                    return {
                        'type': 'action',
                        'content': action_data.get('message', '执行操作中...'),
                        'action': action_data
                    }
        except:
            pass
        
        # 普通文本回复
        return {
            'type': 'text',
            'content': response
        }
    
    def set_task(self, task_description: str):
        """设置当前任务"""
        self.current_task = task_description
        self.task_context = {}
    
    def clear_task(self):
        """清除任务"""
        self.current_task = None
        self.task_context = {}
    
    def save_task_data(self, key: str, value):
        """保存任务数据"""
        self.task_context[key] = value


if __name__ == "__main__":
    # 测试
    agent = ConversationalAgent()
    
    # 测试对话
    response = agent.chat("你好，你能做什么？")
    print(f"Agent: {response['content']}")
