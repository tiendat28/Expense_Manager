import { defineStore } from 'pinia'

let resolver = null

export const useConfirmStore = defineStore('confirm', {
  state: () => ({
    open: false,
    title: 'Xác nhận xóa',
    message: '',
    confirmText: 'Xóa',
    cancelText: 'Hủy',
  }),
  actions: {
    ask({ title = 'Xác nhận xóa', message, confirmText = 'Xóa', cancelText = 'Hủy' } = {}) {
      this.settle(false)
      this.title = title
      this.message = message
      this.confirmText = confirmText
      this.cancelText = cancelText
      this.open = true
      return new Promise((resolve) => {
        resolver = resolve
      })
    },
    settle(value) {
      this.open = false
      const resolve = resolver
      resolver = null
      if (resolve) resolve(value)
    },
  },
})
