from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


messages=[]
while True:
    user_input = input("请输入问题：")
    if user_input=="q":
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages
    )
    # 核心操作，将ai回复加入messages中
    messages.append(response.choices[0].message)
    print(messages)

    print(response.choices[0].message.content)

