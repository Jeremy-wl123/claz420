# tool_websearch.py
import asyncio
import json
import logging
from openai import OpenAI

# 导入我们自己写的模块
from web_research import WebResearch
from ai_client import AIClient
import os
from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(level=logging.INFO)

# ---------- 1. 全局 Researcher 初始化 ----------
_researcher = None


def get_researcher():
    global _researcher
    if _researcher is None:
        # 请替换为你的真实 API Key
        ai_client = AIClient(api_key="sk-xxx", base_url="https://api.deepseek.com")
        _researcher = WebResearch(ai_client)
    return _researcher


# ---------- 2. 工具函数（同步包装器） ----------
def search_position_tool(position: str) -> str:
    """同步包装异步搜索函数，供 OpenAI 工具调用"""
    researcher = get_researcher()
    try:
        # 运行异步方法并等待结果
        profile = asyncio.run(researcher.search_position(position))
        return json.dumps(profile, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"position": position, "error": str(e)}, ensure_ascii=False)


# ---------- 3. 工具定义（OpenAI 格式） ----------
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_position",
            "description": "搜索指定岗位的招聘要求、技术栈、面试题和行业洞察，生成结构化的岗位画像。",
            "parameters": {
                "type": "object",
                "properties": {
                    "position": {
                        "type": "string",
                        "description": "岗位名称，例如 'Python后端开发'、'Java架构师'"
                    }
                },
                "required": ["position"]
            }
        }
    }
]

# ---------- 4. OpenAI 客户端 ----------
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 请替换
    base_url="https://api.deepseek.com",
)


def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    return response.choices[0].message


# ---------- 5. 主对话流程 ----------
if __name__ == "__main__":
    user_query = "我想了解AI应用开发岗位的面试重点和常见问题。"
    messages = [{"role": "user", "content": user_query}]
    print(f"用户>\t {user_query}")

    # 首次调用
    message = send_messages(messages)

    # 循环处理工具调用
    while message.tool_calls:
        for tool_call in message.tool_calls:
            if tool_call.function.name == "search_position":
                args = json.loads(tool_call.function.arguments)
                position = args.get("position")
                print(f"[系统] 调用工具搜索岗位: {position}")
                tool_result = search_position_tool(position)

                # 将模型的工具调用请求加入历史
                messages.append(message)
                # 将工具执行结果加入历史
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })
        # 再次调用模型
        message = send_messages(messages)

    # 输出最终回答
    print(f"模型>\t {message.content}")