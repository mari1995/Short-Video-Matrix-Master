<template>
  <div class="settings-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>系统配置</span>
        <el-button 
          style="float: right; margin-left: 10px;"
          type="primary"
          size="small"
          @click="showAddDialog"
        >
          添加配置
        </el-button>
        <el-button 
          style="float: right;"
          type="text"
          @click="loadConfigs"
        >
          刷新
        </el-button>
      </div>

      <el-table
        :data="configs"
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column
          prop="key"
          label="配置键"
          width="180"
        />
        
        <el-table-column
          prop="value"
          label="配置值"
          min-width="200"
        >
          <template slot-scope="scope">
            <el-input
              v-model="configForm[scope.row.key]"
              :type="scope.row.is_secret ? 'password' : 'text'"
              :placeholder="scope.row.description"
            >
              <template slot="append">
                <el-button 
                  type="primary"
                  size="small"
                  @click="updateConfig(scope.row.key)"
                  :loading="updating[scope.row.key]"
                >
                  保存
                </el-button>
              </template>
            </el-input>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="description"
          label="描述"
          min-width="200"
        />
        
        <el-table-column
          prop="is_secret"
          label="加密存储"
          width="100"
        >
          <template slot-scope="scope">
            <el-tag :type="scope.row.is_secret ? 'danger' : 'info'" size="small">
              {{ scope.row.is_secret ? '是' : '否' }}
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
              @click="showEditDialog(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              type="text"
              size="small"
              class="delete-btn"
              @click="handleDelete(scope.row)"
              :disabled="isSystemConfig(scope.row.key)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑配置对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '添加配置' : '编辑配置'"
      :visible.sync="dialogVisible"
      width="500px"
    >
      <el-form 
        ref="configDialogForm"
        :model="dialogForm"
        :rules="dialogRules"
        label-width="100px"
      >
        <el-form-item 
          label="配置键"
          prop="key"
          v-if="dialogType === 'add'"
        >
          <el-input v-model="dialogForm.key" />
        </el-form-item>
        
        <el-form-item label="配置值" prop="value">
          <el-input 
            v-model="dialogForm.value"
            :type="dialogForm.is_secret ? 'password' : 'text'"
          />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="dialogForm.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        
        <el-form-item label="加密存储">
          <el-switch v-model="dialogForm.is_secret" />
        </el-form-item>
      </el-form>
      
      <span slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleDialogConfirm">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  data() {
    return {
      loading: false,
      configs: [],
      configForm: {},
      updating: {},
      dialogVisible: false,
      dialogType: 'add', // add or edit
      dialogForm: {
        key: '',
        value: '',
        description: '',
        is_secret: false
      },
      dialogRules: {
        key: [
          { required: true, message: '请输入配置键', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9_]+$/, message: '只能包含字母、数字和下划线', trigger: 'blur' }
        ],
        value: [
          { required: true, message: '请输入配置值', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.loadConfigs()
  },
  methods: {
    async loadConfigs() {
      this.loading = true
      try {
        const response = await this.$axios.get('/api/v1/system-config')
        this.configs = response.data
        
        // 初始化表单数据
        this.configs.forEach(config => {
          this.$set(this.configForm, config.key, config.value)
          this.$set(this.updating, config.key, false)
        })
      } catch (error) {
        this.$message.error('加载配置失败')
      } finally {
        this.loading = false
      }
    },
    
    async updateConfig(key) {
      this.updating[key] = true
      try {
        await this.$axios.put(`/api/v1/system-config/${key}`, {
          value: this.configForm[key]
        })
        this.$message.success('更新成功')
        this.loadConfigs()
      } catch (error) {
        this.$message.error('更新失败')
      } finally {
        this.updating[key] = false
      }
    },
    
    showAddDialog() {
      this.dialogType = 'add'
      this.dialogForm = {
        key: '',
        value: '',
        description: '',
        is_secret: false
      }
      this.dialogVisible = true
    },
    
    showEditDialog(config) {
      this.dialogType = 'edit'
      this.dialogForm = {
        key: config.key,
        value: this.configForm[config.key],
        description: config.description,
        is_secret: config.is_secret
      }
      this.dialogVisible = true
    },
    
    async handleDialogConfirm() {
      this.$refs.configDialogForm.validate(async (valid) => {
        if (valid) {
          try {
            if (this.dialogType === 'add') {
              await this.$axios.post('/api/v1/system-config', this.dialogForm)
              this.$message.success('添加成功')
            } else {
              await this.$axios.put(`/api/v1/system-config/${this.dialogForm.key}`, {
                value: this.dialogForm.value,
                description: this.dialogForm.description,
                is_secret: this.dialogForm.is_secret
              })
              this.$message.success('更新成功')
            }
            this.dialogVisible = false
            this.loadConfigs()
          } catch (error) {
            this.$message.error(error.response?.data?.detail || '操作失败')
          }
        }
      })
    },
    
    async handleDelete(config) {
      try {
        await this.$confirm('确定要删除这个配置吗？', '提示', {
          type: 'warning'
        })
        
        await this.$axios.delete(`/api/v1/system-config/${config.key}`)
        this.$message.success('删除成功')
        this.loadConfigs()
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error(error.response?.data?.detail || '删除失败')
        }
      }
    },
    
    isSystemConfig(key) {
      return ['openai_base_url', 'openai_api_key'].includes(key)
    }
  }
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}

.el-form-item {
  margin-bottom: 22px;
}

.delete-btn {
  color: #F56C6C;
}

.delete-btn:hover {
  color: #f78989;
}

.el-table {
  margin-top: 20px;
}
</style> 