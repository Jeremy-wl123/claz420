<template>
  <div>
    <div class="card" style="margin-bottom: 5px;">
      <el-input v-model="data.courseName" style="width: 300px; margin-right: 10px" placeholder="请输入课程名称查询"></el-input>
      <el-input v-if="data.user.role === '管理员'" v-model="data.studentName" style="width: 300px; margin-right: 10px" placeholder="请输入学生名称查询"></el-input>
      <el-button type="primary" @click="load">查询</el-button>
      <el-button type="info" style="margin: 0 10px" @click="reset">重置</el-button>
    </div>

    <div class="card" style="margin-bottom: 5px">
      <div style="margin-bottom: 10px" v-if="data.user.role === '学生'">
        <el-button type="primary" @click="handleAdd" >新增选课</el-button>
      </div>
      <el-table :data="data.tableData" stripe>
        <el-table-column label="课程名称" prop="courseName"></el-table-column>
        <el-table-column label="学生" prop="studentName"></el-table-column>
        <el-table-column label="学年" prop="year"></el-table-column>
        <el-table-column label="选课状态" prop="status">
          <template #default="scope">
            <el-tag type="warning" v-if="scope.row.status === '申请中'">申请中</el-tag>
            <el-tag type="success" v-if="scope.row.status === '已选'">已选</el-tag>
            <el-tag type="danger" v-if="scope.row.status === '已退'">已退</el-tag>
            <el-tag type="danger" v-if="scope.row.status === '未选中'">未选中</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="审核状态" prop="checkStatus">
           <template #default="scope">
            <el-tag type="warning" v-if="scope.row.checkStatus === '待审核'">待审核</el-tag>
            <el-tag type="success" v-if="scope.row.checkStatus === '通过'">通过</el-tag>
            <el-tag type="danger" v-if="scope.row.checkStatus === '拒绝'">拒绝</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="选课时间" prop="time"></el-table-column>
         <el-table-column label="审核" align="center" width="160" v-if="data.user.role === '管理员'">
          <template #default="scope">
            <el-button type="primary" :disabled="scope.row.checkStatus === '通过'" @click="updateCheckStatus(scope.row, '通过')">通过</el-button>
            <el-button type="danger" :disabled="scope.row.checkStatus === '拒绝'"  @click="updateCheckStatus(scope.row, '拒绝')">拒绝</el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="160">
          <template #default="scope">
            <el-button type="primary" v-if="scope.row.status === '已选'" @click="updateStatus(scope.row, '已退')">退课</el-button>
            <el-button type="danger" @click="handleDelete(scope.row.id)" v-if="data.user.role === '管理员'">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="card">
      <el-pagination @current-change="load" background layout="total, prev, pager, next" v-model:page-size="data.pageSize" v-model:current-page="data.pageNum" :total="data.total"/>
    </div>

    <el-dialog title="选课信息" width="40%" v-model="data.formVisible" :close-on-click-modal="false" destroy-on-close>
      <el-form ref="formRef" :model="data.form" :rules="data.rules" label-width="100px" style="padding-right: 50px">
        <el-form-item prop="courseId" label="课程">
          <el-select placeholder="请选择课程" v-model="data.form.courseId">
            <el-option v-for="item in data.courseList" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="学年" prop="year">
          <el-radio-group v-model="data.form.year">
            <el-radio-button v-for="item in ['2025-2026', '2026-2027',  '2027-2028']" :key="item" :label="item" :value="item"></el-radio-button>
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
  courseList: [],
  courseName: null,
  studentName: null,
  rules: {
    courseId: [
      { required: true, message: '请选择课程', trigger: 'change' }
    ],
    year: [
      { required: true, message: '请现在学年', trigger: 'change' }
    ],
  }
})

// 查询课程的信息list
request.get('/course/selectAll', {
  params: {
    majorId: data.user.majorId
  }
}).then(res => {
  data.courseList = res.data
})

// 分页查询
const load = () => {
  request.get('/studentCourse/selectPage', {
    params: {
      pageNum: data.pageNum,
      pageSize: data.pageSize,
      courseName: data.courseName,
      studentName: data.studentName,
      studentId: data.user.role === '管理员' ? null : data.user.id
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
  data.form.studentId = data.user.id
  data.form.status = '申请中'
  data.form.checkStatus = '待审核'
  request.post('/studentCourse/add', data.form).then(res => {
    if (res.code === '200') {
      load()
      ElMessage.success('操作成功')
      data.formVisible = false
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const updateStatus = (row, status) => {
  ElMessageBox.confirm('您确定退课吗？', '退课确认', { type: 'warning' }).then(res => {
    data.form = JSON.parse(JSON.stringify(row))
    data.form.status = status
    request.put('/studentCourse/update', data.form).then(res => {
      if (res.code === '200') {
        load()
        ElMessage.success('操作成功')
      } else {
        ElMessage.error(res.msg)
      }
    })
  }).catch(err=>{})
}

const updateCheckStatus = (row, checkStatus) => {
  ElMessageBox.confirm('您确定审核' + checkStatus + "吗？", '审核确认', { type: 'warning' }).then(res => {
    data.form = JSON.parse(JSON.stringify(row))
    data.form.checkStatus = checkStatus
    request.put('/studentCourse/update', data.form).then(res => {
      if (res.code === '200') {
        load()
        ElMessage.success('操作成功')
      } else {
        ElMessage.error(res.msg)
      }
    })
  }).catch(err=>{})
}

// 编辑保存
const update = () => {
  request.put('/studentCourse/update', data.form).then(res => {
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
    request.delete('/studentCourse/delete/' + id).then(res => {
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