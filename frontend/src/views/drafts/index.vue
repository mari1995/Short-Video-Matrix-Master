<template>
  <div class="drafts-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>草稿箱</span>
        <el-button 
          style="float: right; margin-left: 10px;"
          type="primary"
          size="small"
          @click="showUploadDialog"
        >
          新建草稿
        </el-button>
        <el-button 
          style="float: right;"
          type="text"
          @click="loadDrafts"
        >
          刷新
        </el-button>
      </div>

      <!-- 草稿列表 -->
      <div class="drafts-grid">
        <el-row :gutter="20">
          <el-col 
            :xs="24" :sm="12" :md="8" :lg="6"
            v-for="item in draftsList" 
            :key="item.id"
          >
            <el-card :body-style="{ padding: '0px' }" class="draft-card">
              <div class="draft-image" @click="handlePreview(item)">
                <img :src="item.file_url" class="image">
                <div class="image-hover">
                  <i class="el-icon-zoom-in"></i>
                </div>
              </div>
              <div class="draft-info">
                <h3 class="title" :title="item.title">{{ item.title }}</h3>
                <div class="description" v-if="item.description">
                  {{ item.description }}
                </div>
                <div class="meta">
                  <span class="time">{{ formatDate(item.created_at) }}</span>
                  <div class="actions">
                    <el-button 
                      type="text" 
                      size="mini"
                      @click="handlePreview(item)"
                    >
                      预览
                    </el-button>
                    <el-button 
                      type="text" 
                      size="mini"
                      class="delete-btn"
                      @click="handleDelete(item)"
                    >
                      删除
                    </el-button>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 分页 -->
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

    <!-- 上传对话框 -->
    <el-dialog
      title="新建草稿"
      :visible.sync="showUpload"
      width="500px"
    >
      <el-form 
        ref="uploadForm"
        :model="uploadForm"
        :rules="uploadRules"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="uploadForm.title" />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input 
            type="textarea"
            v-model="uploadForm.description"
            :rows="3"
          />
        </el-form-item>

        <el-form-item label="图片" prop="file">
          <el-upload
            class="upload-demo"
            :action="`${API_URL}/api/v1/drafts/upload`"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :before-upload="beforeUpload"
            :data="uploadForm"
            accept="image/*"
            :auto-upload="false"
            ref="upload"
          >
            <el-button slot="trigger" size="small" type="primary">选择图片</el-button>
            <div slot="tip" class="el-upload__tip">只能上传图片文件</div>
          </el-upload>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="showUpload = false">取消</el-button>
        <el-button type="primary" @click="submitUpload" :loading="uploading">
          上传
        </el-button>
      </span>
    </el-dialog>

    <!-- 预览对话框 -->
    <el-dialog
      :title="currentDraft?.title"
      :visible.sync="showPreview"
      width="70%"
      class="preview-dialog"
    >
      <div class="preview-content">
        <div class="preview-image-container">
          <img 
            v-if="currentDraft?.file_type === 'image'"
            :src="currentDraft?.file_url"
            class="preview-image"
          >
        </div>
        <div class="preview-info">
          <div class="info-item">
            <label>创建时间：</label>
            <span>{{ formatDate(currentDraft?.created_at) }}</span>
          </div>
          <div class="info-item" v-if="currentDraft?.description">
            <label>描述：</label>
            <div class="description-text">{{ currentDraft.description }}</div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { API_URL } from '@/config/api.config'
import { getDraftsList, deleteDraft } from '@/api/drafts'

export default {
  name: 'Drafts',
  data() {
    return {
      API_URL,
      loading: false,
      uploading: false,
      draftsList: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      showUpload: false,
      showPreview: false,
      currentDraft: null,
      uploadForm: {
        title: '',
        description: ''
      },
      uploadRules: {
        title: [
          { required: true, message: '请输入标题', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.loadDrafts()
  },
  methods: {
    async loadDrafts() {
      this.loading = true
      try {
        const response = await getDraftsList({
          skip: (this.currentPage - 1) * this.pageSize,
          limit: this.pageSize
        })
        this.draftsList = response.data.items
        this.total = response.data.total
      } catch (error) {
        this.$message.error('加载草稿箱失败')
      } finally {
        this.loading = false
      }
    },

    handlePageChange(page) {
      this.currentPage = page
      this.loadDrafts()
    },

    formatDate(timestamp) {
      return new Date(timestamp * 1000).toLocaleString()
    },

    showUploadDialog() {
      this.uploadForm = {
        title: '',
        description: ''
      }
      this.showUpload = true
    },

    beforeUpload(file) {
      const isImage = file.type.startsWith('image/')
      if (!isImage) {
        this.$message.error('只能上传图片文件!')
        return false
      }
      return true
    },

    submitUpload() {
      this.$refs.uploadForm.validate(valid => {
        if (valid) {
          this.uploading = true
          this.$refs.upload.submit()
        }
      })
    },

    handleUploadSuccess(response) {
      this.uploading = false
      this.showUpload = false
      this.$message.success('上传成功')
      this.loadDrafts()
    },

    handleUploadError(err) {
      this.uploading = false
      this.$message.error('上传失败：' + err.message)
    },

    handlePreview(draft) {
      this.currentDraft = draft
      this.showPreview = true
    },

    async handleDelete(draft) {
      try {
        await this.$confirm('确定要删除这个草稿吗？', '提示', {
          type: 'warning'
        })
        
        await deleteDraft(draft.id)
        this.$message.success('删除成功')
        this.loadDrafts()
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.drafts-container {
  padding: 20px;
}

.drafts-grid {
  margin: 20px 0;
}

.draft-card {
  margin-bottom: 20px;
  transition: all 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
  }
}

.draft-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  cursor: pointer;
  
  .image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: all 0.3s;
  }
  
  .image-hover {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transition: all 0.3s;
    
    i {
      color: #fff;
      font-size: 30px;
    }
  }
  
  &:hover {
    .image {
      transform: scale(1.1);
    }
    
    .image-hover {
      opacity: 1;
    }
  }
}

.draft-info {
  padding: 14px;
  
  .title {
    margin: 0;
    font-size: 16px;
    color: #303133;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .description {
    margin: 10px 0;
    font-size: 13px;
    color: #606266;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
  
  .meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid #ebeef5;
    
    .time {
      font-size: 12px;
      color: #909399;
    }
    
    .actions {
      .delete-btn {
        color: #F56C6C;
      }
    }
  }
}

.preview-dialog {
  .preview-content {
    .preview-image-container {
      text-align: center;
      margin-bottom: 20px;
      
      .preview-image {
        max-width: 100%;
        max-height: 500px;
        object-fit: contain;
      }
    }
    
    .preview-info {
      padding: 20px;
      background: #f8f9fa;
      border-radius: 4px;
      
      .info-item {
        margin-bottom: 15px;
        
        label {
          font-weight: bold;
          color: #303133;
          margin-right: 10px;
        }
        
        .description-text {
          margin-top: 10px;
          padding: 10px;
          background: #fff;
          border-radius: 4px;
          color: #606266;
          line-height: 1.6;
        }
      }
    }
  }
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 