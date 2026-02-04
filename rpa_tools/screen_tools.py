"""
屏幕操作工具集
基于PyAutoGUI和pydirectinput实现鼠标、键盘操作
"""
import pyautogui
import pydirectinput
import pyperclip
from time import sleep
from typing import Optional, Tuple, Dict, Any
from .base_tool import RPAToolBase, SafetyMixin


class ScreenTool(RPAToolBase, SafetyMixin):
    """屏幕操作工具"""
    
    def __init__(self):
        RPAToolBase.__init__(self)
        SafetyMixin.__init__(self)
        self.description = "屏幕鼠标键盘操作工具"
        
        # PyAutoGUI安全设置
        pyautogui.FAILSAFE = True  # 鼠标移到左上角可紧急停止
        pyautogui.PAUSE = 0.2  # 每次操作后自动暂停
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """通用执行接口（由具体方法调用）"""
        return {"status": "success", "message": "请使用具体方法"}
    
    # ========== 鼠标操作 ==========
    
    def click_at(self, x: int, y: int, clicks: int = 1, button: str = 'left') -> Dict[str, Any]:
        """
        点击指定坐标
        
        Args:
            x: X坐标
            y: Y坐标
            clicks: 点击次数（1=单击, 2=双击）
            button: 'left' | 'right' | 'middle'
        """
        try:
            pyautogui.moveTo(x, y, duration=0.5)
            self.safe_delay(0.2)
            
            for _ in range(clicks):
                pydirectinput.click(x, y, button=button)
                self.safe_delay(0.1)
            
            return {
                "status": "success",
                "action": "click",
                "position": (x, y),
                "message": f"点击坐标({x}, {y})"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def double_click_at(self, x: int, y: int) -> Dict[str, Any]:
        """双击指定坐标"""
        return self.click_at(x, y, clicks=2)
    
    def right_click_at(self, x: int, y: int) -> Dict[str, Any]:
        """右键点击"""
        return self.click_at(x, y, button='right')
    
    def drag_to(self, x1: int, y1: int, x2: int, y2: int, duration: float = 1.0) -> Dict[str, Any]:
        """
        拖拽操作
        
        Args:
            x1, y1: 起始坐标
            x2, y2: 目标坐标
            duration: 拖拽持续时间（秒）
        """
        try:
            pyautogui.moveTo(x1, y1)
            self.safe_delay(0.2)
            pyautogui.dragTo(x2, y2, duration=duration)
            
            return {
                "status": "success",
                "action": "drag",
                "from": (x1, y1),
                "to": (x2, y2),
                "message": f"拖拽从({x1},{y1})到({x2},{y2})"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> Dict[str, Any]:
        """
        滚动鼠标滚轮
        
        Args:
            clicks: 滚动量（正数向上，负数向下）
            x, y: 可选，滚动位置
        """
        try:
            if x is not None and y is not None:
                pyautogui.moveTo(x, y)
                self.safe_delay(0.1)
            
            pyautogui.scroll(clicks)
            
            return {
                "status": "success",
                "action": "scroll",
                "clicks": clicks,
                "message": f"滚动{clicks}次"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== 键盘操作 ==========
    
    def type_text(self, text: str, interval: float = 0.1) -> Dict[str, Any]:
        """
        输入文本（使用剪贴板，支持中文）
        
        Args:
            text: 要输入的文本
            interval: 字符间隔（秒）
        """
        try:
            # 使用剪贴板方式输入（支持中文）
            pyperclip.copy(text)
            self.safe_delay(0.1)
            pyautogui.hotkey('ctrl', 'v')
            self.safe_delay(0.2)
            
            return {
                "status": "success",
                "action": "type",
                "text": text,
                "message": f"输入文本: {text[:50]}..."
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def press_key(self, key: str, presses: int = 1) -> Dict[str, Any]:
        """
        按键操作
        
        Args:
            key: 键名（如 'enter', 'backspace', 'esc'等）
            presses: 按键次数
        """
        try:
            for _ in range(presses):
                pyautogui.press(key)
                self.safe_delay(0.1)
            
            return {
                "status": "success",
                "action": "press",
                "key": key,
                "message": f"按键: {key} x{presses}"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def hotkey(self, *keys) -> Dict[str, Any]:
        """
        组合键操作
        
        Args:
            *keys: 按键序列，如 ('ctrl', 'c')
        """
        try:
            pyautogui.hotkey(*keys)
            self.safe_delay(0.2)
            
            return {
                "status": "success",
                "action": "hotkey",
                "keys": keys,
                "message": f"组合键: {'+'.join(keys)}"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== 截图操作 ==========
    
    def screenshot(self, region: Optional[Tuple[int, int, int, int]] = None, 
                   save_path: Optional[str] = None) -> Dict[str, Any]:
        """
        截屏
        
        Args:
            region: 可选，截图区域 (x, y, width, height)
            save_path: 可选，保存路径
        
        Returns:
            包含PIL Image对象或文件路径
        """
        try:
            img = pyautogui.screenshot(region=region)
            
            result = {
                "status": "success",
                "action": "screenshot",
                "image": img,
                "message": "截图成功"
            }
            
            if save_path:
                img.save(save_path)
                result["path"] = save_path
                result["message"] = f"截图已保存: {save_path}"
            
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_mouse_position(self) -> Dict[str, Any]:
        """获取当前鼠标位置"""
        try:
            x, y = pyautogui.position()
            return {
                "status": "success",
                "position": (x, y),
                "message": f"鼠标位置: ({x}, {y})"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== 剪贴板操作 ==========
    
    def copy_to_clipboard(self, text: str) -> Dict[str, Any]:
        """复制文本到剪贴板"""
        try:
            pyperclip.copy(text)
            return {
                "status": "success",
                "action": "copy",
                "text": text,
                "message": "已复制到剪贴板"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def paste_from_clipboard(self) -> Dict[str, Any]:
        """从剪贴板粘贴"""
        try:
            text = pyperclip.paste()
            return {
                "status": "success",
                "action": "paste",
                "text": text,
                "message": f"剪贴板内容: {text[:100]}..."
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_clipboard_text(self) -> str:
        """获取剪贴板文本"""
        return pyperclip.paste()
