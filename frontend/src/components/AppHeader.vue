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
          class="text-sm bg-green-800/60 hover:bg-green-800 rounded-full px-3 py-1.5 transition-colors"
        >
          Đăng xuất
        </button>
      </div>
    </div>
  </header>
</template>
