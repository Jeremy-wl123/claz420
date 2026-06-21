import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

model = "qwen-plus"

messages = [
    {
        "role": "system",
        "content": "你是一名 Python 教师，回答应简洁并包含示例。",
    }
]

while True:
    question = input("用户：").strip()

    if question.lower() in {"exit", "quit"}:
        print("对话结束")
        break

    if not question:
        continue

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})

    # 持久化存储：仅将对话历史（messages）写入 JSON 文件
    output_path = os.path.join(os.path.dirname(__file__), "conversation.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    print(f"AI：{answer}")