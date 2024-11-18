import axios from 'axios'
import { Message } from 'element-ui'
import { API_URL } from '@/config/api.config'

// 创建axios实例
const service = axios.create({
  baseURL: API_URL,
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    return config
  },
  error => {
    console.log(error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.log('err' + error)
    Message({
      message: error.response?.data?.detail || '请求失败',
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service 