import request from '@/utils/request'

// 获取视频信息
export function getVideoInfo(data) {
  return request({
    url: '/api/v1/youtube/info',
    method: 'post',
    data
  })
}

// 下载视频
export function downloadVideo(data) {
  return request({
    url: '/api/v1/youtube/download',
    method: 'post',
    data
  })
}

// 获取下载列表
export function getDownloadList(params) {
  return request({
    url: '/api/v1/youtube/list',
    method: 'get',
    params
  })
}

// 获取下载状态
export function getDownloadStatus(id) {
  return request({
    url: `/api/v1/youtube/status/${id}`,
    method: 'get'
  })
}

// 取消下载
export function cancelDownload(id) {
  return request({
    url: `/api/v1/youtube/cancel/${id}`,
    method: 'post'
  })
} 