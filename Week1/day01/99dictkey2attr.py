from pydantic import BaseModel

class Res(BaseModel):
    key1:str



r={'key1':'value'}
r1=Res.model_validate(r)
print(r1.key1)

# 简易案例：模拟 API 返回的响应对象（实际 SDK 内部类似这样实现）
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str
    reasoning_content: str | None = None   # 可选字段

class Choice(BaseModel):
    index: int
    message: Message

class Response(BaseModel):
    choices: list[Choice]

# ========== 模拟 API 返回的 JSON 数据 ==========
fake_json = {
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "递归就是函数调用自身。",
                "reasoning_content": "用户问递归，先解释定义，再给例子。"
            }
        }
    ]
}

# SDK 内部将 JSON 解析为对象
response_obj = Response.model_validate(fake_json)

# ========== 方式1：属性访问（推荐） ==========
reasoning = response_obj.choices[0].message.reasoning_content
content = response_obj.choices[0].message.content
print("【属性访问】")
print('reasoning_content:',response_obj.choices[0].message.reasoning_content)
print('message:',response_obj.choices[0].message)
print('choices[0]:',response_obj.choices[0])
print(f"思考内容: {reasoning}")
print(f"最终回答: {content}")

# ========== 方式2：字典 key 访问（不推荐，需要知道底层结构） ==========
# 如果强行把对象转成字典，或者原始 json 还在
print("\n【字典访问】")
# 先转成字典
obj_dict = response_obj.model_dump()
reasoning_dict = obj_dict["choices"][0]["message"]["reasoning_content"]
content_dict = obj_dict["choices"][0]["message"]["content"]
print(f"思考内容: {reasoning_dict}")
print(f"最终回答: {content_dict}")

# ========== 对比好处 ==========
print("\n【对比】")
print("✓ 属性访问：有 IDE 自动补全，拼写错误在编码阶段就能发现")
print("✓ 属性访问：代码更简洁、可读性高")
print("✗ 字典 key：需要记住字符串名字，容易写错（如 'reasoning_content' 少个下划线）")
print("✗ 字典 key：字段名变化时，只能运行时才能发现错误")