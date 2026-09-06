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
  'flex flex-col items-center justify-center gap-0.5 flex-1 py-1.5 text-[10px] font-medium',
  isActive(tabName) ? 'text-green-700' : 'text-gray-500',
]
</script>

<template>
  <nav class="sm:hidden fixed bottom-0 inset-x-0 bg-white border-t z-20 flex overflow-x-auto">
    <router-link v-for="item in items" :key="item.name" :to="{ name: item.name }" :class="itemClass(item.name)">
      <span class="text-lg leading-none">{{ item.icon }}</span>
      <span>{{ item.label }}</span>
    </router-link>
  </nav>
</template>
