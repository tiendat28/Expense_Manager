<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useAuthForm } from '../composables/useAuthForm'
import AuthShell from '../components/PageTitle.vue'

const email = ref('')
const password = ref('')
const auth = useAuthStore()

const { error, loading, submit } = useAuthForm(
  () => auth.login(email.value, password.value),
  'Đăng nhập thất bại. Vui lòng kiểm tra lại email hoặc mật khẩu.'
)
</script>

<template>
  <AuthShell
    title="Đăng nhập tài khoản"
    :error="error"
    :loading="loading"
    submit-label="Đăng nhập"
    loading-label="Đang đăng nhập..."
    footer-text="Chưa có tài khoản?"
    footer-link-text="Đăng ký ngay"
    footer-link-to="/register"
    @submit="submit"
  >
    <div>
      <label class="form-label">Email</label>
      <input v-model="email" type="email" placeholder="name@example.com" required class="form-input" />
    </div>

    <div>
      <label class="form-label">Mật khẩu</label>
      <input v-model="password" type="password" placeholder="••••••••" required class="form-input" />
    </div>
  </AuthShell>
</template>
