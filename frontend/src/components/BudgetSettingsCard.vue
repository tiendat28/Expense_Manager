<script setup>
import { ref, onMounted } from 'vue'
import { useBudgetStore } from '../stores/budget'
import { useToastStore } from '../stores/toast'
import { EXPENSE_CATEGORIES } from '../utils/formatters'

const budget = useBudgetStore()
const toast = useToastStore()
const overall = ref(0)
const categoryTexts = ref({})

async function saveBudgets() {
  const category_budgets = {}
  for (const [k, v] of Object.entries(categoryTexts.value)) {
    if (v && Number(v) > 0) category_budgets[k] = Number(v)
  }
  await budget.update({ monthly_budget: Number(overall.value), category_budgets })
  toast.show('Đã lưu thành công')
}

onMounted(async () => {
  await budget.fetch()
  overall.value = budget.monthlyBudget
  categoryTexts.value = { ...budget.categoryBudgets }
})
</script>

<template>
  <div class="bg-white rounded-2xl p-5 card-shadow">
    <h2 class="font-semibold mb-3">Ngân sách</h2>
    <label class="text-xs text-gray-900">Ngân sách tổng theo tháng</label>
    <input v-model="overall" type="number" class="w-full border rounded-lg px-3 py-2 mb-3" />
    <label class="text-xs text-gray-900">Ngân sách theo danh mục (để trống = không giới hạn)</label>
    <div v-for="c in EXPENSE_CATEGORIES" :key="c.value" class="flex items-center gap-2 py-1">
      <span>{{ c.icon }}</span>
      <span class="flex-1 text-sm">{{ c.value }}</span>
      <input v-model="categoryTexts[c.value]" type="number" placeholder="0" class="w-28 border rounded-lg px-2 py-1 text-right" />
    </div>
    <button @click="saveBudgets" class="mt-3 w-full bg-green-600 text-white rounded-lg py-2">Lưu ngân sách</button>
  </div>
</template>
