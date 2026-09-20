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

// Mới nhất lên đầu
const sorted = computed(() => [...props.items].sort((a, b) => new Date(b.date) - new Date(a.date)))
</script>

<template>
  <h3 class="font-semibold mb-2 text-sm text-gray-900">{{ title }}</h3>
  <div class="bg-white rounded-2xl card-shadow divide-y mb-24">
    <p v-if="!sorted.length" class="text-center text-gray-900 py-6 text-sm">{{ emptyText }}</p>
    <div
      v-for="item in sorted"
      :key="item.id"
      class="flex items-center justify-between px-4 py-3 cursor-pointer"
      @click="$emit('select', item)"
    >
      <div>
        <div>{{ formatVND(item.amount) }}</div>
        <div class="text-xs text-gray-900">{{ formatDateTime(item.date) }}</div>
      </div>
      <span class="text-gray-300">›</span>
    </div>
  </div>
</template>
