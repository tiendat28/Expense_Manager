<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDebtsStore } from '../stores/debts'
import { formatVND, categoryMeta } from '../utils/formatters'
import { percent, remaining as remainingOf } from '../utils/progress'
import DebtFormModal from '../components/DebtFormModal.vue'
import DebtPaymentModal from '../components/DebtPaymentModal.vue'
import PageShell from '../components/PageShell.vue'
import FabButton from '../components/FabButton.vue'
import EmptyState from '../components/EmptyState.vue'

const router = useRouter()
const store = useDebtsStore()

const showAdd = ref(false)
const payingDebt = ref(null)
const typeFilter = ref('ALL') // ALL | lent | owe
const statusFilter = ref('unpaid') // unpaid | paid | ALL

const remaining = (d) => remainingOf(d.total_amount, d.paid_amount)
const progress = (d) => percent(d.paid_amount, d.total_amount)
const isSettled = (d) => remaining(d) <= 0

// Summary stats
const totalLentRemaining = computed(() => store.totalLent)
const totalOweRemaining = computed(() => store.totalOwe)
const netDebt = computed(() => totalLentRemaining.value - totalOweRemaining.value)

function getStatusBadge(d) {
  if (isSettled(d)) {
    return { text: 'Đã tất toán', class: 'bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400' }
  }
  if (d.due_date) {
    const today = new Date().toISOString().slice(0, 10)
    if (d.due_date < today) {
      return { text: 'Quá hạn', class: 'bg-rose-100 dark:bg-rose-950 text-rose-600 dark:text-rose-400' }
    }
    // Sắp đến hạn trong 7 ngày
    const dueTime = new Date(d.due_date).getTime()
    const nowTime = new Date().getTime()
    if (dueTime - nowTime <= 7 * 24 * 3600 * 1000) {
      return { text: 'Sắp đến hạn', class: 'bg-amber-100 dark:bg-amber-950 text-amber-600 dark:text-amber-400' }
    }
  }
  return { text: 'Đang trong hạn', class: 'bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400' }
}

const filteredDebts = computed(() =>
  store.items.filter((d) => {
    if (typeFilter.value !== 'ALL' && d.type !== typeFilter.value) return false
    if (statusFilter.value === 'unpaid' && isSettled(d)) return false
    if (statusFilter.value === 'paid' && !isSettled(d)) return false
    return true
  })
)

onMounted(() => store.fetchAll())
</script>

<template>
  <PageShell>
    <!-- 3 Debt Summary Cards Matching FinFlow HTML -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-5">
      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Tổng phải thu (Cho vay)</span>
          <span class="w-9 h-9 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <i class="fa-solid fa-hand-holding-dollar"></i>
          </span>
        </div>
        <h3 class="font-display font-extrabold text-2xl text-emerald-600 dark:text-emerald-400">
          {{ formatVND(totalLentRemaining) }}
        </h3>
        <p class="text-xs text-slate-400 mt-1">Số tiền người khác còn nợ bạn</p>
      </div>

      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Tổng phải trả (Tôi nợ)</span>
          <span class="w-9 h-9 rounded-xl bg-rose-50 dark:bg-rose-950/80 text-rose-600 dark:text-rose-400 flex items-center justify-center">
            <i class="fa-solid fa-money-bill-transfer"></i>
          </span>
        </div>
        <h3 class="font-display font-extrabold text-2xl text-rose-600 dark:text-rose-400">
          {{ formatVND(totalOweRemaining) }}
        </h3>
        <p class="text-xs text-slate-400 mt-1">Dư nợ bạn cần thanh toán</p>
      </div>

      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Vị thế công nợ ròng</span>
          <span class="w-9 h-9 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <i class="fa-solid fa-scale-unbalanced"></i>
          </span>
        </div>
        <h3 class="font-display font-extrabold text-2xl" :class="netDebt >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'">
          {{ netDebt >= 0 ? '+' : '' }}{{ formatVND(netDebt) }}
        </h3>
        <p class="text-xs text-slate-400 mt-1">Chênh lệch (Phải thu - Phải trả)</p>
      </div>
    </div>

    <!-- Debt Sub-tabs & Action Bar -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white dark:bg-slate-900 p-4 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
      <div class="flex flex-wrap items-center gap-2">
        <!-- Type Filter -->
        <div class="inline-flex p-1 rounded-xl bg-slate-100 dark:bg-slate-800">
          <button
            type="button"
            class="px-3 sm:px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
            :class="typeFilter === 'ALL' ? 'bg-white dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 shadow-2xs' : 'text-slate-600 dark:text-slate-400'"
            @click="typeFilter = 'ALL'"
          >
            Tất cả
          </button>
          <button
            type="button"
            class="px-3 sm:px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
            :class="typeFilter === 'lent' ? 'bg-white dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 shadow-2xs' : 'text-slate-600 dark:text-slate-400'"
            @click="typeFilter = 'lent'"
          >
            Cho vay (Phải thu)
          </button>
          <button
            type="button"
            class="px-3 sm:px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
            :class="typeFilter === 'owe' ? 'bg-white dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 shadow-2xs' : 'text-slate-600 dark:text-slate-400'"
            @click="typeFilter = 'owe'"
          >
            Tôi nợ (Phải trả)
          </button>
        </div>

        <!-- Status Filter: Chưa thanh toán / Đã thanh toán -->
        <div class="inline-flex p-1 rounded-xl bg-slate-100 dark:bg-slate-800">
          <button
            type="button"
            class="px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
            :class="statusFilter === 'unpaid' ? 'bg-white dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 shadow-2xs' : 'text-slate-600 dark:text-slate-400'"
            @click="statusFilter = 'unpaid'"
          >
            Chưa thanh toán
          </button>
          <button
            type="button"
            class="px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
            :class="statusFilter === 'paid' ? 'bg-white dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 shadow-2xs' : 'text-slate-600 dark:text-slate-400'"
            @click="statusFilter = 'paid'"
          >
            Đã thanh toán
          </button>
          <button
            type="button"
            class="px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
            :class="statusFilter === 'ALL' ? 'bg-white dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 shadow-2xs' : 'text-slate-600 dark:text-slate-400'"
            @click="statusFilter = 'ALL'"
          >
            Xem hết
          </button>
        </div>
      </div>

      <button
        @click="showAdd = true"
        class="hidden md:flex px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold items-center gap-2 self-start md:self-auto transition cursor-pointer shadow-sm shadow-emerald-600/20"
      >
        <i class="fa-solid fa-plus"></i> Ghi sổ khoản nợ mới
      </button>
    </div>

    <!-- Empty State -->
    <EmptyState
      v-if="!filteredDebts.length"
      boxed
      :text="statusFilter === 'unpaid' ? 'Không có khoản nợ nào chưa thanh toán.' : 'Không có khoản nợ nào khớp với bộ lọc.'"
    />

    <!-- Debt Cards Grid Matching FinFlow HTML -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-5">
      <div
        v-for="d in filteredDebts"
        :key="d.id"
        class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow flex flex-col justify-between space-y-4 hover:border-emerald-400 dark:hover:border-emerald-700 transition cursor-pointer"
        @click="router.push(`/debts/${d.id}`)"
      >
        <div>
          <!-- Header: Icon, Name, Type Badge, Status -->
          <div class="flex items-start justify-between gap-2">
            <div class="flex items-center gap-3 min-w-0">
              <div
                class="w-11 h-11 rounded-xl flex items-center justify-center font-bold text-sm shrink-0"
                :class="d.type === 'lent' ? 'bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400' : 'bg-rose-50 dark:bg-rose-950/80 text-rose-600 dark:text-rose-400'"
              >
                <i :class="d.type === 'lent' ? 'fa-solid fa-hand-holding-dollar text-base' : 'fa-solid fa-file-signature text-base'"></i>
              </div>
              <div class="min-w-0">
                <div class="flex items-center gap-2 flex-wrap">
                  <h4 class="font-display font-bold text-base text-slate-900 dark:text-white truncate">{{ d.person_name }}</h4>
                  <span
                    class="text-[10px] font-bold uppercase px-2 py-0.5 rounded-md"
                    :class="d.type === 'lent' ? 'bg-emerald-50 dark:bg-emerald-950 text-emerald-600' : 'bg-rose-50 dark:bg-rose-950 text-rose-600'"
                  >
                    {{ d.type === 'lent' ? 'Cho vay' : 'Tôi nợ' }}
                  </span>
                </div>
                <p class="text-xs text-slate-400 mt-0.5 truncate">{{ d.category || 'Khoản nợ' }} • {{ d.note || 'Không có ghi chú' }}</p>
              </div>
            </div>

            <span class="text-[11px] font-semibold px-2.5 py-1 rounded-full shrink-0" :class="getStatusBadge(d).class">
              {{ getStatusBadge(d).text }}
            </span>
          </div>

          <!-- 3 Mini Summary Boxes -->
          <div class="grid grid-cols-3 gap-2 mt-4 p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 text-xs">
            <div>
              <span class="text-slate-400 block text-[11px]">Tổng nợ</span>
              <strong class="text-slate-700 dark:text-slate-200 font-bold">{{ formatVND(d.total_amount) }}</strong>
            </div>
            <div>
              <span class="text-slate-400 block text-[11px]">Đã {{ d.type === 'lent' ? 'thu' : 'trả' }} ({{ Math.round(progress(d)) }}%)</span>
              <strong class="text-emerald-600 dark:text-emerald-400 font-bold">{{ formatVND(d.paid_amount) }}</strong>
            </div>
            <div>
              <span class="text-slate-400 block text-[11px]">Còn lại</span>
              <strong class="text-rose-600 dark:text-rose-400 font-bold">{{ formatVND(remaining(d)) }}</strong>
            </div>
          </div>

          <!-- Progress Bar -->
          <div class="mt-3">
            <div class="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
              <div
                class="h-full rounded-full progress-bar-fill"
                :class="d.type === 'lent' ? 'bg-emerald-500' : 'bg-rose-500'"
                :style="{ width: progress(d) + '%' }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Footer: Due date + CTA -->
        <div class="flex items-center justify-between pt-3 border-t border-slate-100 dark:border-slate-800 text-xs">
          <span class="text-slate-400">
            <i class="fa-regular fa-calendar-check mr-1"></i>
            {{ d.due_date ? `Hẹn: ${d.due_date}` : 'Không hẹn ngày' }}
          </span>

          <span v-if="isSettled(d)" class="text-emerald-600 dark:text-emerald-400 font-semibold">
            <i class="fa-solid fa-check-double mr-1"></i> Hoàn tất 100%
          </span>
          <button
            v-else
            @click.stop="payingDebt = d"
            class="px-3.5 py-1.5 rounded-xl font-semibold text-white transition cursor-pointer"
            :class="d.type === 'lent' ? 'bg-emerald-600 hover:bg-emerald-700' : 'bg-rose-600 hover:bg-rose-700'"
          >
            <i class="fa-solid fa-coins mr-1"></i> {{ d.type === 'lent' ? 'Thu nợ' : 'Trả nợ' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <FabButton @click="showAdd = true" />
    <DebtFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false; store.fetchAll()" />
    <DebtPaymentModal v-if="payingDebt" :debt="payingDebt" @close="payingDebt = null" @saved="payingDebt = null; store.fetchAll()" />
  </PageShell>
</template>
