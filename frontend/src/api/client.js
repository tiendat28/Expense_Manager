import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 401 ở đây nghĩa là token hết hạn -> đá về trang đăng nhập.
// Trừ chính lệnh đăng nhập/đăng ký: 401 lúc đó là "sai mật khẩu", phải để form tự hiện lỗi,
// nếu reload trang thì người dùng không kịp đọc thông báo.
const AUTH_ENDPOINTS = ['/auth/login', '/auth/register']

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const url = error.config?.url || ''
    const isAuthAttempt = AUTH_ENDPOINTS.some((path) => url.includes(path))
    if (error.response?.status === 401 && !isAuthAttempt) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default client
