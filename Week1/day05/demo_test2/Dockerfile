# 使用轻量级 Python 基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装 Python 包
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码和静态文件
COPY 10nl2sql_fastapi.py .
COPY index.html .

# 暴露应用端口
EXPOSE 8000

# 启动命令（使用 uvicorn 运行 FastAPI）
CMD ["uvicorn", "10nl2sql_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]