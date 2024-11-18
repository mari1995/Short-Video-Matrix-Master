<template>
  <div class="video-analysis">
    <el-card class="upload-card">
      <div class="upload-area">
        <el-upload
          class="upload-component"
          drag
          :action="`${API_URL}/api/v1/video-analysis/upload`"
          :headers="uploadHeaders"
          :before-upload="beforeUpload"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          accept="video/*"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">
            将视频拖到此处，或<em>点击上传</em>
          </div>
          <div class="el-upload__tip" slot="tip">只能上传视频文件</div>
        </el-upload>
      </div>
    </el-card>

    <!-- 分析列表 -->
    <el-card class="analysis-list">
      <div slot="header">
        <span>分析记录</span>
        <el-button 
          style="float: right; padding: 3px 0" 
          type="text"
          @click="loadAnalyses"
        >
          刷新
        </el-button>
      </div>

      <el-table
        :data="analysesList"
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column
          prop="file_name"
          label="文件名"
          min-width="200"
        />
        
        <el-table-column
          prop="resolution"
          label="分辨率"
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
          prop="frame_count"
          label="总帧数"
          width="100"
        />
        
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
          label="操作"
          width="150"
          fixed="right"
        >
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="viewAnalysis(scope.row)"
              :disabled="scope.row.status !== 'completed'"
            >
              查看分析
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
          :total="total"
        />
      </div>
    </el-card>

    <!-- 分析结果对话框 -->
    <el-dialog
      title="视频分析结果"
      :visible.sync="showAnalysis"
      width="90%"
      class="analysis-dialog"
    >
      <div v-if="currentAnalysis" class="analysis-content">
        <div class="analysis-info">
          <h3>视频信息</h3>
          <p>文件名：{{ currentAnalysis.file_name }}</p>
          <p>分辨率：{{ currentAnalysis.resolution }}</p>
          <p>时长：{{ formatDuration(currentAnalysis.duration) }}</p>
          <p>帧率：{{ currentAnalysis.fps }} fps</p>
          <p>总帧数：{{ currentAnalysis.frame_count }}</p>
        </div>

        <div class="frames-grid">
          <h3>关键帧 ({{ currentAnalysis.frames_data?.length || 0 }})</h3>
          <el-row :gutter="20">
            <el-col 
              :span="getFrameSpan(frame)"
              v-for="frame in currentAnalysis.frames_data" 
              :key="frame.frame_number"
            >
              <el-card :body-style="{ padding: '0px' }">
                <div 
                  class="frame-image-container"
                  :class="getAspectRatioClass(frame)"
                >
                  <img 
                    :src="frame.url" 
                    class="frame-image"
                    @load="onImageLoad($event, frame)"
                  >
                </div>
                <div class="frame-info">
                  <p>帧号：{{ frame.frame_number }}</p>
                  <p>时间点：{{ formatDuration(frame.timestamp) }}</p>
                  <p v-if="frame.diff_score">差异度：{{ frame.diff_score.toFixed(2) }}</p>
                  <p>分辨率：{{ frame.resolution || '加载中...' }}</p>
                  <p>比例：{{ frame.aspectRatio || '计算中...' }}</p>
                  
                  <!-- 添加解析图片描述按钮 -->
                  <el-button 
                    type="text" 
                    size="small" 
                    @click="handleAnalyzeFrame(frame)"
                    :loading="frame.analyzing"
                  >
                    {{ frame.descriptions ? '查看描述' : '解析图片描述' }}
                  </el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-dialog>

    <!-- 添加图片解析结果对话框 -->
    <el-dialog
      title="帧图片解析结果"
      :visible.sync="showFrameAnalysis"
      width="600px"
      append-to-body
      @closed="handleDialogClose"
    >
      <div v-if="currentFrame" class="frame-analysis">
        <div class="image-preview">
          <img 
            :src="currentFrame.url" 
            class="preview-image"
            @error="handleImageError"
          >
        </div>
        <div class="result-content">
          <div v-if="currentFrame.descriptions && currentFrame.descriptions.length" class="result-item">
            <div class="description-container">
              <div class="description-header">
                <span class="description-title">图片描述：</span>
                <el-button 
                  type="text" 
                  size="small" 
                  @click="copyDescription(currentFrame.descriptions[0].text)"
                  class="copy-btn"
                >
                  <i class="el-icon-document-copy"></i> 复制
                </el-button>
              </div>
              <div class="description-content">
                {{ currentFrame.descriptions[0].text }}
              </div>
            </div>
          </div>
          <el-empty v-else description="无解析结果"></el-empty>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { API_URL } from '@/config/api.config'
import { uploadVideo, getAnalysisList, getAnalysisDetail } from '@/api/video'
import { analyzeImage } from '@/api/image'

export default {
  name: 'VideoAnalysis',
  data() {
    return {
      API_URL,
      uploadHeaders: {
        // 如果需要添加认证信息等，可以在这里设置
      },
      loading: false,
      analysesList: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      showAnalysis: false,
      currentAnalysis: null,
      analyzing: false,
      showFrameAnalysis: false,
      currentFrame: null,
      timestamp: Date.now(),
    }
  },
  created() {
    this.loadAnalyses()
  },
  methods: {
    beforeUpload(file) {
      const isVideo = file.type.startsWith('video/')
      if (!isVideo) {
        this.$message.error('只能上传视频文件！')
        return false
      }
      return true
    },
    
    handleUploadSuccess(response) {
      this.$message.success('上传成功，开始分析视频')
      this.loadAnalyses()
    },
    
    handleUploadError(err) {
      this.$message.error('上传失败：' + err.message)
    },
    
    async loadAnalyses() {
      this.loading = true
      try {
        const skip = (this.currentPage - 1) * this.pageSize
        const response = await getAnalysisList({
          skip,
          limit: this.pageSize
        })
        this.analysesList = response.data.items
        this.total = response.data.total
      } catch (error) {
        this.$message.error('加载分析记录失败')
      } finally {
        this.loading = false
      }
    },
    
    handlePageChange(page) {
      this.currentPage = page
      this.loadAnalyses()
    },
    
    async viewAnalysis(analysis) {
      try {
        const response = await getAnalysisDetail(analysis.id)
        this.currentAnalysis = response.data
        this.showAnalysis = true
      } catch (error) {
        this.$message.error('获取分析结果失败')
      }
    },
    
    formatDuration(seconds) {
      if (!seconds) return '0:00'
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = Math.round(seconds % 60)
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
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
    
    onImageLoad(event, frame) {
      const img = event.target
      // 获取图片实际尺寸
      const width = img.naturalWidth
      const height = img.naturalHeight
      
      // 计算分辨率和宽高比
      frame.resolution = `${width}x${height}`
      frame.aspectRatio = this.calculateAspectRatio(width, height)
      
      // 强制更新视图
      this.$forceUpdate()
    },
    
    calculateAspectRatio(width, height) {
      const gcd = this.getGCD(width, height)
      return `${width/gcd}:${height/gcd}`
    },
    
    getGCD(a, b) {
      // 计算最大公约数
      return b === 0 ? a : this.getGCD(b, a % b)
    },
    
    getFrameSpan(frame) {
      // 根据图片比例返回不同的栅格跨度
      if (!frame.aspectRatio) return 6 // 默认值
      
      const [w, h] = frame.aspectRatio.split(':').map(Number)
      const ratio = w / h
      
      if (ratio > 1.7) { // 宽屏 16:9
        return 8
      } else if (ratio < 0.7) { // 竖屏 9:16
        return 4
      } else { // 接近正方形
        return 6
      }
    },
    
    getAspectRatioClass(frame) {
      if (!frame.aspectRatio) return ''
      
      const [w, h] = frame.aspectRatio.split(':').map(Number)
      const ratio = w / h
      
      if (ratio > 1.7) {
        return 'widescreen'
      } else if (ratio < 0.7) {
        return 'vertical'
      } else {
        return 'square'
      }
    },
    
    async analyzeFrame(frame) {
      this.analyzing = true
      try {
        const response = await this.$axios.post('/api/v1/video-analysis/analyze-frame', {
          image_path: frame.image_path
        })
        
        // 将解析结果添加到帧数据中
        this.$set(frame, 'descriptions', response.data.descriptions)
        
        this.$message.success('解析成功')
      } catch (error) {
        this.$message.error(error.response?.data?.detail || '解析失败')
      } finally {
        this.analyzing = false
      }
    },
    
    copyDescription(text) {
      navigator.clipboard.writeText(text).then(() => {
        this.$message({
          message: '描述文本已复制到剪贴板',
          type: 'success',
          duration: 2000
        });
      }).catch(() => {
        this.$message.error('复制失败，请手动复制');
      });
    },
    
    formatTimestamp(timestamp) {
      const minutes = Math.floor(timestamp / 60)
      const seconds = Math.floor(timestamp % 60)
      const milliseconds = Math.floor((timestamp % 1) * 1000)
      return `${minutes}:${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(3, '0')}`
    },
    
    async handleAnalyzeFrame(frame) {
      if (frame.descriptions) {
        this.currentFrame = { ...frame }
        this.showFrameAnalysis = true
        return
      }

      this.$set(frame, 'analyzing', true)
      
      try {
        const formData = new FormData()
        const response = await fetch(frame.url)
        const blob = await response.blob()
        formData.append('image_file', blob, 'frame.jpg')
        
        const result = await analyzeImage(formData)
        this.$set(frame, 'descriptions', result.data.descriptions)
        this.currentFrame = { ...frame }
        this.showFrameAnalysis = true
        
      } catch (error) {
        this.$message.error(error.response?.data?.detail || '图片解析失败')
      } finally {
        this.$set(frame, 'analyzing', false)
      }
    },
    
    handleDialogClose() {
      // 对话框关闭时更新时间戳
      this.timestamp = Date.now()
      // 清除当前帧
      this.currentFrame = null
    },
    
    handleImageError() {
      this.$message.error('图片加载失败')
    },
  }
}
</script>

<style scoped>
.video-analysis {
  padding: 20px;
  height: 100%;
  background-color: #f0f2f5;
}

.upload-card {
  margin-bottom: 20px;
}

.upload-area {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.analysis-list {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.analysis-dialog {
  .analysis-content {
    max-height: 70vh;
    overflow-y: auto;
  }
}

.analysis-info {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 4px;
}

.frames-grid {
  margin-top: 20px;
}

.frame-image-container {
  position: relative;
  width: 100%;
  overflow: hidden;
  background: #000;
}

/* 16:9 宽屏比例 */
.frame-image-container.widescreen {
  padding-bottom: 56.25%; /* 16:9 = 9/16 = 0.5625 */
}

/* 9:16 竖屏比例 */
.frame-image-container.vertical {
  padding-bottom: 177.78%; /* 9:16 = 16/9 = 1.7778 */
}

/* 1:1 正方形比例 */
.frame-image-container.square {
  padding-bottom: 100%;
}

.frame-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #000;
}

.frame-info {
  padding: 10px;
  font-size: 12px;
  color: #606266;
  background: #f8f9fa;
}

.frame-info p {
  margin: 5px 0;
  line-height: 1.4;
}

/* 响应式布局调整 */
@media (max-width: 1200px) {
  .el-col {
    width: 33.33% !important;
  }
}

@media (max-width: 768px) {
  .el-col {
    width: 50% !important;
  }
}

@media (max-width: 480px) {
  .el-col {
    width: 100% !important;
  }
}

.el-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
  
  &:hover {
    transform: translateY(-2px);
  }
}

.frame-analysis {
  padding: 20px;
}

.image-preview {
  text-align: center;
  margin-bottom: 20px;
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 4px;
}

.result-content {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
}

.description-container {
  background: #fff;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 15px;
  border: 1px solid #ebeef5;
}

.description-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.description-title {
  font-weight: bold;
  color: #303133;
}

.description-content {
  color: #606266;
  line-height: 1.6;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
}

.copy-btn {
  padding: 0;
}

.copy-btn:hover {
  color: #409EFF;
}
</style> 