import requests, json
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def get_weather(city):
    """
    查询高德地图天气函数
    :param city_adcode: 必要参数，字符串类型，城市的 adcode 编码，例如北京市是 110000
    :return：高德地图天气 API 查询结果，JSON 格式字符串，包含实况/预报天气信息
    """
    # Step 1. 高德地图天气 API 地址
    url = "https://restapi.amap.com/v3/weather/weatherInfo"

    # Step 2. 设置请求参数（完全按高德官方要求）
    params = {
        "key": os.getenv("GAODE_API_KEY"),  # 高德 Web 服务 API Key
        "city": city,                       # 城市
        "extensions": "all",               # base=实况天气，all=预报天气
        "output": "json"                    # 返回 JSON 格式
    }

    # Step 3. 发送 GET 请求
    response = requests.get(url, params=params)

    # Step 4. 解析响应并返回 JSON 字符串
    data = response.json()
    return json.dumps(data, ensure_ascii=False, indent=2)

print(get_weather("深圳")) # 查询深圳天气
print(get_weather("北京")) # 查询北京天气