from typing import Optional

from fastapi import APIRouter
from pydantic import create_model, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from common.exception_handler import CustomException
from common.result import Result, PageInfo
from models import Student, Clazz

router = APIRouter(prefix="/student", tags=["学生管理"])

StudentPydantic = pydantic_model_creator(Student)

StudentCreatePydantic = create_model(
    "StudentCreatePydantic",
    **{
        name: (Optional[field.annotation], None)
        for name, field in StudentPydantic.model_fields.items()
    },
    clazz_id=(Optional[int], Field(None, alias="clazzId"))
)


# 新增
@router.post("/add")
async def add(student_create_pydantic: StudentCreatePydantic):
    db_student = await Student.get_or_none(username=student_create_pydantic.username)
    if db_student is not None:
        raise CustomException("账号重复")
    student_create_pydantic.score = 0
    # 将参数转换成 字典数据
    create_data = student_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    create_data['role'] = '学生'  # 设置默认的角色
    create_data['password'] = '123'  # 设置默认的密码
    await Student.create(**create_data)  # no=xxx,name=xxx,college=xxx
    return Result.success()


# 更新
@router.put("/update")
async def add(student_create_pydantic: StudentCreatePydantic):
    if student_create_pydantic.id is None:
        raise CustomException("缺少参数ID")
    # 将参数转换成 字典数据
    update_data = student_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await Student.filter(id=student_create_pydantic.id).update(**update_data)  # no=xxx,name=xxx,college=xxx where id = xxx
    return Result.success()


# 删除
@router.delete('/delete/{student_id}')
async def delete(student_id: int):
    await Student.filter(id=student_id).delete()
    return Result.success()


# 单个查询
@router.get('/selectById/{student_id}')
async def select_by_id(student_id: int):
    student = await Student.get_or_none(id=student_id)
    return Result.success(student)


# 查询所有数据
@router.get('/selectAll')
async def select_all(name: str = ""):
    student_list = await Student.filter(name__contains=name)  # name__contains表示根据name进行模糊查询
    return Result.success(student_list)


# 分页查询数据
@router.get('/selectPage')
async def select_page(name: str = "", clazzName: str = "", majorName: str = "", pageNum: int = 1, pageSize: int = 10):
    # name__contains表示根据name进行模糊查询  prefetch_related 关联查询到 major模块的数据
    query = Student.filter(name__contains=name)
    if clazzName and clazzName != "":
        query = query.filter(clazz__name__contains=clazzName)
    if majorName and clazzName != "":
        query = query.filter(clazz__major__name__contains=majorName)
    query = query.prefetch_related("clazz__major")
    student_list = await query.order_by("-id").offset((pageNum - 1) * pageSize).limit(pageSize)
    total = await query.count()
    # student_list 转成字典数据
    # majorName 怎么返回？？
    # {id=xxx, name=xxx, no=xxx}
    student_dict_list = [
        {
            **StudentPydantic.model_validate(student).model_dump(),  # id=xxx,no=xxx,name=xxx
            "clazzId": student.clazz.id if student.clazz else None,
            "clazzName": student.clazz.name if student.clazz else None,
            "majorName": student.clazz.major.name if student.clazz and student.clazz.major else None
        }
        for student in student_list
    ]
    page_info = PageInfo(list=student_dict_list, total=total)
    return Result.success(page_info)
