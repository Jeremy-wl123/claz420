# ai_client.py
from openai import AsyncOpenAI

class AIClient:
    """异步 AI 客户端，用于调用 LLM 生成内容"""
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def reason(self, messages: list, max_tokens: int = 4096) -> str:
        """异步发送消息并返回模型回复"""
        response = await self.client.chat.completions.create(
            model="deepseek-chat",   # 或 "deepseek-v4-pro"
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content