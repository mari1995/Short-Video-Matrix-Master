<template>
  <div class="file-manager">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>文件管理器</span>
        <el-breadcrumb separator="/" class="path-breadcrumb">
          <el-breadcrumb-item :to="{ path: '/files', query: { path: 'static' }}">static</el-breadcrumb-item>
          <el-breadcrumb-item 
            v-for="(part, index) in pathParts" 
            :key="index"
            :to="{ path: '/files', query: { path: getPathUpTo(index) }}"
          >
            {{ part }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </div>

      <el-table
        :data="fileList"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column label="名称" min-width="200">
          <template slot-scope="scope">
            <i :class="getFileIcon(scope.row)" class="file-icon"></i>
            <span 
              class="file-name"
              @click="handleFileClick(scope.row)"
              :class="{ 'is-folder': scope.row.is_dir }"
            >
              {{ scope.row.name }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="size" label="大小" width="120">
          <template slot-scope="scope">
            {{ formatFileSize(scope.row.size) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="modified_time" label="修改时间" width="180">
          <template slot-scope="scope">
            {{ formatDate(scope.row.modified_time) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="120" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="handleDelete(scope.row)"
              class="delete-btn"
            >
              删除
            </el-button>
            <el-button
              v-if="!scope.row.is_dir"
              type="text"
              size="small"
              @click="handleDownload(scope.row)"
            >
              下载
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加视频预览对话框 -->
    <el-dialog
      :title="currentFile ? currentFile.name : '视频预览'"
      :visible.sync="showVideoPreview"
      width="80%"
      :before-close="handleClosePreview"
      class="video-preview-dialog"
    >
      <div class="video-player-container">
        <video
          ref="videoPlayer"
          class="video-player"
          controls
          :src="videoUrl"
          @error="handleVideoError"
        >
          您的浏览器不支持 HTML5 视频播放
        </video>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClosePreview">关闭</el-button>
        <el-button type="primary" @click="handleDownload(currentFile)">下载</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'FileManager',
  data() {
    return {
      loading: false,
      fileList: [],
      currentPath: 'static',
      showVideoPreview: false,
      currentFile: null,
      videoUrl: '',
      baseUrl: process.env.VUE_APP_BASE_API || ''
    }
  },
  computed: {
    pathParts() {
      const path = this.currentPath
      return path.split('/').slice(1)
    }
  },
  created() {
    this.loadFiles()
  },
  watch: {
    '$route.query.path': {
      handler(newPath) {
        if (newPath) {
          this.currentPath = newPath
          this.loadFiles()
        }
      },
      immediate: true
    }
  },
  methods: {
    async loadFiles() {
      this.loading = true
      try {
        const response = await this.$axios.get(`/api/v1/files/list?path=${this.currentPath}`)
        this.fileList = response.data.items
      } catch (error) {
        this.$message.error('加载文件列表失败')
      } finally {
        this.loading = false
      }
    },
    
    getFileIcon(file) {
      if (file.is_dir) return 'el-icon-folder'
      const ext = file.name.split('.').pop().toLowerCase()
      const iconMap = {
        mp4: 'el-icon-video-camera',
        mp3: 'el-icon-headset',
        jpg: 'el-icon-picture',
        jpeg: 'el-icon-picture',
        png: 'el-icon-picture',
        pdf: 'el-icon-document',
      }
      return iconMap[ext] || 'el-icon-document'
    },
    
    handleFileClick(file) {
      if (file.is_dir) {
        this.$router.push({
          query: { path: file.path }
        })
      } else if (this.isVideoFile(file)) {
        this.previewVideo(file)
      }
    },
    
    isVideoFile(file) {
      return file.name.toLowerCase().endsWith('.mp4')
    },
    
    previewVideo(file) {
      this.currentFile = file
      this.videoUrl = `${this.baseUrl}/${file.path}`
      this.showVideoPreview = true
      
      // 在下一个 tick 后设置视频自动播放
      this.$nextTick(() => {
        if (this.$refs.videoPlayer) {
          this.$refs.videoPlayer.play().catch(() => {
            // 自动播放可能被浏览器阻止，这是正常的
            console.log('Auto-play was prevented')
          })
        }
      })
    },
    
    handleClosePreview() {
      if (this.$refs.videoPlayer) {
        this.$refs.videoPlayer.pause()
      }
      this.showVideoPreview = false
      this.currentFile = null
      this.videoUrl = ''
    },
    
    handleVideoError() {
      this.$message.error('视频加载失败')
      this.handleClosePreview()
    },
    
    async handleDelete(file) {
      try {
        await this.$confirm('确定要删除这个文件吗？', '提示', {
          type: 'warning'
        })
        
        await this.$axios.delete(`/api/v1/files/delete?path=${file.path}`)
        this.$message.success('删除成功')
        this.loadFiles()
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
        }
      }
    },
    
    handleDownload(file) {
      const link = document.createElement('a')
      link.href = `${this.baseUrl}/${file.path}`
      link.download = file.name
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
    },
    
    formatDate(timestamp) {
      return new Date(timestamp * 1000).toLocaleString()
    },
    
    getPathUpTo(index) {
      return ['static', ...this.pathParts.slice(0, index + 1)].join('/')
    }
  }
}
</script>

<style scoped>
.file-manager {
  padding: 20px;
}

.path-breadcrumb {
  margin-top: 10px;
}

.file-icon {
  margin-right: 8px;
  font-size: 16px;
}

.file-name {
  cursor: pointer;
}

.file-name:hover {
  color: #409EFF;
}

.is-folder {
  color: #409EFF;
  cursor: pointer;
}

.delete-btn {
  color: #F56C6C;
}

.delete-btn:hover {
  color: #f78989;
}

.video-preview-dialog {
  display: flex;
  flex-direction: column;
}

.video-player-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000;
  border-radius: 4px;
  overflow: hidden;
}

.video-player {
  width: 100%;
  max-height: 70vh;
  object-fit: contain;
}

/* 针对移动设备的响应式设计 */
@media (max-width: 768px) {
  .video-preview-dialog {
    width: 95% !important;
    margin: 0 auto;
  }
  
  .video-player {
    max-height: 50vh;
  }
}

/* 美化视频控制器 */
.video-player::-webkit-media-controls {
  background-color: rgba(0, 0, 0, 0.5);
}

.video-player::-webkit-media-controls-panel {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 10px;
}

/* 添加文件图标的颜色 */
.el-icon-video-camera {
  color: #409EFF;
}

/* 预览按钮样式 */
.preview-btn {
  color: #409EFF;
}

.preview-btn:hover {
  color: #66b1ff;
}
</style> 