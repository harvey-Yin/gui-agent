"""
数据处理工具
提供通用的数据解析、转换和处理功能
"""
import re
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .base_tool import RPAToolBase


class DataTool(RPAToolBase):
    """数据处理工具"""
    
    def __init__(self):
        super().__init__()
        self.description = "数据解析、转换和处理工具"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """通用执行接口"""
        return {"status": "success", "message": "请使用具体方法"}
    
    # ========== 文本解析 ==========
    
    def extract_by_regex(self, text: str, pattern: str, 
                        group: int = 0, all_matches: bool = False) -> Dict[str, Any]:
        """
        使用正则表达式提取文本
        
        Args:
            text: 源文本
            pattern: 正则表达式
            group: 捕获组索引（0=整个匹配）
            all_matches: 是否返回所有匹配
        """
        try:
            if all_matches:
                matches = re.findall(pattern, text)
                return {
                    "status": "success",
                    "matches": matches,
                    "count": len(matches),
                    "message": f"找到 {len(matches)} 个匹配"
                }
            else:
                match = re.search(pattern, text)
                if match:
                    result = match.group(group) if group <= match.lastindex else match.group(0)
                    return {
                        "status": "success",
                        "match": result,
                        "message": f"提取成功: {result}"
                    }
                else:
                    return {
                        "status": "success",
                        "match": None,
                        "message": "未找到匹配"
                    }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def parse_structured_text(self, text: str, patterns: Dict[str, str]) -> Dict[str, Any]:
        """
        解析结构化文本（基于多个正则表达式）
        
        Args:
            text: 源文本
            patterns: 字段名到正则表达式的映射
        """
        try:
            results = {}
            for field, pattern in patterns.items():
                match = re.search(pattern, text, re.S)
                if match:
                    if match.lastindex and match.lastindex >= 1:
                        results[field] = match.group(1).strip()
                    else:
                        results[field] = match.group(0).strip()
                else:
                    results[field] = None
            
            return {
                "status": "success",
                "data": results,
                "message": f"解析完成: {len(results)} 个字段"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== 日期时间处理 ==========
    
    def parse_date(self, date_str: str, format: str = "%Y-%m-%d") -> Dict[str, Any]:
        """
        解析日期字符串
        
        Args:
            date_str: 日期字符串
            format: 日期格式
        """
        try:
            date_obj = datetime.strptime(date_str, format)
            return {
                "status": "success",
                "date": date_obj,
                "iso": date_obj.isoformat(),
                "message": f"解析日期: {date_str}"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def calculate_date_offset(self, base_date: str, offset_days: int,
                             date_format: str = "%Y-%m-%d") -> Dict[str, Any]:
        """
        计算日期偏移
        
        Args:
            base_date: 基准日期字符串
            offset_days: 偏移天数（正数=未来，负数=过去）
            date_format: 日期格式
        """
        try:
            base = datetime.strptime(base_date, date_format)
            result_date = base + timedelta(days=offset_days)
            
            return {
                "status": "success",
                "base_date": base_date,
                "offset_days": offset_days,
                "result_date": result_date.strftime(date_format),
                "message": f"{base_date} + {offset_days}天 = {result_date.strftime(date_format)}"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== 数据转换 ==========
    
    def convert_to_json(self, data: Any) -> Dict[str, Any]:
        """转换为JSON字符串"""
        try:
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            return {
                "status": "success",
                "json": json_str,
                "message": "转换为JSON成功"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def parse_json(self, json_str: str) -> Dict[str, Any]:
        """解析JSON字符串"""
        try:
            data = json.loads(json_str)
            return {
                "status": "success",
                "data": data,
                "message": "解析JSON成功"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== 文本处理 ==========
    
    def clean_text(self, text: str, remove_chars: str = "；,，:. \n") -> Dict[str, Any]:
        """
        清理文本
        
        Args:
            text: 源文本
            remove_chars: 要移除的字符
        """
        try:
            cleaned = text.strip(remove_chars)
            return {
                "status": "success",
                "original": text,
                "cleaned": cleaned,
                "message": "文本清理完成"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def split_text(self, text: str, delimiter: str = "\n",
                  remove_empty: bool = True) -> Dict[str, Any]:
        """
        分割文本
        
        Args:
            text: 源文本
            delimiter: 分隔符
            remove_empty: 是否移除空行
        """
        try:
            lines = text.split(delimiter)
            if remove_empty:
                lines = [line.strip() for line in lines if line.strip()]
            
            return {
                "status": "success",
                "lines": lines,
                "count": len(lines),
                "message": f"分割完成: {len(lines)} 行"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def replace_text(self, text: str, old: str, new: str,
                    count: int = -1) -> Dict[str, Any]:
        """
        替换文本
        
        Args:
            text: 源文本
            old: 要替换的文本
            new: 新文本
            count: 替换次数（-1=全部）
        """
        try:
            result = text.replace(old, new, count)
            actual_count = text.count(old) if count == -1 else min(count, text.count(old))
            
            return {
                "status": "success",
                "original": text,
                "result": result,
                "replacements": actual_count,
                "message": f"替换完成: {actual_count} 处"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== 数据验证 ==========
    
    def validate_phone(self, phone: str) -> Dict[str, Any]:
        """验证手机号码（中国）"""
        try:
            pattern = r'^1[3-9]\d{9}$'
            is_valid = bool(re.match(pattern, phone))
            
            return {
                "status": "success",
                "phone": phone,
                "valid": is_valid,
                "message": "有效手机号" if is_valid else "无效手机号"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """验证电子邮件地址"""
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            is_valid = bool(re.match(pattern, email))
            
            return {
                "status": "success",
                "email": email,
                "valid": is_valid,
                "message": "有效邮箱" if is_valid else "无效邮箱"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
