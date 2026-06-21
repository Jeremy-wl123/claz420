import asyncio
import json
import logging
import os
import socket
from contextlib import asynccontextmanager
from pathlib import Path

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

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

STATIC_DIR = Path(__file__).parent / "static"

client = AsyncOpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    timeout=60.0,
)

# ---------- System Prompt（引导 Markdown 输出）----------
SYSTEM_PROMPT = (
    "你是一名专业助手。"
)


# ---------- 生命周期 ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动/关闭时的资源管理"""
    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except Exception:
            local_ip = "127.0.0.1"
    print(f"\n✅ 服务已启动，局域网访问: http://{local_ip}:8000\n")
    logger.info(f"服务启动，局域网: http://{local_ip}:8000")
    yield
    # 关闭时清理
    logger.info("服务关闭")


app = FastAPI(title="Ollama Chat API", lifespan=lifespan)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


# ---------- Pydantic 模型 ----------
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    answer: str
    model: str


# ---------- 静态文件 ----------
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    """返回聊天机器人前端页面"""
    index_path = STATIC_DIR / "chat.html"
    if not index_path.exists():
        return {"message": "前端页面未找到，请创建 static/chat.html"}
    return FileResponse(str(index_path))


# ---------- API 端点 ----------
@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "model": LLM_MODEL}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """非流式聊天（保留兼容）"""
    try:
        response = await client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message},
            ],
            temperature=0.2,
        )
    except Exception as exc:
        logger.error(f"LLM调用失败: {exc}", exc_info=True)
        raise HTTPException(status_code=502, detail="模型服务暂时不可用") from exc

    answer = response.choices[0].message.content or ""
    return ChatResponse(answer=answer, model=LLM_MODEL)


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    流式聊天端点（SSE）
    前端通过 EventSource 或 fetch + ReadableStream 消费流式输出。
    """

    async def stream_generator():
        try:
            stream = await client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": request.message},
                ],
                temperature=0.2,
                stream=True,
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield f"data: {json.dumps({'content': delta.content}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except asyncio.CancelledError:
            logger.info("客户端断开连接，流式调用已取消")
            raise
        except Exception as e:
            logger.error(f"流式调用失败: {e}", exc_info=True)
            yield f"data: {json.dumps({'error': '模型服务暂时不可用'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        stream_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 nginx 缓冲
        },
    )


# ---------- 直接运行入口 ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
