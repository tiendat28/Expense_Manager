<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push({ name: 'dashboard' })
  } catch (e) {
    error.value = e.response?.data?.detail || 'Đăng nhập thất bại'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <form @submit.prevent="submit" class="bg-white p-8 rounded-2xl shadow-sm w-full max-w-sm space-y-4">
      <h1 class="text-2xl font-bold text-center">Đăng nhập</h1>
      <input v-model="email" type="email" placeholder="Email" required class="w-full border rounded-lg px-3 py-2" />
      <input v-model="password" type="password" placeholder="Mật khẩu" required class="w-full border rounded-lg px-3 py-2" />
      <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
      <button :disabled="loading" class="w-full bg-green-600 text-white rounded-lg py-2 font-medium disabled:opacity-50">
        {{ loading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
      </button>
      <p class="text-center text-sm text-gray-900">
        Chưa có tài khoản?
        <router-link to="/register" class="text-green-600">Đăng ký</router-link>
      </p>
    </form>
  </div>
</template>
