<script setup>
import { computed } from 'vue'
import { formatVND } from '../utils/formatters'
import { formatDateTime } from '../utils/date'

const props = defineProps({
  title: { type: String, required: true },
  items: { type: Array, default: () => [] },
  emptyText: { type: String, required: true },
})
defineEmits(['select'])

const sorted = computed(() => [...props.items].sort((a, b) => new Date(b.date) - new Date(a.date)))
</script>

<template>
  <div class="space-y-3">
    <h3 class="font-display font-bold text-sm text-slate-800 dark:text-slate-200">{{ title }}</h3>
    <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 divide-y divide-slate-100 dark:divide-slate-800 card-shadow overflow-hidden transition-colors">
      <p v-if="!sorted.length" class="text-center text-slate-400 py-6 text-xs">{{ emptyText }}</p>
      <div
        v-for="item in sorted"
        :key="item.id"
        class="flex items-center justify-between px-5 py-3.5 hover:bg-slate-50/80 dark:hover:bg-slate-800/50 cursor-pointer transition"
        @click="$emit('select', item)"
      >
        <div>
          <div class="font-bold text-sm text-emerald-600 dark:text-emerald-400">+{{ formatVND(item.amount) }}</div>
          <div class="text-[11px] text-slate-400 mt-0.5">{{ formatDateTime(item.date) }}</div>
        </div>
        <span class="text-slate-400 text-xs flex items-center gap-1">
          <span>Chi tiết</span>
          <i class="fa-solid fa-chevron-right text-[10px]"></i>
        </span>
      </div>
    </div>
  </div>
</template>
