import os
import asyncio
from openai import AsyncOpenAI  # 改用异步客户端
from dotenv import load_dotenv

load_dotenv()

async def main():
    # 使用 AsyncOpenAI 客户端
    client = AsyncOpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    # 发起流式请求，stream=True
    response = await client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "请用三句中文介绍什么是AI的API。"}
        ],
        stream=True,
    )

    # 异步迭代响应块
    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)

# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())

''' 
1. 直接调用会发生什么？
当你执行 main() 时，它不会进入函数体内部，而是立即返回一个协程对象（Coroutine Object）。

python
if __name__ == "__main__":
    main()  # 只是创建了一个协程对象，没有执行任何 print 或 API 请求
此时脚本会瞬间执行完毕并退出，终端里不会有任何“AI 回答”的输出。你如果在交互式环境（如 REPL）里打印它，会看到类似 <coroutine object main at 0x...> 的结果。

2. 为什么必须用 asyncio.run()？
asyncio.run(main()) 做了两件缺一不可的事：

创建事件循环（Event Loop）：相当于启动一个“异步调度器”。

驱动协程执行：将你那个“待执行的计划”（协程对象）交给调度器去一步一步推进（遇到 await 就切出去，收到数据再切回来）。

如果不经过这一步，异步代码中的 await client.chat.completions.create(...) 和 async for 就没有调度器去管理，自然永远停留在“计划”阶段。
'''