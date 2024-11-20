import request from '@/utils/request'

// 用户相关接口
export const userApi = {
  login(data) {
    return request({
      url: '/api/v1/auth/login',
      method: 'post',
      data
    })
  },
  logout() {
    return request({
      url: '/api/v1/auth/logout',
      method: 'post'
    })
  }
}

// YouTube相关接口
export const youtubeApi = {
  getVideoInfo(url) {
    return request({
      url: '/api/v1/youtube/info',
      method: 'get',
      params: { url }
    })
  },
  downloadVideo(url) {
    return request({
      url: '/api/v1/youtube/download',
      method: 'post',
      data: { url }
    })
  },
  getHistory(params) {
    return request({
      url: '/api/v1/youtube/history',
      method: 'get',
      params
    })
  },
  deleteHistory(id) {
    return request({
      url: `/api/v1/youtube/history/${id}`,
      method: 'delete'
    })
  },
  getDownloadUrl(fileName) {
    return `http://127.0.0.1:8000/static/youtube/downloads/${fileName}`
  }
}

// 视频分析相关接口
export const videoApi = {
  uploadVideo(data) {
    return request({
      url: '/api/v1/video-analysis/upload',
      method: 'post',
      data,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  getAnalysisList(params) {
    return request({
      url: '/api/v1/video-analysis/list',
      method: 'get',
      params
    })
  },
  getAnalysisDetail(id) {
    return request({
      url: `/api/v1/video-analysis/analysis/${id}`,
      method: 'get'
    })
  },
  deleteAnalysis(id) {
    return request({
      url: `/api/v1/video-analysis/${id}`,
      method: 'delete'
    })
  }
}

// 图片分析相关接口
export const imageApi = {
  analyzeImage(data) {
    return request({
      url: '/api/v1/image-analysis/describe',
      method: 'post',
      data
    })
  }
}

// 文件管理相关接口
export const fileApi = {
  getFileList(params) {
    return request({
      url: '/api/v1/files/list',
      method: 'get',
      params
    })
  },
  deleteFile(path) {
    return request({
      url: '/api/v1/files/delete',
      method: 'delete',
      params: { path }
    })
  },
  getFileUrl(path) {
    return `http://127.0.0.1:8000/${path}`
  }
}

// 草稿箱相关接口
export const draftApi = {
  getDraftsList(params) {
    return request({
      url: '/api/v1/drafts/list',
      method: 'get',
      params
    })
  },
  addToDrafts(data) {
    return request({
      url: '/api/v1/drafts/upload',
      method: 'post',
      data
    })
  },
  addToDraftsByUrl(data) {
    return request({
      url: '/api/v1/drafts/add-by-url',
      method: 'post',
      data
    })
  },
  deleteDraft(id) {
    return request({
      url: `/api/v1/drafts/${id}`,
      method: 'delete'
    })
  }
}

// 系统配置相关接口
export const settingsApi = {
  getConfigs() {
    return request({
      url: '/api/v1/system-config',
      method: 'get'
    })
  },
  createConfig(data) {
    return request({
      url: '/api/v1/system-config',
      method: 'post',
      data
    })
  },
  updateConfig(key, data) {
    return request({
      url: `/api/v1/system-config/${key}`,
      method: 'put',
      data
    })
  },
  deleteConfig(key) {
    return request({
      url: `/api/v1/system-config/${key}`,
      method: 'delete'
    })
  }
}

// 视频编辑器相关接口
export const videoEditorApi = {
  generateVideo(data) {
    return request({
      url: '/api/v1/video-editor/generate',
      method: 'post',
      data,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  getGenerateStatus(taskId) {
    return request({
      url: `/api/v1/video-editor/status/${taskId}`,
      method: 'get'
    })
  },
  getGenerateHistory(params) {
    return request({
      url: '/api/v1/video-editor/history',
      method: 'get',
      params
    })
  }
}

// 统计相关接口
export const statisticsApi = {
  getOverview() {
    return request({
      url: '/api/v1/statistics/overview',
      method: 'get'
    })
  },
  getRecentAnalyses() {
    return request({
      url: '/api/v1/statistics/recent',
      method: 'get'
    })
  }
}

export default {
  userApi,
  youtubeApi,
  videoApi,
  imageApi,
  fileApi,
  draftApi,
  settingsApi,
  videoEditorApi,
  statisticsApi
} 