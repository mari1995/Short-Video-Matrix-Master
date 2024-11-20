<template>
  <div class="youtube-downloader">
    <el-card class="box-card">
      <div class="header">
        <div class="logo">
          <i class="el-icon-video-play" style="color: #FF0000; font-size: 24px;"></i>
          <i class="el-icon-download" style="color: #4285f4; font-size: 24px;"></i>
        </div>
        <h1>YouTube Video Downloader</h1>
        <p>支持YouTube视频和Shorts视频下载</p>
      </div>

      <div class="download-form">
        <el-input
          v-model="youtubeUrl"
          placeholder="请输入YouTube视频链接或Shorts链接..."
          class="url-input"
          clearable
        >
          <el-button 
            slot="append"
            type="primary" 
            @click="getVideoInfo"
            :loading="loading"
          >
            获取信息
          </el-button>
          <el-button 
            slot="append"
            type="success" 
            @click="handleDownload"
            :loading="downloading"
          >
            下载视频
          </el-button>
        </el-input>
      </div>

      <div class="video-info" v-if="videoInfo">
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="thumbnail-container">
              <img :src="videoInfo.thumbnail_url" class="thumbnail">
              <div class="video-type" v-if="videoInfo.is_shorts">
                <el-tag type="danger" size="medium">Shorts视频</el-tag>
              </div>
            </div>
          </el-col>
          <el-col :span="16">
            <h3 class="video-title" :title="videoInfo.title">{{ videoInfo.title }}</h3>
            <div class="video-meta">
              <p><i class="el-icon-user"></i> 作者: {{ videoInfo.author }}</p>
              <p>
                <i class="el-icon-timer"></i> 
                时长: {{ formatDuration(videoInfo.length) }}
                <el-tag 
                  size="mini" 
                  type="warning" 
                  v-if="videoInfo.is_shorts"
                  style="margin-left: 5px"
                >
                  短视频
                </el-tag>
              </p>
              <p><i class="el-icon-view"></i> 观看: {{ formatViews(videoInfo.views) }}</p>
            </div>
            
            <div class="download-tips" v-if="videoInfo.is_shorts">
              <el-alert
                title="Shorts视频提示"
                type="info"
                :closable="false"
                show-icon
              >
                <template slot="title">
                  Shorts视频通常为竖屏格式，建议使用手机观看
                </template>
                视频时长: {{ formatDuration(videoInfo.length) }}
              </el-alert>
            </div>

            <div class="description" v-if="videoInfo.description">
              <el-collapse>
                <el-collapse-item title="视频描述">
                  <p class="description-text">{{ videoInfo.description }}</p>
                </el-collapse-item>
              </el-collapse>
            </div>
          </el-col>
        </el-row>
      </div>

      <div class="disclaimer">
        <p>请确保遵守相关法律法规，不要下载受版权保护的内容。</p>
      </div>
    </el-card>

    <!-- 下载进度对话框 -->
    <el-dialog
      :title="videoInfo ? '下载进度' : '准备下载'"
      :visible.sync="showProgress"
      :close-on-click-modal="false"
      width="400px"
    >
      <div class="download-progress">
        <el-progress 
          :percentage="downloadProgress" 
          :status="downloadProgress === 100 ? 'success' : ''"
        ></el-progress>
        <p class="progress-text">{{ downloadStatus }}</p>
        
        <!-- 添加重新下载按钮 -->
        <el-button 
          v-if="downloadProgress === 100 && downloadedFileName"
          type="primary"
          size="small"
          @click="triggerDownload(downloadedUrl, downloadedFileName)"
        >
          下载文件
        </el-button>
      </div>
      <template v-slot:footer>
        <el-button @click="showProgress = false" :disabled="downloading">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 添加历史记录表格 -->
    <el-card class="box-card history-card">
      <div slot="header" class="clearfix">
        <span>下载历史</span>
        <el-button 
          style="float: right; padding: 3px 0" 
          type="text"
          @click="loadHistory"
        >
          刷新
        </el-button>
      </div>
      
      <el-table
        :data="downloadHistory"
        style="width: 100%"
        v-loading="historyLoading"
      >
        <el-table-column
          prop="title"
          label="标题"
          min-width="200"
        >
          <template slot-scope="scope">
            <div class="video-title-cell">
              <img 
                :src="scope.row.thumbnail_url" 
                class="history-thumbnail"
              >
              <span>{{ scope.row.title }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="author"
          label="作者"
          width="120"
        />
        
        <el-table-column
          prop="duration"
          label="时长"
          width="100"
        >
          <template slot-scope="scope">
            {{ formatDuration(scope.row.duration) }}
          </template>
        </el-table-column>
        
        <el-table-column
          prop="download_time"
          label="下载时间"
          width="180"
        >
          <template slot-scope="scope">
            {{ formatDate(scope.row.download_time) }}
          </template>
        </el-table-column>
        
        <el-table-column
          prop="status"
          label="状态"
          width="100"
        >
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
              {{ scope.row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column
          label="操作"
          width="200"
          fixed="right"
        >
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.status === 'success'"
              type="text"
              size="small"
              @click="redownloadFile(scope.row)"
            >
              重新下载
            </el-button>
            <el-button
              v-if="scope.row.status === 'success'"
              type="text"
              size="small"
              @click="downloadToLocal(scope.row)"
            >
              下载到本地
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          @current-change="handlePageChange"
          :current-page.sync="currentPage"
          :page-size="pageSize"
          layout="total, prev, pager, next"
          :total="totalHistory"
        >
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import { youtubeApi } from '@/api'

export default {
  name: 'YoutubeDownloader',
  data() {
    return {
      youtubeUrl: '',
      loading: false,
      downloading: false,
      videoInfo: null,
      showProgress: false,
      downloadProgress: 0,
      downloadStatus: '准备下载...',
      downloadedFileName: '',
      downloadedUrl: '',
      baseUrl: process.env.VUE_APP_BASE_API || '',
      downloadHistory: [],
      historyLoading: false,
      currentPage: 1,
      pageSize: 10,
      totalHistory: 0
    }
  },
  created() {
    this.loadHistory()
  },
  methods: {
    async getVideoInfo() {
      if (!this.youtubeUrl) {
        this.$message.warning('请输入YouTube视频URL')
        return
      }

      this.loading = true
      try {
        const response = await youtubeApi.getVideoInfo(this.youtubeUrl)
        this.videoInfo = response.data
        
        // 如果是Shorts视频，显示提示
        if (this.videoInfo.is_shorts) {
          this.$notify({
            title: 'Shorts视频',
            message: '检测到这是一个Shorts短视频，已自动优化下载设置',
            type: 'info',
            duration: 3000
          })
        }
      } catch (error) {
        this.$message.error(error.response?.data?.detail || '获取视频信息失败')
      } finally {
        this.loading = false
      }
    },

    async handleDownload() {
      if (!this.youtubeUrl) {
        this.$message.warning('请输入YouTube视频URL')
        return
      }

      this.downloading = true
      this.showProgress = true
      this.downloadProgress = 0
      this.downloadStatus = '正在下载...'

      try {
        // 确保已登录
        if (!this.$store.state.user.token) {
          this.$message.error('请先登录')
          this.$router.push('/login')
          return
        }

        const response = await youtubeApi.downloadVideo(this.youtubeUrl)
        
        // 处理下载进度信息
        if (response.data.progress) {
          const progress = response.data.progress
          this.downloadProgress = progress.progress || 0
          if (progress.speed) {
            const speed = this.formatSpeed(progress.speed)
            const eta = this.formatEta(progress.eta)
            this.downloadStatus = `正在下载... ${speed}/s - 剩余时间: ${eta}`
          }
        }

        // 更新视频信息
        if (!this.videoInfo) {
          this.videoInfo = {
            title: response.data.title,
            author: response.data.author,
            is_shorts: response.data.is_shorts,
          }
        }

        this.downloadProgress = 100
        this.downloadStatus = '下载完成！'
        
        // 保存下载文件信息，但不自动下载
        this.downloadedFileName = response.data.file_name
        this.downloadedUrl = `${this.baseUrl || ''}${response.data.download_url}`
        
        // 显示下载成功提示，并刷新历史记录
        this.$message.success('下载成功！点击"重新下载"按钮可下载文件')
        this.loadHistory()
      } catch (error) {
        this.downloadStatus = '下载失败'
        this.$message.error(error.response?.data?.detail || '下载失败')
      } finally {
        this.downloading = false
      }
    },

    triggerDownload(url, fileName) {
      const link = document.createElement('a')
      link.href = url
      link.download = fileName
      link.target = '_blank'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },

    formatDuration(seconds) {
      if (!seconds) return '未知时长'
      if (seconds < 60) {
        return `${seconds}秒`
      }
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
    },

    formatViews(views) {
      if (!views) return '未知'
      if (views >= 10000) {
        return `${(views / 10000).toFixed(1)}万`
      }
      return new Intl.NumberFormat().format(views)
    },

    formatSpeed(bytesPerSecond) {
      if (!bytesPerSecond) return '0 KB'
      const units = ['B', 'KB', 'MB', 'GB']
      let size = bytesPerSecond
      let unitIndex = 0
      while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024
        unitIndex++
      }
      return `${size.toFixed(1)} ${units[unitIndex]}`
    },

    formatEta(seconds) {
      if (!seconds) return '未知'
      if (seconds < 60) return `${seconds}秒`
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes}分${remainingSeconds}秒`
    },

    async loadHistory() {
      this.historyLoading = true
      try {
        const response = await youtubeApi.getHistory({
          skip: (this.currentPage - 1) * this.pageSize,
          limit: this.pageSize
        })
        
        if (response.data && Array.isArray(response.data.items)) {
          this.downloadHistory = response.data.items
          this.totalHistory = response.data.total
        } else {
          throw new Error('Invalid response format')
        }
      } catch (error) {
        console.error('Load history error:', error)
        this.$message.error('加载历史记录失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.historyLoading = false
      }
    },
    
    handlePageChange(page) {
      this.currentPage = page
      this.loadHistory()
    },
    
    redownloadFile(record) {
      if (record.file_url) {
        this.downloadToLocal(record)
      }
    },
    
    formatDate(date) {
      return new Date(date).toLocaleString()
    },
    
    downloadToLocal(record) {
      if (record.file_url) {
        // 使用 fetch 下载文件
        fetch(record.file_url)
          .then(response => response.blob())
          .then(blob => {
            // 创建 Blob URL
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = record.title + '.mp4';  // 设置下载文件名
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            // 释放 Blob URL
            window.URL.revokeObjectURL(url);
          })
          .catch(error => {
            console.error('Download error:', error);
            this.$message.error('下载失败');
          });
      } else {
        this.$message.warning('文件URL不存在');
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.youtube-downloader {
  padding: 20px;
  height: 100%;
  background-color: #f0f2f5;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  margin-bottom: 20px;
}

.download-form {
  margin: 20px 0;
  padding: 0 20px;
}

.url-input {
  width: 100%;
}

.video-info {
  margin: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.thumbnail-container {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.thumbnail {
  width: 100%;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.thumbnail:hover {
  transform: scale(1.02);
}

.video-type {
  text-align: center;
  margin-top: 10px;
}

.video-title {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
  font-size: 1.5em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.video-meta {
  color: #606266;
  font-size: 14px;
  line-height: 1.8;
}

.video-meta i {
  margin-right: 8px;
  color: #409EFF;
}

.video-meta p {
  margin: 8px 0;
}

.download-tips {
  margin: 15px 0;
}

.description {
  margin-top: 20px;
}

.description-text {
  white-space: pre-wrap;
  color: #606266;
  font-size: 14px;
  max-height: 200px;
  overflow-y: auto;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
  line-height: 1.6;
}

.disclaimer {
  margin-top: 20px;
  text-align: center;
  color: #909399;
  font-size: 14px;
}

.el-collapse {
  border: none;
}

.download-progress {
  padding: 30px;
  text-align: center;
}

.progress-text {
  margin-top: 15px;
  color: #606266;
  font-size: 14px;
}

.history-card {
  margin: 20px 0;
  min-height: 400px;
}

.video-title-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.history-thumbnail {
  width: 80px;
  height: 45px;
  object-fit: cover;
  border-radius: 4px;
  transition: transform 0.3s ease;
}

.history-thumbnail:hover {
  transform: scale(1.05);
}

.pagination-container {
  margin: 20px;
  padding: 10px 0;
  text-align: right;
  border-top: 1px solid #ebeef5;
}

@media (max-width: 768px) {
  .youtube-downloader {
    padding: 10px;
  }
  
  .video-info {
    margin: 10px;
    padding: 15px;
  }
  
  .download-form {
    padding: 0 10px;
  }
  
  .video-title {
    font-size: 1.2em;
  }
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.el-card {
  transition: transform 0.3s ease;
}

.el-card:hover {
  transform: translateY(-2px);
}

.el-button {
  transition: all 0.3s ease;
}

.el-table {
  margin: 20px 0;
  max-height: calc(100vh - 400px);
  overflow-y: auto;
}

.el-button + .el-button {
  margin-left: 10px;
}

.el-button.download-btn {
  color: #67C23A;
  
  &:hover {
    color: #85ce61;
  }
}
</style> 