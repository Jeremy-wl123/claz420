import ast
import json
import operator
import os
from typing import Any, Callable

from openai import OpenAI


MAX_STEPS = 6

COURSES = {
    "RAG": {
        "hours": 12,
        "prerequisites": ["Python", "大模型 API", "Prompt"],
        "description": "学习文档处理、向量检索、重排与答案生成。",
    },
    "Agent": {
        "hours": 10,
        "prerequisites": ["Prompt", "Function Calling", "RAG"],
        "description": "学习目标、工具、状态、循环与安全边界。",
    },
}


def get_course_info(course_name: str) -> dict[str, Any]:
    """查询课程基础信息。"""
    course = COURSES.get(course_name)
    if course is None:
        return {
            "ok": False,
            "data": None,
            "error_code": "COURSE_NOT_FOUND",
            "message": f"未找到课程：{course_name}",
        }

    return {
        "ok": True,
        "data": {"name": course_name, **course},
        "error_code": None,
        "message": "查询成功",
    }


ALLOWED_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate_expression(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return evaluate_expression(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    if isinstance(node, ast.BinOp):
        operation = ALLOWED_BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("只支持加、减、乘、除")
        return operation(
            evaluate_expression(node.left),
            evaluate_expression(node.right),
        )

    if isinstance(node, ast.UnaryOp):
        operation = ALLOWED_UNARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("不支持该一元运算")
        return operation(evaluate_expression(node.operand))

    raise ValueError("表达式包含不允许的内容")


def calculate(expression: str) -> dict[str, Any]:
    """安全计算简单四则运算，不使用 eval。"""
    try:
        tree = ast.parse(expression, mode="eval")
        value = evaluate_expression(tree)
        return {
            "ok": True,
            "data": {"expression": expression, "result": value},
            "error_code": None,
            "message": "计算成功",
        }
    except (SyntaxError, ValueError, ZeroDivisionError) as exc:
        return {
            "ok": False,
            "data": None,
            "error_code": "INVALID_EXPRESSION",
            "message": str(exc),
        }


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_info",
            "description": "查询指定课程的课时、前置知识和课程说明。",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_name": {
                        "type": "string",
                        "description": "课程名称，例如 RAG 或 Agent。",
                    }
                },
                "required": ["course_name"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算只包含数字、括号和加减乘除的表达式。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "需要计算的表达式，例如 12 * 45。",
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
    },
]

TOOL_REGISTRY: dict[str, Callable[..., dict[str, Any]]] = {
    "get_course_info": get_course_info,
    "calculate": calculate,
}


def execute_tool(name: str, arguments_json: str) -> dict[str, Any]:
    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        return {
            "ok": False,
            "data": None,
            "error_code": "TOOL_NOT_ALLOWED",
            "message": f"工具未注册或不允许调用：{name}",
        }

    try:
        arguments = json.loads(arguments_json)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "data": None,
            "error_code": "INVALID_JSON",
            "message": f"工具参数不是合法 JSON：{exc}",
        }

    try:
        return tool(**arguments)
    except TypeError as exc:
        return {
            "ok": False,
            "data": None,
            "error_code": "INVALID_ARGUMENTS",
            "message": f"工具参数不符合要求：{exc}",
        }
    except Exception as exc:
        return {
            "ok": False,
            "data": None,
            "error_code": "TOOL_EXECUTION_ERROR",
            "message": f"工具执行失败：{exc}",
        }


def create_client() -> tuple[OpenAI, str]:
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")

    if not api_key:
        raise RuntimeError("未配置环境变量 LLM_API_KEY")
    if not base_url:
        raise RuntimeError("未配置环境变量 LLM_BASE_URL")
    if not model:
        raise RuntimeError("未配置环境变量 LLM_MODEL")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=60.0,
        max_retries=2,
    )
    return client, model


def run_agent(user_input: str) -> str:
    client, model = create_client()

    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "你是课程学习助手。"
                "课程信息必须通过工具查询，不得编造。"
                "数学计算应使用 calculate 工具。"
                "获得足够信息后，直接给出简洁、清晰的最终回答。"
            ),
        },
        {"role": "user", "content": user_input},
    ]

    for step in range(1, MAX_STEPS + 1):
        print(f"\n--- Agent Step {step} ---")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message
        messages.append(assistant_message.model_dump(exclude_none=True))

        if not assistant_message.tool_calls:
            return assistant_message.content or "任务已结束，但模型没有返回内容。"

        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            arguments_json = tool_call.function.arguments

            print(f"调用工具：{tool_name}")
            print(f"工具参数：{arguments_json}")

            result = execute_tool(tool_name, arguments_json)
            print(f"工具结果：{result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )

    return "任务未在最大步骤数内完成，已停止执行。"


if __name__ == "__main__":
    question = input("用户：").strip()
    if not question:
        raise SystemExit("输入不能为空")

    answer = run_agent(question)
    print(f"\nAgent：{answer}")