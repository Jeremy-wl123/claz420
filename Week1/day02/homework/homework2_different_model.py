import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def call_deepseek(user_message: str) -> str:
    """调用 DeepSeek API（带 reasoning_effort 和 thinking 参数）"""
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )
    completion = client.chat.completions.create(
        model="deepseek-v4-pro",          # 请确保模型名称正确
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": user_message},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    return completion.choices[0].message.content

def call_qwen(user_message: str) -> str:
    """调用阿里云百炼 Qwen-Plus API"""
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "你是一名耐心、准确的人工智能课程助教"},
            {"role": "user", "content": user_message},
        ],
    )
    return completion.choices[0].message.content

def main():
    print("请选择要使用的模型：")
    print("1. DeepSeek V4 Pro (带深度思考)")
    print("2. 阿里云百炼 Qwen-Plus")
    choice = input("请输入序号 (1 或 2): ").strip()

    if choice not in ("1", "2"):
        print("无效选择，默认使用 Qwen-Plus。")
        choice = "2"

    user_input = input("\n请输入你的问题: ").strip()
    if not user_input:
        print("问题不能为空。")
        return

    try:
        if choice == "1":
            print("\n正在调用 DeepSeek...")
            answer = call_deepseek(user_input)
        else:
            print("\n正在调用 Qwen-Plus...")
            answer = call_qwen(user_input)

        print("\n=== 模型回复 ===\n")
        print(answer)
    except Exception as e:
        print(f"\n调用失败: {e}")
        print("请检查环境变量 DEEPSEEK_API_KEY 或 DASHSCOPE_API_KEY 是否正确配置。")

if __name__ == "__main__":
    main()