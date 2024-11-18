import request from '@/utils/request'

// 用户登录
export function login(data) {
  return request({
    url: '/api/v1/auth/login',
    method: 'post',
    data
  })
}

// 用户登出
export function logout() {
  return request({
    url: '/api/v1/auth/logout',
    method: 'post'
  })
} 