"""
SQL 校验模块
-----------
负责教学级 SQL 只读安全校验。
"""
import logging
import re

from model.config import ALLOWED_TABLES, FORBIDDEN_KEYWORDS

logger = logging.getLogger(__name__)


def validate_sql(sql: str) -> str:
    """
    完成教学级只读 SQL 校验。

    校验规则：
    1. 必须是 SELECT 或 WITH 开头
    2. 不允许包含多条 SQL 语句
    3. 不允许包含禁止的关键字
    4. 只允许查询白名单中的表

    Args:
        sql: 待校验的 SQL 语句。

    Returns:
        校验通过并清理后的 SQL 语句。

    Raises:
        ValueError: 校验不通过时抛出。
    """
    logger.debug(f"开始校验 SQL: {sql}")

    normalized = sql.strip().rstrip(";").strip()
    lowered = normalized.lower()

    # 规则1：只允许 SELECT 或 WITH 开头
    if not re.match(r"^(select|with)\b", lowered):
        raise ValueError("只允许 SELECT 或只读 WITH 查询")

    # 规则2：禁止多条 SQL
    if ";" in normalized:
        raise ValueError("一次只允许执行一条 SQL")

    # 规则3：禁止危险关键字
    words = set(re.findall(r"\b[a-z_]+\b", lowered))
    dangerous = words & FORBIDDEN_KEYWORDS
    if dangerous:
        raise ValueError(f"SQL 包含禁止关键字：{', '.join(sorted(dangerous))}")

    # 规则4：表名白名单校验
    referenced_tables = set(
        re.findall(r"\b(?:from|join)\s+([a-z_][a-z0-9_]*)", lowered)
    )
    cte_names = set(
        re.findall(r"(?:\bwith\b|,)\s*([a-z_][a-z0-9_]*)\s+as\s*\(", lowered)
    )
    illegal_tables = referenced_tables - ALLOWED_TABLES - cte_names
    if illegal_tables:
        raise ValueError(f"SQL 访问了未授权表：{', '.join(sorted(illegal_tables))}")

    logger.info("SQL 校验通过")
    return normalized
