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


async def ask_question_stream(prompt: str, idx: int) -> str:
    """
    异步流式请求，实时打印回答内容（逐字），同时累积完整文本并返回。
    """
    print(f"\n[问题 {idx+1}] {prompt}\n回答: ", end="", flush=True)
    full_response = ""
    try:
        stream = await client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        print("\n" + "-" * 40)
    except Exception as e:
        print(f"\n请求出错: {e}")
    return full_response


async def main_async(questions: list[str]):
    start = time.perf_counter()
    print(f"开始异步并发流式请求: {time.perf_counter()}")
    # 并发执行所有流式请求，每个任务内部会实时打印
    await asyncio.gather(*[ask_question_stream(q, i) for i, q in enumerate(questions)])
    elapsed = time.perf_counter() - start
    print(f"异步并发总耗时: {elapsed:.2f} 秒\n")


# 同步串行版本（流式）
def main_sync(questions: list[str]):
    from openai import OpenAI
    sync_client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )
    start = time.perf_counter()
    print(f"开始同步串行流式请求: {time.perf_counter()}")
    for idx, q in enumerate(questions):
        print(f"\n[问题 {idx+1}] {q}\n回答: ", end="", flush=True)
        try:
            stream = sync_client.chat.completions.create(
                model="deepseek-v4-flash",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": q}
                ],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
            print("\n" + "-" * 40)
        except Exception as e:
            print(f"\n请求出错: {e}")
    elapsed = time.perf_counter() - start
    print(f"同步串行总耗时: {elapsed:.2f} 秒\n")


# 多线程并发版本（流式）
def main_threaded(questions: list[str]):
    from concurrent.futures import ThreadPoolExecutor
    from openai import OpenAI

    sync_client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    def ask_sync_stream(q: str, idx: int):
        """每个线程执行的同步流式请求，内部实时打印"""
        print(f"\n[问题 {idx+1}] {q}\n回答: ", end="", flush=True)
        try:
            stream = sync_client.chat.completions.create(
                model="deepseek-v4-flash",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": q}
                ],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
            print("\n" + "-" * 40)
        except Exception as e:
            print(f"\n请求出错: {e}")

    start = time.perf_counter()
    print(f"开始多线程并发流式请求: {time.perf_counter()}")

    with ThreadPoolExecutor(max_workers=3) as executor:
        # 提交任务，并传入索引
        futures = [executor.submit(ask_sync_stream, q, i) for i, q in enumerate(questions)]
        # 等待所有任务完成
        for future in futures:
            future.result()  # 确保异常被抛出

    elapsed = time.perf_counter() - start
    print(f"多线程并发总耗时: {elapsed:.2f} 秒\n")


if __name__ == "__main__":
    questions = [
        "重复说十遍我爱你老爸。",
        "重复说十遍我爱你老妈",
        "重复说十遍我爱你老婆"
    ]
    # 运行异步并发流式
    asyncio.run(main_async(questions))

    # 运行同步串行流式
    main_sync(questions)

    # 运行多线程并发流式
    main_threaded(questions)