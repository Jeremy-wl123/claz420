import sqlglot
from sqlglot import expressions as exp

def validate_sql(sql: str) -> dict:
    """
    校验 SQL 语句的语法和基本安全规则。
    返回包含 status 和 message 的字典。
    """
    try:
        # 解析 SQL 为 AST（默认使用 SQLite 方言，可按需指定）
        ast = sqlglot.parse_one(sql)
    except sqlglot.errors.ParseError as e:
        return {"status": "error", "message": f"语法错误: {e}"}

    # 规则1：仅允许 SELECT 查询
    if not isinstance(ast, exp.Select):
        return {"status": "error", "message": f"仅允许 SELECT 查询，不允许 {ast.__class__.__name__}"}

    # 规则2：检查 WHERE 子句中是否包含 '1=1'（可能导致全表返回）
    for node in ast.walk():
        if isinstance(node, exp.Where):
            where_sql = node.sql().lower()
            if "1=1" in where_sql:
                return {"status": "warning", "message": "WHERE 子句中包含 '1=1'，可能返回全表数据"}

    return {"status": "success", "message": "SQL 校验通过"}


if __name__ == "__main__":
    # 测试用例：包含正面、反面和警告场景
    test_cases = [
        # 正面案例
        ("SELECT id, name FROM users WHERE age > 18", "正面：简单 SELECT 查询"),
        ("SELECT department, COUNT(*) FROM employees GROUP BY department", "正面：带聚合的查询"),
        # 反面案例
        ("SELECT * FORM users", "反面：关键字拼写错误（FORM）"),
        ("DELETE FROM users WHERE id = 1", "反面：非 SELECT 操作"),
        ("DROP TABLE logs", "反面：DDL 操作"),
        # 警告案例
        ("SELECT * FROM logs WHERE 1=1 AND status = 'active'", "警告：WHERE 中包含 1=1"),
    ]

    for sql, desc in test_cases:
        print(f"--- {desc} ---")
        print(f"SQL: {sql}")
        result = validate_sql(sql)
        print(f"结果: {result}\n")