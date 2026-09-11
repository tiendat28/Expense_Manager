<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { primaryTabs, moreTabs, settingsTab } from '../navTabs'
import { useFabStore } from '../stores/fab'

const route = useRoute()
const router = useRouter()
const fab = useFabStore()
const showMore = ref(false)
const moreItems = [...moreTabs, settingsTab]

const leftTabs = primaryTabs.slice(0, 2)
const rightTabs = primaryTabs.slice(2)

function isActive(tabName) {
  return route.name === tabName || (tabName === 'savings' && route.name === 'savings-detail') ||
    (tabName === 'debts' && route.name === 'debt-detail')
}

const isMoreActive = computed(() => moreItems.some((item) => isActive(item.name)))

const itemClass = (tabName) => [
  'flex flex-col items-center justify-center gap-0.5 flex-1 min-w-0 py-1.5 rounded-2xl transition-colors',
  isActive(tabName) ? 'bg-green-100 text-green-700' : 'text-gray-400',
]

const moreButtonClass = computed(() => [
  'flex flex-col items-center justify-center gap-0.5 flex-1 min-w-0 py-1.5 rounded-2xl transition-colors',
  isMoreActive.value ? 'bg-green-100 text-green-700' : 'text-gray-400',
])

function onAdd() {
  showMore.value = false
  if (fab.handler) fab.trigger()
  else router.push({ name: 'transactions', query: { add: '1' } })
}
</script>

<template>
  <div v-if="showMore" class="sm:hidden fixed inset-0 z-20" @click="showMore = false"></div>

  <div v-if="showMore" class="sm:hidden fixed bottom-20 inset-x-3 z-30 bg-white rounded-2xl card-shadow p-2 space-y-1">
    <router-link
      v-for="item in moreItems"
      :key="item.name"
      :to="{ name: item.name }"
      @click="showMore = false"
      class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors"
      :class="isActive(item.name) ? 'bg-green-50 text-green-700' : 'text-gray-900 hover:bg-gray-50'"
    >
      <span class="text-lg">{{ item.icon }}</span>
      <span>{{ item.label }}</span>
    </router-link>
  </div>

  <nav class="glass sm:hidden fixed bottom-3 inset-x-3 z-20 bg-white/80 backdrop-blur-xl rounded-[28px] border border-white/40 flex items-center px-1 py-1">
    <router-link v-for="item in leftTabs" :key="item.name" :to="{ name: item.name }" :class="itemClass(item.name)">
      <span class="text-lg leading-none">{{ item.icon }}</span>
      <span class="text-[9px] leading-none font-medium truncate max-w-full px-0.5">{{ item.label }}</span>
    </router-link>

    <button type="button" class="flex-1 min-w-0 flex justify-center" aria-label="Thêm mới" @click="onAdd">
      <span
        class="glass-fab -mt-6 w-[52px] h-[52px] rounded-full bg-gradient-to-br from-green-500 to-green-700 text-white text-2xl leading-none flex items-center justify-center"
      >+</span>
    </button>

    <router-link v-for="item in rightTabs" :key="item.name" :to="{ name: item.name }" :class="itemClass(item.name)">
      <span class="text-lg leading-none">{{ item.icon }}</span>
      <span class="text-[9px] leading-none font-medium truncate max-w-full px-0.5">{{ item.label }}</span>
    </router-link>

    <button type="button" :class="moreButtonClass" @click="showMore = !showMore">
      <span class="text-lg leading-none">☰</span>
      <span class="text-[9px] leading-none font-medium truncate max-w-full px-0.5">Thêm</span>
    </button>
  </nav>
</template>
