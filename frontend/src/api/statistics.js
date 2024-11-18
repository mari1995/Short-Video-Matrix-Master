import request from '@/utils/request'

// 获取统计数据
export function getStatistics() {
  return request({
    url: '/api/v1/statistics/overview',
    method: 'get'
  })
}

// 获取最近的分析记录
export function getRecentAnalyses() {
  return request({
    url: '/api/v1/statistics/recent',
    method: 'get'
  })
} 