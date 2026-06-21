<template>
  <div class="login-container">
    <div class="login-box">
      <div style="font-weight: bold; font-size: 30px; text-align: center; margin-bottom: 30px; color: #1967e3">欢 迎 登 录</div>
      <el-form :model="data.form"  ref="formRef" :rules="data.rules">
        <el-form-item prop="username">
          <el-input :prefix-icon="User" size="large" v-model="data.form.username" placeholder="请输入账号" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input :prefix-icon="Lock" size="large" v-model="data.form.password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item prop="role">
          <el-select size="large" style="width: 100%" v-model="data.form.role">
            <el-option value="管理员" label="管理员"></el-option>
            <el-option value="学生" label="学生"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button size="large" type="primary" style="width: 100%" @click="login">登 录</el-button>
        </el-form-item>
      </el-form>
      <div style="text-align: right;">
        还没有账号？请 <router-link to="/register">注册</router-link>
      </div>
    </div>

    <el-dialog title="郑重声明" v-model="data.dialogVisible" :show-close="false" width="40%" :close-on-click-modal="false" destroy-on-close>
      <div style="font-size: 16px; line-height: 26px; margin-bottom: 20px; text-align: justify">
        本项目仅限于<b style="color: #000">内部交流学习</b>，不要用于其他商业用途。
        <b style="color: #ff2424">作为一家以就业为导向的人才服务公司，我们专注做一件事：帮你敲开大数据和人工智能行业的大门。</b>
        <b style="color: #000">我们的使命:提升一千万人职场价值</b>
      </div>
      <div style="margin-top: 10px; font-size: 16px; color: #000">
        本项目合作网页：<b>沃林官网（<a href="https://www.wolindata.com" target="_blank">https://www.wolindata.com</a>）</b>
      </div>
      <div style="margin-top: 5px; font-size: 16px"></div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="data.dialogVisible=false">我承诺先舍后得，正面积极，终身学习，建立关系</el-button>
        </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
  import { reactive, ref } from "vue";
  import { User, Lock } from "@element-plus/icons-vue";
  import request from "@/utils/request";
  import {ElMessage} from "element-plus";
  import router from "@/router";

  const data = reactive({
    dialogVisible: true,
    form: { role: '管理员' },
    rules: {
      username: [
        { required: true, message: '请输入账号', trigger: 'blur' },
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
      ],
    }
  })

  const formRef = ref()

  // 点击登录按钮的时候会触发这个方法
  const login = () => {
    formRef.value.validate((valid => {
      if (valid) {
        // 调用后台的接口
        request.post('/login', data.form).then(res => {
          if (res.code === '200') {
            ElMessage.success("登录成功")
            router.push('/manager/home')
            localStorage.setItem('system-user', JSON.stringify(res.data))
          } else {
            ElMessage.error(res.msg)
          }
        })
      }
    })).catch(error => {
      console.error(error)
    })
  }

</script>

<style scoped>
.login-container {
  height: 100vh;
  overflow:hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #2e3143;
  background-size: cover;
}
.login-box {
  width: 350px;
  padding: 50px 30px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  background-color: #fff;
}
</style>