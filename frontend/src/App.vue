<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'
import AppBottomNav from './components/AppBottomNav.vue'
import ToastContainer from './components/ToastContainer.vue'

const route = useRoute()
const auth = useAuthStore()
const showShell = computed(() => !route.meta.public)

onMounted(() => {
  if (auth.isAuthenticated && !auth.user) {
    auth.fetchMe().catch(() => {})
  }
})
</script>

<template>
  <div v-if="showShell" class="h-screen bg-gray-50 flex flex-col overflow-hidden">
    <AppHeader />
    <div class="flex flex-1 min-h-0">
      <AppSidebar />
      <main class="flex-1 overflow-y-auto overflow-x-hidden pb-16 sm:pb-0">
        <router-view />
      </main>
    </div>
    <AppBottomNav />
  </div>
  <div v-else class="min-h-screen bg-gray-50">
    <router-view />
  </div>
  <ToastContainer />
</template>
