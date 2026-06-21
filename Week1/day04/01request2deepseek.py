import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"

user_input = "你好"

# 请求体（只保留必要参数）
payload = {
    "model": "deepseek-v4-pro",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": user_input}
    ],
    "max_tokens": 4096,
    "temperature": 1
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# 发送请求
# 请求行	由 requests.post(URL) 自动生成（POST + 路径 + HTTP版本）
# 请求头	headers 字典（Content-Type, Authorization）
# 请求体	payload 字典通过 json= 参数传递，自动转为JSON

response = requests.post(URL, headers=headers,json=payload)

# 解析响应
if response.status_code == 200:
    result = response.json()
    reply = result["choices"][0]["message"]["content"]
    print("助手回复:", reply)
else:
    print("请求失败，状态码:", response.status_code)
    print("错误信息:", response.text)

