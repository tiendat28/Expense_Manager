<script setup>
import { computed } from 'vue'
import { useTransactionsStore } from '../stores/transactions'
import { useBudgetStore } from '../stores/budget'
import { formatVND, categoryMeta, EXPENSE_CATEGORIES } from '../utils/formatters'

defineProps({
  scrollable: { type: Boolean, default: false },
  emptyText: {
    type: String,
    default: 'Chưa có dữ liệu chi tiêu theo danh mục trong tháng này.',
  },
})

const txStore = useTransactionsStore()
const budgetStore = useBudgetStore()

const spentMap = computed(() => {
  const map = {}
  ;(txStore.monthlyStats.category_totals || []).forEach((c) => {
    map[c.category] = Number(c.total) || 0
  })
  return map
})

const items = computed(() => {
  const totals = txStore.monthlyStats.category_totals || []
  const maxSpent = Math.max(...totals.map((c) => Number(c.total) || 0), 1)

  const list = EXPENSE_CATEGORIES.map((cat) => {
    const limit = Number(budgetStore.categoryBudgets[cat.value]) || 0
    const spent = spentMap.value[cat.value] || 0
    const meta = categoryMeta(cat.value, 'expense')
    const over = limit > 0 && spent > limit
    const barWidth = limit > 0 ? Math.min(100, (spent / limit) * 100) : Math.min(100, (spent / maxSpent) * 100)
    const barHex = over ? '#ef4444' : meta.hex || '#10b981'

    return {
      category: cat.value,
      emoji: meta.emoji || '➖',
      limit,
      spent,
      over,
      barWidth,
      barHex,
    }
  }).filter((b) => b.spent > 0 || b.limit > 0)

  return list.sort((a, b) => b.spent - a.spent)
})
</script>

<template>
  <div
    v-if="items.length"
    :class="scrollable ? 'flex-1 overflow-y-auto pr-1.5 mt-4 space-y-4 min-h-0' : 'space-y-3.5'"
  >
    <div v-for="b in items" :key="b.category">
      <div class="flex items-center justify-between text-xs sm:text-sm mb-1.5">
        <span class="flex items-center gap-2 text-slate-800 dark:text-slate-100 font-medium">
          <span class="text-base leading-none">{{ b.emoji }}</span>
          <span>{{ b.category }}</span>
        </span>
        <span :class="b.over ? 'text-red-500 dark:text-red-400 font-bold' : 'text-slate-600 dark:text-slate-300 font-medium'">
          {{ formatVND(b.spent) }}<template v-if="b.limit > 0">/{{ formatVND(b.limit) }}</template>
        </span>
      </div>

      <div class="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
        <div
          class="h-full rounded-full progress-bar-fill"
          :style="{ width: b.barWidth + '%', backgroundColor: b.barHex }"
        ></div>
      </div>
    </div>
  </div>

  <p v-else class="text-xs text-slate-400 py-8 text-center">
    {{ emptyText }}
  </p>
</template>
