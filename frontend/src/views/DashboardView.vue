<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTransactionsStore } from '../stores/transactions'
import { useBudgetStore } from '../stores/budget'
import { useDebtsStore } from '../stores/debts'
import { formatVND, categoryMeta } from '../utils/formatters'
import MonthlyTrendChart from '../components/MonthlyTrendChart.vue'
import CategoryDonutChart from '../components/CategoryDonutChart.vue'
import CategoryRow from '../components/CategoryRow.vue'
import TransactionFormModal from '../components/TransactionFormModal.vue'
import PageShell from '../components/PageShell.vue'
import FabButton from '../components/FabButton.vue'

const router = useRouter()
const tx = useTransactionsStore()
const budget = useBudgetStore()
const debtsStore = useDebtsStore()

const showAdd = ref(false)

const balance = computed(() => tx.monthlyStats.income_total - tx.monthlyStats.expense_total)
const remaining = computed(() => budget.monthlyBudget - tx.monthlyStats.expense_total)
const budgetUsedPercent = computed(() =>
  budget.monthlyBudget > 0 ? ((tx.monthlyStats.expense_total / budget.monthlyBudget) * 100).toFixed(1) : 0
)

const recentTransactions = computed(() => (tx.items || []).slice(0, 5))
const activeDebts = computed(() => debtsStore.unsettledList.slice(0, 4))

function onSelectMonth(item) {
  tx.selectedYear = item.year
  tx.selectedMonth = item.month
  tx.refreshAll()
}

onMounted(async () => {
  await Promise.all([
    budget.fetch().catch(() => {}),
    tx.refreshAll().catch(() => {}),
    debtsStore.fetchAll().catch(() => {}),
  ])
})
</script>

<template>
  <PageShell>
    <!-- 4 KPI Cards Matching FinFlow HTML -->
    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 sm:gap-5">
      <!-- KPI 1: Số dư ròng tháng -->
      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow relative overflow-hidden transition-colors">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">Số dư ròng tháng</span>
          <div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <i class="fa-solid fa-landmark text-base"></i>
          </div>
        </div>
        <h2 class="font-display font-extrabold text-2xl sm:text-3xl text-slate-900 dark:text-white tracking-tight">
          {{ formatVND(balance) }}
        </h2>
        <div class="flex items-center justify-between mt-3 pt-3 border-t border-slate-100 dark:border-slate-800/80 text-xs">
          <span class="inline-flex items-center gap-1 font-semibold" :class="balance >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'">
            <i :class="balance >= 0 ? 'fa-solid fa-arrow-trend-up' : 'fa-solid fa-arrow-trend-down'"></i>
            {{ balance >= 0 ? 'Thặng dư' : 'Thâm hụt' }}
          </span>
          <span class="text-slate-400">Tháng {{ tx.selectedMonth }}/{{ tx.selectedYear }}</span>
        </div>
      </div>

      <!-- KPI 2: Tổng thu tháng -->
      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">Tổng thu tháng {{ tx.selectedMonth }}</span>
          <div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <i class="fa-solid fa-circle-arrow-down text-base"></i>
          </div>
        </div>
        <h2 class="font-display font-extrabold text-2xl sm:text-3xl text-emerald-600 dark:text-emerald-400 tracking-tight">
          {{ formatVND(tx.monthlyStats.income_total) }}
        </h2>
        <div class="flex items-center justify-between mt-3 pt-3 border-t border-slate-100 dark:border-slate-800/80 text-xs">
          <span class="inline-flex items-center gap-1 font-semibold text-emerald-600 dark:text-emerald-400">
            <i class="fa-solid fa-arrow-trend-up"></i> Khoản thu
          </span>
          <span class="text-slate-400">{{ (tx.items || []).filter(t => t.type === 'income').length }} giao dịch</span>
        </div>
      </div>

      <!-- KPI 3: Tổng chi tháng -->
      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">Tổng chi tháng {{ tx.selectedMonth }}</span>
          <div class="w-10 h-10 rounded-xl bg-rose-50 dark:bg-rose-950/80 text-rose-600 dark:text-rose-400 flex items-center justify-center">
            <i class="fa-solid fa-circle-arrow-up text-base"></i>
          </div>
        </div>
        <h2 class="font-display font-extrabold text-2xl sm:text-3xl text-rose-600 dark:text-rose-400 tracking-tight">
          {{ formatVND(tx.monthlyStats.expense_total) }}
        </h2>
        <div class="flex items-center justify-between mt-3 pt-3 border-t border-slate-100 dark:border-slate-800/80 text-xs">
          <span class="inline-flex items-center gap-1 font-semibold text-rose-600 dark:text-rose-400">
            <i class="fa-solid fa-circle-dot"></i> Khoản chi
          </span>
          <span class="text-slate-400">{{ (tx.items || []).filter(t => t.type === 'expense').length }} giao dịch</span>
        </div>
      </div>

      <!-- KPI 4: Ngân sách còn lại -->
      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">Ngân sách còn lại</span>
          <div class="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950/80 text-amber-600 dark:text-amber-400 flex items-center justify-center">
            <i class="fa-solid fa-scale-balanced text-base"></i>
          </div>
        </div>
        <h2 class="font-display font-extrabold text-2xl sm:text-3xl tracking-tight" :class="remaining >= 0 ? 'text-slate-900 dark:text-white' : 'text-rose-600 dark:text-rose-400'">
          {{ formatVND(Math.max(0, remaining)) }}
        </h2>
        <div class="flex items-center justify-between mt-3 pt-3 border-t border-slate-100 dark:border-slate-800/80 text-xs">
          <span class="inline-flex items-center gap-1 font-semibold text-emerald-600 dark:text-emerald-400">
            Đã dùng {{ budgetUsedPercent }}%
          </span>
          <span class="text-slate-400">Hạn mức: {{ formatVND(budget.monthlyBudget) }}</span>
        </div>
      </div>
    </div>

    <!-- Charts Row: Trend 6 Months + Category Breakdown Donut -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Bar Chart: Cashflow Trend 6 Months -->
      <div class="lg:col-span-2 bg-white dark:bg-slate-900 p-5 sm:p-6 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow flex flex-col justify-between transition-colors">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
          <div>
            <h3 class="font-display font-bold text-base text-slate-900 dark:text-white">Xu hướng chi tiêu (6 tháng gần nhất)</h3>
            <p class="text-xs text-slate-400">Chạm vào từng cột để đồng bộ xem chi tiết tháng đó</p>
          </div>
          <div class="flex items-center gap-3 text-xs">
            <span class="flex items-center gap-1.5 text-slate-600 dark:text-slate-300 font-medium">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Tháng được chọn
            </span>
            <span class="flex items-center gap-1.5 text-slate-400">
              <span class="w-2.5 h-2.5 rounded-full bg-slate-400 dark:bg-slate-600"></span> Tháng khác
            </span>
          </div>
        </div>
        <div class="w-full">
          <MonthlyTrendChart
            :trend="tx.trend"
            :selected-year="tx.selectedYear"
            :selected-month="tx.selectedMonth"
            @select="onSelectMonth"
          />
        </div>
      </div>

      <!-- Doughnut Chart: Category Breakdown -->
      <div class="bg-white dark:bg-slate-900 p-5 sm:p-6 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow flex flex-col justify-between transition-colors">
        <div>
          <h3 class="font-display font-bold text-base text-slate-900 dark:text-white">Cơ cấu chi tiêu tháng {{ tx.selectedMonth }}</h3>
          <p class="text-xs text-slate-400 mb-4">Phân bổ tỷ trọng theo nhóm danh mục chính</p>
        </div>
        <CategoryDonutChart :category-totals="tx.monthlyStats.category_totals" />
      </div>
    </div>

    <!-- Bottom 3 Widgets: Theo danh mục, Giao dịch gần đây, Sổ nợ -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Widget 1: Theo danh mục -->
      <div class="card-surface p-5 sm:p-6 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-display font-bold text-base text-slate-800 dark:text-white">Theo danh mục</h3>
            <button
              @click="router.push({ name: 'budget' })"
              class="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline cursor-pointer shrink-0"
            >
              Điều chỉnh →
            </button>
          </div>
          <CategoryRow />
        </div>
      </div>

      <!-- Widget 2: 5 Recent Transactions -->
      <div class="bg-white dark:bg-slate-900 p-5 sm:p-6 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow flex flex-col justify-between transition-colors">
        <div>
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-display font-bold text-base text-slate-900 dark:text-white">Giao dịch gần đây</h3>
            <button
              @click="router.push({ name: 'transactions' })"
              class="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline cursor-pointer"
            >
              Xem tất cả →
            </button>
          </div>
          <div v-if="recentTransactions.length" class="space-y-3">
            <div
              v-for="t in recentTransactions"
              :key="t.id"
              class="flex items-center justify-between p-2.5 rounded-xl hover:bg-slate-50 dark:hover:bg-slate-800/60 transition"
            >
              <div class="flex items-center gap-3 min-w-0">
                <div class="w-9 h-9 rounded-xl bg-emerald-50 dark:bg-emerald-950/70 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
                  <i :class="['fa-solid', categoryMeta(t.category, t.type).icon, 'text-xs']"></i>
                </div>
                <div class="min-w-0">
                  <p class="text-xs font-semibold text-slate-800 dark:text-slate-100 truncate">{{ t.note || t.category }}</p>
                  <p class="text-[11px] text-slate-400">{{ t.category }} • {{ t.date }}</p>
                </div>
              </div>
              <span
                class="text-xs font-bold shrink-0 ml-2"
                :class="t.type === 'income' ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'"
              >
                {{ t.type === 'income' ? '+' : '-' }}{{ formatVND(t.amount) }}
              </span>
            </div>
          </div>
          <p v-else class="text-xs text-slate-400 py-6 text-center">Chưa có giao dịch nào trong tháng này.</p>
        </div>
      </div>

      <!-- Widget 3: Active Debts -->
      <div class="bg-white dark:bg-slate-900 p-5 sm:p-6 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow flex flex-col justify-between transition-colors">
        <div>
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-display font-bold text-base text-slate-900 dark:text-white">Sổ nợ cần thu / trả</h3>
            <button
              @click="router.push({ name: 'debts' })"
              class="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline cursor-pointer"
            >
              Chi tiết →
            </button>
          </div>
          <div v-if="activeDebts.length" class="space-y-3">
            <div
              v-for="d in activeDebts"
              :key="d.id"
              class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50/70 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800"
            >
              <div class="min-w-0">
                <div class="flex items-center gap-1.5">
                  <span
                    class="text-[10px] font-bold uppercase px-1.5 py-0.5 rounded"
                    :class="d.type === 'lent' ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400' : 'bg-rose-100 dark:bg-rose-950 text-rose-600 dark:text-rose-400'"
                  >
                    {{ d.type === 'lent' ? 'Thu nợ' : 'Trả nợ' }}
                  </span>
                  <p class="text-xs font-semibold text-slate-800 dark:text-slate-100 truncate">{{ d.person_name }}</p>
                </div>
                <p class="text-[11px] text-slate-400 mt-0.5">
                  <span v-if="d.due_date">Hạn: {{ d.due_date }} • </span>
                  Còn: <strong class="text-slate-700 dark:text-slate-200">{{ formatVND(d.total_amount - d.paid_amount) }}</strong>
                </p>
              </div>
              <router-link
                :to="`/debts/${d.id}`"
                class="text-[11px] font-semibold px-2.5 py-1.5 rounded-lg bg-slate-200/80 dark:bg-slate-700 hover:bg-emerald-600 hover:text-white text-slate-700 dark:text-slate-200 transition shrink-0 cursor-pointer"
              >
                Cập nhật
              </router-link>
            </div>
          </div>
          <p v-else class="text-xs text-slate-400 py-6 text-center">Không có khoản nợ nào đang chờ tất toán.</p>
        </div>
      </div>
    </div>

    <FabButton @click="showAdd = true" />
    <TransactionFormModal v-if="showAdd" @close="showAdd = false" @saved="tx.refreshAll(); showAdd = false" />
  </PageShell>
</template>
