import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue'), meta: { public: true } },
  { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue'), meta: { public: true } },
  { path: '/', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
  { path: '/transactions', name: 'transactions', component: () => import('../views/TransactionsView.vue') },
  { path: '/savings', name: 'savings', component: () => import('../views/SavingsView.vue') },
  { path: '/savings/:id', name: 'savings-detail', component: () => import('../views/SavingsDetailView.vue') },
  { path: '/debts', name: 'debts', component: () => import('../views/DebtsView.vue') },
  { path: '/debts/:id', name: 'debt-detail', component: () => import('../views/DebtDetailView.vue') },
  { path: '/bills', name: 'bills', component: () => import('../views/BillsView.vue') },
  { path: '/budget', name: 'budget', component: () => import('../views/BudgetView.vue') },
  { path: '/settings', name: 'settings', component: () => import('../views/SettingsView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: 'login' }
  }
  if (to.meta.public && auth.isAuthenticated) {
    return { name: 'dashboard' }
  }
})

export default router
