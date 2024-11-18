import request from '@/utils/request'

// 获取下载历史列表
export function getDownloadHistory(params) {
  return request({
    url: '/api/v1/youtube/history',
    method: 'get',
    params
  })
}

// 删除下载历史
export function deleteDownloadHistory(id) {
  return request({
    url: `/api/v1/youtube/history/${id}`,
    method: 'delete'
  })
}

// 清空下载历史
export function clearDownloadHistory() {
  return request({
    url: '/api/v1/youtube/history/clear',
    method: 'post'
  })
}

// 获取下载历史统计
export function getDownloadStats() {
  return request({
    url: '/api/v1/youtube/history/stats',
    method: 'get'
  })
} 