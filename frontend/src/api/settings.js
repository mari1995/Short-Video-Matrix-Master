import request from '@/utils/request'

// 获取系统配置列表
export function getConfigs() {
  return request({
    url: '/api/v1/system-config',
    method: 'get'
  })
}

// 更新配置
export function updateConfig(key, data) {
  return request({
    url: `/api/v1/system-config/${key}`,
    method: 'put',
    data
  })
}

// 添加配置
export function addConfig(data) {
  return request({
    url: '/api/v1/system-config',
    method: 'post',
    data
  })
}

// 删除配置
export function deleteConfig(key) {
  return request({
    url: `/api/v1/system-config/${key}`,
    method: 'delete'
  })
} 