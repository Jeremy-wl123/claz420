"""
健康检查控制器
------------
处理 /health 端点的请求。
"""


async def health_check() -> dict:
    """返回服务健康状态"""
    return {"status": "ok"}
