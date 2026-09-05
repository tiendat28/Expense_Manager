import { defineStore } from 'pinia'
import client from '../api/client'

export const useTransactionsStore = defineStore('transactions', {
  state: () => ({
    selectedYear: new Date().getFullYear(),
    selectedMonth: new Date().getMonth() + 1,
    items: [],
    monthlyStats: { income_total: 0, expense_total: 0, category_totals: [] },
    trend: [],
  }),
  actions: {
    async fetchMonth() {
      const { data } = await client.get('/transactions', {
        params: { year: this.selectedYear, month: this.selectedMonth },
      })
      this.items = data
    },
    async fetchStats() {
      const { data } = await client.get('/transactions/stats/monthly', {
        params: { year: this.selectedYear, month: this.selectedMonth },
      })
      this.monthlyStats = data
    },
    async fetchTrend() {
      const { data } = await client.get('/transactions/stats/trend', { params: { months: 6 } })
      this.trend = data
    },
    async refreshAll() {
      await Promise.all([this.fetchMonth(), this.fetchStats(), this.fetchTrend()])
    },
    changeMonth(delta) {
      let m = this.selectedMonth + delta
      let y = this.selectedYear
      if (m > 12) { m = 1; y += 1 }
      if (m < 1) { m = 12; y -= 1 }
      this.selectedMonth = m
      this.selectedYear = y
      this.refreshAll()
    },
    async create(payload) {
      await client.post('/transactions', payload)
      await this.refreshAll()
    },
    async update(id, payload) {
      await client.put(`/transactions/${id}`, payload)
      await this.refreshAll()
    },
    async remove(id) {
      await client.delete(`/transactions/${id}`)
      await this.refreshAll()
    },
  },
})
