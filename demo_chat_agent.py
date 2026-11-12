# -*- coding: utf-8 -*-
"""
交互式Agent Demo - 对话式RPA助手
可以和AI聊天，让AI帮你完成电脑操作任务
"""

from rpa_tools.conversational_agent import ConversationalAgent
from typing import Dict
import sys
import io

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def print_separator():
    print("\n" + "─" * 70 + "\n")


def print_agent_message(content: str, action_info: Dict = None):
    """打印Agent消息"""
    print(f"🤖 Agent: {content}")
    
    if action_info:
        print(f"\n   💭 思考: {action_info.get('thought', '')}")
        print(f"   🎯 操作: {action_info.get('tool')} {action_info.get('params', {})}")


def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    交互式RPA Agent                               ║
║                                                                  ║
║  你可以：                                                        ║
║    💬 和AI聊天                                                  ║
║    📋 布置任务让AI执行                                          ║
║    👁️  让AI查看屏幕（MAI-UI-2B）                               ║
║    🎯 让AI操作电脑                                              ║
║                                                                  ║
║  示例指令：                                                      ║
║    - "帮我打开WPS"                                              ║
║    - "查看一下当前屏幕有什么"                                    ║
║    - "帮我获取北京的天气"                                        ║
║    - "根据天气生成一篇文章并保存到WPS"                           ║
║                                                                  ║
║  输入 'quit' 或 'exit' 退出                                     ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # 检查服务
    print("🔍 请确保以下服务正在运行:")
    print("   1. MAI-UI-2B Docker: docker-compose up -d")
    print("   2. Ollama: ollama serve")
    print()
    
    # 创建Agent
    agent = ConversationalAgent()
    
    print("✅ Agent已就绪！开始对话吧！")
    print_separator()
    
    # 主循环
    while True:
        try:
            # 获取用户输入
            user_input = input("👤 你: ").strip()
            
            if not user_input:
                continue
            
            # 退出命令
            if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                print("\n👋 再见！")
                break
            
            print()  # 空行
            
            # 发送给Agent
            response = agent.chat(user_input)
            
            if response['type'] == 'text':
                # 纯文本回复
                print(f"🤖 Agent: {response['content']}")
            
            elif response['type'] == 'action':
                # 需要执行操作
                action_info = response['action']
                print_agent_message(response['content'], action_info)
                
                # 询问用户是否执行
                confirm = input("\n   ❓ 是否执行此操作？(y/n): ").strip().lower()
                
                if confirm in ['y', 'yes', '是', '']:
                    print("\n   ⏳ 执行中...")
                    
                    # 执行操作
                    result = agent.execute_action(action_info)
                    
                    if result['success']:
                        print(f"   ✅ {result['result']}")
                        
                        # 如果有返回数据，保存并显示
                        if result.get('data'):
                            # 保存到任务上下文
                            tool = action_info.get('tool')
                            if tool == 'get_weather':
                                agent.save_task_data('weather', result['data'])
                                print(f"   📊 天气数据已保存")
                            elif tool == 'generate_article':
                                agent.save_task_data('article', result['data'])
                                print(f"   📝 文章已生成 ({len(result['data'])} 字)")
                            elif tool == 'look_screen':
                                vision_data = result['data']
                                print(f"\n   👁️  视觉分析:")
                                print(f"      应用: {vision_data.get('current_app')}")
                                print(f"      状态: {vision_data.get('task_status')}")
                                print(f"      建议: {vision_data.get('suggestion', '')[:60]}...")
                    else:
                        print(f"   ❌ {result['result']}")
                else:
                    print("   ⏭️  已跳过")
            
            print_separator()
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            print_separator()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
