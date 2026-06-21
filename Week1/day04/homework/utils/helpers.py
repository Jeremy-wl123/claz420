"""
工具函数模块
----------
提供通用的辅助函数。
"""
import json
import re
import socket
from typing import Any


def get_local_ip() -> str:
    """尝试获取本机局域网 IP 地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "无法获取（请检查网络）"


def parse_json_content(content: str) -> dict[str, Any]:
    """
    兼容纯 JSON 和被 Markdown 代码块包裹的 JSON。

    处理两种格式：
    - 纯 JSON: `{"key": "value"}`
    - Markdown 包裹: ```json\n{"key": "value"}\n```
    """
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("模型返回内容不是 JSON 对象")
    return data
