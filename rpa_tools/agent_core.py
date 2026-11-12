"""
Agent核心 - 主循环控制
"""

import time
from typing import List, Dict
from .vision_module import VisionModule
from .reasoning_module import ReasoningModule
from .action_module import ActionModule


class VisionGuidedAgent:
    """视觉引导的自主Agent"""
    
    def __init__(self, task_description: str, max_iterations: int = 20):
        """
        初始化Agent
        
        Args:
            task_description: 任务描述
            max_iterations: 最大迭代次数（防止无限循环）
        """
        self.task = task_description
        self.max_iterations = max_iterations
        
        # 初始化模块
        self.vision = VisionModule()
        self.reasoning = ReasoningModule()
        self.action = ActionModule()
        
        # 状态管理
        self.state = "INIT"
        self.history = []
        self.iteration = 0
        self.task_data = {}  # 存储任务相关数据（如天气、文章等）
        
        # 可用工具
        self.available_tools = [
            'open_wps',
            'click',
            'type_text',
            'paste_text',
            'hotkey',
            'wait',
            'get_weather',
            'generate_article',
            'complete_task'
        ]
    
    def run(self) -> bool:
        """
        运行Agent主循环
        
        Returns:
            True if task completed successfully, False otherwise
        """
        print("=" * 70)
        print(f"🤖 Agent启动")
        print(f"📋 任务: {self.task}")
        print("=" * 70)
        
        while self.iteration < self.max_iterations:
            self.iteration += 1
            
            print(f"\n{'='*70}")
            print(f"🔄 迭代 {self.iteration}/{self.max_iterations}")
            print(f"{'='*70}")
            
            # 1. 感知 (Perception)
            observation = self.perceive()
            
            # 检查是否完成
            if self.is_task_complete(observation):
                print("\n✅ 任务完成！")
                return True
            
            # 2. 推理 (Reasoning)
            decision = self.reason(observation)
            
            # 3. 行动 (Action)
            result = self.act(decision)
            
            # 4. 反思 (Reflection)
            self.reflect(decision, result)
            
            # 短暂暂停
            time.sleep(1)
        
        print(f"\n⚠️ 达到最大迭代次数 ({self.max_iterations})，任务可能未完成")
        return False
    
    def perceive(self) -> Dict:
        """感知阶段 - 观察当前状态"""
        print("\n👁️  [感知] 分析当前屏幕...")
        
        observation = self.vision.analyze_screen(
            task_description=self.task,
            current_state=self.state
        )
        
        print(f"  当前应用: {observation['current_app']}")
        print(f"  任务状态: {observation['task_status']}")
        print(f"  AI建议: {observation['suggestion'][:50]}...")
        
        return observation
    
    def reason(self, observation: Dict) -> Dict:
        """推理阶段 - 决定下一步行动"""
        print("\n🧠 [推理] 决策下一步行动...")
        
        decision = self.reasoning.decide_next_action(
            task=self.task,
            current_state=self.state,
            observation=observation,
            history=self.history[-5:],  # 只传递最近5条历史
            available_tools=self.available_tools
        )
        
        print(f"  推理: {decision['reasoning'][:80]}...")
        print(f"  行动: {decision['action']}")
        print(f"  参数: {decision['params']}")
        print(f"  信心: {decision.get('confidence', 0.5):.2f}")
        
        return decision
    
    def act(self, decision: Dict) -> Dict:
        """行动阶段 - 执行决策"""
        print("\n🎯 [行动] 执行操作...")
        
        action = decision['action']
        params = decision['params']
        
        result = self.action.execute(action, params)
        
        # 特殊处理：保存数据
        if result['success'] and result['data']:
            if action == 'get_weather':
                self.task_data['weather'] = result['data']
            elif action == 'generate_article':
                self.task_data['article'] = result['data']
        
        status = "✅" if result['success'] else "❌"
        print(f"  {status} {result['result']}")
        
        return result
    
    def reflect(self, decision: Dict, result: Dict):
        """反思阶段 - 记录并更新状态"""
        print("\n💭 [反思] 更新状态...")
        
        # 记录历史
        self.history.append({
            'iteration': self.iteration,
            'state': self.state,
            'action': decision['action'],
            'params': decision['params'],
            'result': result['result'],
            'success': result['success']
        })
        
        # 更新状态
        if result['success']:
            # 根据行动更新状态
            if decision['action'] == 'open_wps':
                self.state = "WPS_OPENED"
            elif decision['action'] == 'get_weather':
                self.state = "WEATHER_OBTAINED"
            elif decision['action'] == 'generate_article':
                self.state = "ARTICLE_GENERATED"
            elif decision['action'] == 'paste_text' and 'article' in str(decision['params']):
                self.state = "CONTENT_WRITTEN"
            elif decision['action'] == 'complete_task':
                self.state = "COMPLETED"
        
        print(f"  状态: {self.state}")
        print(f"  历史记录: {len(self.history)} 条")
    
    def is_task_complete(self, observation: Dict) -> bool:
        """判断任务是否完成"""
        # 方式1: 状态判断
        if self.state == "COMPLETED":
            return True
        
        # 方式2: 视觉判断
        if observation.get('task_status') == 'COMPLETED':
            return True
        
        # 方式3: 历史记录判断
        if self.history and self.history[-1]['action'] == 'complete_task':
            return True
        
        return False
    
    def get_summary(self) -> Dict:
        """获取执行摘要"""
        return {
            'task': self.task,
            'iterations': self.iteration,
            'final_state': self.state,
            'success': self.state == "COMPLETED",
            'history_count': len(self.history),
            'task_data': self.task_data
        }


if __name__ == "__main__":
    # 测试
    agent = VisionGuidedAgent(
        task_description="打开WPS并根据今天的天气生成一篇文章保存到文档中"
    )
    
    success = agent.run()
    
    print("\n" + "=" * 70)
    print("📊 执行摘要")
    print("=" * 70)
    summary = agent.get_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
