"""
Ollama + LangChain 集成测试
验证环境配置是否正确
"""

import ollama
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def test_ollama_direct():
    """测试直接调用Ollama"""
    print("=" * 50)
    print("测试1: 直接调用Ollama API")
    print("=" * 50)
    
    try:
        response = ollama.chat(
            model='qwen:7b',
            messages=[
                {
                    'role': 'user',
                    'content': '你好，请用一句话介绍你自己。'
                }
            ]
        )
        print(f"[OK] Ollama响应: {response['message']['content']}")
        return True
    except Exception as e:
        print(f"[FAIL] Ollama调用失败: {e}")
        return False

def test_langchain_integration():
    """测试LangChain集成"""
    print("\n" + "=" * 50)
    print("测试2: LangChain + Ollama集成")
    print("=" * 50)
    
    try:
        # 创建LangChain的Ollama LLM
        llm = Ollama(
            model="qwen:7b",
            base_url="http://localhost:11434"
        )
        
        # 创建简单的Prompt模板
        prompt = PromptTemplate(
            input_variables=["task"],
            template="你是一个RPA自动化助手。用户的任务是: {task}\n请简要说明你会如何执行这个任务。"
        )
        
        # 创建Chain
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # 测试调用
        result = chain.run(task="帮我打开记事本")
        print(f"[OK] LangChain响应:\n{result}")
        return True
    except Exception as e:
        print(f"[FAIL] LangChain集成失败: {e}")
        return False

def test_rpa_dependencies():
    """测试RPA依赖"""
    print("\n" + "=" * 50)
    print("测试3: RPA工具依赖检查")
    print("=" * 50)
    
    try:
        import pyautogui
        import cv2
        import PIL
        
        # 获取屏幕尺寸
        screen_size = pyautogui.size()
        print(f"[OK] PyAutoGUI可用 - 屏幕尺寸: {screen_size}")
        
        # 检查OpenCV版本
        print(f"[OK] OpenCV可用 - 版本: {cv2.__version__}")
        
        # 检查PIL
        print(f"[OK] Pillow可用 - 版本: {PIL.__version__}")
        
        return True
    except Exception as e:
        print(f"[FAIL] RPA依赖检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("\n" + "="*50)
    print("开始环境测试...")
    print("="*50 + "\n")
    
    results = []
    
    # 运行所有测试
    results.append(("Ollama直接调用", test_ollama_direct()))
    results.append(("LangChain集成", test_langchain_integration()))
    results.append(("RPA工具依赖", test_rpa_dependencies()))
    
    # 输出总结
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    for name, passed in results:
        status = "[OK] 通过" if passed else "[FAIL] 失败"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n[SUCCESS] 所有测试通过！环境配置成功！")
        print("\n下一步：可以开始开发Agent核心代码")
    else:
        print("\n[WARNING] 部分测试失败，请检查配置")

if __name__ == "__main__":
    main()
