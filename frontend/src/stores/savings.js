import { defineStore } from 'pinia'
import client from '../api/client'

export const useSavingsStore = defineStore('savings', {
  state: () => ({ goals: [] }),
  actions: {
    async fetchAll() {
      const { data } = await client.get('/savings')
      this.goals = data
    },
    async create(payload) {
      await client.post('/savings', payload)
      await this.fetchAll()
    },
    async update(id, payload) {
      await client.put(`/savings/${id}`, payload)
      await this.fetchAll()
    },
    async remove(id) {
      await client.delete(`/savings/${id}`)
      await this.fetchAll()
    },
    async addContribution(goalId, payload) {
      await client.post(`/savings/${goalId}/contributions`, payload)
      await this.fetchAll()
    },
    async updateContribution(goalId, contributionId, payload) {
      await client.put(`/savings/${goalId}/contributions/${contributionId}`, payload)
      await this.fetchAll()
    },
    async removeContribution(goalId, contributionId) {
      await client.delete(`/savings/${goalId}/contributions/${contributionId}`)
      await this.fetchAll()
    },
  },
})
