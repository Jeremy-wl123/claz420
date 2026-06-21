from typing import Optional

from fastapi import APIRouter
from pydantic import create_model, BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from common.exception_handler import CustomException
from common.result import Result, PageInfo
from models import Major

router = APIRouter(prefix="/major",tags=["专业"])

MajorPydantic = pydantic_model_creator(Major)

MajorCreatePydantic = create_model(
    "MajorCreatePydantic",
    **{
        name: (Optional[field.annotation], None)
        for name, field in MajorPydantic.model_fields.items()
    }
)


# 新增
@router.post("/add")
async def add(major_create_pydantic: MajorCreatePydantic):
    db_major = await Major.get_or_none(no=major_create_pydantic.no)
    if db_major is not None:
        raise CustomException("专业代码重复")
    # 将参数转换成 字典数据
    create_data = major_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await Major.create(**create_data)  # no=xxx,name=xxx,college=xxx
    return Result.success()


# 更新
@router.put("/update")
async def add(major_create_pydantic: MajorCreatePydantic):
    if major_create_pydantic.id is None:
        raise CustomException("缺少参数ID")
    # 将参数转换成 字典数据
    update_data = major_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await Major.filter(id=major_create_pydantic.id).update(**update_data)  # no=xxx,name=xxx,college=xxx where id = xxx
    return Result.success()


# 删除
@router.delete('/delete/{major_id}')
async def delete(major_id: int):
    await Major.filter(id=major_id).delete()
    return Result.success()


# 单个查询
@router.get('/selectById/{major_id}')
async def select_by_id(major_id: int):
    major = await Major.get_or_none(id=major_id)
    return Result.success(major)


# 查询所有数据
@router.get('/selectAll')
async def select_all(name: str = ""):
    major_list = await Major.filter(name__contains=name)  # name__contains表示根据name进行模糊查询
    return Result.success(major_list)


# 分页查询数据
@router.get('/selectPage')
async def select_page(name: str = "", pageNum: int = 1, pageSize: int = 10):
    query = Major.filter(name__contains=name)  # name__contains表示根据name进行模糊查询
    major_list = await query.order_by("-id").offset((pageNum - 1) * pageSize).limit(pageSize)
    total = await query.count()
    # major_list 转成字典数据
    major_dict_list = [
        MajorPydantic.model_validate(major).model_dump()
        for major in major_list
    ]
    page_info = PageInfo(list=major_dict_list, total=total)
    return Result.success(page_info)
