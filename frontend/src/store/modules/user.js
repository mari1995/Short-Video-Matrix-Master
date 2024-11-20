import userApi from '@/api'
import { getToken, setToken, removeToken } from '@/utils/auth'
import router from '@/router'

const state = {
  token: getToken()
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  }
}

const actions = {
  // 用户登录
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      userApi.login({ username: username.trim(), password: password })
        .then(response => {
          const { data } = response
          commit('SET_TOKEN', data.access_token)
          setToken(data.access_token)
          resolve()
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  // 用户登出
  logout({ commit }) {
    return new Promise((resolve, reject) => {
      userApi.logout().then(() => {
        // 清除 token
        commit('SET_TOKEN', '')
        removeToken()
        // 重定向到登录页
        router.push('/login')
        resolve()
      }).catch(error => {
        // 即使退出失败也清除 token
        commit('SET_TOKEN', '')
        removeToken()
        router.push('/login')
        reject(error)
      })
    })
  },

  // 移除 Token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      removeToken()
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 