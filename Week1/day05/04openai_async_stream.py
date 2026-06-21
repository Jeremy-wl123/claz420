import os
import asyncio
import time
from openai import AsyncOpenAI, OpenAI
from dotenv import load_dotenv

load_dotenv()

# 初始化异步客户端
async_client = AsyncOpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 同步客户端（用于对比）
sync_client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


async def ask_question_stream(prompt: str, task_id: int) -> str:
    """
    发送流式请求，实时打印每个数据块的内容，并返回完整回答。
    """
    response = await async_client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True,  # 启用流式
    )

    prefix = f"[问题{task_id}] "
    full_content = ""
    # 标记是否已开始输出（用于控制换行）
    first_chunk = True

    async for chunk in response:
        # 获取增量内容（如果有）
        delta = chunk.choices[0].delta
        if delta and delta.content:
            content = delta.content
            full_content += content
            # 第一次打印时先输出前缀，然后紧跟内容
            if first_chunk:
                print(f"\n{prefix}", end="", flush=True)
                first_chunk = False
            print(content, end="", flush=True)

    # 每个问题结束后换行并打印分隔线
    if not first_chunk:  # 如果确实有内容输出
        print("\n" + "-" * 40)
    else:
        # 如果无内容（极少情况），直接打印提示
        print(f"{prefix}（无内容）")
        print("-" * 40)

    return full_content


async def main_async(questions: list[str]):
    """异步并发流式请求"""
    print("===== 异步并发流式 =====")
    start = time.perf_counter()
    tasks = [ask_question_stream(q, i+1) for i, q in enumerate(questions)]
    # 并发执行，但每个任务内部实时打印，输出会交错但带有标识
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    print(f"异步并发流式总耗时: {elapsed:.2f} 秒\n")


def main_sync(questions: list[str]):
    """同步串行流式请求（对比用）"""
    print("===== 同步串行流式 =====")
    start = time.perf_counter()
    for idx, q in enumerate(questions, 1):
        prefix = f"[问题{idx}] "
        response = sync_client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": q}
            ],
            stream=True,
        )
        print(f"\n{prefix}", end="", flush=True)
        full = ""
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                content = delta.content
                full += content
                print(content, end="", flush=True)
        print("\n" + "-" * 40)
    elapsed = time.perf_counter() - start
    print(f"同步串行流式总耗时: {elapsed:.2f} 秒")


if __name__ == "__main__":
    questions = [
        "重复说十遍我爱你老婆,每一遍前面加第几遍。",
        "重复说十遍我爱你老爸,每一遍前面加第几遍。",
        "重复说十遍我爱你老妈,每一遍前面加第几遍。"
    ]

    # 运行异步流式版本
    asyncio.run(main_async(questions))

    # 运行同步流式版本（取消注释以对比）
    main_sync(questions)