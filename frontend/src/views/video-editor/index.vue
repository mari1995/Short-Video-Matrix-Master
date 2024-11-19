<template>
  <div class="video-editor">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>图片生成视频</span>
      </div>

      <!-- 图片上传区域 -->
      <el-upload
        class="image-uploader"
        action="#"
        :auto-upload="false"
        :on-change="handleImageChange"
        :file-list="imageList"
        multiple
        list-type="picture-card"
        accept="image/*"
      >
        <i class="el-icon-plus"></i>
        <div class="el-upload__tip" slot="tip">选择多张图片，将按顺序生成视频</div>
      </el-upload>

      <!-- 视频参数设置 -->
      <div class="video-settings" v-if="imageList.length > 0">
        <el-form :model="videoSettings" label-width="100px">
          <el-form-item label="视频时长">
            <el-input-number 
              v-model="videoSettings.duration" 
              :min="1" 
              :max="60"
              :step="1"
            /> 秒
          </el-form-item>
          
          <el-form-item label="转场效果">
            <el-select v-model="videoSettings.transition">
              <el-option label="淡入淡出" value="fade" />
              <el-option label="滑动" value="slide" />
              <el-option label="缩放" value="zoom" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="背景音乐">
            <el-upload
              class="music-uploader"
              action="#"
              :auto-upload="false"
              :on-change="handleMusicChange"
              :show-file-list="false"
              accept="audio/*"
            >
              <el-button size="small" type="primary">选择音乐</el-button>
              <span v-if="musicFile" class="music-name">{{ musicFile.name }}</span>
            </el-upload>
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              @click="handleGenerate"
              :loading="generating"
            >
              生成视频
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 生成历史 -->
      <div class="generate-history">
        <h3>生成��史</h3>
        <el-table
          :data="historyList"
          v-loading="loading"
          style="width: 100%"
        >
          <el-table-column
            prop="created_at"
            label="创建时间"
            width="180"
          >
            <template slot-scope="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          
          <el-table-column
            prop="status"
            label="状态"
            width="100"
          >
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column
            prop="duration"
            label="时长"
            width="100"
          >
            <template slot-scope="scope">
              {{ scope.row.duration }}秒
            </template>
          </el-table-column>
          
          <el-table-column
            label="操作"
            width="150"
            fixed="right"
          >
            <template slot-scope="scope">
              <el-button
                v-if="scope.row.status === 'completed'"
                type="text"
                size="small"
                @click="handlePreview(scope.row)"
              >
                预览
              </el-button>
              <el-button
                v-if="scope.row.status === 'completed'"
                type="text"
                size="small"
                @click="handleDownload(scope.row)"
              >
                下载
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 预览对话框 -->
    <el-dialog
      title="视频预览"
      :visible.sync="showPreview"
      width="70%"
      :before-close="handleClosePreview"
    >
      <div class="video-preview">
        <video
          v-if="previewUrl"
          ref="videoPlayer"
          class="video-player"
          controls
          :src="previewUrl"
        >
          您的浏览器不支持 HTML5 视频播放
        </video>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { generateVideo, getGenerateStatus, getGenerateHistory } from '@/api/video-editor'

export default {
  name: 'VideoEditor',
  data() {
    return {
      imageList: [],
      musicFile: null,
      videoSettings: {
        duration: 10,
        transition: 'fade'
      },
      generating: false,
      loading: false,
      historyList: [],
      showPreview: false,
      previewUrl: '',
      currentPage: 1,
      pageSize: 10,
      total: 0
    }
  },
  created() {
    this.loadHistory()
  },
  methods: {
    handleImageChange(file, fileList) {
      this.imageList = fileList
    },
    
    handleMusicChange(file) {
      this.musicFile = file
    },
    
    async handleGenerate() {
      if (this.imageList.length < 2) {
        this.$message.warning('请至少选择2张图片')
        return
      }
      
      this.generating = true
      try {
        const formData = new FormData()
        
        // 添加图片文件
        this.imageList.forEach((file, index) => {
          formData.append('images', file.raw)
        })
        
        // 添加音乐文件
        if (this.musicFile) {
          formData.append('music', this.musicFile.raw)
        }
        
        // 添加视频设置
        formData.append('settings', JSON.stringify(this.videoSettings))
        
        const response = await generateVideo(formData)
        this.$message.success('开始生成视频')
        this.loadHistory()
      } catch (error) {
        this.$message.error(error.response?.data?.detail || '生成失败')
      } finally {
        this.generating = false
      }
    },
    
    async loadHistory() {
      this.loading = true
      try {
        const response = await getGenerateHistory({
          skip: (this.currentPage - 1) * this.pageSize,
          limit: this.pageSize
        })
        this.historyList = response.data.items
        this.total = response.data.total
      } catch (error) {
        this.$message.error('加载历史记录失败')
      } finally {
        this.loading = false
      }
    },
    
    getStatusType(status) {
      const types = {
        completed: 'success',
        processing: 'warning',
        failed: 'danger'
      }
      return types[status] || 'info'
    },
    
    getStatusText(status) {
      const texts = {
        completed: '完成',
        processing: '处理中',
        failed: '失败'
      }
      return texts[status] || status
    },
    
    formatDate(timestamp) {
      return new Date(timestamp * 1000).toLocaleString()
    },
    
    handlePreview(record) {
      this.previewUrl = record.video_url
      this.showPreview = true
    },
    
    handleDownload(record) {
      const link = document.createElement('a')
      link.href = record.video_url
      link.download = `video_${record.id}.mp4`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    
    handleClosePreview() {
      if (this.$refs.videoPlayer) {
        this.$refs.videoPlayer.pause()
      }
      this.showPreview = false
      this.previewUrl = ''
    }
  }
}
</script>

<style lang="scss" scoped>
.video-editor {
  padding: 20px;
}

.image-uploader {
  .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    
    &:hover {
      border-color: #409EFF;
    }
  }
}

.video-settings {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 4px;
}

.music-uploader {
  display: inline-block;
  
  .music-name {
    margin-left: 10px;
    color: #606266;
  }
}

.generate-history {
  margin-top: 30px;
  
  h3 {
    margin-bottom: 20px;
    color: #303133;
  }
}

.video-preview {
  text-align: center;
  
  .video-player {
    max-width: 100%;
    max-height: 70vh;
  }
}

.el-upload--picture-card {
  width: 148px;
  height: 148px;
  line-height: 146px;
}

.el-upload-list--picture-card .el-upload-list__item {
  width: 148px;
  height: 148px;
}
</style> 