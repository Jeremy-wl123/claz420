"""
Pydantic 数据模型
---------------
定义 API 的请求和响应数据结构。
"""
from typing import Any, List
from pydantic import BaseModel


class QueryRequest(BaseModel):
    """自然语言查询请求"""
    question: str


class QueryResponse(BaseModel):
    """查询结果响应"""
    sql: str
    explanation: str
    columns: List[str]
    rows: List[List[Any]]
    truncated: bool
    row_count: int


class ErrorResponse(BaseModel):
    """错误响应"""
    detail: str
