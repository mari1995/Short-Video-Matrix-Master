import request from '@/utils/request'

// 获取文件列表
export function getFileList(params) {
  return request({
    url: '/api/v1/files/list',
    method: 'get',
    params
  })
}

// 删除文件
export function deleteFile(path) {
  return request({
    url: '/api/v1/files/delete',
    method: 'delete',
    params: { path }
  })
}

// 获取文件预览URL
export function getFileUrl(path) {
  return `http://127.0.0.1:8000/${path}`
}

// 解析图片描述
export function analyzeImage(data) {
  return request({
    url: '/api/v1/image-analysis/describe',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
} 