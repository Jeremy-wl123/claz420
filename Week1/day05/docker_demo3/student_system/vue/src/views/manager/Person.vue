<template>
  <div style="width: 40%">
    <div class="card" style="padding: 30px">
      <el-form ref="formRef" :model="data.user" :rules="data.rules" label-width="100px" style="padding-right: 50px">
        <div style="margin: 20px 0; text-align: center">
          <el-upload :show-file-list="false" class="avatar-uploader" :action="uploadUrl" :on-success="handleFileUpload">
            <img v-if="data.user.avatar" :src="data.user.avatar" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </div>
        <el-form-item label="账号" prop="username">
          <el-input disabled v-model="data.user.username" autocomplete="off" />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="data.user.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="学分" prop="score" v-if="data.user.role === '学生'">
          <el-input disabled v-model="data.user.score" autocomplete="off" />
        </el-form-item>
         <el-form-item label="所属班级" prop="clazzId" v-if="data.user.role === '学生'">
          <el-select disabled placeholder="请选择班级" v-model="data.user.clazzId">
            <el-option v-for="item in data.classList" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
         <el-form-item label="所属专业" v-if="data.user.role === '学生'">
          <el-select disabled v-model="data.user.majorId">
            <el-option v-for="item in data.majorList" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <div style="text-align: center">
          <el-button type="primary" @click="save">保存</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import {reactive, ref} from "vue"
import request from "@/utils/request";
import {ElMessage} from "element-plus";

// 文件上传的接口地址
const uploadUrl = import.meta.env.VITE_BASE_URL + '/files/upload'

const formRef = ref()
const data = reactive({
  user: JSON.parse(localStorage.getItem('system-user') || '{}'),
  classList: [],
  majorList: [],
  rules: {
    username: [
      {required: true, message: '请输入账号', trigger: 'blur'}
    ],
    name: [
      {required: true, message: '请输入名称', trigger: 'blur'}
    ],
  }
})

// 查询班级的信息list
request.get('/clazz/selectAll').then(res => {
  data.classList = res.data
})

// 查询专业的信息list
request.get('/major/selectAll').then(res => {
  data.majorList = res.data
})

const handleFileUpload = (file) => {
  data.user.avatar = file.data
}

const emit = defineEmits(["updateUser"])
// 把当前修改的用户信息存储到后台数据库
const save = () => {
  formRef.value.validate(valid => {
    if (valid) {
      if (data.user.role === '管理员') {
        request.put('/admin/update', data.user).then(res => {
          if (res.code === '200') {
            ElMessage.success('更新成功')
            //把更新后的用户信息存储到缓存
            localStorage.setItem('system-user', JSON.stringify(data.user))
            emit('updateUser')
          } else {
            ElMessage.error(res.msg)
          }
        })
      }
      if (data.user.role === '学生') {
        request.put('/student/update', data.user).then(res => {
          if (res.code === '200') {
            ElMessage.success('更新成功')
            //把更新后的用户信息存储到缓存
            localStorage.setItem('system-user', JSON.stringify(data.user))
            emit('updateUser')
          } else {
            ElMessage.error(res.msg)
          }
        })
      }
    }
  })
}
</script>

<style scoped>
.avatar-uploader .avatar {
  width: 120px;
  height: 120px;
  display: block;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  text-align: center;
}
</style>