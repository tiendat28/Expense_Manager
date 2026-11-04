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
  toast.show('Đã lưu thiết lập ngân sách thành công!')
}

onMounted(async () => {
  await budget.fetch()
  overall.value = budget.monthlyBudget
  categoryTexts.value = { ...budget.categoryBudgets }
})
</script>

<template>
  <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 p-5 sm:p-7 card-shadow max-w-2xl mx-auto flex flex-col max-h-[calc(100vh-7.5rem)] md:max-h-[calc(100vh-8rem)] transition-colors">
    <div class="border-b border-slate-100 dark:border-slate-800 pb-3.5 shrink-0">
      <h2 class="font-display font-bold text-base sm:text-lg text-slate-900 dark:text-white flex items-center gap-2">
        <i class="fa-solid fa-sliders text-emerald-600 dark:text-emerald-400"></i> Thiết lập hạn mức ngân sách
      </h2>
      <p class="text-xs text-slate-400 mt-1">
        Kiểm soát chi tiêu tự động với hệ thống cảnh báo màu khi chạm hoặc vượt hạn mức.
      </p>
    </div>

    <!-- Overall monthly budget -->
    <div class="space-y-1.5 pt-4 shrink-0">
      <label class="block text-xs font-semibold text-slate-500 dark:text-slate-400">
        Tổng ngân sách chi tiêu hàng tháng (VNĐ)
      </label>
      <div class="relative">
        <input
          v-model="overall"
          type="number"
          step="500000"
          min="0"
          placeholder="VD: 15000000"
          class="w-full px-4 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white font-bold text-base focus:outline-none focus:border-emerald-500"
        />
        <span class="absolute right-4 top-1/2 -translate-y-1/2 text-xs font-semibold text-slate-400">VNĐ</span>
      </div>
    </div>

    <!-- Per-category budget limits (Scrollable inside div) -->
    <div class="flex-1 flex flex-col min-h-0 pt-4">
      <label class="block text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2.5 shrink-0">
        Hạn mức theo từng danh mục (Để trống = không giới hạn)
      </label>

      <div class="flex-1 overflow-y-auto pr-1.5 space-y-2.5 min-h-0 max-h-[42vh] sm:max-h-[48vh]">
        <div
          v-for="c in EXPENSE_CATEGORIES"
          :key="c.value"
          class="flex items-center justify-between gap-3 p-3 rounded-xl bg-slate-50/80 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-800"
        >
          <div class="flex items-center gap-2.5 min-w-0">
            <span class="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-xs shrink-0">
              <i :class="['fa-solid', c.icon]"></i>
            </span>
            <span class="text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200 truncate">
              {{ c.value }}
            </span>
          </div>

          <div class="relative w-36 sm:w-44 shrink-0">
            <input
              v-model="categoryTexts[c.value]"
              type="number"
              step="100000"
              min="0"
              placeholder="Không giới hạn"
              class="w-full px-3 py-1.5 text-right text-xs rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 focus:outline-none focus:border-emerald-500 font-semibold"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Submit button -->
    <div class="pt-4 mt-3 border-t border-slate-100 dark:border-slate-800 shrink-0">
      <button
        @click="saveBudgets"
        class="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-700 hover:to-green-600 text-white font-semibold text-sm shadow-md shadow-emerald-500/25 transition cursor-pointer"
      >
        <i class="fa-solid fa-check mr-1.5"></i> Lưu thiết lập ngân sách
      </button>
    </div>
  </div>
</template>
