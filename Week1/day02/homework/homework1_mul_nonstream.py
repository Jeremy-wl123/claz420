# 作业：
# 1.完成多轮对话的demo
# 2.完成让用户选择不同模型的调用不同模型的回复demo
# 3.完成一次持久化存储对话
# 4.完成一次流式输出demo
# 5.完成RAG流程图的绘制
# 6.选做：调用xiaomi、硅基流动、chatgpt等其他 AI API 服务
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

model = "deepseek-v4-pro"  # 可以使用 ds 也可以使用qwen

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

    if not question: # 直接输入回车
        continue

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})

    print(f"AI：{answer}")