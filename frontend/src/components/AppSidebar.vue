<script setup>
import { useRoute } from 'vue-router'
import { navTabs as tabs } from '../navTabs'

const route = useRoute()

function isActive(tabName) {
  return route.name === tabName || (tabName === 'savings' && route.name === 'savings-detail') ||
    (tabName === 'debts' && route.name === 'debt-detail')
}

const linkClass = (tabName) => [
  'flex items-center gap-3 mx-2 mb-1 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors',
  isActive(tabName) ? 'bg-green-50 text-green-700' : 'text-gray-900 hover:bg-gray-50',
]
</script>

<template>
  <nav class="hidden sm:flex bg-white border-r w-56 shrink-0 py-4 flex-col overflow-y-auto">
    <div>
      <router-link v-for="tab in tabs" :key="tab.name" :to="{ name: tab.name }" :class="linkClass(tab.name)">
        <span class="text-lg">{{ tab.icon }}</span>
        <span>{{ tab.label }}</span>
      </router-link>
    </div>

    <div class="mt-auto pt-2 border-t">
      <router-link :to="{ name: 'settings' }" :class="linkClass('settings')">
        <span class="text-lg">⚙️</span>
        <span>Cài đặt</span>
      </router-link>
    </div>
  </nav>
</template>
