import os
import asyncio
import time
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# 初始化异步客户端
client = AsyncOpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


async def ask_question(prompt: str) -> str:
    """发送一个非流式请求，返回完整回答"""
    response = await client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=False,  # 非流式，便于收集完整结果
    )
    return response.choices[0].message.content


async def main_async(questions: list[str]):
    # # 准备三个不同的问题
    # questions = [
    #     "用一句话解释什么是异步编程。",
    #     "列举 Python 中三个常用的异步库。",
    #     "浅析异步 I/O 与多线程的区别。"
    # ]

    # 并发执行所有请求
    start = time.perf_counter()
    print(f"开始并发请求: {time.perf_counter()}")
    results = await asyncio.gather(*[ask_question(q) for q in questions])
    elapsed = time.perf_counter() - start

    # 打印结果
    for q, ans in zip(questions, results):
        print(f"问题: {q}\n回答: {ans}\n{'-' * 40}")

    print(f"异步并发总耗时: {elapsed:.2f} 秒")


# 同步版本（对比用）
def main_sync(questions: list[str]):
    from openai import OpenAI  # 同步客户端
    sync_client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )
    # questions = [
    #     "用一句话解释什么是异步编程。",
    #     "列举 Python 中三个常用的异步库。",
    #     "浅析异步 I/O 与多线程的区别。"
    # ]
    start = time.perf_counter()
    print(f"开始并发请求: {time.perf_counter()}")
    for q in questions:
        response = sync_client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": q}
            ],
            stream=False,
        )
        print(f"问题: {q}\n回答: {response.choices[0].message.content}\n{'-' * 40}")
    elapsed = time.perf_counter() - start
    print(f"同步串行总耗时: {elapsed:.2f} 秒")


if __name__ == "__main__":
    questions = [
        "重复说十遍我爱你老婆。",
        "重复说十遍我爱你老爸",
        "重复说十遍我爱你老妈"
    ]
    # 运行异步版本
    asyncio.run(main_async(questions))

    # 运行同步版本（取消注释以对比）
    main_sync(questions)