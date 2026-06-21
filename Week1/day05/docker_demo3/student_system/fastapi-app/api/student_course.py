from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import create_model, BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from common.exception_handler import CustomException
from common.result import Result, PageInfo
from models import StudentCourse, Grade

router = APIRouter(prefix="/studentCourse", tags=["学生选课"])

StudentCoursePydantic = pydantic_model_creator(StudentCourse)

StudentCourseCreatePydantic = create_model(
    "StudentCourseCreatePydantic",
    **{
        name: (Optional[field.annotation], None)
        for name, field in StudentCoursePydantic.model_fields.items()
    },
    student_id=(Optional[int], Field(None, alias="studentId")),
    course_id=(Optional[int], Field(None, alias="courseId")),
)


# 新增
@router.post("/add")
async def add(student_course_create_pydantic: StudentCourseCreatePydantic):
    # 当前的这个学生是否有已选的课程
    db_student_course = await (StudentCourse.filter(student_id=student_course_create_pydantic.student_id)
                               .filter(course_id=student_course_create_pydantic.course_id)
                               .filter(status__not='已退').filter(status__not='未选中')
                               .first())
    if db_student_course is not None:
        raise CustomException("该课程已被选")
    student_course_create_pydantic.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 将参数转换成 字典数据
    create_data = student_course_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await StudentCourse.create(**create_data)  # no=xxx,name=xxx,college=xxx
    return Result.success()


# 更新
@router.put("/update")
async def add(student_course_create_pydantic: StudentCourseCreatePydantic):
    if student_course_create_pydantic.id is None:
        raise CustomException("缺少参数ID")
    if student_course_create_pydantic.status == '已退':
        grade = await (Grade.filter(student_id=student_course_create_pydantic.student_id)
                       .filter(course_id=student_course_create_pydantic.course_id).first())
        if grade is not None:
            raise CustomException('当前课程已打分，无法退课')
    if student_course_create_pydantic.checkStatus == '通过':
        student_course_create_pydantic.status = '已选'
    elif student_course_create_pydantic.checkStatus == '拒绝':
        student_course_create_pydantic.status = '未选中'
    # 将参数转换成 字典数据
    update_data = student_course_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    await StudentCourse.filter(id=student_course_create_pydantic.id).update(
        **update_data)  # no=xxx,name=xxx,college=xxx where id = xxx
    return Result.success()


# 删除
@router.delete('/delete/{student_course_id}')
async def delete(student_course_id: int):
    await StudentCourse.filter(id=student_course_id).delete()
    return Result.success()


# 单个查询
@router.get('/selectById/{student_course_id}')
async def select_by_id(student_course_id: int):
    studentCourse = await StudentCourse.get_or_none(id=student_course_id)
    return Result.success(studentCourse)


# 查询所有数据
@router.get('/selectAll')
async def select_all(studentId: int = 0, status: str = ""):
    query = StudentCourse.all().prefetch_related("course")
    if studentId > 0:
        query = query.filter(student__id=studentId)
    if status != "":
        query = query.filter(status=status)
    student_course_list = await query
    student_course_dict_list = [
        {
            **StudentCoursePydantic.model_validate(student_course).model_dump(),
            "courseId": student_course.course.id if student_course.course else None,
            "courseName": student_course.course.name if student_course.course else None
        }
        for student_course in student_course_list
    ]
    return Result.success(student_course_dict_list)


# 分页查询数据
@router.get('/selectPage')
async def select_page(studentName: str = "", courseName: str = "", studentId: int = 0, pageNum: int = 1,
                      pageSize: int = 10):
    #  prefetch_related 关联查询到 major模块的数据
    query = StudentCourse.all().prefetch_related("course", "student")
    if studentName != "":
        query = query.filter(student__name__contains=studentName)
    if courseName != "":
        query = query.filter(course__name__contains=courseName)
    if studentId > 0:
        query = query.filter(student__id=studentId)
    student_course_list = await query.order_by("-id").offset((pageNum - 1) * pageSize).limit(pageSize)
    total = await query.count()
    student_course_dict_list = [
        {
            **StudentCoursePydantic.model_validate(student_course).model_dump(),  # id=xxx,no=xxx,name=xxx
            "studentId": student_course.student.id if student_course.student else None,
            "courseId": student_course.course.id if student_course.course else None,
            "studentName": student_course.student.name if student_course.student else None,
            "courseName": student_course.course.name if student_course.course else None
        }
        for student_course in student_course_list
    ]
    page_info = PageInfo(list=student_course_dict_list, total=total)
    return Result.success(page_info)
