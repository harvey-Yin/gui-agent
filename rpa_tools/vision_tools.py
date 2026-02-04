"""
视觉识别工具集
基于OpenCV和PyAutoGUI实现图像识别和定位
"""
import cv2
import numpy as np
import pyautogui
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path
import time
from .base_tool import RPAToolBase


class VisionTool(RPAToolBase):
    """视觉识别工具"""
    
    def __init__(self, image_dir: str = "picture"):
        super().__init__()
        self.description = "图像识别和元素定位工具"
        self.image_dir = Path(image_dir)
        self.confidence = 0.8
        self.grayscale = True
        
        # 多尺度搜索配置
        self.scales = [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7]
        self.scale_cache = {}  # 缓存最佳缩放比例
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """通用执行接口"""
        return {"status": "success", "message": "请使用具体方法"}
    
    # ========== 图像定位（PyAutoGUI方式） ==========
    
    def find_image(self, template_name: str, confidence: Optional[float] = None,
                   region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
        """
        在屏幕上查找图像（单尺度精确匹配）
        
        Args:
            template_name: 模板图片文件名
            confidence: 匹配置信度（0-1），默认使用self.confidence
            region: 搜索区域 (x, y, width, height)
        
        Returns:
            包含位置信息的字典
        """
        try:
            template_path = self.image_dir / template_name
            if not template_path.exists():
                return {
                    "status": "error",
                    "message": f"模板图片不存在: {template_path}"
                }
            
            conf = confidence if confidence is not None else self.confidence
            location = pyautogui.locateOnScreen(
                str(template_path),
                confidence=conf,
                region=region
            )
            
            if location:
                center = pyautogui.center(location)
                return {
                    "status": "success",
                    "found": True,
                    "position": (center.x, center.y),
                    "box": location,
                    "message": f"找到图像 {template_name} at ({center.x}, {center.y})"
                }
            else:
                return {
                    "status": "success",
                    "found": False,
                    "message": f"未找到图像: {template_name}"
                }
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def find_all_images(self, template_name: str, confidence: Optional[float] = None) -> Dict[str, Any]:
        """
        查找屏幕上所有匹配的图像
        
        Returns:
            包含所有匹配位置的列表
        """
        try:
            template_path = self.image_dir / template_name
            if not template_path.exists():
                return {
                    "status": "error",
                    "message": f"模板图片不存在: {template_path}"
                }
            
            conf = confidence if confidence is not None else self.confidence
            locations = list(pyautogui.locateAllOnScreen(
                str(template_path),
                confidence=conf
            ))
            
            centers = [pyautogui.center(loc) for loc in locations]
            positions = [(c.x, c.y) for c in centers]
            
            return {
                "status": "success",
                "found": len(positions) > 0,
                "count": len(positions),
                "positions": positions,
                "message": f"找到 {len(positions)} 个匹配项"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== 多尺度匹配（OpenCV方式） ==========
    
    def find_image_multiscale(self, template_name: str, 
                             confidence: Optional[float] = None) -> Dict[str, Any]:
        """
        多尺度图像匹配（适应不同DPI和缩放）
        
        基于您现有项目中的实现
        """
        try:
            template_path = self.image_dir / template_name
            if not template_path.exists():
                return {
                    "status": "error",
                    "message": f"模板图片不存在: {template_path}"
                }
            
            # 读取模板
            template = cv2.imread(str(template_path), 
                                cv2.IMREAD_GRAYSCALE if self.grayscale else cv2.IMREAD_COLOR)
            if template is None:
                return {"status": "error", "message": "无法读取模板图片"}
            
            h, w = template.shape[:2]
            
            # 截取屏幕
            screenshot = pyautogui.screenshot()
            screen = cv2.cvtColor(np.array(screenshot), 
                                cv2.COLOR_RGB2GRAY if self.grayscale else cv2.COLOR_RGB2BGR)
            
            conf = confidence if confidence is not None else self.confidence
            
            # 优先使用缓存的最佳缩放比例
            scales_to_try = self.scales.copy()
            if template_name in self.scale_cache:
                best_scale = self.scale_cache[template_name]
                scales_to_try = [best_scale] + [s for s in scales_to_try if s != best_scale]
            
            # 多尺度搜索
            for scale in scales_to_try:
                # 检查缩放后尺寸是否合理
                if screen.shape[0] * scale < h or screen.shape[1] * scale < w:
                    continue
                
                # 缩放屏幕
                resized_screen = cv2.resize(screen, None, fx=scale, fy=scale, 
                                          interpolation=cv2.INTER_AREA)
                
                # 模板匹配
                result = cv2.matchTemplate(resized_screen, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val >= conf:
                    # 计算中心点坐标（还原到原始尺寸）
                    x = int((max_loc[0] + w / 2) / scale)
                    y = int((max_loc[1] + h / 2) / scale)
                    
                    # 缓存最佳缩放比例
                    self.scale_cache[template_name] = scale
                    
                    return {
                        "status": "success",
                        "found": True,
                        "position": (x, y),
                        "confidence": float(max_val),
                        "scale": scale,
                        "message": f"找到图像 {template_name} at ({x}, {y}), 置信度: {max_val:.2f}"
                    }
            
            return {
                "status": "success",
                "found": False,
                "message": f"未找到图像: {template_name}"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== 等待元素出现 ==========
    
    def wait_for_element(self, template_name: str, timeout: float = 10.0,
                        interval: float = 0.5, use_multiscale: bool = False) -> Dict[str, Any]:
        """
        等待图像元素出现
        
        Args:
            template_name: 模板图片文件名
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
            use_multiscale: 是否使用多尺度匹配
        """
        start_time = time.time()
        
        while True:
            # 选择匹配方法
            if use_multiscale:
                result = self.find_image_multiscale(template_name)
            else:
                result = self.find_image(template_name)
            
            if result.get("found"):
                result["message"] = f"元素出现: {template_name}"
                return result
            
            # 检查超时
            if time.time() - start_time > timeout:
                return {
                    "status": "error",
                    "found": False,
                    "message": f"等待超时({timeout}s): {template_name}"
                }
            
            time.sleep(interval)
    
    # ========== 点击图像 ==========
    
    def click_image(self, template_name: str, clicks: int = 1, 
                   timeout: float = 10.0, use_multiscale: bool = True) -> Dict[str, Any]:
        """
        查找并点击图像
        
        Args:
            template_name: 模板图片文件名
            clicks: 点击次数
            timeout: 查找超时时间
            use_multiscale: 是否使用多尺度匹配
        """
        # 等待元素出现
        result = self.wait_for_element(template_name, timeout, use_multiscale=use_multiscale)
        
        if not result.get("found"):
            return result
        
        # 点击
        try:
            x, y = result["position"]
            import pydirectinput
            for _ in range(clicks):
                pydirectinput.click(x, y)
                time.sleep(0.1)
            
            return {
                "status": "success",
                "action": "click_image",
                "template": template_name,
                "position": (x, y),
                "message": f"点击图像 {template_name} at ({x}, {y})"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== 相对定位点击 ==========
    
    def click_relative(self, anchor_template: str, offset_x: int, offset_y: int,
                      timeout: float = 10.0) -> Dict[str, Any]:
        """
        基于锚点图像的相对位置点击
        
        Args:
            anchor_template: 锚点模板图片
            offset_x: X轴偏移（像素）
            offset_y: Y轴偏移（像素）
            timeout: 查找超时
        """
        # 查找锚点
        result = self.wait_for_element(anchor_template, timeout, use_multiscale=True)
        
        if not result.get("found"):
            return result
        
        # 计算目标位置
        try:
            anchor_x, anchor_y = result["position"]
            target_x = anchor_x + offset_x
            target_y = anchor_y + offset_y
            
            import pydirectinput
            pydirectinput.click(target_x, target_y)
            time.sleep(0.2)
            
            return {
                "status": "success",
                "action": "click_relative",
                "anchor": anchor_template,
                "anchor_position": (anchor_x, anchor_y),
                "target_position": (target_x, target_y),
                "offset": (offset_x, offset_y),
                "message": f"相对点击: 锚点({anchor_x},{anchor_y}) + 偏移({offset_x},{offset_y}) = ({target_x},{target_y})"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
