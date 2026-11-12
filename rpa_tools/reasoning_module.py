"""
推理模块 - 使用qwen进行决策
"""

import requests
import json
from typing import Dict, List, Optional


class ReasoningModule:
    """推理决策模块"""
    
    def __init__(self, api_base: str = "http://localhost:11434/api/generate"):
        self.api_base = api_base
        self.model_name = "deepseek-r1:8b"
        
    def decide_next_action(self,
                          task: str,
                          current_state: str,
                          observation: Dict,
                          history: List[Dict],
                          available_tools: List[str]) -> Dict:
        """
        决定下一步行动
        
        Args:
            task: 任务描述
            current_state: 当前状态
            observation: 视觉观察结果
            history: 历史行动记录
            available_tools: 可用工具列表
        
        Returns:
            {
                'reasoning': '推理过程',
                'action': '工具名称',
                'params': {...},
                'expected_result': '预期结果',
                'confidence': 0.0-1.0
            }
        """
        # 构建决策提示
        prompt = self._build_decision_prompt(
            task, current_state, observation, history, available_tools
        )
        
        # 调用qwen
        try:
            response = requests.post(
                self.api_base,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,  # 较低温度，更确定性
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                decision_text = result['response']
                
                # 解析决策
                decision = self._parse_decision(decision_text)
                return decision
            else:
                return self._fallback_decision("API错误")
                
        except Exception as e:
            return self._fallback_decision(f"推理失败: {e}")
    
    def _build_decision_prompt(self,
                               task: str,
                               state: str,
                               obs: Dict,
                               history: List[Dict],
                               tools: List[str]) -> str:
        """构建决策提示"""
        
        # 历史记录摘要
        history_summary = self._summarize_history(history)
        
        prompt = f"""你是一个智能RPA Agent，需要完成任务并做出决策。

【任务】
{task}

【当前状态】
{state}

【视觉观察】
- 当前应用: {obs.get('current_app', '未知')}
- 任务进度: {obs.get('task_status', '未知')}
- 关键元素: {', '.join(obs.get('key_elements', []))}
- AI建议: {obs.get('suggestion', '无')}

【历史行动】
{history_summary}

【可用工具】
{self._format_tools(tools)}

【决策要求】
1. 分析当前情况
2. 判断任务进度
3. 选择最合适的下一步行动
4. 只执行一个操作

请以JSON格式返回决策（只返回JSON，不要其他内容）：
{{
  "reasoning": "你的分析和推理过程",
  "action": "工具名称",
  "params": {{}},
  "expected_result": "预期结果",
  "confidence": 0.8
}}

决策："""
        
        return prompt
    
    def _summarize_history(self, history: List[Dict]) -> str:
        """总结历史记录"""
        if not history:
            return "无历史记录"
        
        # 只显示最近3条
        recent = history[-3:]
        summary = []
        for i, item in enumerate(recent, 1):
            action = item.get('action', '未知')
            result = item.get('result', '未知')
            summary.append(f"{i}. {action} → {result}")
        
        return "\n".join(summary)
    
    def _format_tools(self, tools: List[str]) -> str:
        """格式化工具列表"""
        tool_descriptions = {
            'open_wps': '打开WPS文字应用',
            'click': 'click(x, y) - 点击屏幕坐标',
            'type_text': 'type_text(text) - 输入文本',
            'hotkey': 'hotkey(*keys) - 按快捷键，如 hotkey("ctrl", "s")',
            'wait': 'wait(seconds) - 等待指定秒数',
            'get_weather': 'get_weather() - 获取天气数据',
            'generate_article': 'generate_article(prompt) - AI生成文章',
            'paste_text': 'paste_text(text) - 使用剪贴板粘贴文本（适合中文）',
            'complete_task': 'complete_task() - 标记任务完成'
        }
        
        formatted = []
        for tool in tools:
            desc = tool_descriptions.get(tool, tool)
            formatted.append(f"- {desc}")
        
        return "\n".join(formatted)
    
    def _parse_decision(self, text: str) -> Dict:
        """解析决策文本"""
        try:
            # 尝试提取JSON
            # 查找第一个 { 和最后一个 }
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = text[start:end]
                decision = json.loads(json_str)
                
                # 验证必需字段
                required = ['reasoning', 'action', 'params']
                if all(k in decision for k in required):
                    # 设置默认值
                    decision.setdefault('expected_result', '未知')
                    decision.setdefault('confidence', 0.7)
                    return decision
            
            # JSON解析失败，尝试文本解析
            return self._parse_text_decision(text)
            
        except Exception as e:
            print(f"[WARNING] 决策解析失败: {e}")
            return self._fallback_decision("解析失败")
    
    def _parse_text_decision(self, text: str) -> Dict:
        """从文本中提取决策（备用方案）"""
        # 简单的关键词匹配
        action = "wait"
        params = {"seconds": 2}
        
        if "打开" in text or "启动" in text:
            action = "open_wps"
            params = {}
        elif "点击" in text:
            action = "click"
            params = {"x": 500, "y": 300}
        elif "输入" in text or "写入" in text:
            action = "type_text"
            params = {"text": ""}
        elif "快捷键" in text or "ctrl" in text.lower():
            action = "hotkey"
            params = {"keys": ["ctrl", "n"]}
        
        return {
            'reasoning': text[:200],
            'action': action,
            'params': params,
            'expected_result': '未知',
            'confidence': 0.5
        }
    
    def _fallback_decision(self, reason: str) -> Dict:
        """备用决策"""
        return {
            'reasoning': f"使用备用决策: {reason}",
            'action': 'wait',
            'params': {'seconds': 2},
            'expected_result': '等待后重新观察',
            'confidence': 0.3
        }


if __name__ == "__main__":
    # 测试
    reasoning = ReasoningModule()
    
    observation = {
        'current_app': 'Desktop',
        'task_status': 'NOT_STARTED',
        'key_elements': ['桌面图标'],
        'suggestion': '需要打开WPS'
    }
    
    decision = reasoning.decide_next_action(
        task="打开WPS并创建天气文章",
        current_state="INIT",
        observation=observation,
        history=[],
        available_tools=['open_wps', 'wait', 'click']
    )
    
    print("决策结果：")
    print(json.dumps(decision, ensure_ascii=False, indent=2))
