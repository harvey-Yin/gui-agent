"""
RPA工具基类
提供所有RPA工具的通用接口和功能
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging
import time
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)


class RPAToolBase(ABC):
    """RPA工具抽象基类"""
    
    def __init__(self):
        self.name: str = self.__class__.__name__
        self.description: str = ""
        self.logger = logging.getLogger(self.name)
        self.execution_history = []
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行工具的核心逻辑
        
        Returns:
            Dict包含:
                - status: "success" | "error"
                - result: 执行结果
                - message: 描述信息
        """
        pass
    
    def pre_check(self) -> bool:
        """执行前的安全检查"""
        return True
    
    def post_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """执行后的结果处理"""
        return result
    
    def log_execution(self, params: dict, result: dict):
        """记录执行日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool": self.name,
            "params": params,
            "result": result
        }
        self.execution_history.append(log_entry)
        self.logger.info(f"执行 {self.name}: {result.get('message', '')}")
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        完整的执行流程（包含前置检查、执行、后处理、日志）
        """
        try:
            # 前置检查
            if not self.pre_check():
                return {
                    "status": "error",
                    "message": "前置检查失败"
                }
            
            # 执行核心逻辑
            result = self.execute(**kwargs)
            
            # 后处理
            result = self.post_process(result)
            
            # 记录日志
            self.log_execution(kwargs, result)
            
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "message": f"执行失败: {str(e)}"
            }
            self.logger.error(f"{self.name} 执行异常: {e}", exc_info=True)
            return error_result


class SafetyMixin:
    """安全机制混入类"""
    
    def __init__(self):
        self.safe_mode = True
        self.operation_delay = 0.5  # 操作间延迟（秒）
    
    def safe_delay(self, seconds: Optional[float] = None):
        """安全延迟"""
        delay = seconds if seconds is not None else self.operation_delay
        time.sleep(delay)
    
    def confirm_dangerous_operation(self, operation: str) -> bool:
        """危险操作确认（在实际使用中可以接入用户确认）"""
        if not self.safe_mode:
            return True
        # 这里可以扩展为实际的用户确认机制
        logging.warning(f"危险操作: {operation}")
        return True
