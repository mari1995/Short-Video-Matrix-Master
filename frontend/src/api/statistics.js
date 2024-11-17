import request from '@/utils/request'

export function getStatisticsOverview() {
  return request({
    url: '/api/v1/statistics/overview',
    method: 'get',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  })
} 