import request from '@/utils/request'

// 获取下载历史列表
export function getDownloadHistory(params) {
  return request({
    url: '/api/v1/youtube/history',
    method: 'get',
    params
  })
}

// 获取下载历史详情
export function getHistoryDetail(id) {
  return request({
    url: `/api/v1/youtube/history/${id}`,
    method: 'get'
  })
}

// 删除下载历史
export function deleteHistory(id) {
  return request({
    url: `/api/v1/youtube/history/${id}`,
    method: 'delete'
  })
}

// 获取下载文件URL
export function getDownloadUrl(fileName) {
  fileName = fileName.replace(/^static\/youtube\/downloads\//, '')
  return `http://127.0.0.1:8000/static/youtube/downloads/${fileName}`
}

// 下载文件到本地
export function downloadToLocal(url, fileName) {
  const iframe = document.createElement('iframe')
  iframe.style.display = 'none'
  document.body.appendChild(iframe)
  
  try {
    const form = iframe.contentDocument.createElement('form')
    form.method = 'GET'
    form.action = url
    
    const fileNameInput = iframe.contentDocument.createElement('input')
    fileNameInput.type = 'hidden'
    fileNameInput.name = 'filename'
    fileNameInput.value = fileName
    form.appendChild(fileNameInput)
    
    iframe.contentDocument.body.appendChild(form)
    form.submit()
    
    setTimeout(() => {
      document.body.removeChild(iframe)
    }, 5000)
  } catch (error) {
    console.warn('Fallback to simple download:', error)
    const link = document.createElement('a')
    link.href = url
    link.download = fileName
    link.style.display = 'none'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
} 