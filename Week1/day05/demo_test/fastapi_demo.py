from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(title="AI Chat API")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="用户问题")


class ChatResponse(BaseModel):
    answer: str


def call_llm(message: str) -> str:
    # 第一版先使用模拟回答，后续替换成真实模型调用。
    return f"AI收到你的问题：{message}"


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        answer = call_llm(request.message)
        return ChatResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="模型调用失败",
        ) from exc

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)