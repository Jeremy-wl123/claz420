import json
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

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
    """发送消息给大模型，并记录请求和响应关键信息。"""
    logger.info(f"发起大模型调用，模型: {MODEL_NAME}")
    logger.debug(f"请求消息: {json.dumps(messages, ensure_ascii=False, indent=2)}")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    choice = response.choices[0]
    assistant_msg = choice.message

    # 记录响应概览
    if assistant_msg.tool_calls:
        tool_names = [tc.function.name for tc in assistant_msg.tool_calls]
        logger.info(f"模型返回工具调用请求: {tool_names}")
        logger.debug(f"完整工具调用参数: {[tc.function.arguments for tc in assistant_msg.tool_calls]}")
    else:
        content_preview = (assistant_msg.content or "").replace('\n', ' ')[:100]
        logger.info(f"模型直接返回文本（无工具调用）: {content_preview}...")

    return choice


def execute_tool(tool_call) -> str:
    """执行具体的工具函数，并记录执行过程和结果。"""
    function_name = tool_call.function.name
    logger.info(f"执行工具: {function_name}")

    try:
        arguments = json.loads(tool_call.function.arguments)
        logger.debug(f"工具参数: {json.dumps(arguments, ensure_ascii=False)}")
    except json.JSONDecodeError as e:
        error_msg = json.dumps(
            {"error": "模型生成的工具参数不是合法 JSON"},
            ensure_ascii=False,
        )
        logger.error(f"工具参数解析失败: {e}")
        return error_msg

    if function_name == "get_weather":
        location = arguments.get("location")
        if not location:
            error_msg = json.dumps(
                {"error": "缺少必填参数 location"},
                ensure_ascii=False,
            )
            logger.warning(f"工具 {function_name} 调用缺少 location 参数")
            return error_msg

        result = get_weather(location)
        logger.info(f"工具 {function_name} 执行成功，查询地点: {location}")
        logger.debug(f"工具返回结果: {json.dumps(result, ensure_ascii=False)}")
        return json.dumps(result, ensure_ascii=False)

    error_msg = json.dumps(
        {"error": f"未注册的工具：{function_name}"},
        ensure_ascii=False,
    )
    logger.error(f"尝试调用未注册工具: {function_name}")
    return error_msg


def run_conversation(user_input: str) -> str:
    """运行完整的对话流程，包含多轮工具调用（当前仅一轮）。"""
    logger.info(f"用户输入: {user_input}")

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

    # 第一次调用模型
    first_choice = send_messages(messages)
    assistant_message = first_choice.message

    # 若无工具调用，直接返回文本
    if not assistant_message.tool_calls:
        final_content = assistant_message.content or "模型未返回有效内容。"
        logger.info(f"最终回答（无工具调用）: {final_content[:100]}...")
        return final_content

    # 将助手消息加入对话历史
    messages.append(assistant_message.model_dump(exclude_none=True))

    # 执行所有工具调用（当前仅一轮，但支持多个）
    for tool_call in assistant_message.tool_calls:
        tool_result = execute_tool(tool_call)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result,
            }
        )

    # 第二次调用模型，获取最终答案
    logger.info("将工具结果返回模型，请求最终回答")
    final_choice = send_messages(messages)
    final_content = final_choice.message.content or "模型未返回最终回答。"
    logger.info(f"最终回答: {final_content[:200]}...")
    return final_content


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