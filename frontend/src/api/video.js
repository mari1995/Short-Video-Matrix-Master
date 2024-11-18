import request from '@/utils/request'

// 视频分析相关接口
export function uploadVideo(data) {
  return request({
    url: '/api/v1/video-analysis/upload',
    method: 'post',
    data
  })
}

export function getAnalysisList(params) {
  return request({
    url: '/api/v1/video-analysis/list',
    method: 'get',
    params
  })
}

export function getAnalysisDetail(id) {
  return request({
    url: `/api/v1/video-analysis/analysis/${id}`,
    method: 'get'
  })
} 