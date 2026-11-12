"""
本地Qwen3-8B-FP8服务 - 替代Ollama
使用transformers直接加载模型，提供OpenAI兼容API
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify
import torch
import json

app = Flask(__name__)

# 全局变量
model = None
tokenizer = None
MODEL_NAME = "Qwen/Qwen3-8B-FP8"

def load_model():
    """加载模型"""
    global model, tokenizer
    
    print(f"正在加载模型: {MODEL_NAME}")
    print("这可能需要几分钟...")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        device_map="auto"
    )
    
    print("✅ 模型加载完成！")

@app.route('/api/generate', methods=['POST'])
def generate():
    """Ollama兼容的生成接口"""
    data = request.json
    
    prompt = data.get('prompt', '')
    stream = data.get('stream', False)
    temperature = data.get('temperature', 0.7)
    
    # 准备输入
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False  # 非思考模式，更快
    )
    
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    # 生成
    with torch.no_grad():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=2048,
            temperature=temperature,
            do_sample=True
        )
    
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    response_text = tokenizer.decode(output_ids, skip_special_tokens=True)
    
    if stream:
        # 简化的流式响应
        return jsonify({
            "response": response_text,
            "done": True
        })
    else:
        return jsonify({
            "response": response_text,
            "model": MODEL_NAME,
            "done": True
        })

@app.route('/api/tags', methods=['GET'])
def tags():
    """列出模型"""
    return jsonify({
        "models": [{
            "name": MODEL_NAME,
            "size": "8.2B"
        }]
    })

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("=" * 70)
    print("Qwen3-8B-FP8 本地服务")
    print("=" * 70)
    
    # 加载模型
    load_model()
    
    print("\n" + "=" * 70)
    print("🚀 服务启动")
    print("=" * 70)
    print("API地址: http://localhost:11434")
    print("兼容Ollama API格式")
    print("\n按Ctrl+C停止服务")
    print("=" * 70)
    
    # 启动Flask服务
    app.run(host='0.0.0.0', port=11434, debug=False)
