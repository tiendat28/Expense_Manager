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
  'flex items-center justify-center flex-1 py-2.5',
  isActive(tabName) ? 'text-green-700' : 'text-gray-400',
]
</script>

<template>
  <nav class="sm:hidden fixed bottom-0 inset-x-0 bg-white border-t z-20 flex">
    <router-link v-for="item in items" :key="item.name" :to="{ name: item.name }" :class="itemClass(item.name)" :title="item.label" :aria-label="item.label">
      <span class="text-xl leading-none">{{ item.icon }}</span>
    </router-link>
  </nav>
</template>
