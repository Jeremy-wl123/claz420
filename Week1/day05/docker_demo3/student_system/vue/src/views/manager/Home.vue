<template>
  <div>

    <div class="card" style="margin-bottom: 10px">
      <div>欢迎您，<b>{{ data.user.name }}</b> 祝您今天过得开心！</div>
    </div>
    <div class="card" style="line-height:30px">
      <div>沃林数智：<a style="color: #1890ff" href="https://www.wolindata.com/">程序员Ric</a> 出品，感谢大家的支持~</div>
      <div>从0开始带你做一套完整的前后端分离项目，<b style="color: red">完全免费</b>，只可做自己学习</div>
      <div>获取项目资料请访问：<a style="color: #1890ff; font-weight: bold" href="https://www.wolindata.com/">https://www.wolindata.com/</a></div>
      <div>另外，wolindata是我们的官方网站，关于课程更多信息，大家可以来这里看看：
        <a style="color: #1890ff; font-weight: bold" href="https://www.wolindata.com/">https://www.wolindata.com/</a></div>
    </div>

    <div class="card" style="margin-top: 10px; padding: 20px; width: 50%">
      <div style="margin-bottom: 20px; font-size: 20px">系统公告</div>
      <el-timeline>
        <el-timeline-item type="primary" hollow :timestamp="item.time" placement="top" v-for="item in data.noticeList" :key="item.id">
          <div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.content }}</p>
          </div>
        </el-timeline-item>
      </el-timeline>
    </div>

  </div>
</template>

<script setup>
import { reactive } from "vue";
import request from "@/utils/request";

const data = reactive({
  user: JSON.parse(localStorage.getItem('system-user') || '{}'),
  noticeList: []
})

request.get('/notice/selectAll').then(res => { data.noticeList = res.data })
</script>