import { ref } from 'vue'
import { useRouter } from 'vue-router'

/**
 * Phần dùng chung của form đăng nhập / đăng ký: cờ loading, thông báo lỗi,
 * và chuyển về trang chủ khi thành công.
 */
export function useAuthForm(action, failMessage) {
  const router = useRouter()
  const error = ref('')
  const loading = ref(false)

  async function submit() {
    error.value = ''
    loading.value = true
    try {
      await action()
      router.push({ name: 'dashboard' })
    } catch (e) {
      error.value = e.response?.data?.detail || failMessage
    } finally {
      loading.value = false
    }
  }

  return { error, loading, submit }
}
