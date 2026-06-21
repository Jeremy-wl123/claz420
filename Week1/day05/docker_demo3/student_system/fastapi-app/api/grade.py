from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import create_model, BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.expressions import F

from common.exception_handler import CustomException
from common.result import Result, PageInfo
from models import Grade, Student, Course

router = APIRouter(prefix="/grade", tags=["成绩管理"])

GradePydantic = pydantic_model_creator(Grade)

GradeCreatePydantic = create_model(
    "GradeCreatePydantic",
    **{
        name: (Optional[field.annotation], None)
        for name, field in GradePydantic.model_fields.items()
    },
    student_id=(Optional[int], Field(None, alias="studentId")),
    course_id=(Optional[int], Field(None, alias="courseId"))
)


# 新增
@router.post("/add")
async def add(grade_create_pydantic: GradeCreatePydantic):
    # 当前的这个学生是否有已选的课程
    db_grade = await (Grade.filter(student_id=grade_create_pydantic.student_id)
                      .filter(course_id=grade_create_pydantic.course_id)
                      .first())
    if db_grade is not None:
        raise CustomException("该学生课程成绩已被录入")
    grade_create_pydantic.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 将参数转换成 字典数据
    create_data = grade_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await Grade.create(**create_data)  # no=xxx,name=xxx,college=xxx
    if grade_create_pydantic.ispass == '是':
        # 查询课程的学分
        course = await Course.filter(id=grade_create_pydantic.course_id).first()
        add_score = course.score
        # 设置学分
        await Student.filter(id=grade_create_pydantic.student_id).update(score=F('score') + add_score)
    return Result.success()


# 更新
@router.put("/update")
async def add(grade_create_pydantic: GradeCreatePydantic):
    if grade_create_pydantic.id is None:
        raise CustomException("缺少参数ID")
    # 将参数转换成 字典数据
    update_data = grade_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await Grade.filter(id=grade_create_pydantic.id).update(**update_data)  # no=xxx,name=xxx,college=xxx where id = xxx
    return Result.success()


# 删除
@router.delete('/delete/{grade_id}')
async def delete(grade_id: int):
    await Grade.filter(id=grade_id).delete()
    return Result.success()


# 单个查询
@router.get('/selectById/{grade_id}')
async def select_by_id(grade_id: int):
    grade = await Grade.get_or_none(id=grade_id)
    return Result.success(grade)


# 查询所有数据
@router.get('/selectAll')
async def select_all(name: str = ""):
    query = Grade.all()
    grade_list = await query.filter(name__contains=name)
    return Result.success(grade_list)


# 分页查询数据
@router.get('/selectPage')
async def select_page(studentId: int = 0, studentName: str = "", courseName: str = "", pageNum: int = 1, pageSize: int = 10):
    # name__contains表示根据name进行模糊查询  prefetch_related 关联查询到 major模块的数据
    query = Grade.all().prefetch_related("student", "course")
    if studentId > 0:
        query = query.filter(student__id=studentId)
    if studentName != "":
        query = query.filter(student__name__contains=studentName)
    if courseName != "":
        query = query.filter(course__name__contains=courseName)
    grade_list = await query.order_by("-id").offset((pageNum - 1) * pageSize).limit(pageSize)
    total = await query.count()
    grade_dict_list = [
        {
            **GradePydantic.model_validate(grade).model_dump(),  # id=xxx,no=xxx,name=xxx
            "studentName": grade.student.name if grade.student else None,
            "courseName": grade.course.name if grade.course else None
        }
        for grade in grade_list
    ]
    page_info = PageInfo(list=grade_dict_list, total=total)
    return Result.success(page_info)
