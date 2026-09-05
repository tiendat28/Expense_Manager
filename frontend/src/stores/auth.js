import { defineStore } from 'pinia'
import client from '../api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || null,
    user: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(email, password) {
      const { data } = await client.post('/auth/login', { email, password })
      this.setToken(data.access_token)
      await this.fetchMe()
    },
    async register(email, password, name) {
      const { data } = await client.post('/auth/register', { email, password, name })
      this.setToken(data.access_token)
      await this.fetchMe()
    },
    async fetchMe() {
      const { data } = await client.get('/auth/me')
      this.user = data
    },
    setToken(token) {
      this.token = token
      localStorage.setItem('access_token', token)
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('access_token')
    },
  },
})
