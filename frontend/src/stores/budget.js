import { defineStore } from 'pinia'
import client from '../api/client'

export const useBudgetStore = defineStore('budget', {
  state: () => ({ monthlyBudget: 5000000, categoryBudgets: {} }),
  actions: {
    async fetch() {
      const { data } = await client.get('/budgets')
      this.monthlyBudget = data.monthly_budget
      this.categoryBudgets = data.category_budgets
    },
    async update(payload) {
      const { data } = await client.put('/budgets', payload)
      this.monthlyBudget = data.monthly_budget
      this.categoryBudgets = data.category_budgets
    },
  },
})
