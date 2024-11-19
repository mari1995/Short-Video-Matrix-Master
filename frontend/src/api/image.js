import request from '@/utils/request'

// 图片分析相关接口
export function analyzeImage(imageUrl) {
  return request({
    url: '/api/v1/image-analysis/describe',
    method: 'post',
    data: {
      image_url: imageUrl  // 使用 JSON 格式
    }
  })
} 