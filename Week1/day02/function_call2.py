import json
import os

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def get_weather(location: str) -> dict:
    """教学用模拟天气函数，真实项目中应调用天气 API。"""
    mock_weather = {
        "杭州，浙江": {
            "temperature": 24,
            "unit": "celsius",
            "condition": "晴",
        },
        "北京": {
            "temperature": 28,
            "unit": "celsius",
            "condition": "多云",
        },
    }

    return mock_weather.get(
        location,
        {
            "location": location,
            "temperature": None,
            "condition": "暂未查询到该地区的天气数据",
        },
    )


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前天气。当用户询问实时天气、温度或天气状况时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市和省份，例如：杭州，浙江",
                    }
                },
                "required": ["location"],
            },
        },
    }
]


def send_messages(messages):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    return response.choices[0]


def execute_tool(tool_call) -> str:
    function_name = tool_call.function.name

    try:
        arguments = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError:
        return json.dumps(
            {"error": "模型生成的工具参数不是合法 JSON"},
            ensure_ascii=False,
        )

    if function_name == "get_weather":
        location = arguments.get("location")

        if not location:
            return json.dumps(
                {"error": "缺少必填参数 location"},
                ensure_ascii=False,
            )

        result = get_weather(location)
        return json.dumps(result, ensure_ascii=False)

    return json.dumps(
        {"error": f"未注册的工具：{function_name}"},
        ensure_ascii=False,
    )


def run_conversation(user_input: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个天气助手。需要实时天气时必须调用工具，"
                "不要编造天气数据。请使用中文回答。"
            ),
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    first_choice = send_messages(messages)
    assistant_message = first_choice.message

    if not assistant_message.tool_calls:
        return assistant_message.content or "模型未返回有效内容。"

    messages.append(
        assistant_message.model_dump(exclude_none=True)
    )

    for tool_call in assistant_message.tool_calls:
        tool_result = execute_tool(tool_call)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result,
            }
        )

    final_choice = send_messages(messages)
    return final_choice.message.content or "模型未返回最终回答。"


if __name__ == "__main__":
    # question = "杭州，浙江现在天气怎么样？"
    # print(f"User>\t{question}")
    #
    # answer = run_conversation(question)
    # print(f"Model>\t{answer}")
    #
    # question = "北京，现在天气怎么样？"
    # print(f"User>\t{question}")
    #
    # answer = run_conversation(question)
    # print(f"Model>\t{answer}")
    #
    # question = "深圳现在天气怎么样？"
    # print(f"User>\t{question}")
    #
    # answer = run_conversation(question)
    # print(f"Model>\t{answer}")

    question = "深圳、北京、杭州现在天气怎么样？"
    print(f"User>\t{question}")

    answer = run_conversation(question)
    print(f"Model>\t{answer}")