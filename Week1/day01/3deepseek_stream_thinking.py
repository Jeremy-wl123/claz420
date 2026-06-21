# 请先安装依赖：pip install openai python-dotenv
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 开启流式 + 思考模式
response = client.chat.completions.create(
    model="deepseek-reasoner",          # 使用支持思考的模型，如 deepseek-reasoner
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "请比较 Python 和 JavaScript 的优缺点。"}
    ],
    stream=True,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print("=== 思考过程（reasoning）===")
sep_printed = False                      # ✅ 改用普通变量作为标志
for chunk in response:
    delta = chunk.choices[0].delta

    # 打印思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content:
        print(delta.reasoning_content, end="", flush=True)

    # 打印最终回答，并在第一次出现时加上分隔线
    if hasattr(delta, "content") and delta.content:
        if not sep_printed:
            print("\n\n=== 最终回答 ===")
            sep_printed = True
        print(delta.content, end="", flush=True)