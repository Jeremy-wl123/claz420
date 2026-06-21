"""
数据库模型与操作
--------------
SQLAlchemy 表定义、数据库引擎创建、Schema 获取、查询执行。
"""
import logging
from typing import Any, List, Tuple

from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Float, ForeignKey

from .config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, ALLOWED_TABLES, MAX_ROWS

logger = logging.getLogger(__name__)


def get_engine(database: str = None):
    """
    创建 SQLAlchemy 数据库引擎。

    Args:
        database: 目标数据库名，为 None 则不指定数据库（用于建库操作）。
    """
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    if database:
        url += f"/{database}"
    return create_engine(
        url,
        pool_recycle=3600,
        pool_pre_ping=True,
        echo=False,
        future=True,
    )


# ---------- SQLAlchemy 表定义 ----------

metadata = MetaData()

students = Table(
    "students", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("age", Integer, nullable=False),
    Column("city", String(100), nullable=False),
)

courses = Table(
    "courses", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("teacher", String(100), nullable=False),
)

enrollments = Table(
    "enrollments", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("student_id", Integer, ForeignKey("students.id"), nullable=False),
    Column("course_id", Integer, ForeignKey("courses.id"), nullable=False),
    Column("score", Float, nullable=False),
)


def create_demo_database():
    """创建演示数据库和表，并写入样例数据。"""
    logger.info("开始创建演示数据库及表结构")
    try:
        # 先创建数据库（不指定数据库名连接）
        engine_sys = get_engine(None)
        with engine_sys.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
            conn.commit()
            logger.info(f"数据库 {DB_NAME} 创建/确认成功")

        # 连接目标数据库
        engine = get_engine(DB_NAME)

        # 重建表结构
        metadata.drop_all(engine)
        metadata.create_all(engine)
        logger.info("表结构重建完成")

        # 插入样例数据
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT IGNORE INTO students(id, name, age, city) VALUES
                (1, '张三', 20, '北京'),
                (2, '李四', 22, '上海'),
                (3, '王五', 21, '北京'),
                (4, '赵六', 23, '深圳'),
                (5, '陈晨', 20, '杭州')
            """))
            conn.execute(text("""
                INSERT IGNORE INTO courses(id, name, teacher) VALUES
                (1, 'Python 基础', 'Luke'),
                (2, '数据库原理', 'Jack'),
                (3, 'AI 应用开发', 'Ric')
            """))
            conn.execute(text("""
                INSERT IGNORE INTO enrollments(id, student_id, course_id, score) VALUES
                (1, 1, 1, 91),
                (2, 2, 1, 86),
                (3, 3, 1, 95),
                (4, 4, 2, 88),
                (5, 5, 2, 82),
                (6, 1, 3, 90),
                (7, 3, 3, 93),
                (8, 5, 3, 87)
            """))
            conn.commit()
            logger.info("样例数据插入完成")
    except Exception as e:
        logger.error(f"创建数据库失败: {e}", exc_info=True)
        raise


def get_schema() -> str:
    """
    读取允许暴露给模型的表结构信息。

    Returns:
        格式化的表结构字符串，包含列定义和表间关系。
    """
    logger.debug("获取数据库 Schema")
    engine = get_engine(DB_NAME)
    schema_parts = []
    with engine.connect() as conn:
        for table_name in sorted(ALLOWED_TABLES):
            result = conn.execute(text(f"SHOW COLUMNS FROM {table_name}"))
            columns = result.fetchall()
            col_text = ", ".join(f"{row[0]} {row[1]}" for row in columns)
            schema_parts.append(f"{table_name}({col_text})")

    # 追加表间关系说明
    schema_parts.append("关系：enrollments.student_id = students.id")
    schema_parts.append("关系：enrollments.course_id = courses.id")
    schema_str = "\n".join(schema_parts)
    logger.debug(f"获取到的 Schema:\n{schema_str}")
    return schema_str


def execute_read_only_query(sql: str, max_rows: int = MAX_ROWS) -> Tuple[List[str], List[Tuple[Any, ...]], bool]:
    """
    以只读模式执行 SQL 查询。

    Args:
        sql: 经过校验的 SQL 查询语句。
        max_rows: 最大返回行数。

    Returns:
        (列名列表, 行数据列表, 是否被截断)
    """
    logger.info(f"执行只读查询: {sql}")

    engine = get_engine(DB_NAME)
    with engine.connect() as conn:
        conn.execute(text("SET SESSION TRANSACTION READ ONLY"))
        conn.execute(text("START TRANSACTION READ ONLY"))

        result = conn.execute(text(sql))

        columns = list(result.keys())
        rows_all = result.fetchmany(max_rows + 1)
        truncated = len(rows_all) > max_rows
        rows = rows_all[:max_rows]

        conn.commit()
        logger.info(f"查询返回 {len(rows)} 行，是否截断: {truncated}")
        return columns, rows, truncated
