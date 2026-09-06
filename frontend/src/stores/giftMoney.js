import { defineStore } from 'pinia'
import client from '../api/client'

export const useGiftMoneyStore = defineStore('giftMoney', {
  state: () => ({ items: [] }),
  actions: {
    async fetchAll() {
      const { data } = await client.get('/gift-money')
      this.items = data
    },
    async create(payload) {
      await client.post('/gift-money', payload)
      await this.fetchAll()
    },
    async update(id, payload) {
      await client.put(`/gift-money/${id}`, payload)
      await this.fetchAll()
    },
    async remove(id) {
      await client.delete(`/gift-money/${id}`)
      await this.fetchAll()
    },
  },
})
