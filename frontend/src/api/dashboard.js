import request from '@/utils/request'

export function getDashboardStats() {
  return request({
    url: '/api/v1/dashboard/stats',
    method: 'get'
  })
} 