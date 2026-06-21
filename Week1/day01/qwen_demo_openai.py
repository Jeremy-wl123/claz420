import json
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

try:
    client = OpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下为华北2（北京）地域的URL，各地域的URL不同。
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    messages= [
        {'role': 'system', 'content': '你是一名耐心、准确的人工智能课程助教'},
        {'role': 'user', 'content': '请用三句话解释什么是大模型 API？'}
    ]
    completion = client.chat.completions.create(
        model="qwen-plus",  # 模型列表: https://help.aliyun.com/model-studio/getting-started/models
        messages=messages,
    )
    print(completion.choices[0].message.content)

    # 查看完整输出
    print(completion)
    print(completion.model_dump_json(indent=2, ensure_ascii=False))

    # 保存为JSON文件
    output_path = os.path.join(os.path.dirname(__file__), "output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(completion.model_dump_json(indent=2, ensure_ascii=False))
    print(f"已保存至: {output_path}")
except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")