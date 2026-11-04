<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBillsStore, isBillPaidThisMonth } from '../stores/bills'
import { useBudgetStore } from '../stores/budget'
import { useTransactionsStore } from '../stores/transactions'
import { formatVND, categoryMeta } from '../utils/formatters'
import BillFormModal from '../components/BillFormModal.vue'
import CategoryRow from '../components/CategoryRow.vue'
import PageShell from '../components/PageShell.vue'
import FabButton from '../components/FabButton.vue'

const router = useRouter()
const billsStore = useBillsStore()
const budgetStore = useBudgetStore()
const txStore = useTransactionsStore()

const showAddBill = ref(false)
const editingBill = ref(null)

onMounted(async () => {
  await Promise.all([
    billsStore.fetchAll().catch(() => {}),
    budgetStore.fetch().catch(() => {}),
    txStore.refreshAll().catch(() => {}),
  ])
})
</script>

<template>
  <PageShell>
    <!-- Grid 12 cols with internal scrollable containers -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <!-- Column 1 (7 cols): Ngân sách chi tiêu theo danh mục -->
      <div class="lg:col-span-7 card-surface p-5 sm:p-6 flex flex-col max-h-[75vh] lg:max-h-[calc(100vh-8.5rem)]">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-slate-100 dark:border-slate-800 shrink-0">
          <div>
            <h3 class="font-display font-bold text-base sm:text-lg text-slate-900 dark:text-white">
              Theo danh mục (Tháng {{ txStore.selectedMonth }})
            </h3>
            <p class="text-xs text-slate-400">
              Theo dõi chi tiêu thực tế so với hạn mức ngân sách từng danh mục
            </p>
          </div>
          <button
            @click="router.push({ name: 'budget' })"
            class="px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 text-xs font-semibold transition self-start sm:self-auto cursor-pointer shrink-0"
          >
            <i class="fa-solid fa-sliders mr-1"></i> Điều chỉnh hạn mức
          </button>
        </div>

        <CategoryRow
          scrollable
          empty-text="Chưa thiết lập ngân sách danh mục. Bấm 'Điều chỉnh hạn mức' để đặt ngân sách chi tiêu."
        />
      </div>

      <!-- Column 2 (5 cols): Hóa đơn định kỳ -->
      <div class="lg:col-span-5 card-surface p-5 sm:p-6 flex flex-col max-h-[75vh] lg:max-h-[calc(100vh-8.5rem)]">
        <div class="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800 shrink-0">
          <div>
            <h3 class="font-display font-bold text-base sm:text-lg text-slate-900 dark:text-white">Hóa đơn định kỳ</h3>
            <p class="text-xs text-slate-400">Thanh toán 1 chạm tự động ghi sổ</p>
          </div>
          <button
            @click="showAddBill = true"
            class="hidden md:inline-flex items-center px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold transition cursor-pointer shadow-sm shadow-emerald-600/20 shrink-0"
          >
            <i class="fa-solid fa-plus mr-1"></i> Thêm
          </button>
        </div>

        <div v-if="billsStore.items.length" class="flex-1 overflow-y-auto pr-1.5 mt-4 space-y-3.5 min-h-0">
          <div
            v-for="b in billsStore.items"
            :key="b.id"
            class="p-4 rounded-2xl bg-slate-50/80 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-800 flex items-center justify-between gap-3 hover:border-emerald-300 dark:hover:border-emerald-700 transition"
          >
            <div class="flex items-center gap-3 min-w-0 cursor-pointer" @click="editingBill = b">
              <div class="w-10 h-10 rounded-xl bg-rose-50 dark:bg-rose-950/80 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0">
                <i :class="['fa-solid', categoryMeta(b.category, 'expense').icon]"></i>
              </div>
              <div class="min-w-0">
                <h4 class="font-bold text-xs sm:text-sm text-slate-800 dark:text-slate-100 truncate">
                  {{ b.name }}
                  <span v-if="!b.is_active" class="text-xs text-slate-400 ml-1">🔕</span>
                </h4>
                <p class="text-[11px] text-slate-400 mt-0.5">
                  Ngày {{ b.due_day }} hàng tháng • <strong class="text-slate-700 dark:text-slate-200">{{ formatVND(b.amount) }}</strong>
                </p>
              </div>
            </div>

            <span
              v-if="isBillPaidThisMonth(b)"
              class="text-xs font-semibold px-3 py-1.5 rounded-xl bg-emerald-100 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 shrink-0"
            >
              <i class="fa-solid fa-check mr-1"></i> Đã trả
            </span>
            <button
              v-else
              @click="billsStore.markPaid(b.id)"
              class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold transition shrink-0 shadow-sm shadow-emerald-600/20 cursor-pointer"
            >
              Thanh toán ngay
            </button>
          </div>
        </div>

        <div v-else class="text-center py-10 text-xs text-slate-400">
          Chưa có hóa đơn định kỳ nào. Nhấn "+ Thêm" để tạo mới.
        </div>
      </div>
    </div>

    <FabButton @click="showAddBill = true" />
    <BillFormModal v-if="showAddBill" @close="showAddBill = false" @saved="showAddBill = false" />
    <BillFormModal v-if="editingBill" :existing="editingBill" @close="editingBill = null" @saved="editingBill = null" />
  </PageShell>
</template>
