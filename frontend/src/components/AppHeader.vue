<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSidebar } from '../composables/useSidebar'
import { useTheme } from '../composables/useTheme'
import { useFabStore } from '../stores/fab'
import { useTransactionsStore } from '../stores/transactions'
import { useBillsStore } from '../stores/bills'
import { useDebtsStore } from '../stores/debts'
import { formatVND } from '../utils/formatters'
import { formatHeaderDate } from '../utils/date'

const route = useRoute()
const router = useRouter()
const sidebar = useSidebar()
const { isDark, toggleTheme } = useTheme()
const fab = useFabStore()
const txStore = useTransactionsStore()
const billsStore = useBillsStore()
const debtsStore = useDebtsStore()

const showNotif = ref(false)

const titles = {
  dashboard: { title: 'Tổng quan tài chính', sub: 'Bức tranh toàn cảnh tài sản, dòng tiền và nghĩa vụ thanh toán' },
  transactions: { title: 'Sổ giao dịch chi tiết', sub: 'Quản lý mọi dòng tiền thu chi theo danh mục và tài khoản' },
  debts: { title: 'Sổ nợ — Cho vay & Đi vay', sub: 'Theo dõi tiến độ thu hồi nợ, lịch nhắc hẹn và tất toán công nợ' },
  'debt-detail': { title: 'Chi tiết khoản nợ', sub: 'Lịch sử thanh toán và tiến độ hoàn thành' },
  savings: { title: 'Tiết kiệm & Mục tiêu tích lũy', sub: 'Quản lý quỹ mục tiêu cá nhân và danh mục tích lũy' },
  'savings-detail': { title: 'Chi tiết mục tiêu tích lũy', sub: 'Lịch sử nạp tích lũy và tiến độ' },
  giftmoney: { title: 'Sổ Hiếu Hỉ thông minh (Tiền mừng)', sub: 'Tra cứu nhanh lịch sử có đi có lại đám cưới, tân gia, đầy tháng' },
  bills: { title: 'Hóa đơn định kỳ', sub: 'Kiểm soát hạn mức và thanh toán hóa đơn 1 chạm' },
  budget: { title: 'Ngân sách chi tiêu', sub: 'Thiết lập hạn mức ngân sách tháng và từng danh mục' },
  settings: { title: 'Cài đặt & Sao lưu', sub: 'Quản lý dữ liệu dự phòng và xuất báo cáo' },
}

const currentTitle = computed(() => titles[route.name] || { title: 'FiveDream', sub: 'Quản trị tài chính cá nhân' })
const currentDateFormatted = computed(() => formatHeaderDate())

// Thông báo nhắc nhở
const unpaidBills = computed(() => billsStore.unpaidList)
const activeDebts = computed(() => debtsStore.unsettledList)
const notifCount = computed(() => unpaidBills.value.length + activeDebts.value.length)

function onPrimaryCTA() {
  if (!fab.trigger()) {
    router.push({ name: 'transactions', query: { add: '1' } })
  }
}

onMounted(() => {
  billsStore.fetchAll().catch(() => {})
  debtsStore.fetchAll().catch(() => {})
})
</script>

<template>
  <header class="h-16 sm:h-20 bg-white/90 dark:bg-slate-900/90 glass-card border-b border-slate-200/90 dark:border-slate-800 px-3 sm:px-6 lg:px-8 flex items-center justify-between gap-2 sm:gap-4 z-30 shrink-0 sticky top-0 transition-colors">
    <!-- Left: Tablet toggle + Page Title (Mobile hides hamburger because BottomNav has menu) -->
    <div class="flex items-center gap-2.5 sm:gap-3 min-w-0">
      <button
        @click="sidebar.toggle"
        class="hidden md:inline-flex lg:hidden p-2 sm:p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition cursor-pointer shrink-0"
        aria-label="Mở menu"
      >
        <i class="fa-solid fa-bars"></i>
      </button>
      <div class="min-w-0">
        <h1 class="font-display font-bold text-sm sm:text-xl text-slate-900 dark:text-white truncate">
          {{ currentTitle.title }}
        </h1>
        <p class="text-xs text-slate-500 dark:text-slate-400 hidden md:block truncate">
          {{ currentTitle.sub }} • {{ currentDateFormatted }}
        </p>
      </div>
    </div>

    <!-- Right Controls -->
    <div class="flex items-center gap-1.5 sm:gap-2.5 shrink-0">
      <!-- Period Selector (Tháng/Năm) - Visible on mobile, iPad & desktop -->
      <div class="flex items-center bg-slate-100 dark:bg-slate-800 rounded-xl px-2 sm:px-2.5 py-1.5 border border-slate-200/80 dark:border-slate-700/60 text-[11px] sm:text-xs">
        <i class="fa-regular fa-calendar text-emerald-600 dark:text-emerald-400 mr-1.5 hidden sm:inline-block"></i>
        <select
          v-model.number="txStore.selectedMonth"
          @change="txStore.refreshAll()"
          class="bg-transparent font-semibold text-slate-700 dark:text-slate-200 focus:outline-none cursor-pointer pr-0.5 sm:pr-1"
        >
          <option v-for="m in 12" :key="m" :value="m" class="bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100">
            Tháng {{ m }}
          </option>
        </select>
        <select
          v-model.number="txStore.selectedYear"
          @change="txStore.refreshAll()"
          class="bg-transparent font-semibold text-slate-700 dark:text-slate-200 focus:outline-none cursor-pointer"
        >
          <option v-for="y in [2024, 2025, 2026, 2027]" :key="y" :value="y" class="bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100">
            /{{ y }}
          </option>
        </select>
      </div>

      <!-- Theme Toggle Button -->
      <button
        @click="toggleTheme"
        class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-amber-400 hover:bg-slate-200 dark:hover:bg-slate-700 flex items-center justify-center transition cursor-pointer shrink-0"
        :title="isDark ? 'Chuyển sang chế độ Sáng' : 'Chuyển sang chế độ Tối'"
      >
        <i :class="isDark ? 'fa-solid fa-sun text-sm' : 'fa-solid fa-moon text-sm'"></i>
      </button>

      <!-- Notification Bell -->
      <div class="relative shrink-0">
        <button
          @click="showNotif = !showNotif"
          class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 flex items-center justify-center transition relative cursor-pointer"
          title="Thông báo nhắc hạn"
        >
          <i class="fa-regular fa-bell text-sm"></i>
          <span
            v-if="notifCount > 0"
            class="w-2.5 h-2.5 rounded-full bg-rose-500 absolute top-1.5 sm:top-2 right-2 sm:right-2.5 ring-2 ring-white dark:ring-slate-900"
          ></span>
        </button>

        <!-- Dropdown menu -->
        <div
          v-if="showNotif"
          class="fixed inset-0 z-40"
          @click="showNotif = false"
        ></div>

        <div
          v-if="showNotif"
          class="absolute right-0 mt-2 w-72 sm:w-80 bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 p-4 z-50 animate-fade-in"
        >
          <div class="flex items-center justify-between pb-2.5 mb-2.5 border-b border-slate-100 dark:border-slate-800">
            <span class="font-bold text-xs uppercase tracking-wider text-slate-500">Nhắc hạn quan trọng</span>
            <span class="text-[11px] text-emerald-600 dark:text-emerald-400 font-semibold">
              {{ notifCount }} mục
            </span>
          </div>

          <div class="space-y-2.5 text-xs max-h-72 overflow-y-auto">
            <div
              v-for="b in unpaidBills.slice(0, 3)"
              :key="'bill-' + b.id"
              @click="router.push({ name: 'bills' }); showNotif = false"
              class="p-2.5 rounded-xl bg-rose-50/70 dark:bg-rose-950/40 border border-rose-100 dark:border-rose-900/50 cursor-pointer hover:opacity-90 transition"
            >
              <p class="font-semibold text-rose-700 dark:text-rose-300">
                <i class="fa-solid fa-bolt mr-1"></i> {{ b.name }}
              </p>
              <p class="text-slate-500 dark:text-slate-400 mt-0.5">
                {{ formatVND(b.amount) }} • Ngày {{ b.due_day }} hàng tháng
              </p>
            </div>

            <div
              v-for="d in activeDebts.slice(0, 3)"
              :key="'debt-' + d.id"
              @click="router.push({ name: 'debts' }); showNotif = false"
              class="p-2.5 rounded-xl bg-amber-50/70 dark:bg-amber-950/40 border border-amber-100 dark:border-amber-900/50 cursor-pointer hover:opacity-90 transition"
            >
              <p class="font-semibold text-amber-700 dark:text-amber-300">
                <i class="fa-solid fa-clock mr-1"></i> {{ d.type === 'lent' ? 'Cho vay' : 'Tôi nợ' }}: {{ d.person_name }}
              </p>
              <p class="text-slate-500 dark:text-slate-400 mt-0.5">
                Còn {{ formatVND(d.total_amount - d.paid_amount) }}
                <span v-if="d.due_date">• Hạn: {{ d.due_date }}</span>
              </p>
            </div>

            <p v-if="!notifCount" class="text-center py-4 text-slate-400 text-xs">
              Không có khoản nợ hay hóa đơn nào cần nhắc hạn.
            </p>
          </div>
        </div>
      </div>

      <!-- Primary CTA: Add Transaction Button (Hidden on mobile since BottomNav has center +) -->
      <button
        @click="onPrimaryCTA"
        class="hidden md:flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-700 hover:to-green-600 text-white font-semibold text-xs sm:text-sm shadow-lg shadow-emerald-500/25 transition active:scale-95 cursor-pointer shrink-0"
      >
        <i class="fa-solid fa-plus text-xs"></i>
        <span>Thêm giao dịch</span>
      </button>
    </div>
  </header>
</template>
