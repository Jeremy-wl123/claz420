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
        stream=False,
    )
    return response.choices[0].message.content


async def main_async(questions: list[str]):
    start = time.perf_counter()
    print(f"开始并发请求: {time.perf_counter()}")
    results = await asyncio.gather(*[ask_question(q) for q in questions])
    elapsed = time.perf_counter() - start

    for q, ans in zip(questions, results):
        print(f"问题: {q}\n回答: {ans}\n{'-' * 40}")
    print(f"异步并发总耗时: {elapsed:.2f} 秒")


# 同步串行版本
def main_sync(questions: list[str]):
    from openai import OpenAI
    sync_client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )
    start = time.perf_counter()
    print(f"开始串行请求: {time.perf_counter()}")
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


# ========== 新增：多线程同步并发版本 ==========
def main_threaded(questions: list[str]):
    from concurrent.futures import ThreadPoolExecutor
    from openai import OpenAI

    # 创建一个同步客户端，它可以在多线程中共享（线程安全）
    sync_client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    def ask_sync(q: str):
        """每个线程执行的同步请求"""
        response = sync_client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": q}
            ],
            stream=False,
        )
        return q, response.choices[0].message.content

    start = time.perf_counter()
    print(f"开始多线程并发请求: {time.perf_counter()}")

    with ThreadPoolExecutor(max_workers=len(questions)) as executor:
        # 提交所有任务
        futures = [executor.submit(ask_sync, q) for q in questions]
        # 按提交顺序获取结果并打印
        for future in futures:   # as_completed(futures): 目前需要等待，实际工程谁完成打印谁
            q, ans = future.result()
            print(f"问题: {q}\n回答: {ans}\n{'-' * 40}")

    elapsed = time.perf_counter() - start
    print(f"多线程并发总耗时: {elapsed:.2f} 秒")
# ===========================================


if __name__ == "__main__":
    questions = [
        "重复说十遍我爱你。",
        "重复说十遍我爱你",
        "重复说十遍我爱你"
    ]
    # questions = [
    #     # 问题1：技术原理类（需要详细拆解计算过程，约400-600字）
    #     "请详细解释Transformer架构中的多头自注意力机制（Multi-Head Self-Attention）的具体计算流程。必须包含Q、K、V矩阵的生成、缩放点积公式、多头拼接以及残差连接的全过程，并说明为何这种设计能捕捉长距离依赖。请务必写满大约500字。",
    #
    #     # 问题2：科幻创作类（需要构建情节和人物，约400-600字）
    #     "请以《星际穿越》中的五维空间为背景，创作一个短篇科幻片段。主角是库珀的女儿墨菲，她在成年后首次尝试通过书架背后的引力异常与过去的父亲进行沟通。请着重描写她的心理挣扎、科学推理过程以及记忆闪回。请务必写满大约500字。",
    #
    #     # 问题3：商业策划类（需要结构化列表和具体建议，约400-600字）
    #     "假设你是一名资深商业顾问，请为一家濒临倒闭的线下实体书店制定一份详细的数字化转型方案。方案需包含：线上线下融合的会员体系、基于私域流量的社群运营策略、以及针对Z世代人群的选品与空间改造建议。请用清晰的分点论述，字数保持在500字左右。"
    # ]
    # 运行异步版本
    asyncio.run(main_async(questions))

    # 运行同步串行版本
    main_sync(questions)

    # ========== 新增：运行多线程版本 ==========
    main_threaded(questions)
    # ===========================================