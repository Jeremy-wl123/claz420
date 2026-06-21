"""
查询控制器
---------
处理 /query 端点的请求：自然语言 → SQL → 执行 → 返回结果。
"""
import logging

from fastapi import HTTPException, status

from model.schemas import QueryRequest, QueryResponse
from model.database import get_schema, execute_read_only_query
from service.ai_service import create_client, generate_sql
from service.validator import validate_sql

logger = logging.getLogger(__name__)


async def handle_query(request: QueryRequest) -> QueryResponse:
    """
    接收自然语言问题，生成并执行 SQL，返回查询结果。

    处理流程：
        1. 获取数据库 Schema
        2. 创建 AI 客户端
        3. 调用模型生成 SQL
        4. 校验 SQL 安全性
        5. 执行只读查询
        6. 构造并返回响应
    """
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="问题内容不能为空"
        )

    try:
        # Step 1: 获取数据库 Schema
        schema = get_schema()

        # Step 2: 创建 AI 客户端
        client = create_client()

        # Step 3: 生成 SQL
        generated = generate_sql(client, question, schema)

        # Step 4: 校验 SQL
        safe_sql = validate_sql(generated["sql"])

        # Step 5: 执行查询
        columns, rows, truncated = execute_read_only_query(safe_sql)

        # Step 6: 构造响应（tuple → list 便于 JSON 序列化）
        rows_serializable = [list(row) for row in rows]

        return QueryResponse(
            sql=safe_sql,
            explanation=generated["explanation"],
            columns=columns,
            rows=rows_serializable,
            truncated=truncated,
            row_count=len(rows_serializable)
        )

    except (ValueError, RuntimeError) as e:
        logger.warning(f"业务逻辑错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"服务器内部错误: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务内部错误，请查看日志"
        )
