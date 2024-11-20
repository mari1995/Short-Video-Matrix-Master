<template>
  <div class="settings-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>系统配置</span>
        <div class="header-buttons">
          <el-button 
            type="success"
            class="buy-api-btn"
            size="medium"
            icon="el-icon-shopping-cart-2"
            @click="handleBuyApi"
          >
            <i class="el-icon-key"></i>
            购买 API Key
          </el-button>
          <el-button 
            type="text"
            @click="showAddDialog"
          >
            添加配置
          </el-button>
        </div>
      </div>

      <el-table
        :data="configs"
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column
          prop="config_key"
          label="配置键"
          width="180"
        />
        
        <el-table-column
          prop="config_value"
          label="配置值"
        >
          <template slot-scope="scope">
            <template v-if="scope.row.is_secret">
              ******
            </template>
            <template v-else>
              {{ scope.row.config_value }}
            </template>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="description"
          label="描述"
        />
        
        <el-table-column
          label="操作"
          width="150"
          fixed="right"
        >
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="handleEdit(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              type="text"
              size="small"
              class="delete-btn"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '添加配置' : '编辑配置'"
      :visible.sync="dialogVisible"
      width="500px"
    >
      <el-form
        ref="configForm"
        :model="configForm"
        :rules="configRules"
        label-width="100px"
      >
        <el-form-item 
          label="配置键" 
          prop="config_key"
          v-if="dialogType === 'add'"
        >
          <el-input v-model="configForm.config_key" />
        </el-form-item>
        
        <el-form-item 
          label="配置值" 
          prop="config_value"
        >
          <el-input 
            v-model="configForm.config_value"
            :type="configForm.is_secret ? 'password' : 'text'"
          />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input 
            type="textarea" 
            v-model="configForm.description"
          />
        </el-form-item>
        
        <el-form-item label="是否加密" prop="is_secret">
          <el-switch v-model="configForm.is_secret" />
        </el-form-item>
      </el-form>
      
      <span slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { settingsApi } from '@/api'

export default {
  name: 'Settings',
  data() {
    return {
      loading: false,
      configs: [],
      dialogVisible: false,
      dialogType: 'add', // add or edit
      configForm: {
        config_key: '',
        config_value: '',
        description: '',
        is_secret: false
      },
      configRules: {
        config_key: [
          { required: true, message: '请输入配置键', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9_]+$/, message: '只能包含字母、数字和下划线', trigger: 'blur' }
        ],
        config_value: [
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
        const response = await settingsApi.getConfigs()
        this.configs = response.data
      } catch (error) {
        this.$message.error('加载配置失败')
      } finally {
        this.loading = false
      }
    },

    showAddDialog() {
      this.dialogType = 'add'
      this.configForm = {
        config_key: '',
        config_value: '',
        description: '',
        is_secret: false
      }
      this.dialogVisible = true
    },

    handleEdit(row) {
      this.dialogType = 'edit'
      this.configForm = {
        config_key: row.config_key,
        config_value: row.config_value,
        description: row.description,
        is_secret: row.is_secret
      }
      this.dialogVisible = true
    },

    async handleSubmit() {
      try {
        await this.$refs.configForm.validate()
        
        if (this.dialogType === 'add') {
          await settingsApi.createConfig(this.configForm)
          this.$message.success('添加成功')
        } else {
          await settingsApi.updateConfig(this.configForm.config_key, {
            config_value: this.configForm.config_value,
            description: this.configForm.description,
            is_secret: this.configForm.is_secret
          })
          this.$message.success('更新成功')
        }
        
        this.dialogVisible = false
        this.loadConfigs()
      } catch (error) {
        this.$message.error(error.response?.data?.detail || '操作失败')
      }
    },

    async handleDelete(row) {
      try {
        await this.$confirm('确定要删除这个配置吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await settingsApi.deleteConfig(row.config_key)
        this.$message.success('删除成功')
        this.loadConfigs()
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error(error.response?.data?.detail || '删除失败')
        }
      }
    },

    handleBuyApi() {
      window.open('https://api.cinfohubs.buzz/', '_blank')
    }
  }
}
</script>

<style lang="scss" scoped>
.settings-container {
  padding: 20px;
}

.header-buttons {
  float: right;
  display: flex;
  align-items: center;
  gap: 15px;
}

.buy-api-btn {
  background: linear-gradient(45deg, #67C23A, #85ce61) !important;
  border: none !important;
  color: white !important;
  padding: 10px 20px !important;
  border-radius: 20px !important;
  font-weight: 600 !important;
  letter-spacing: 1px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  box-shadow: 0 2px 6px rgba(103, 194, 58, 0.3);
  transition: all 0.3s ease !important;
  
  i {
    margin-right: 6px;
    font-size: 16px;
    vertical-align: middle;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(103, 194, 58, 0.4) !important;
    background: linear-gradient(45deg, #85ce61, #95d475) !important;
  }
  
  &:active {
    transform: translateY(1px);
    box-shadow: 0 2px 4px rgba(103, 194, 58, 0.2) !important;
  }
  
  &:focus {
    outline: none;
  }
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