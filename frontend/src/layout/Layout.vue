<template>
  <div class="app-wrapper">
    <!-- 侧边栏 -->
    <div class="sidebar-container">
      <div class="logo">
        <span>管理系统</span>
      </div>
      <el-menu
        :default-active="$route.path"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <!-- 首页 -->
        <el-menu-item index="/dashboard">
          <i class="el-icon-s-home"></i>
          <span slot="title">首页</span>
        </el-menu-item>

        <!-- 视频相关功能组 -->
        <el-menu-item-group title="视频功能">
          <!-- YouTube下载器 -->
          <el-menu-item index="/youtube">
            <i class="el-icon-video-play"></i>
            <span slot="title">YouTube下载器</span>
          </el-menu-item>

          <!-- 视频分析 -->
          <el-menu-item index="/video-analysis">
            <i class="el-icon-film"></i>
            <span slot="title">视频分析</span>
          </el-menu-item>

          <!-- 视频剪辑 -->
          <el-menu-item index="/video-editor">
            <i class="el-icon-scissors"></i>
            <span slot="title">视频剪辑</span>
          </el-menu-item>
        </el-menu-item-group>

        <!-- 文件管理相关组 -->
        <el-menu-item-group title="文件管理">
          <!-- 文件管理器 -->
          <el-menu-item index="/files">
            <i class="el-icon-folder"></i>
            <span slot="title">文件管理</span>
          </el-menu-item>

          <!-- 草稿箱 -->
          <el-menu-item index="/drafts">
            <i class="el-icon-document"></i>
            <span slot="title">草稿箱</span>
          </el-menu-item>
        </el-menu-item-group>

        <!-- 系统设置 -->
        <el-menu-item index="/settings">
          <i class="el-icon-setting"></i>
          <span slot="title">配置中心</span>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <navbar />
      
      <!-- 主要内容 -->
      <div class="app-main">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './components/Navbar'

export default {
  name: 'Layout',
  components: {
    Navbar
  }
}
</script>

<style lang="scss" scoped>
.app-wrapper {
  height: 100%;
  width: 100%;
  display: flex;
}

.sidebar-container {
  width: 210px;
  height: 100%;
  background: #304156;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  overflow-y: auto;

  .logo {
    height: 50px;
    line-height: 50px;
    text-align: center;
    color: #fff;
    font-size: 20px;
    font-weight: bold;
    border-bottom: 1px solid #1f2d3d;
  }

  .el-menu {
    border: none;
  }

  .el-menu-item-group__title {
    padding: 10px 20px;
    color: #909399;
    font-size: 12px;
    line-height: normal;
    height: auto;
  }
}

.main-container {
  flex: 1;
  margin-left: 210px;
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.app-main {
  flex: 1;
  padding: 20px;
  background: #f0f2f5;
  position: relative;
}

// 美化滚动条
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #304156;
}

::-webkit-scrollbar-thumb {
  background: #41546d;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #4a5f7c;
}
</style> 