"""
配置模块
------
集中管理所有应用配置常量。
"""

# ---------- 数据库配置 ----------
DB_NAME = "teaching"
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "123456"

# ---------- SQL 安全策略 ----------
ALLOWED_TABLES = {"students", "courses", "enrollments"}

FORBIDDEN_KEYWORDS = {
    "insert", "update", "delete", "drop", "alter",
    "create", "replace", "truncate", "attach", "detach",
    "pragma", "vacuum",
}

# ---------- 查询限制 ----------
MAX_ROWS = 100
