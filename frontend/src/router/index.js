import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'
import Login from '../views/Login.vue'
import YoutubeDownloader from '@/views/youtube/index.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { public: true }
  },
  {
    path: '/',
    component: () => import('../layout/Layout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '首页', icon: 'el-icon-s-home' }
      },
      {
        path: '/youtube',
        name: 'Youtube',
        component: YoutubeDownloader,
        meta: {
          title: 'YouTube下载器',
          icon: 'video-play'
        }
      },
      {
        path: '/files',
        name: 'Files',
        component: () => import('../views/files/index.vue'),
        meta: { title: '文件管理', icon: 'el-icon-folder' }
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  const token = store.state.token
  if (!to.meta.public && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router 