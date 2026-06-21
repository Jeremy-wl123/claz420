import os, json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

MODELS = {
    "1": "deepseek-v4-pro",
    "2": "deepseek-reasoner",
    "3": "deepseek-chat"
}

HISTORY_FILE = "chat_history.json"


def select_model():
    print("可用模型：")
    for k, v in MODELS.items():
        print(f"{k}: {v}")
    choice = input("请选择模型编号（默认1）：") or "1"
    return MODELS.get(choice, "deepseek-v4-pro")


def load_messages():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return [{"role": "system", "content": "You are a helpful assistant."}]


def save_messages(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def stream_chat(messages, model, show_reasoning=True):
    # 是否启用思考模式由模型决定，这里简单判断
    extra = {}
    if "reasoner" in model:
        extra = {"reasoning_effort": "high", "extra_body": {"thinking": {"type": "enabled"}}}

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
        **extra
    )

    collected_reasoning = ""
    collected_content = ""
    sep_printed = False
    for chunk in response:
        delta = chunk.choices[0].delta
        if hasattr(delta, "reasoning_content") and delta.reasoning_content:
            if show_reasoning:
                print(delta.reasoning_content, end="", flush=True)
            collected_reasoning += delta.reasoning_content
        if hasattr(delta, "content") and delta.content:
            if not sep_printed and show_reasoning:
                print("\n\n=== 最终回答 ===")
                sep_printed = True
            print(delta.content, end="", flush=True)
            collected_content += delta.content
    print()
    return collected_content  # 多轮对话只需存储最终回答


def main():
    current_model = select_model()
    messages = load_messages()
    if len(messages) > 1:
        print("(已加载历史对话)")

    while True:
        try:
            user_input = input("\n用户：").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.lower() in {"exit", "quit",'q'}:
            break
        if user_input.lower() == "/save":
            save_messages(messages)
            print("对话已保存。")
            continue
        if user_input.lower() == "/clear":
            messages = [messages[0]]
            save_messages(messages)
            print("历史已清空。")
            continue
        if user_input.lower() == "/model":
            current_model = select_model()
            continue
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        print("AI：", end="")
        reply = stream_chat(messages, current_model)
        messages.append({"role": "assistant", "content": reply})
        save_messages(messages)


if __name__ == "__main__":
    main()