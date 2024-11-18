<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical"
        background-color="#304156"
        text-color="#fff"
        active-text-color="#409EFF"
        router
      >
        <template v-for="item in menuItems">
          <!-- 有子菜单的情况 -->
          <el-submenu 
            v-if="item.children" 
            :index="item.path || item.title" 
            :key="item.title"
          >
            <template slot="title">
              <i :class="item.icon"></i>
              <span>{{ item.title }}</span>
            </template>
            <el-menu-item 
              v-for="child in item.children"
              :key="child.path"
              :index="child.path"
            >
              <i :class="child.icon"></i>
              <span>{{ child.title }}</span>
            </el-menu-item>
          </el-submenu>
          
          <!-- 没有子菜单的情况 -->
          <el-menu-item 
            v-else 
            :index="item.path"
            :key="item.path"
          >
            <i :class="item.icon"></i>
            <span slot="title">{{ item.title }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header>
        <div class="header-right">
          <el-dropdown>
            <span class="el-dropdown-link">
              管理员<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人信息</el-dropdown-item>
              <el-dropdown-item>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { menuItems } from './components/Sidebar/menu'

export default {
  name: 'Layout',
  data() {
    return {
      menuItems
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100%;
}
.el-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.el-aside {
  background-color: #304156;
}
.el-menu {
  border-right: none;
}
.header-right {
  margin-right: 20px;
}
.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
}
</style> 