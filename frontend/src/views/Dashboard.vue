<template>
  <div class="dashboard-container">
    <!-- 统计卡片 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="card-header">
            <i class="el-icon-user"></i>
            <span>用户总数</span>
          </div>
          <div class="card-number">{{ stats.total_users || 0 }}</div>
          <div class="card-footer">
            本周新增: {{ stats.new_users_this_week || 0 }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="card-header">
            <i class="el-icon-data-line"></i>
            <span>今日活跃用户</span>
          </div>
          <div class="card-number">{{ stats.today_active_users || 0 }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 趋势图表 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="24">
        <el-card shadow="hover">
          <div slot="header">
            <span>用户增长趋势</span>
          </div>
          <div class="chart-container" ref="userTrendChart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getStatisticsOverview } from '@/api/statistics'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {
        total_users: 0,
        today_active_users: 0,
        new_users_this_week: 0,
        user_trend: []
      },
      userTrendChart: null
    }
  },
  methods: {
    async fetchData() {
      try {
        const token = this.$store.state.token
        if (!token) {
          this.$message.error('请先登录')
          this.$router.push('/login')
          return
        }

        const data = await getStatisticsOverview()
        this.stats = data
        this.initUserTrendChart()
      } catch (error) {
        console.error('获取统计数据失败:', error)
        if (error.response?.status === 401) {
          this.$message.error('登录已过期，请重新登录')
          this.$store.dispatch('logout')
          this.$router.push('/login')
        } else {
          this.$message.error('获取统计数据失败')
        }
      }
    },
    initUserTrendChart() {
      if (this.userTrendChart) {
        this.userTrendChart.dispose()
      }
      
      this.userTrendChart = echarts.init(this.$refs.userTrendChart)
      
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: this.stats.user_trend.map(item => item.date),
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          minInterval: 1
        },
        series: [{
          name: '新增用户',
          type: 'line',
          smooth: true,
          data: this.stats.user_trend.map(item => item.value),
          areaStyle: {
            opacity: 0.3
          }
        }]
      }
      
      this.userTrendChart.setOption(option)
    }
  },
  mounted() {
    this.fetchData()
    window.addEventListener('resize', () => {
      if (this.userTrendChart) {
        this.userTrendChart.resize()
      }
    })
  },
  beforeDestroy() {
    if (this.userTrendChart) {
      this.userTrendChart.dispose()
    }
    window.removeEventListener('resize', this.userTrendChart.resize)
  }
}
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 20px;
  
  .stat-card {
    .card-header {
      display: flex;
      align-items: center;
      margin-bottom: 15px;
      
      i {
        font-size: 20px;
        margin-right: 10px;
        color: #409EFF;
      }
      
      span {
        font-size: 16px;
        color: #606266;
      }
    }
    
    .card-number {
      font-size: 28px;
      font-weight: bold;
      color: #303133;
      margin-bottom: 10px;
    }
    
    .card-footer {
      font-size: 14px;
      color: #909399;
    }
  }
  
  .chart-row {
    margin-top: 20px;
    
    .chart-container {
      height: 400px;
    }
  }
}
</style> 