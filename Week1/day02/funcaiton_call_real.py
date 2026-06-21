from openai import OpenAI
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 1. 定义一个获取天气的工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "城市名，如杭州"},
                },
                "required": ["location"],
            },
        },
    }
]

# 2. 用户提问
messages = [{"role": "user", "content": "杭州天气怎么样？"}]

# 第一次调用模型：模型会返回 tool_calls
response = client.chat.completions.create(
    model="deepseek-chat",  # 换成你实际可用的模型名，如 deepseek-v4-pro
    messages=messages,
    tools=tools,  # 传入工具列表
)

# 获取模型的回复（通常包含 tool_calls）
assistant_msg = response.choices[0].message
print("模型第一次回复：", assistant_msg)

# 3. 将模型的回复加入对话历史（必须转换为字典，否则 API 会报错）
messages.append(assistant_msg.model_dump())  # 或 dict(assistant_msg)


def get_weather(location: str) -> str:
    """调用高德地图天气API查询真实天气"""
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "key": os.getenv("GAODE_API_KEY"),
        "city": location,
        "extensions": "all",
        "output": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return json.dumps(data, ensure_ascii=False, indent=2)

# 4. 执行工具调用
if assistant_msg.tool_calls:
    tool_call = assistant_msg.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    result = get_weather(args["location"])
    tool_result = {"role": "tool", "tool_call_id": tool_call.id, "content": result}
    messages.append(tool_result)

# 5. 第二次调用模型，将工具返回的结果发给模型，生成最终回答
final_response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,
)
final_answer = final_response.choices[0].message.content
print("最终回答：", final_answer)