import os
from dashscope import Generation
import dashscope
from dotenv import load_dotenv
load_dotenv()

# 以下为华北2（北京）地域的URL，各地域的URL不同。
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
messages =[
            {'role': 'system', 'content': '你是一名耐心、准确的人工智能课程助教'},
            {'role': 'user', 'content': '请用三句话解释什么是大模型 API？'}
        ]

response = Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",   # 模型列表：https://help.aliyun.com/model-studio/getting-started/models
    messages=messages,
    result_format="message"
)

if response.status_code == 200:
    print(response.output.choices[0].message.content)
else:
    print(f"HTTP返回码：{response.status_code}")
    print(f"错误码：{response.code}")
    print(f"错误信息：{response.message}")
    print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")

