from typing import Optional

from datetime import datetime
from fastapi import APIRouter
from pydantic import create_model, BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from common.exception_handler import CustomException
from common.result import Result, PageInfo
from models import Notice

router = APIRouter(prefix="/notice", tags=["公告管理"])

NoticePydantic = pydantic_model_creator(Notice)

NoticeCreatePydantic = create_model(
    "NoticeCreatePydantic",
    **{
        name: (Optional[field.annotation], None)
        for name, field in NoticePydantic.model_fields.items()
    }
)


# 新增
@router.post("/add")
async def add(notice_create_pydantic: NoticeCreatePydantic):
    notice_create_pydantic.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 将参数转换成 字典数据
    create_data = notice_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await Notice.create(**create_data)  # no=xxx,name=xxx,college=xxx
    return Result.success()


# 更新
@router.put("/update")
async def add(notice_create_pydantic: NoticeCreatePydantic):
    if notice_create_pydantic.id is None:
        raise CustomException("缺少参数ID")
    # 将参数转换成 字典数据
    update_data = notice_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await Notice.filter(id=notice_create_pydantic.id).update(**update_data)  # no=xxx,name=xxx,college=xxx where id = xxx
    return Result.success()


# 删除
@router.delete('/delete/{notice_id}')
async def delete(notice_id: int):
    await Notice.filter(id=notice_id).delete()
    return Result.success()


# 单个查询
@router.get('/selectById/{notice_id}')
async def select_by_id(notice_id: int):
    notice = await Notice.get_or_none(id=notice_id)
    return Result.success(notice)


# 查询所有数据
@router.get('/selectAll')
async def select_all(title: str = ""):
    notice_list = await Notice.filter(title__contains=title).order_by("-id")  # title__contains表示根据name进行模糊查询
    return Result.success(notice_list)


# 分页查询数据
@router.get('/selectPage')
async def select_page(title: str = "", pageNum: int = 1, pageSize: int = 10):
    query = Notice.filter(title__contains=title)  # title__contains表示根据name进行模糊查询
    notice_list = await query.order_by("-id").offset((pageNum - 1) * pageSize).limit(pageSize)
    total = await query.count()
    # notice_list 转成字典数据
    notice_dict_list = [
        NoticePydantic.model_validate(notice).model_dump()
        for notice in notice_list
    ]
    page_info = PageInfo(list=notice_dict_list, total=total)
    return Result.success(page_info)
