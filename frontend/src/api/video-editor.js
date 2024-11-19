import request from '@/utils/request'

// 图片生成视频
export function generateVideo(data) {
  return request({
    url: '/api/v1/video-editor/generate',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 获取生成任务状态
export function getGenerateStatus(taskId) {
  return request({
    url: `/api/v1/video-editor/status/${taskId}`,
    method: 'get'
  })
}

// 获取生成历史
export function getGenerateHistory(params) {
  return request({
    url: '/api/v1/video-editor/history',
    method: 'get',
    params
  })
} 