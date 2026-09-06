<script setup>
import { onMounted, computed, ref } from 'vue'
import { useTransactionsStore } from '../stores/transactions'
import { useBudgetStore } from '../stores/budget'
import { formatVND, categoryMeta } from '../utils/formatters'
import CategoryRow from '../components/CategoryRow.vue'
import MonthlyTrendChart from '../components/MonthlyTrendChart.vue'
import CategoryDonutChart from '../components/CategoryDonutChart.vue'
import TransactionFormModal from '../components/TransactionFormModal.vue'
import PageShell from '../components/PageShell.vue'

const tx = useTransactionsStore()
const budget = useBudgetStore()
const showAdd = ref(false)

const monthNames = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12']

const balance = computed(() => tx.monthlyStats.income_total - tx.monthlyStats.expense_total)
const progress = computed(() => {
  if (!budget.monthlyBudget) return 0
  return Math.min(tx.monthlyStats.expense_total / budget.monthlyBudget, 1) * 100
})
const remaining = computed(() => budget.monthlyBudget - tx.monthlyStats.expense_total)

const yearOptions = computed(() => {
  const currentYear = new Date().getFullYear()
  const options = []
  for (let y = currentYear; y >= currentYear - 5; y--) options.push(y)
  return options
})

function onChangeMonth() {
  tx.refreshAll()
}

function onSelectMonth(item) {
  tx.selectedYear = item.year
  tx.selectedMonth = item.month
  tx.refreshAll()
}

onMounted(async () => {
  await budget.fetch()
  await tx.refreshAll()
})
</script>

<template>
  <PageShell>
    <template #sticky>
      <div class="flex items-center justify-between flex-wrap gap-2">
        <h1 class="text-xl sm:text-2xl font-bold text-green-800">Tổng quan tài chính</h1>
        <div class="flex items-center gap-2 bg-white rounded-full shadow-sm px-1 py-1">
          <select
            v-model.number="tx.selectedMonth"
            @change="onChangeMonth"
            class="text-sm font-semibold text-gray-700 bg-transparent px-2 py-1 border-0 outline-none cursor-pointer"
          >
            <option v-for="(name, i) in monthNames" :key="i" :value="i + 1">{{ name }}</option>
          </select>
          <select
            v-model.number="tx.selectedYear"
            @change="onChangeMonth"
            class="text-sm font-semibold text-gray-700 bg-transparent px-2 py-1 border-0 outline-none cursor-pointer"
          >
            <option v-for="y in yearOptions" :key="y" :value="y">{{ y }}</option>
          </select>
        </div>
      </div>
    </template>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="bg-white rounded-2xl p-5 shadow-sm flex items-center gap-4">
        <div class="w-12 h-12 rounded-full bg-green-100 text-green-600 flex items-center justify-center text-xl shrink-0">💼</div>
        <div>
          <div class="text-xs text-gray-900 mb-0.5">Số dư tháng này</div>
          <div class="text-xl font-bold" :class="balance >= 0 ? 'text-gray-800' : 'text-red-600'">{{ formatVND(balance) }}</div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-5 shadow-sm flex items-center gap-4">
        <div class="w-12 h-12 rounded-full bg-green-100 text-green-600 flex items-center justify-center text-xl shrink-0">↓</div>
        <div>
          <div class="text-xs text-gray-900 mb-0.5">Tổng thu nhập</div>
          <div class="text-xl font-bold text-green-600">{{ formatVND(tx.monthlyStats.income_total) }}</div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-5 shadow-sm flex items-center gap-4">
        <div class="w-12 h-12 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-xl shrink-0">↑</div>
        <div>
          <div class="text-xs text-gray-900 mb-0.5">Tổng chi tiêu</div>
          <div class="text-xl font-bold text-red-600">{{ formatVND(tx.monthlyStats.expense_total) }}</div>
        </div>
      </div>
    </div>

    <div v-if="budget.monthlyBudget" class="bg-white rounded-2xl p-5 shadow-sm">
      <div class="h-2 bg-gray-100 rounded-full overflow-hidden mb-2">
        <div class="h-full rounded-full" :class="progress >= 100 ? 'bg-red-500' : 'bg-green-500'" :style="{ width: progress + '%' }"></div>
      </div>
      <div class="flex justify-between text-xs">
        <span class="text-gray-900">Ngân sách: {{ formatVND(budget.monthlyBudget) }}</span>
        <span :class="remaining >= 0 ? 'text-green-600' : 'text-red-600'">
          {{ remaining >= 0 ? 'Còn lại: ' + formatVND(remaining) : 'Vượt: ' + formatVND(-remaining) }}
        </span>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div class="bg-white rounded-2xl p-5 shadow-sm">
        <h2 class="font-semibold text-gray-700 mb-3 text-center">Phân bổ chi tiêu</h2>
        <CategoryDonutChart :category-totals="tx.monthlyStats.category_totals" />
      </div>
      <div class="bg-white rounded-2xl p-5 shadow-sm">
        <h2 class="font-semibold text-gray-700 mb-1">Xu hướng 6 tháng gần đây</h2>
        <p class="text-xs text-gray-900 mb-2">Chạm vào cột để xem tháng đó</p>
        <MonthlyTrendChart :trend="tx.trend" :selected-year="tx.selectedYear" :selected-month="tx.selectedMonth" @select="onSelectMonth" />
      </div>
    </div>

    <div v-if="tx.monthlyStats.category_totals.length" class="bg-white rounded-2xl p-5 shadow-sm">
      <h2 class="font-semibold text-gray-700 mb-3">Theo danh mục</h2>
      <CategoryRow
        v-for="item in tx.monthlyStats.category_totals"
        :key="item.category"
        :category="item.category"
        :icon="categoryMeta(item.category, 'expense').icon"
        :color="categoryMeta(item.category, 'expense').color"
        :total="item.total"
        :limit="budget.categoryBudgets[item.category]"
      />
    </div>
    <p v-else class="text-gray-900 text-sm text-center py-6">Không có chi tiêu nào trong tháng này</p>

    <button @click="showAdd = true" class="glass-fab fixed bottom-20 sm:bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-green-500 to-green-700 text-white text-2xl hover:brightness-110">+</button>
    <TransactionFormModal v-if="showAdd" @close="showAdd = false" @saved="tx.refreshAll(); showAdd = false" />
  </PageShell>
</template>
