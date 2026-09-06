<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <header class="bg-green-700 text-white sticky top-0 z-20">
    <div class="flex items-center justify-between px-4 py-3">
      <div class="flex items-center gap-2">
        <span class="text-2xl">💰</span>
        <span class="font-bold text-lg">Quản Lý Chi Tiêu</span>
      </div>
      <div class="flex items-center gap-3">
        <span class="hidden sm:inline text-sm text-green-50">{{ auth.user?.name || auth.user?.email || '' }}</span>
        <button
          @click="logout"
          title="Đăng xuất"
          aria-label="Đăng xuất"
          class="bg-green-800/60 hover:bg-green-800 rounded-full p-2 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
            <path d="M18.36 6.64a9 9 0 1 1-12.73 0" />
            <line x1="12" y1="2" x2="12" y2="12" />
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>
