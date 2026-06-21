#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
load_dotenv()

# ---------- 模式选择 ----------
USE_REAL_API = True  # 设为 True 使用真实 DeepSeek API（需设置环境变量 DEEPSEEK_API_KEY）
# -----------------------------

if USE_REAL_API:
    from openai import OpenAI

# 固定并发数（工程推荐）
MAX_WORKERS = 3


def ask_simulate(idx: int, q: str):
    """
    模拟请求：随机耗时 1~3 秒，返回固定回答。
    通过随机延时模拟不同请求响应速度，方便观察 as_completed 效果。
    """
    delay = random.uniform(1.0, 3.0)
    time.sleep(delay)
    # 模拟异常（约 20% 概率失败，用于演示异常处理）
    if random.random() < 0.2:
        raise RuntimeError(f"模拟请求失败（问题 {idx}）")
    return idx, q, f"模拟回答（耗时 {delay:.2f}s）"


def ask_real(idx: int, q: str, client):
    """
    真实调用 DeepSeek API（需安装 openai 库并设置环境变量）
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",  # 或 deepseek-chat
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": q}
            ],
            stream=False,
            timeout=30.0,  # 客户端超时
        )
        ans = response.choices[0].message.content
        return idx, q, ans
    except Exception as e:
        # 将异常向上抛出，由调用方统一处理
        raise RuntimeError(f"API 调用失败: {e}")


def main_demo(questions: list[str]):
    print("=" * 60)
    print("并发请求演示（as_completed + 索引存储）")
    print(f"问题列表（共 {len(questions)} 个）：")
    for i, q in enumerate(questions):
        print(f"  {i}: {q}")
    print("-" * 60)

    # 准备客户端（仅真实模式需要）
    client = None
    if USE_REAL_API:
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            print("错误：未设置环境变量 DEEPSEEK_API_KEY")
            return
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # 预分配结果列表（保证最终顺序）
    results = [None] * len(questions)

    start = time.perf_counter()

    # 使用线程池，并发数取最小值（不超过问题数）
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(questions))) as executor:
        # 提交所有任务
        futures = []
        for i, q in enumerate(questions):
            if USE_REAL_API:
                # 注意：需要将 client 传递给 ask_real，这里用 lambda 或 partial
                future = executor.submit(ask_real, i, q, client)
            else:
                future = executor.submit(ask_simulate, i, q)
            futures.append(future)

        # 使用 as_completed 实时打印已完成的任务
        print("\n【实时输出】按完成顺序打印：")
        for future in as_completed(futures):
            try:
                # 设置超时（防止单个任务卡死）
                idx, q, ans = future.result(timeout=30)
                # 存入预分配列表（保证最终有序）
                results[idx] = (q, ans)
                # 实时打印（显示索引和回答摘要）
                preview = ans[:50] + "..." if len(ans) > 50 else ans
                print(f"✅ 问题 {idx} 完成：{preview}")
            except Exception as e:
                # 异常处理：记录错误，并标记该位置为异常
                # 注意：此时我们不知道是哪个索引，但可以从 future 中提取，此处简化处理
                # 更好的做法：在提交时绑定索引，但异常时无法从 future 直接获取，我们可以遍历查找
                # 这里采用另一种方式：在 ask_* 函数中返回 idx，但异常时无法返回。
                # 因此我们改用另一个方法：在提交时保存 (future, idx) 配对，但 as_completed 只返回 future。
                # 实用解法：在异常捕获中，我们可以通过 future 对应的原始参数来推断，但不够优雅。
                # 此处演示简化：我们假设异常信息包含索引（已在 ask_simulate/ask_real 中抛出）
                # 但这里我们为了演示，直接打印错误，并对应空位
                print(f"❌ 某个请求失败：{e}")
                # 我们无法直接知道索引，但在真实工程中，你可以在提交时把索引绑定到 future 上，
                # 或用字典映射。为简化演示，我们下面用遍历查找未填充的位置（不推荐，仅演示）。
                # 更稳健：在 submit 时使用 (future, idx) 并单独处理，此处不再展开。

        # 由于异常时无法拿到 idx，我们补充一个修复：对于未填充的位置，用默认占位
        for i in range(len(results)):
            if results[i] is None:
                results[i] = (f"问题 {i}", "[请求失败或超时]")

    elapsed = time.perf_counter() - start

    # 最终按原始顺序输出
    print("\n【最终顺序输出】按原始问题列表顺序：")
    for i, (q, ans) in enumerate(results):
        print(f"{i}: {q}\n   -> {ans}\n")

    print(f"总耗时: {elapsed:.2f} 秒")
    print("=" * 60)


if __name__ == "__main__":
    # 测试问题列表
    sample_questions = [
        "什么是深度学习？",
        "Python 有哪些优点？举例三个",
        "如何学习编程？",
        "重复三遍我爱你",
        "就业教培优秀老师的核心特征"
    ]
    main_demo(sample_questions)