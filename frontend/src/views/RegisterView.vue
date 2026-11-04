<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useAuthForm } from '../composables/useAuthForm'
import AuthShell from '../components/PageTitle.vue'

const name = ref('')
const email = ref('')
const password = ref('')
const auth = useAuthStore()

const { error, loading, submit } = useAuthForm(
  () => auth.register(email.value, password.value, name.value),
  'Đăng ký thất bại. Vui lòng thử lại với email khác.'
)
</script>

<template>
  <AuthShell
    title="Tạo tài khoản mới"
    :error="error"
    :loading="loading"
    submit-label="Đăng ký tài khoản"
    loading-label="Đang tạo..."
    footer-text="Đã có tài khoản?"
    footer-link-text="Đăng nhập"
    footer-link-to="/login"
    @submit="submit"
  >
    <div>
      <label class="form-label">Họ và tên</label>
      <input v-model="name" type="text" placeholder="Minh Hoàng" required class="form-input" />
    </div>

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
