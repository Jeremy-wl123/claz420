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
"""

# 用户输入的自然语言问题
user_prompt = "查询年龄大于30岁员工的姓名、工资"


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

response = client.chat.completions.create(
    model="eepseek-v4-pro",
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