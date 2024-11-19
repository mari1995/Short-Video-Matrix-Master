<template>
  <div class="dashboard">
    <el-card class="welcome-card">
      <div class="welcome-content">
        <h1>欢迎使用管理系统</h1>
        <p>这是一个基于 Vue + Element UI + FastAPI + SQLite 的现代化管理后台系统</p>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Dashboard'
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
}

.welcome-content {
  text-align: center;
  padding: 40px 20px;
}

.welcome-content h1 {
  color: #303133;
  margin-bottom: 20px;
}

.welcome-content p {
  color: #606266;
  font-size: 16px;
  line-height: 1.6;
}
</style> 