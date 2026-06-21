import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "请用三句中文介绍什么是AI的API。"}
    ],
    stream=True,                         # 开启流式输出
    # 不设置 reasoning_effort 和 extra_body 中的 thinking，即不使用深度思考
)


# print(response.choices[0].message.content)

# 逐块输出内容
for chunk in response:
    content = chunk.choices[0].delta.content
    if content:                          # 避免输出 None
        print(content, end="", flush=True)

