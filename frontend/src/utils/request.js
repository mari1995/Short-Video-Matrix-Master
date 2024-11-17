import axios from 'axios'
import store from '@/store'
import { Message } from 'element-ui'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API || 'http://127.0.0.1:8000',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: false
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    console.log('Full request config:', {
      baseURL: config.baseURL,
      url: config.url,
      fullPath: `${config.baseURL}${config.url}`,
      method: config.method,
      data: config.data,
      headers: config.headers
    })
    
    const token = store.state.token || localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    console.log('Response:', response)
    return response.data
  },
  error => {
    console.error('Response error:', {
      status: error.response?.status,
      data: error.response?.data,
      config: error.config
    })
    
    const response = error.response
    const data = response?.data
    
    let message = '请求失败'
    if (data?.detail?.message) {
      message = data.detail.message
    } else if (data?.detail) {
      message = typeof data.detail === 'object' ? data.detail.message : data.detail
    } else if (Array.isArray(data)) {
      message = data.map(err => err.msg).join('; ')
    }
    
    if (error.response?.status === 401) {
      // 清除 token 并跳转到登录页
      store.dispatch('logout')
      router.push('/login')
      Message({
        message: '登录已过期，请重新登录',
        type: 'error',
        duration: 5 * 1000
      })
    } else {
      Message({
        message: message,
        type: 'error',
        duration: 5 * 1000
      })
    }
    return Promise.reject(error)
  }
)

export default service 