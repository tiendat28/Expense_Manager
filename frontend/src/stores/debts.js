import { defineStore } from 'pinia'
import client from '../api/client'

export const useDebtsStore = defineStore('debts', {
  state: () => ({ items: [] }),
  getters: {
    oweList: (state) => state.items.filter((d) => d.type === 'owe'),
    lentList: (state) => state.items.filter((d) => d.type === 'lent'),
    totalOwe: (state) =>
      state.items.filter((d) => d.type === 'owe').reduce((s, d) => s + Math.max(d.total_amount - d.paid_amount, 0), 0),
    totalLent: (state) =>
      state.items.filter((d) => d.type === 'lent').reduce((s, d) => s + Math.max(d.total_amount - d.paid_amount, 0), 0),
  },
  actions: {
    async fetchAll() {
      const { data } = await client.get('/debts')
      this.items = data
    },
    async create(payload) {
      await client.post('/debts', payload)
      await this.fetchAll()
    },
    async update(id, payload) {
      await client.put(`/debts/${id}`, payload)
      await this.fetchAll()
    },
    async remove(id) {
      await client.delete(`/debts/${id}`)
      await this.fetchAll()
    },
    async addPayment(id, payload) {
      await client.post(`/debts/${id}/payments`, payload)
      await this.fetchAll()
    },
    async updatePayment(id, paymentId, payload) {
      await client.put(`/debts/${id}/payments/${paymentId}`, payload)
      await this.fetchAll()
    },
    async removePayment(id, paymentId) {
      await client.delete(`/debts/${id}/payments/${paymentId}`)
      await this.fetchAll()
    },
  },
})
