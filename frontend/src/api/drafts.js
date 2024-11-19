import request from '@/utils/request'

// 获取草稿箱列表
export function getDraftsList(params) {
  return request({
    url: '/api/v1/drafts/list',
    method: 'get',
    params
  })
}

// 添加到草稿箱
export function addToDrafts(data) {
  return request({
    url: '/api/v1/drafts/upload',
    method: 'post',
    data
  })
}

// 通过URL添加到草稿箱
export function addToDraftsByUrl(data) {
  return request({
    url: '/api/v1/drafts/add-by-url',
    method: 'post',
    data
  })
}

// 删除草稿
export function deleteDraft(id) {
  return request({
    url: `/api/v1/drafts/${id}`,
    method: 'delete'
  })
} 