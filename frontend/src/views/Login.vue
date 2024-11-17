<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="title">管理后台系统</div>
      <el-form
        ref="loginForm"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="el-icon-user"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="el-icon-lock"
            @keyup.enter.native="handleLogin"
          />
        </el-form-item>
        <el-button
          :loading="loading"
          type="primary"
          class="login-button"
          @click="handleLogin"
        >
          登录
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { login } from '@/api/auth'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      },
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      try {
        await this.$refs.loginForm.validate()
        this.loading = true
        
        const response = await login(this.loginForm)
        if (response.access_token) {
          this.$store.commit('SET_TOKEN', response.access_token)
          await this.$router.push('/')
          this.$message.success('登录成功')
        }
      } catch (error) {
        console.error('登录错误:', error)
        this.$message.error(error.response?.data?.detail || '登录失败')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f3f3f3;

  .login-card {
    width: 400px;
    padding: 20px;

    .title {
      text-align: center;
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 30px;
    }

    .login-form {
      .login-button {
        width: 100%;
      }
    }
  }
}
</style> 