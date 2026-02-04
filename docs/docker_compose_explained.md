# Docker Compose配置详解

这个文件定义了如何启动vLLM服务来运行MAI-UI-8B模型。逐行解释如下：

```yaml
version: '3.8'  # Docker Compose文件格式版本，3.8支持GPU配置

services:       # 定义要启动的服务列表
  vllm-mai-ui:  # 服务名称，可以是任意名字
    # 镜像来源：官方vLLM镜像，支持OpenAI兼容API
    image: vllm/vllm-openai:latest
    
    # 容器名称：启动后在Docker Desktop中看到的名字
    container_name: mai-ui-8b-agent
    
    # 端口映射：宿主机端口:容器内端口
    # 我们访问localhost:8001，流量会被转发到容器的8000端口
    ports:
      - "8001:8000"
    
    # 环境变量配置
    environment:
      # 关键！设置HuggingFace国内镜像，解决下载慢/失败问题
      - HF_ENDPOINT=https://hf-mirror.com
      # 指定使用第1块GPU（如果你有多卡，可以改为0,1等）
      - CUDA_VISIBLE_DEVICES=0
    
    # 卷挂载：数据持久化
    volumes:
      # 将Windows用户的HuggingFace缓存目录映射到容器内
      # ${USERPROFILE}在Windows下自动替换为 C:\Users\你的用户名
      # 作用：下载一次模型后，下次启动直接用，不用重新下载
      - ${USERPROFILE}/.cache/huggingface:/root/.cache/huggingface
    
    # 启动命令：vLLM服务的参数配置
    command: >
      # 指定使用的模型ID（会自动从HuggingFace下载）
      --model Tongyi-MAI/MAI-UI-8B
      
      # API中显示的模型名称
      --served-model-name MAI-UI-8B
      
      # 监听地址：0.0.0.0表示允许外部访问（不仅仅是localhost）
      --host 0.0.0.0
      --port 8000
      
      # 允许执行远程代码（MAI-UI模型必需）
      --trust-remote-code
      
      # 使用半精度浮点数（节省显存，fp16）
      --dtype float16
      
      # [关键优化] 显存利用率限制
      # 0.85表示只使用85%的显存，留15%给系统，防止OOM崩溃
      --gpu-memory-utilization 0.85
      
      # [关键优化] 上下文长度限制
      # 限制为1024 tokens（原为4096+），大幅减少KV Cache显存占用
      --max-model-len 1024
      
      # [关键优化] 强制Eager模式
      # 禁用CUDA Graph加速，虽然慢一点点，但能显著节省显存
      --enforce-eager
    
    # 部署配置：GPU支持的关键部分
    deploy:
      resources:
        reservations:
          devices:
            # 声明使用NVIDIA显卡
            - driver: nvidia
              count: 1          # 使用1个GPU
              capabilities: [gpu]
    
    # 重启策略：除非手动停止，否则挂了自动重启
    restart: unless-stopped
    
    # 健康检查：每30秒检查一次API是否存活
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/v1/models"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 核心配置总结

对于你的 **12GB显存**，最重要的三行是：

1. `gpu-memory-utilization 0.85`: 留出空间给Windows桌面和其他进程。
2. `max-model-len 1024`: 牺牲处理长文的能力，换取显存不爆炸。
3. `enforce-eager`: 牺牲一点速度，换取更稳定的启动。
