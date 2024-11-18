import Vue from 'vue'
import Router from 'vue-router'
import { getToken } from '@/utils/auth'
import store from '@/store'
import Login from '../views/Login.vue'
import YoutubeDownloader from '@/views/youtube/index.vue'

Vue.use(Router)

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
      },
      {
        path: '/video-analysis',
        name: 'VideoAnalysis',
        component: () => import('../views/video-analysis/index.vue'),
        meta: { title: '视频分析', icon: 'el-icon-film' }
      },
      {
        path: '/settings',
        name: 'Settings',
        component: () => import('../views/settings/index.vue'),
        meta: { title: '配置中心', icon: 'el-icon-setting' }
      }
    ]
  }
]

const router = new Router({
  routes
})

router.beforeEach(async(to, from, next) => {
  const hasToken = getToken()

  if (hasToken) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else {
      next()
    }
  } else {
    if (to.path === '/login') {
      next()
    } else {
      next(`/login?redirect=${to.path}`)
    }
  }
})

export default router 