import request from '@/utils/request'

// 图片分析相关接口
export function analyzeImage(data) {
  return request({
    url: '/api/v1/image-analysis/describe',
    method: 'post',
    data
  })
} 