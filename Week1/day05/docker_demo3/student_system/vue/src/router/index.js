import {createRouter, createWebHistory} from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/login' },
    {
      path: '/manager',
      component: () => import('@/views/Manager.vue'),
      redirect: '/manager/home',
      children: [
        { path: 'person', component: () => import('@/views/manager/Person.vue')},
        { path: 'password', component: () => import('@/views/manager/Password.vue')},
        { path: 'home', component: () => import('@/views/manager/Home.vue')},
        { path: 'admin', component: () => import('@/views/manager/Admin.vue')},
        { path: 'major', component: () => import('@/views/manager/Major.vue')},
        { path: 'clazz', component: () => import('@/views/manager/Clazz.vue')},
        { path: 'student', component: () => import('@/views/manager/Student.vue')},
        { path: 'course', component: () => import('@/views/manager/Course.vue')},
        { path: 'studentCourse', component: () => import('@/views/manager/StudentCourse.vue')},
        { path: 'grade', component: () => import('@/views/manager/Grade.vue')},
        { path: 'notice', component: () => import('@/views/manager/Notice.vue')},
      ]
    },
    { path: '/login', component: () => import('@/views/Login.vue')},
    { path: '/register', component: () => import('@/views/Register.vue')},
  ]
})

export default router
