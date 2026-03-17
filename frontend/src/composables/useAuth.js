import { reactive, computed } from 'vue'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

const state = reactive({
  token: localStorage.getItem('mirofish_token') || null,
  user: JSON.parse(localStorage.getItem('mirofish_user') || 'null'),
})

const isAuthenticated = computed(() => !!state.token)

function setAuth(token, user) {
  state.token = token
  state.user = user
  localStorage.setItem('mirofish_token', token)
  localStorage.setItem('mirofish_user', JSON.stringify(user))
}

function clearAuth() {
  state.token = null
  state.user = null
  localStorage.removeItem('mirofish_token')
  localStorage.removeItem('mirofish_user')
}

async function login(username, password) {
  const res = await axios.post(`${API_BASE}/api/auth/login`, { username, password })
  const data = res.data
  if (!data.success) {
    throw new Error(data.error || 'Login failed')
  }
  setAuth(data.token, data.user)
  return data
}

function logout() {
  clearAuth()
}

function getToken() {
  return state.token
}

async function checkAuth() {
  const token = state.token
  if (!token) return false
  try {
    const res = await axios.get(`${API_BASE}/api/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    if (res.data && res.data.success) {
      state.user = res.data.user
      return true
    }
    clearAuth()
    return false
  } catch {
    clearAuth()
    return false
  }
}

export function useAuth() {
  return {
    state,
    isAuthenticated,
    login,
    logout,
    getToken,
    checkAuth,
  }
}
