<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'
import AppBottomNav from './components/AppBottomNav.vue'
import ToastContainer from './components/ToastContainer.vue'
import ConfirmDialog from './components/ConfirmDialog.vue'

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
  <div v-if="showShell" class="h-screen bg-slate-100/80 dark:bg-slate-950 text-slate-800 dark:text-slate-100 flex overflow-hidden transition-colors">
    <!-- Left Sidebar -->
    <AppSidebar />

    <!-- Main Content Column -->
    <div class="flex-1 flex flex-col h-screen overflow-hidden min-w-0">
      <AppHeader />
      <main class="flex-1 overflow-y-auto overflow-x-hidden p-3.5 sm:p-6 lg:p-8 space-y-5 sm:space-y-6 pb-24 md:pb-8">
        <router-view />
      </main>
    </div>

    <!-- Mobile Bottom Navigation -->
    <AppBottomNav />
  </div>

  <div v-else class="min-h-screen bg-slate-100/80 dark:bg-slate-950 text-slate-800 dark:text-slate-100">
    <router-view />
  </div>

  <ToastContainer />
  <ConfirmDialog />
</template>
