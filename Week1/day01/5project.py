import json
import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
)

load_dotenv()

# ---------------------------------------------------------------------------
# 类型 & 配置
# ---------------------------------------------------------------------------
Provider = Literal["qwen", "deepseek"]

PROVIDER_CONFIGS: dict[Provider, dict] = {
    "qwen": {
        "api_key_env": "DASHSCOPE_API_KEY",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
    },
    "deepseek": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
    },
}


# ---------------------------------------------------------------------------
# LLM 封装类
# ---------------------------------------------------------------------------
class LLMClient:
    """统一封装 Qwen / DeepSeek 调用。"""

    def __init__(self, provider: Provider):
        config = PROVIDER_CONFIGS[provider]
        api_key = os.getenv(config["api_key_env"])
        if not api_key:
            raise RuntimeError(
                f"未检测到环境变量 {config['api_key_env']}，"
                f"请检查 .env 文件"
            )

        self.provider = provider
        self.model = config["model"]
        self.client = OpenAI(
            api_key=api_key,
            base_url=config["base_url"],
            timeout=60.0,
            max_retries=2,
        )

    def chat(
        self,
        messages: list[ChatCompletionMessageParam],
        **kwargs,
    ) -> ChatCompletion:
        """发送对话请求，返回完整的 ChatCompletion 对象。"""
        request_kwargs: dict = {
            "model": self.model,
            "messages": messages,
            **kwargs,
        }

        if self.provider == "deepseek":
            request_kwargs.setdefault("extra_body", {})
            request_kwargs["extra_body"].setdefault(
                "thinking", {"type": "enabled"}
            )

        return self.client.chat.completions.create(**request_kwargs)

    def ask(
        self,
        messages: list[ChatCompletionMessageParam],
        **kwargs,
    ) -> str:
        """发送对话请求，直接返回文本回复。"""
        response = self.chat(messages, **kwargs)
        return response.choices[0].message.content or ""


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------
def save_response(response: ChatCompletion, filename: str = "output.json") -> str:
    """将 ChatCompletion 保存为 JSON 文件，返回文件路径。"""
    output_path = os.path.join(os.path.dirname(__file__), filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.model_dump_json(indent=2, ensure_ascii=False))
    return output_path


# ---------------------------------------------------------------------------
# 演示
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    messages= [
        {"role": "system", "content": "你是一名 AI 课程助教。"},
        {"role": "user", "content": "请用一句话解释 API Key 的作用。"},
    ]

    # Qwen
    print("=" * 50)
    print("Qwen 回复：")
    qwen = LLMClient("qwen")
    qwen_response = qwen.chat(messages)
    print(qwen.ask(messages))

    # DeepSeek
    print("=" * 50)
    print("DeepSeek 回复：")
    deepseek = LLMClient("deepseek")
    print(deepseek.ask(messages))

    # 保存完整响应
    path = save_response(qwen_response, "qwen_output.json")
    print(f"\nQwen 完整响应已保存至: {path}")