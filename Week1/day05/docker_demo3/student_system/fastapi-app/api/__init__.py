import importlib
import pkgutil

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from common.exception_handler import CustomException
from common.result import Result
from models import Admin, Student


class Account(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    username: str | None = None
    password: str | None = None
    newPassword: str | None = None
    role: str | None = None
    name: str | None = None
    avatar: str | None = None
    clazzId: int | None = None
    majorId: int | None = None
    score: int | None = None


api_router = APIRouter()


# 登录
@api_router.post("/login")
async def login(account: Account):
    if account.role == '管理员':
        admin = await Admin.get_or_none(username=account.username)
        if admin is None:
            raise CustomException("账号或密码错误")
        if admin.password != account.password:
            raise CustomException("账号或密码错误")
        account = Account.model_validate(admin)
    elif account.role == '学生':
        student = await Student.get_or_none(username=account.username).prefetch_related("clazz__major")
        if student is None:
            raise CustomException("账号或密码错误")
        if student.password != account.password:
            raise CustomException("账号或密码错误")
        account = Account.model_validate(student)
        account.clazzId = student.clazz.id if student and student.clazz else None
        account.majorId = student.clazz.major.id if student and student.clazz and student.clazz.major else None
    else:
        raise CustomException("角色错误")
    return Result.success(account)


# 注册
@api_router.post("/register")
async def register(account: Account):
    if account.username is None:
        raise CustomException("账号不能为空")
    if account.password is None:
        raise CustomException("密码不能为空")
    # 设置默认的name
    if account.name is None:
        account.name = account.username
    student = await Student.get_or_none(username=account.username)
    if student is not None:
        raise CustomException("账号已存在")
    create_data = account.model_dump(exclude_unset=True, exclude={"id"})
    create_data['score'] = 0
    await Student.create(**create_data)
    return Result.success()


# 修改密码
@api_router.put("/updatePassword")
async def update_password(account: Account):
    if account.role == '管理员':
        admin = await Admin.get_or_none(id=account.id)
        if admin is None:
            raise CustomException("未找到用户")
        if admin.password != account.password:
            raise CustomException("原密码错误")
        if admin.password == account.newPassword:
            raise CustomException("新密码不能原密码跟相同")
        await Admin.filter(id=admin.id).update(password=account.newPassword)
    if account.role == '学生':
        student = await Student.get_or_none(id=account.id)
        if student is None:
            raise CustomException("未找到用户")
        if student.password != account.password:
            raise CustomException("原密码错误")
        if student.password == account.newPassword:
            raise CustomException("新密码不能原密码跟相同")
        await Student.filter(id=student.id).update(password=account.newPassword)
    return Result.success(account)


# 自动导入当前目录下的所有模块
for _, module_name, _ in pkgutil.iter_modules(__path__, __name__ + "."):
    module = importlib.import_module(module_name)
    if hasattr(module, "router"):
        # 假设每个端点文件都有一个 router 变量
        api_router.include_router(module.router)
