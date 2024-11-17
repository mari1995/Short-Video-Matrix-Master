import request from '@/utils/request'

export function login(data) {
  console.log('Login request data:', data)
  return request({
    url: '/api/v1/auth/login',
    method: 'post',
    data: {
      username: data.username,
      password: data.password
    }
  })
}

export function getUserInfo() {
  return request({
    url: '/api/v1/users/me',
    method: 'get'
  })
} 