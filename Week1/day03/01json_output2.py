import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)


def call_json_output(system_prompt, user_prompt):
    """通用的 JSON 输出调用函数"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.chat.completions.create(
        model="deepseek-v4-pro",   # 或 "deepseek-chat"
        messages=messages,
        response_format={'type': 'json_object'}
    )
    content = response.choices[0].message.content
    print("原始 JSON 字符串:", content)
    parsed = json.loads(content)
    print("解析后的 Python 对象:", parsed)
    # print("类型:", type(parsed))
    # print("-" * 50)
    return parsed


# ========== 所有 Prompt 定义放在顶层，且 SQL 优先 ==========


# 1. 问答解析
system_prompt_qa = """
用户将提供一些考试文本。请解析出“问题”和“答案”，并以JSON格式输出。

示例输入：
世界上最高的山峰是什么？珠穆朗玛峰。

示例JSON输出：
{
    "question": "世界上最高的山峰是什么？",
    "answer": "珠穆朗玛峰"
}
"""
user_prompt_qa = "世界上最长的河流是什么？尼罗河"

# 2. 命名实体识别 (NER)
system_prompt_ner = """
你是一个命名实体识别（NER）系统。请从用户输入的文本中提取出所有的人名（PERSON）、地名（LOCATION）和组织名（ORGANIZATION），并以JSON数组格式返回。

输出的JSON必须包含一个 "entities" 字段，其值为一个对象数组，每个对象有 "text" 和 "type" 两个字段。

示例输入：
马云在杭州创立了阿里巴巴集团。

示例JSON输出：
{
    "entities": [
        {"text": "马云", "type": "PERSON"},
        {"text": "杭州", "type": "LOCATION"},
        {"text": "阿里巴巴集团", "type": "ORGANIZATION"}
    ]
}
"""
user_prompt_ner = "苹果公司的CEO蒂姆·库克昨天访问了北京，并与当地开发者进行了交流。"


# 3. NL2SQL（放在最上面）
system_prompt_sql = """
你是一个自然语言转SQL查询的助手。请将用户的问题转换为SQL查询语句，并以JSON格式输出。

输出的JSON必须包含一个 "sql" 字段，值为生成的SQL语句。

假设数据库包含以下表：
- 表名：employees
  字段：id (INT), name (VARCHAR), department (VARCHAR), salary (INT), hire_date (DATE)

示例输入：
查询所有销售部门的员工姓名和工资。

示例JSON输出：
{
    "sql": "SELECT name, salary FROM employees WHERE department = '销售'"
}
"""
user_prompt_sql = "统计2023年之后入职的员工总数，按部门分组。"

# ========== 主入口：只包含函数调用 ==========
if __name__ == "__main__":
    # call_json_output(system_prompt_qa, user_prompt_qa)
    # print('=' * 50)
    # call_json_output(system_prompt_ner, user_prompt_ner)
    print('=' * 50)
    call_json_output(system_prompt_sql, user_prompt_sql)
