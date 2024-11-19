import request from '@/utils/request'

// 获取系统配置列表
export function getSystemConfigs() {
  return request({
    url: '/api/v1/system-config/list',
    method: 'get'
  })
}

// 更新系统配置
export function updateSystemConfigs(data) {
  return request({
    url: '/api/v1/system-config/update',
    method: 'post',
    data
  })
} 