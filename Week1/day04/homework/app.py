"""
应用入口
-------
FastAPI 应用创建、中间件配置、生命周期管理、启动入口。

启动方式：
    python app.py
    或
    uvicorn app:app --host 0.0.0.0 --port 8000

访问前端：
    http://localhost:8000
"""
# 必须最先导入，确保日志系统在其他模块使用 logging 前完成初始化
import utils.logger  # noqa: F401 触发 setup_logging()

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from model.database import create_demo_database
from model.schemas import QueryRequest, QueryResponse, ErrorResponse
from controller.query_controller import handle_query
from controller.health_controller import health_check
from utils.helpers import get_local_ip

logger = logging.getLogger(__name__)

# 静态文件目录（相对于本文件）
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


# ---------- 生命周期管理 ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动/关闭时的资源管理"""
    logger.info("应用启动，初始化数据库...")
    try:
        create_demo_database()
        logger.info("数据库初始化完成")
        local_ip = get_local_ip()
        logger.info(f"局域网访问地址: http://{local_ip}:8000")
        print(f"\n✅ 服务已启动，局域网访问: http://{local_ip}:8000\n")
    except Exception as e:
        logger.critical(f"数据库初始化失败: {e}", exc_info=True)
        raise
    yield
    # 关闭时清理（当前无需额外操作）


# ---------- 创建 FastAPI 应用 ----------
app = FastAPI(
    title="NL2SQL 教学服务",
    description="基于 DeepSeek 的自然语言转 SQL 查询接口",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------- CORS 中间件 ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请替换为具体前端地址
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- 挂载静态文件目录 ----------
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")


# ---------- API 端点注册 ----------
@app.get("/", response_model=None)
async def root():
    """返回前端页面"""
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.post("/query", response_model=QueryResponse, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def query(request: QueryRequest):
    """自然语言转 SQL 查询接口"""
    return await handle_query(request)


@app.get("/health")
async def health():
    """健康检查接口"""
    return await health_check()


# ---------- 直接运行入口 ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
