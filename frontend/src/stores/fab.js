import { defineStore } from 'pinia'

// Lets the mobile bottom nav "+" trigger the add action of whichever page is open.
export const useFabStore = defineStore('fab', {
  state: () => ({ handler: null }),
  actions: {
    register(fn) {
      this.handler = fn
    },
    unregister(fn) {
      if (this.handler === fn) this.handler = null
    },
    trigger() {
      if (this.handler) this.handler()
    },
  },
})
