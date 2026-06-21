import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# 系统提示：定义表结构 + 生成SQL的规则，并给出JSON输出示例
system_prompt = """
你是一个SQL专家。请根据用户的问题，生成对应的SQL查询语句。

数据库中有以下表：
表名: employees
  - id (INTEGER) PRIMARY KEY
  - name (TEXT) NOT NULL
  - age (INTEGER)
  - department_id (INTEGER) 外键引用 departments(id)
  - salary (REAL)
  

请根据用户的问题，生成一个完整的SQL查询语句，并以JSON格式输出，格式如下：
{
    "sql": "生成的SQL语句",
    "explanation": "一句话说明查询逻辑"
}

示例：
用户问题：查询所有员工的姓名和工资。
输出：
{
    "sql": "SELECT name, salary FROM employees;",
    "explanation": "查询所有员工的姓名、工资"
}


注意：
- 只生成SELECT，字段名必须与表结构一致。
"""
# 这里只是软限制


# 用户输入的自然语言问题
user_prompt = "查询年龄大于30岁员工的姓名、工资"


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    response_format={'type': 'json_object'},
)

# 获取模型返回的JSON字符串
result_json_str = response.choices[0].message.content
# print("原始JSON字符串:", result_json_str)

# 解析为字典
result_dict = json.loads(result_json_str)
print("解析后的字典:", result_dict)

# 提取并打印生成的SQL
sql = result_dict.get("sql")
print("生成的SQL语句:", sql)



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


result = validate_sql(sql)
print(f"结果: {result}\n")

