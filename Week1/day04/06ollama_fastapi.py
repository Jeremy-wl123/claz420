import json
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import socket
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

# ---------- 日志 ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------- 配置 ----------
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:0.6b")

STATIC_DIR = Path(__file__).parent / "static"

client = AsyncOpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    timeout=60.0,
)


# ---------- 生命周期 ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动/关闭时的资源管理"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        local_ip = ip
        print(f"\n✅ 服务已启动，局域网访问: http://{local_ip}:8000\n")
        logger.info(f"服务启动，局域网: http://{local_ip}:8000")
    except Exception:
        print("⚠️ 无法获取局域网IP，仅可通过 localhost 访问")
    yield
    # 关闭时清理
    logger.info("服务关闭")


app = FastAPI(title="Ollama Chat API", lifespan=lifespan)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    answer: str
    model: str


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = await client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一名语言简洁的助手，每次只回复100字以内",
                },
                {
                    "role": "user",
                    "content": request.message,
                },
            ],
            temperature=0.2,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="模型服务暂时不可用",
        ) from exc

    answer = response.choices[0].message.content or ""
    return ChatResponse(answer=answer, model=LLM_MODEL)

# ---------- 直接运行入口 ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
