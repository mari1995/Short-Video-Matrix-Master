const TokenKey = 'Admin-Token'

export function getToken() {
  return localStorage.getItem(TokenKey)
}

export function setToken(token) {
  return localStorage.setItem(TokenKey, token)
}

export function removeToken() {
  // 清除 token
  localStorage.removeItem(TokenKey)
  // 清除其他相关的用户数据
  localStorage.removeItem('user')
  sessionStorage.clear()
} 