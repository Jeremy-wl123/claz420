# weather_assistant.py
import json
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 中的环境变量

# ---------- 配置 ----------
MODEL_NAME = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")  # 可用 deepseek-chat
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GAODE_API_KEY = os.getenv("GAODE_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)


# ---------- 真实天气查询（高德地图 API）----------
def get_real_weather(location: str) -> dict:
    """
    调用高德地图天气 API 获取指定城市的实况天气。
    参数 location: 城市名称，如 "杭州"、"北京"；也支持 "杭州，浙江" 格式，会自动提取城市名。
    返回统一格式的天气字典，包含 temperature（温度）、condition（天气状况）、unit（单位）等字段。
    """
    # 从 "杭州，浙江" 或 "杭州" 中提取城市名（逗号/空格前部分）
    city = location.split("，")[0].split(",")[0].strip()

    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "key": GAODE_API_KEY,
        "city": city,
        "extensions": "base",  # base = 实况天气
        "output": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        # 检查高德返回状态
        if data.get("status") != "1":
            return {
                "error": f"高德 API 返回错误: {data.get('info', '未知错误')}",
                "location": location
            }

        lives = data.get("lives", [])
        if not lives:
            return {
                "error": f"未查询到城市 '{city}' 的天气数据",
                "location": location
            }

        live = lives[0]  # 取第一条实况数据
        # 高德返回的温度是字符串，天气现象是中文
        return {
            "location": live.get("city", city),
            "temperature": int(live.get("temperature", 0)),
            "unit": "celsius",
            "condition": live.get("weather", "未知"),
            "humidity": live.get("humidity", ""),     # 湿度（额外信息）
            "wind": live.get("winddirection", "") + live.get("windpower", "")
        }
    except Exception as e:
        return {
            "error": f"天气服务异常: {str(e)}",
            "location": location
        }


# ---------- 工具定义（OpenAI Function Calling 格式）----------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前实时天气。当用户询问温度、天气状况、是否适合出行等需要实时气象信息时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：杭州、北京、深圳。如果用户提供了省份信息，只需提取城市名。"
                    }
                },
                "required": ["location"],
            },
        },
    }
]


def send_messages(messages):
    """调用 DeepSeek 模型，自动判断是否使用工具"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    return response.choices[0]


def execute_tool(tool_call) -> str:
    """执行模型请求的工具，并返回标准 JSON 字符串结果"""
    function_name = tool_call.function.name

    try:
        arguments = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError:
        return json.dumps({"error": "模型生成的工具参数不是合法 JSON"}, ensure_ascii=False)

    if function_name == "get_weather":
        location = arguments.get("location")
        if not location:
            return json.dumps({"error": "缺少必填参数 location"}, ensure_ascii=False)

        # 调用真实天气 API
        weather_data = get_real_weather(location)

        # 如果返回结果中包含 error 字段，直接返回错误信息；否则返回标准天气数据
        if "error" in weather_data:
            return json.dumps(weather_data, ensure_ascii=False)
        else:
            # 只保留给模型的最关键字段，避免冗余信息
            simplified = {
                "location": weather_data["location"],
                "temperature": weather_data["temperature"],
                "unit": weather_data["unit"],
                "condition": weather_data["condition"],
            }
            return json.dumps(simplified, ensure_ascii=False)

    return json.dumps({"error": f"未注册的工具：{function_name}"}, ensure_ascii=False)


def run_conversation(user_input: str) -> str:
    """处理单轮用户问题，自动调用工具（如果需要），返回最终文本回答"""
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个专业的天气助手。当用户询问天气时，必须调用 get_weather 工具获取实时数据，"
                "绝对不能编造天气信息。请用中文回答，回答要自然、友好，可以适当补充湿度、风力等额外信息（如果工具返回了）。"
            ),
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    # 第一次调用模型（可能触发工具调用）
    first_choice = send_messages(messages)
    assistant_message = first_choice.message

    # 如果模型没有要求调用工具，直接返回文本回答
    if not assistant_message.tool_calls:
        return assistant_message.content or "模型未返回有效内容。"

    # 将模型的工具调用请求加入对话历史
    messages.append(assistant_message.model_dump(exclude_none=True))

    # 依次执行每个工具调用
    for tool_call in assistant_message.tool_calls:
        tool_result = execute_tool(tool_call)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result,
        })

    # 第二次调用模型：将工具返回结果输入，让模型生成最终自然语言回答
    final_choice = send_messages(messages)
    return final_choice.message.content or "模型未返回最终回答。"


# ---------- 测试示例 ----------
if __name__ == "__main__":
    test_questions = [
        "杭州，浙江现在天气怎么样？",
        "北京现在天气怎么样？",
        "深圳今天天气好吗？"
    ]

    for q in test_questions:
        print(f"User>\t{q}")
        answer = run_conversation(q)
        print(f"Model>\t{answer}\n")