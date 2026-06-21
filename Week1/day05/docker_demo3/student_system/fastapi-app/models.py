from tortoise.models import Model
from tortoise import fields


class Admin(Model):
    """管理员模块"""
    id = fields.IntField(pk=True, null=False)
    username = fields.CharField(max_length=255, null=True)
    password = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)
    avatar = fields.CharField(max_length=255, null=True)
    role = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'admin'


class Major(Model):
    """专业模块"""
    id = fields.IntField(pk=True, null=False)
    no = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)
    college = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'major'


class Clazz(Model):
    """班级模块"""
    id = fields.IntField(pk=True, null=False)
    no = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)
    major = fields.ForeignKeyField('models.Major', null=True)
    teacher = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'clazz'


class Student(Model):
    """学生模块"""
    id = fields.IntField(pk=True, null=False)
    username = fields.CharField(max_length=255, null=True)
    password = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)
    avatar = fields.CharField(max_length=255, null=True)
    role = fields.CharField(max_length=255, null=True)
    score = fields.IntField(max_length=11, null=True)
    clazz = fields.ForeignKeyField('models.Clazz', null=True)

    class Meta:
        table = 'student'


class Course(Model):
    """课程模块"""
    id = fields.IntField(pk=True, null=False)
    no = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)
    score = fields.IntField(max_length=11, null=True)
    teacher = fields.CharField(max_length=255, null=True)
    major = fields.ForeignKeyField('models.Major', null=True)

    class Meta:
        table = 'course'


class StudentCourse(Model):
    """选课信息"""
    id = fields.IntField(pk=True, null=False)
    student = fields.ForeignKeyField('models.Student', null=True)
    course = fields.ForeignKeyField('models.Course', null=True)
    year = fields.CharField(max_length=255, null=True)
    status = fields.CharField(max_length=255, null=True)
    checkStatus = fields.CharField(max_length=255, null=True, source_field="check_status")
    time = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'student_course'


class Grade(Model):
    id = fields.IntField(pk=True, null=False)
    student = fields.ForeignKeyField('models.Student', null=True)
    course = fields.ForeignKeyField('models.Course', null=True)
    score = fields.IntField(max_length=11, null=True)
    ispass = fields.CharField(max_length=255, null=True)
    time = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'grade'


class Notice(Model):
    id = fields.IntField(pk=True, null=False)
    title = fields.CharField(max_length=255, null=True)
    content = fields.CharField(max_length=255, null=True)
    time = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'notice'
