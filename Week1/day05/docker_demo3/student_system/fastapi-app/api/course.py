from typing import Optional

from fastapi import APIRouter
from pydantic import create_model, BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from common.exception_handler import CustomException
from common.result import Result, PageInfo
from models import Course

router = APIRouter(prefix="/course",tags=['课程管理'])

CoursePydantic = pydantic_model_creator(Course)

CourseCreatePydantic = create_model(
    "CourseCreatePydantic",
    **{
        name: (Optional[field.annotation], None)
        for name, field in CoursePydantic.model_fields.items()
    },
    major_id=(Optional[int], Field(None, alias="majorId"))
)


# 新增
@router.post("/add")
async def add(course_create_pydantic: CourseCreatePydantic):
    db_course = await Course.get_or_none(no=course_create_pydantic.no)
    if db_course is not None:
        raise CustomException("课程编号重复")
    # 将参数转换成 字典数据
    create_data = course_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await Course.create(**create_data)  # no=xxx,name=xxx,college=xxx
    return Result.success()


# 更新
@router.put("/update")
async def add(course_create_pydantic: CourseCreatePydantic):
    if course_create_pydantic.id is None:
        raise CustomException("缺少参数ID")
    # 将参数转换成 字典数据
    update_data = course_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await Course.filter(id=course_create_pydantic.id).update(**update_data)  # no=xxx,name=xxx,college=xxx where id = xxx
    return Result.success()


# 删除
@router.delete('/delete/{course_id}')
async def delete(course_id: int):
    await Course.filter(id=course_id).delete()
    return Result.success()


# 单个查询
@router.get('/selectById/{course_id}')
async def select_by_id(course_id: int):
    course = await Course.get_or_none(id=course_id)
    return Result.success(course)


# 查询所有数据
@router.get('/selectAll')
async def select_all(name: str = "", majorId: int = 0):
    query = Course.all()
    if majorId > 0:
        query = query.prefetch_related("major").filter(major__id=majorId)
    course_list = await query.filter(name__contains=name)
    return Result.success(course_list)


# 分页查询数据
@router.get('/selectPage')
async def select_page(name: str = "", no: str = "", teacher: str = "",  majorId: int = 0, pageNum: int = 1, pageSize: int = 10):
    # name__contains表示根据name进行模糊查询  prefetch_related 关联查询到 major模块的数据
    query = (Course.filter(name__contains=name).filter(no__contains=no).filter(teacher__contains=teacher)
             .prefetch_related("major"))
    if majorId and majorId > 0:
        query = query.filter(major__id=majorId)
    course_list = await query.order_by("-id").offset((pageNum - 1) * pageSize).limit(pageSize)
    total = await query.count()
    course_dict_list = [
        {
            **CoursePydantic.model_validate(course).model_dump(),  # id=xxx,no=xxx,name=xxx
            "majorName": course.major.name if course.major else None
        }
        for course in course_list
    ]
    page_info = PageInfo(list=course_dict_list, total=total)
    return Result.success(page_info)
