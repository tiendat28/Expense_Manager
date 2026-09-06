<script setup>
import { useRoute } from 'vue-router'
import { navTabs, settingsTab } from '../navTabs'

const route = useRoute()
const items = [...navTabs, settingsTab]

function isActive(tabName) {
  return route.name === tabName || (tabName === 'savings' && route.name === 'savings-detail') ||
    (tabName === 'debts' && route.name === 'debt-detail')
}

const itemClass = (tabName) => [
  'flex flex-col items-center justify-center gap-0.5 flex-1 min-w-0 py-1.5 rounded-2xl transition-colors',
  isActive(tabName) ? 'bg-green-100 text-green-700' : 'text-gray-400',
]
</script>

<template>
  <nav class="glass sm:hidden fixed bottom-3 inset-x-3 z-20 bg-white/80 backdrop-blur-xl rounded-[28px] border border-white/40 flex px-1 py-1">
    <router-link v-for="item in items" :key="item.name" :to="{ name: item.name }" :class="itemClass(item.name)">
      <span class="text-lg leading-none">{{ item.icon }}</span>
      <span class="text-[9px] leading-none font-medium truncate max-w-full px-0.5">{{ item.label }}</span>
    </router-link>
  </nav>
</template>
