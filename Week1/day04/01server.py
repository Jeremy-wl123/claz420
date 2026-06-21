from fastapi import FastAPI, Form, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# ========== 定义数据模型 ==========
class QueryModel(BaseModel):
    question: str
    page: Optional[int] = 1
    limit: Optional[int] = 10

class UserModel(BaseModel):
    username: str
    password: str

# ========== 1. 接收 JSON 数据（最常用）==========
@app.post("/api/query")
async def query_json(data: QueryModel):
    """接收 JSON 格式的请求"""
    return {
        "status": "success",
        "received": data.dict(),
        "message": f"收到问题: {data.question}，第{data.page}页"
    }

# ========== 2. 接收表单数据 ==========
@app.post("/api/login")
async def login_form(
    username: str = Form(...),
    password: str = Form(...)
):
    """接收表单格式的请求"""
    return {
        "status": "success",
        "username": username,
        "message": "登录成功" if username == "admin" and password == "123456" else "登录失败"
    }

# ========== 3. 接收 URL 查询参数 ==========
@app.post("/api/search")
async def search_params(
    keyword: str,
    page: int = 1,
    category: Optional[str] = None
):
    """接收 URL 查询参数（?key=value）"""
    return {
        "status": "success",
        "keyword": keyword,
        "page": page,
        "category": category,
        "results": [f"结果{i}" for i in range(1, 4)]
    }

# ========== 4. 接收路径参数 ==========
@app.post("/api/user/{user_id}")
async def get_user(
    user_id: int,
    name: Optional[str] = None
):
    """接收 URL 路径参数 + 查询参数"""
    return {
        "status": "success",
        "user_id": user_id,
        "name": name or "未提供",
        "message": f"查询用户 {user_id}"
    }

# ========== 5. 接收混合参数（JSON + 查询参数）==========
@app.post("/api/advanced")
async def advanced_query(
    data: QueryModel,
    token: Optional[str] = None  # 查询参数
):
    """同时接收 JSON 体和 URL 查询参数"""
    return {
        "status": "success",
        "question": data.question,
        "page": data.page,
        "token": token,
        "message": "混合参数接收成功"
    }

# ========== 6. 接收文件上传 ==========
@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """接收文件上传"""
    content = await file.read()
    return {
        "status": "success",
        "filename": file.filename,
        "file_size": len(content),
        "description": description,
        "content_type": file.content_type
    }

# ========== 7. 接收原始文本 ==========
@app.post("/api/raw")
async def raw_text(request):
    """接收原始文本（不常用）"""
    body = await request.body()
    text = body.decode('utf-8')
    return {
        "status": "success",
        "received_text": text,
        "length": len(text)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)