import json
import os
from dashscope import MultiModalConversation
import dashscope
from dotenv import load_dotenv
load_dotenv()

dashscope.base_http_api_url = 'https://llm-zw41x57m8nuezmhp.cn-beijing.maas.aliyuncs.com/api/v1'

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/thtclx/input1.png"},
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/iclsnx/input2.png"},
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/gborgw/input3.png"},
            {"text": "图1中的女生穿着图2中的黑色裙子按图3的姿势坐下"}
        ]
    }
]

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")

response = MultiModalConversation.call(
    api_key=api_key,
    model="qwen-image-2.0",
    messages=messages,
    result_format='message',
    stream=False,
    n=2,
    watermark=True,
    negative_prompt=""
)

print(json.dumps(response, ensure_ascii=False))