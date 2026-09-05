import { defineStore } from 'pinia'
import client from '../api/client'

export const useBillsStore = defineStore('bills', {
  state: () => ({ items: [] }),
  actions: {
    async fetchAll() {
      const { data } = await client.get('/bills')
      this.items = data
    },
    async create(payload) {
      await client.post('/bills', payload)
      await this.fetchAll()
    },
    async update(id, payload) {
      await client.put(`/bills/${id}`, payload)
      await this.fetchAll()
    },
    async remove(id) {
      await client.delete(`/bills/${id}`)
      await this.fetchAll()
    },
    async toggleActive(id) {
      await client.post(`/bills/${id}/toggle-active`)
      await this.fetchAll()
    },
    async markPaid(id) {
      await client.post(`/bills/${id}/mark-paid`, null, { params: { add_as_expense: true } })
      await this.fetchAll()
    },
  },
})
