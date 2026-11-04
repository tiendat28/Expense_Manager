<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { primaryTabs, moreTabs, settingsTab, isTabActive } from '../navTabs'
import { useFabStore } from '../stores/fab'

const route = useRoute()
const router = useRouter()
const fab = useFabStore()
const showMore = ref(false)
const moreItems = [...moreTabs, settingsTab]

const leftTabs = primaryTabs.slice(0, 2)
const rightTabs = primaryTabs.slice(2)

const isActive = (tabName) => isTabActive(tabName, route.name)

const isMoreActive = computed(() => moreItems.some((item) => isActive(item.name)))

const itemClass = (tabName) => [
  'flex flex-col items-center justify-center gap-1 flex-1 min-w-0 py-2 rounded-2xl transition-all',
  isActive(tabName)
    ? 'text-emerald-600 dark:text-emerald-400 font-bold'
    : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-200',
]

const moreButtonClass = computed(() => [
  'flex flex-col items-center justify-center gap-1 flex-1 min-w-0 py-2 rounded-2xl transition-all',
  isMoreActive.value
    ? 'text-emerald-600 dark:text-emerald-400 font-bold'
    : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-200',
])

function onAdd() {
  showMore.value = false
  if (!fab.trigger()) router.push({ name: 'transactions', query: { add: '1' } })
}
</script>

<template>
  <div v-if="showMore" class="md:hidden fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs" @click="showMore = false"></div>

  <!-- More Sheet -->
  <div
    v-if="showMore"
    class="md:hidden fixed bottom-20 inset-x-3 z-50 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/80 dark:border-slate-800 shadow-2xl p-2 space-y-1 animate-fade-in"
  >
    <router-link
      v-for="item in moreItems"
      :key="item.name"
      :to="{ name: item.name }"
      @click="showMore = false"
      class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors"
      :class="
        isActive(item.name)
          ? 'bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 font-semibold'
          : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
      "
    >
      <i :class="[item.icon, 'w-5 text-center text-sm']"></i>
      <span>{{ item.label }}</span>
    </router-link>
  </div>

  <!-- Bottom Navigation Bar (Mobile < 768px) -->
  <nav class="md:hidden fixed bottom-3 inset-x-3 z-30 bg-white/95 dark:bg-slate-900/95 backdrop-blur-xl rounded-[28px] border border-slate-200/90 dark:border-slate-700/80 card-shadow flex items-center px-1.5 py-1">
    <router-link v-for="item in leftTabs" :key="item.name" :to="{ name: item.name }" :class="itemClass(item.name)">
      <i :class="[item.icon, 'text-base']"></i>
      <span class="text-[10px] leading-tight truncate max-w-full px-0.5">{{ item.label }}</span>
    </router-link>

    <!-- Center Floating Action Button -->
    <button type="button" class="flex-1 min-w-0 flex justify-center -mt-6 cursor-pointer" aria-label="Thêm mới" @click="onAdd">
      <span
        class="glass-fab w-12 h-12 rounded-full bg-gradient-to-br from-emerald-500 via-emerald-600 to-green-600 text-white text-xl flex items-center justify-center shadow-lg shadow-emerald-500/35 active:scale-95 transition"
      >
        <i class="fa-solid fa-plus"></i>
      </span>
    </button>

    <router-link v-for="item in rightTabs" :key="item.name" :to="{ name: item.name }" :class="itemClass(item.name)">
      <i :class="[item.icon, 'text-base']"></i>
      <span class="text-[10px] leading-tight truncate max-w-full px-0.5">{{ item.label }}</span>
    </router-link>

    <button type="button" :class="moreButtonClass" @click="showMore = !showMore">
      <i class="fa-solid fa-bars text-base"></i>
      <span class="text-[10px] leading-tight truncate max-w-full px-0.5">Thêm</span>
    </button>
  </nav>
</template>
