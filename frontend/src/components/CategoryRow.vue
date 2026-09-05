<script setup>
import { computed } from 'vue'
import { formatVND } from '../utils/formatters'

const props = defineProps({
  category: String,
  icon: String,
  color: String,
  total: Number,
  limit: { type: Number, default: null },
})

const hasLimit = computed(() => props.limit && props.limit > 0)
const isOverLimit = computed(() => hasLimit.value && props.total > props.limit)
const percent = computed(() => {
  if (hasLimit.value) return Math.min(props.total / props.limit, 1) * 100
  return 0
})
</script>

<template>
  <div class="mb-3">
    <div class="flex items-center text-sm mb-1">
      <span class="w-6 text-center">{{ icon }}</span>
      <span class="flex-1 ml-2">{{ category }}</span>
      <span v-if="hasLimit" class="text-xs" :class="isOverLimit ? 'text-red-600 font-bold' : 'text-gray-900'">
        {{ formatVND(total) }}/{{ formatVND(limit) }}
      </span>
      <span v-else class="font-medium text-red-600">{{ formatVND(total) }}</span>
    </div>
    <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
      <div
        class="h-full rounded-full"
        :style="{ width: (hasLimit ? percent : 0) + '%', backgroundColor: isOverLimit ? '#ef4444' : color }"
      ></div>
    </div>
  </div>
</template>
