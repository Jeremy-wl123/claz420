import requests
import json

BASE_URL = "http://127.0.0.1:8000"


# ========== 1. 测试 JSON 数据 ==========
def test_json():
    print("=" * 50)
    print("1. 测试 JSON 数据")

    url = f"{BASE_URL}/api/query"
    data = {
        "question": "有哪些老师",
        "page": 2,
        "limit": 5
    }

    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


# ========== 2. 测试表单数据 ==========
def test_form():
    print("=" * 50)
    print("2. 测试表单数据")

    url = f"{BASE_URL}/api/login"
    data = {
        "username": "admin",
        "password": "123456"
    }

    # 使用 data= 发送表单
    response = requests.post(url, data=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


# ========== 3. 测试 URL 查询参数 ==========
def test_params():
    print("=" * 50)
    print("3. 测试 URL 查询参数")

    url = f"{BASE_URL}/api/search"
    params = {
        "keyword": "Python",
        "page": 3,
        "category": "编程"
    }

    # 使用 params= 添加查询参数
    response = requests.post(url, params=params)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


# ========== 4. 测试路径参数 ==========
def test_path_params():
    print("=" * 50)
    print("4. 测试路径参数")

    user_id = 1001
    url = f"{BASE_URL}/api/user/{user_id}"
    params = {"name": "张三"}  # 这是查询参数

    response = requests.post(url, params=params)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


# ========== 5. 测试混合参数 ==========
def test_mixed():
    print("=" * 50)
    print("5. 测试混合参数（JSON + 查询参数）")

    url = f"{BASE_URL}/api/advanced"
    json_data = {
        "question": "有哪些课程",
        "page": 1
    }
    params = {"token": "abc123"}

    # 同时使用 json= 和 params=
    response = requests.post(url, json=json_data, params=params)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


# ========== 6. 测试文件上传 ==========
def test_upload():
    print("=" * 50)
    print("6. 测试文件上传")

    url = f"{BASE_URL}/api/upload"
    files = {"file": ("test.txt", "这是文件内容", "text/plain")}
    data = {"description": "测试文件"}

    response = requests.post(url, files=files, data=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


# ========== 7. 测试原始文本 ==========
def test_raw():
    print("=" * 50)
    print("7. 测试原始文本")

    url = f"{BASE_URL}/api/raw"
    raw_text = "这是一段原始文本数据"

    # 发送原始字符串
    response = requests.post(url, data=raw_text, headers={"Content-Type": "text/plain"})
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


# ========== 8. 测试错误处理 ==========
def test_error_handling():
    print("=" * 50)
    print("8. 测试错误处理")

    url = f"{BASE_URL}/api/login"

    try:
        # 测试超时
        response = requests.post(url, json={"username": "test"}, timeout=0.001)
    except requests.exceptions.Timeout:
        print("⏰ 请求超时")
    except requests.exceptions.ConnectionError:
        print("🔌 连接失败")

    # 测试错误状态码
    response = requests.post(f"{BASE_URL}/api/notexist")
    if response.status_code == 404:
        print("❌ 接口不存在 (404)")
    print()


# ========== 9. 测试请求头 ==========
def test_headers():
    print("=" * 50)
    print("9. 测试自定义请求头")

    url = f"{BASE_URL}/api/query"
    headers = {
        "Authorization": "Bearer token_here",
        "User-Agent": "MyTestApp/1.0",
        "X-Custom-Header": "custom_value"
    }
    json_data = {"question": "有请求头的查询"}

    response = requests.post(url, json=json_data, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


# ========== 10. 测试会话保持 ==========
def test_session():
    print("=" * 50)
    print("10. 测试会话保持")

    session = requests.Session()

    # 第一次请求
    response1 = session.post(f"{BASE_URL}/api/login", data={"username": "admin", "password": "123456"})
    print(f"第一次响应: {response1.json()}")

    # 第二次请求（会话会自动携带 cookies）
    response2 = session.post(f"{BASE_URL}/api/query", json={"question": "会话中的查询"})
    print(f"第二次响应: {response2.json()}")
    print()


# ========== 主函数 ==========
if __name__ == "__main__":
    print("\n🚀 开始测试 FastAPI 接口\n")

    test_json()
    test_form()
    test_params()
    test_path_params()
    test_mixed()
    test_upload()
    test_raw()
    test_error_handling()
    test_headers()
    test_session()

    print("✅ 所有测试完成！")