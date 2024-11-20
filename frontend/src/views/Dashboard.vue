<template>
  <div class="dashboard-container">
    <el-card class="welcome-card">
      <div class="welcome-header">
        <h1>欢迎使用 Short-Video-Matrix-Master</h1>
        <p class="subtitle">一站式短视频管理与分析平台</p>
      </div>

      <el-divider></el-divider>

      <div class="feature-section">
        <h2>主要功能</h2>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="feature-card">
              <i class="el-icon-video-play"></i>
              <h3>YouTube 视频下载</h3>
              <p>支持 YouTube 视频和 Shorts 下载，自动记录下载历史</p>
            </div>
          </el-col>
          
          <el-col :span="8">
            <div class="feature-card">
              <i class="el-icon-film"></i>
              <h3>视频智能分析</h3>
              <p>自动提取关键帧，AI 分析图片内容，生成详细描述</p>
            </div>
          </el-col>
          
          <el-col :span="8">
            <div class="feature-card">
              <i class="el-icon-scissors"></i>
              <h3>视频剪辑工具</h3>
              <p>支持图片合成视频，添加转场效果和背景音乐</p>
            </div>
          </el-col>
        </el-row>

        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :span="8">
            <div class="feature-card">
              <i class="el-icon-folder"></i>
              <h3>文件管理</h3>
              <p>统一管理上传的视频、图片等文件，支持预览和下载</p>
            </div>
          </el-col>
          
          <el-col :span="8">
            <div class="feature-card">
              <i class="el-icon-document"></i>
              <h3>草稿箱</h3>
              <p>临时存储和管理素材，支持从视频分析结果添加</p>
            </div>
          </el-col>
          
          <el-col :span="8">
            <div class="feature-card">
              <i class="el-icon-setting"></i>
              <h3>系统配置</h3>
              <p>灵活的系统设置，支持配置 API 密钥等参数</p>
            </div>
          </el-col>
        </el-row>
      </div>

      <el-divider></el-divider>

      <div class="quick-start">
        <h2>快速开始</h2>
        <el-steps :active="1" simple>
          <el-step title="配置系统" description="在系统配置中设置 API 密钥"></el-step>
          <el-step title="上传视频" description="上传视频或使用 YouTube 下载器"></el-step>
          <el-step title="开始分析" description="使用视频分析工具处理视频"></el-step>
        </el-steps>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Dashboard'
}
</script>

<style lang="scss" scoped>
.dashboard-container {
  
  .welcome-card {
    margin-bottom: 20px;
  }
  
  .welcome-header {
    text-align: center;
    margin-bottom: 30px;
    
    h1 {
      color: #303133;
      margin-bottom: 10px;
    }
    
    .subtitle {
      color: #606266;
      font-size: 16px;
    }
  }
  
  .feature-section {
    margin: 30px 0;
    
    h2 {
      color: #303133;
      margin-bottom: 20px;
    }
  }
  
  .feature-card {
    text-align: center;
    padding: 20px;
    height: 100%;
    background: #f8f9fa;
    border-radius: 8px;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    i {
      font-size: 40px;
      color: #409EFF;
      margin-bottom: 15px;
    }
    
    h3 {
      color: #303133;
      margin-bottom: 10px;
    }
    
    p {
      color: #606266;
      font-size: 14px;
      line-height: 1.6;
    }
  }
  
  .quick-start {
    margin: 30px 0;
    
    h2 {
      color: #303133;
      margin-bottom: 20px;
    }
  }
}
</style> 