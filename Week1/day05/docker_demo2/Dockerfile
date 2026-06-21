FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 替换为国内镜像源，加速 pip 安装
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# ---- 先复制依赖文件，利用 Docker 缓存层 ----
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ---- 复制项目文件 ----
COPY 10nl2sql_fastapi.py .
COPY index.html .

# ---- 暴露端口 ----
EXPOSE 8000

# ---- 通过环境变量配置数据库和 API Key（作为默认值，docker-compose.yml 可覆盖）----
ENV DB_HOST=localhost \
    DB_PORT=3306 \
    DB_USER=root \
    DB_PASSWORD=123456 \
    DB_NAME=teaching \
    PYTHONUNBUFFERED=1

# ---- 创建非 root 用户，提升容器安全性 ----
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app
USER appuser

# ---- 健康检查 ----
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# ---- 启动命令 ----
CMD ["python", "10nl2sql_fastapi.py"]
