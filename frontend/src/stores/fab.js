import { defineStore } from 'pinia'

// Cho nút "+" ở thanh điều hướng mobile gọi được hành động thêm mới của trang đang mở.
export const useFabStore = defineStore('fab', {
  state: () => ({ handler: null }),
  actions: {
    register(fn) {
      this.handler = fn
    },
    unregister(fn) {
      if (this.handler === fn) this.handler = null
    },
    // Trả về true nếu trang hiện tại có đăng ký hành động thêm mới.
    trigger() {
      if (!this.handler) return false
      this.handler()
      return true
    },
  },
})
