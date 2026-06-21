FROM python:3.10-slim

WORKDIR /app

# 安装依赖
COPY fastapi-app/requirements_1.txt .
RUN pip install --no-cache-dir -r requirements_1.txt

# 复制后端代码
COPY fastapi-app/ .

# 上传文件目录
VOLUME ["/app/files"]

EXPOSE 9090

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090"]
