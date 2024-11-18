<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 统计卡片 -->
      <el-col :span="6" v-for="(item, index) in statistics" :key="index">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon">
            <i :class="item.icon"></i>
          </div>
          <div class="stat-info">
            <div class="stat-title">{{ item.title }}</div>
            <div class="stat-value">{{ item.value }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近分析记录 -->
    <el-card class="recent-analyses" style="margin-top: 20px;">
      <div slot="header">
        <span>最近分析记录</span>
      </div>
      <el-table
        :data="recentAnalyses"
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column
          prop="file_name"
          label="文件名"
          min-width="200"
        />
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
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { getStatistics, getRecentAnalyses } from '@/api/statistics'

export default {
  name: 'Dashboard',
  
  data() {
    return {
      loading: false,
      statistics: [
        { title: '总分析次数', value: 0, icon: 'el-icon-data-analysis' },
        { title: '今日分析', value: 0, icon: 'el-icon-time' },
        { title: '视频数量', value: 0, icon: 'el-icon-video-camera' },
        { title: '图片数量', value: 0, icon: 'el-icon-picture' }
      ],
      recentAnalyses: []
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    async fetchData() {
      this.loading = true
      try {
        // 获取统计数据
        const statsRes = await getStatistics()
        const stats = statsRes.data
        
        // 更新统计卡片数据
        this.statistics[0].value = stats.total_analyses || 0
        this.statistics[1].value = stats.today_analyses || 0
        this.statistics[2].value = stats.video_count || 0
        this.statistics[3].value = stats.image_count || 0

        // 获取最近分析记录
        const recentRes = await getRecentAnalyses()
        this.recentAnalyses = recentRes.data.items || []

      } catch (error) {
        console.error('Error fetching dashboard data:', error)
        this.$message.error('获取统计数据失败')
      } finally {
        this.loading = false
      }
    },

    formatDate(timestamp) {
      return new Date(timestamp * 1000).toLocaleString()
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
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  font-size: 48px;
  margin-right: 20px;
  color: #409EFF;
}

.stat-info {
  flex-grow: 1;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.recent-analyses {
  margin-top: 20px;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .el-col {
    margin-bottom: 20px;
  }
}
</style> 