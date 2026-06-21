<template>
  <div>

    <div class="card" style="margin-bottom: 5px;">
      <el-input v-model="data.courseName" style="width: 300px; margin-right: 10px" placeholder="请输入课程名称查询"></el-input>
      <el-input v-if="data.user.role === '管理员'" v-model="data.studentName" style="width: 300px; margin-right: 10px" placeholder="请输入学生名称查询"></el-input>
      <el-button type="primary" @click="load">查询</el-button>
      <el-button type="info" style="margin: 0 10px" @click="reset">重置</el-button>
    </div>

    <div class="card" style="margin-bottom: 5px">
      <div style="margin-bottom: 10px" v-if="data.user.role === '管理员'">
        <el-button type="primary" @click="handleAdd" >新增</el-button>
      </div>
      <el-table :data="data.tableData" stripe>
        <el-table-column label="课程名称" prop="courseName"></el-table-column>
        <el-table-column label="学生名称" prop="studentName"></el-table-column>
        <el-table-column label="分数" prop="score"></el-table-column>
        <el-table-column label="是否及格" prop="ispass">
          <template #default="scope">
            <b style="color: #1abc00" v-if="scope.row.ispass === '是'">是</b>
            <b style="color: red" v-if="scope.row.ispass === '否'">否</b>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="time"></el-table-column>
        <el-table-column label="操作" align="center" width="160" v-if="data.user.role === '管理员'">
          <template #default="scope">
            <el-button type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="card">
      <el-pagination @current-change="load" background layout="total, prev, pager, next" v-model:page-size="data.pageSize" v-model:current-page="data.pageNum" :total="data.total"/>
    </div>

    <el-dialog title="成绩信息" width="40%" v-model="data.formVisible" :close-on-click-modal="false" destroy-on-close>
      <el-form ref="formRef" :model="data.form" :rules="data.rules" label-width="100px" style="padding-right: 50px">
        <el-form-item label="学生" prop="studentId" v-if="!data.form.id">
          <el-select placeholder="请选择学生" v-model="data.form.studentId" @change="selectCourse">
            <el-option v-for="item in data.studentList" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="课程" prop="courseId" v-if="!data.form.id">
          <el-select :disabled="!data.form.studentId" placeholder="请选择课程" v-model="data.form.courseId">
            <el-option v-for="item in data.studentCourseList" :key="item.id" :label="item.courseName" :value="item.courseId"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="成绩" prop="score">
          <el-input-number style="width: 200px" :min="1" placeholder="请输入成绩" v-model="data.form.score" autocomplete="off" />
        </el-form-item>
        <el-form-item label="是否合格" prop="ispass">
          <el-radio-group v-model="data.form.ispass">
            <el-radio-button label="是" value="是"></el-radio-button>
            <el-radio-button label="否" value="否"></el-radio-button>
          </el-radio-group>
        </el-form-item>

      </el-form>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="data.formVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">保 存</el-button>
      </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import request from "@/utils/request";
import {reactive, ref} from "vue";
import {ElMessageBox, ElMessage} from "element-plus";

const formRef = ref()
const data = reactive({
  user: JSON.parse(localStorage.getItem('system-user') || '{}'),
  pageNum: 1,
  pageSize: 10,
  total: 0,
  formVisible: false,
  form: {},
  tableData: [],
  studentList: [],
  studentCourseList: [],
  courseName: null,
  studentName: null,
  rules: {
    studentId: [
      { required: true, message: '请选择学生', trigger: 'change' }
    ],
    courseId: [
      { required: true, message: '请选择课程', trigger: 'change' }
    ],
    score: [
      { required: true, message: '请输入成绩', trigger: 'blur' }
    ],
    ispass: [
      { required: true, message: '请选择是否合格', trigger: 'change' }
    ],
  }
})

// 查询学生的信息list
request.get('/student/selectAll').then(res => {
  data.studentList = res.data
})

// 查询选课的接口
const selectCourse = () => {
  data.form.courseId = null  // 先清空课程
  request.get('/studentCourse/selectAll', {
    params: {
      studentId: data.form.studentId,
      status: '已选'
    }
  }).then(res => {
  data.studentCourseList = res.data
})
}

// 分页查询
const load = () => {
  request.get('/grade/selectPage', {
    params: {
      pageNum: data.pageNum,
      pageSize: data.pageSize,
      courseName: data.courseName,
      studentName: data.studentName,
      studentId: data.user.role === '管理员' ? null : data.user.id,
    }
  }).then(res => {
    if (res.code === '200') {
      data.tableData = res.data?.list
      data.total = res.data?.total
    } else {
      ElMessage.error(res.msg)
    }
  })
}
load()

// 新增
const handleAdd = () => {
  data.form = {}
  data.formVisible = true
}

// 编辑
const handleEdit = (row) => {
  data.form = JSON.parse(JSON.stringify(row))
  data.formVisible = true
}

// 新增保存
const add = () => {
  request.post('/grade/add', data.form).then(res => {
    if (res.code === '200') {
      load()
      ElMessage.success('操作成功')
      data.formVisible = false
    } else {
      ElMessage.error(res.msg)
    }
  })
}

// 编辑保存
const update = () => {
  request.put('/grade/update', data.form).then(res => {
    if (res.code === '200') {
      load()
      ElMessage.success('操作成功')
      data.formVisible = false
    } else {
      ElMessage.error(res.msg)
    }
  })
}

// 弹窗保存
const save = () => {
  formRef.value.validate(valid => {
    if (valid) {
      // data.form有id就是更新，没有就是新增
      data.form.id ? update() : add()
    }
  })
}

// 删除
const handleDelete = (id) => {
  ElMessageBox.confirm('删除后数据无法恢复，您确定删除吗?', '删除确认', { type: 'warning' }).then(res => {
    request.delete('/grade/delete/' + id).then(res => {
      if (res.code === '200') {
        load()
        ElMessage.success('操作成功')
      } else {
        ElMessage.error(res.msg)
      }
    })
  }).catch(err => {})
}

// 重置
const reset = () => {
  data.courseName = null
  data.studentName = null
  load()
}
</script>