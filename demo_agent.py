"""
视觉引导Agent Demo
使用MAI-UI-2B和qwen实现自主决策的RPA Agent

任务：打开WPS并根据今天的天气生成一篇文章保存到文档中
"""

from rpa_tools import VisionGuidedAgent
import sys


def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                  视觉引导的自主Agent Demo                        ║
║                                                                  ║
║  技术栈:                                                         ║
║    👁️  MAI-UI-2B  - 视觉感知                                    ║
║    🧠 qwen:7b    - 推理决策                                     ║
║    🎯 pyautogui  - 操作执行                                     ║
║                                                                  ║
║  架构: Perception → Reasoning → Action → Reflection             ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # 检查服务
    print("🔍 检查服务状态...")
    print("  ⚠️  请确保以下服务正在运行:")
    print("     1. MAI-UI-2B Docker: docker-compose up -d")
    print("     2. Ollama: ollama serve")
    print()
    
    input("按Enter键开始运行Agent...")
    
    # 创建Agent
    agent = VisionGuidedAgent(
        task_description="打开WPS并根据今天的天气生成一篇文章保存到文档中",
        max_iterations=20
    )
    
    # 运行
    try:
        success = agent.run()
        
        # 显示摘要
        print("\n" + "=" * 70)
        print("📊 执行摘要")
        print("=" * 70)
        
        summary = agent.get_summary()
        print(f"任务: {summary['task']}")
        print(f"迭代次数: {summary['iterations']}")
        print(f"最终状态: {summary['final_state']}")
        print(f"成功: {'✅ 是' if summary['success'] else '❌ 否'}")
        print(f"历史记录: {summary['history_count']} 条")
        
        if summary['task_data']:
            print(f"\n任务数据:")
            for key, value in summary['task_data'].items():
                if isinstance(value, str):
                    print(f"  {key}: {value[:50]}...")
                else:
                    print(f"  {key}: {value}")
        
        print("\n" + "=" * 70)
        
        if success:
            print("🎉 Agent成功完成任务！")
        else:
            print("⚠️  Agent未能完成任务，请查看日志")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        return 1
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
