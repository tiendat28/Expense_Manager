<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTransactionsStore } from '../stores/transactions'
import { usePagination } from '../composables/usePagination'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { formatVND, categoryMeta, EXPENSE_CATEGORIES, INCOME_CATEGORIES } from '../utils/formatters'
import TransactionFormModal from '../components/TransactionFormModal.vue'
import PageShell from '../components/PageShell.vue'
import FabButton from '../components/FabButton.vue'
import RowActions from '../components/RowActions.vue'
import PaginationBar from '../components/PaginationBar.vue'
import EmptyState from '../components/EmptyState.vue'

const tx = useTransactionsStore()
const confirmDelete = useConfirmDelete()
const route = useRoute()
const router = useRouter()

const filter = ref('all')
const category = ref('all')
const keyword = ref('')
const showAdd = ref(false)
const editing = ref(null)

const categoryGroups = computed(() => {
  const groups = []
  if (filter.value !== 'income') groups.push({ label: 'Chi tiêu', items: EXPENSE_CATEGORIES })
  if (filter.value !== 'expense') groups.push({ label: 'Thu nhập', items: INCOME_CATEGORIES })
  return groups
})

const filtered = computed(() =>
  tx.items.filter((t) => {
    if (filter.value !== 'all' && t.type !== filter.value) return false
    if (category.value !== 'all' && t.category !== category.value) return false
    if (keyword.value) {
      const kw = keyword.value.toLowerCase().trim()
      const noteMatch = (t.note || '').toLowerCase().includes(kw)
      const catMatch = (t.category || '').toLowerCase().includes(kw)
      if (!noteMatch && !catMatch) return false
    }
    return true
  })
)

const incomeTotal = computed(() =>
  filtered.value.filter((t) => t.type === 'income').reduce((sum, t) => sum + Number(t.amount), 0)
)
const expenseTotal = computed(() =>
  filtered.value.filter((t) => t.type === 'expense').reduce((sum, t) => sum + Number(t.amount), 0)
)
const netTotal = computed(() => incomeTotal.value - expenseTotal.value)

const { page, pageCount, paginated } = usePagination(filtered)

const amountClass = (t) => (t.type === 'income' ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400')
const signedAmount = (t) => `${t.type === 'income' ? '+' : '-'}${formatVND(t.amount)}`

watch(filter, () => {
  const stillValid = categoryGroups.value.some((g) => g.items.some((c) => c.value === category.value))
  if (!stillValid) category.value = 'all'
})
watch([filter, category, keyword], () => (page.value = 1))

function removeTransaction(t) {
  return confirmDelete(`Bạn có chắc chắn muốn xóa giao dịch "${t.note || t.category}"?`, () => tx.remove(t.id))
}

onMounted(() => {
  tx.refreshAll()
  if (route.query.add) {
    showAdd.value = true
    router.replace({ name: 'transactions' })
  }
})
</script>

<template>
  <PageShell>
    <!-- Filter & Search Toolbar matching FinFlow -->
    <div class="bg-white dark:bg-slate-900 p-4 sm:p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow space-y-4 transition-colors">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <!-- Type Segmented Filter -->
        <div class="inline-flex p-1 rounded-xl bg-slate-100 dark:bg-slate-800 self-start">
          <button
            type="button"
            class="px-3.5 sm:px-4 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
            :class="filter === 'all' ? 'bg-white dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 shadow-2xs' : 'text-slate-600 dark:text-slate-400'"
            @click="filter = 'all'"
          >
            Tất cả
          </button>
          <button
            type="button"
            class="px-3.5 sm:px-4 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
            :class="filter === 'income' ? 'bg-white dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 shadow-2xs' : 'text-slate-600 dark:text-slate-400'"
            @click="filter = 'income'"
          >
            Khoản thu (+)
          </button>
          <button
            type="button"
            class="px-3.5 sm:px-4 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
            :class="filter === 'expense' ? 'bg-white dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 shadow-2xs' : 'text-slate-600 dark:text-slate-400'"
            @click="filter = 'expense'"
          >
            Khoản chi (-)
          </button>
        </div>

        <!-- Category & Search & Add Button -->
        <div class="flex flex-wrap items-center gap-2.5 sm:gap-3">
          <select
            v-model="category"
            class="px-3.5 py-2 text-xs font-medium rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200/70 dark:border-slate-700 text-slate-700 dark:text-slate-200 focus:outline-none focus:border-emerald-500"
          >
            <option value="all">Tất cả danh mục</option>
            <optgroup v-for="g in categoryGroups" :key="g.label" :label="g.label">
              <option v-for="c in g.items" :key="g.label + c.value" :value="c.value">
                {{ c.value }}
              </option>
            </optgroup>
          </select>

          <div class="relative flex-1 min-w-[180px] sm:w-56">
            <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
            <input
              v-model="keyword"
              type="text"
              placeholder="Tìm nội dung giao dịch..."
              class="w-full pl-8 pr-3 py-2 text-xs rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200/70 dark:border-slate-700 text-slate-700 dark:text-slate-200 focus:outline-none focus:border-emerald-500"
            />
          </div>

          <button
            @click="showAdd = true"
            class="hidden md:flex px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold transition items-center gap-1.5 cursor-pointer shadow-sm shadow-emerald-600/20"
          >
            <i class="fa-solid fa-plus"></i> Thêm mới
          </button>
        </div>
      </div>

      <!-- Filtered Mini Summary Bar -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs">
        <div class="p-2.5 rounded-xl bg-emerald-50/70 dark:bg-emerald-950/30 flex items-center justify-between">
          <span class="text-slate-500 dark:text-slate-400">Tổng thu (lọc):</span>
          <strong class="text-emerald-600 dark:text-emerald-400 font-bold">+{{ formatVND(incomeTotal) }}</strong>
        </div>
        <div class="p-2.5 rounded-xl bg-rose-50/70 dark:bg-rose-950/30 flex items-center justify-between">
          <span class="text-slate-500 dark:text-slate-400">Tổng chi (lọc):</span>
          <strong class="text-rose-600 dark:text-rose-400 font-bold">-{{ formatVND(expenseTotal) }}</strong>
        </div>
        <div class="p-2.5 rounded-xl bg-slate-100/80 dark:bg-slate-800/60 flex items-center justify-between">
          <span class="text-slate-500 dark:text-slate-400">Chênh lệch ròng:</span>
          <strong class="font-bold" :class="netTotal >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'">
            {{ netTotal >= 0 ? '+' : '' }}{{ formatVND(netTotal) }}
          </strong>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <EmptyState v-if="!filtered.length" boxed text="Không tìm thấy giao dịch nào khớp với bộ lọc." />

    <!-- Transactions List / Table -->
    <div v-else class="space-y-4">
      <!-- Mobile: Card List -->
      <div class="sm:hidden space-y-3">
        <div
          v-for="t in paginated"
          :key="t.id"
          class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 p-4 card-shadow space-y-3"
        >
          <div class="flex items-start justify-between gap-2">
            <div class="flex items-center gap-3 min-w-0">
              <div class="w-9 h-9 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
                <i :class="['fa-solid', categoryMeta(t.category, t.type).icon, 'text-xs']"></i>
              </div>
              <div class="min-w-0">
                <p class="font-semibold text-sm text-slate-800 dark:text-slate-100 truncate">{{ t.note || t.category }}</p>
                <p class="text-xs text-slate-400">{{ t.date }} • {{ t.category }}</p>
              </div>
            </div>
            <div class="text-right shrink-0">
              <span class="font-bold text-sm" :class="amountClass(t)">{{ signedAmount(t) }}</span>
            </div>
          </div>

          <div class="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-slate-800/80 text-xs">
            <span
              class="px-2 py-0.5 rounded-full font-semibold"
              :class="t.type === 'income' ? 'bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400' : 'bg-rose-50 dark:bg-rose-950/80 text-rose-600 dark:text-rose-400'"
            >
              {{ t.type === 'income' ? 'Khoản thu' : 'Khoản chi' }}
            </span>
            <RowActions @edit="editing = t" @remove="removeTransaction(t)" />
          </div>
        </div>
      </div>

      <!-- Desktop/iPad: Sleek Table -->
      <div class="hidden sm:block bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow overflow-hidden transition-colors">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-200/80 dark:border-slate-800 text-[11px] font-bold uppercase tracking-wider text-slate-400 bg-slate-50/50 dark:bg-slate-800/40">
                <th class="py-3.5 px-5">Ngày</th>
                <th class="py-3.5 px-5">Nội dung diễn giải</th>
                <th class="py-3.5 px-5">Danh mục</th>
                <th class="py-3.5 px-5 text-center">Phân loại</th>
                <th class="py-3.5 px-5 text-right">Số tiền</th>
                <th class="py-3.5 px-5 text-center">Thao tác</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/70 text-sm">
              <tr
                v-for="t in paginated"
                :key="t.id"
                class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition"
              >
                <td class="py-3.5 px-5 text-xs text-slate-500 dark:text-slate-400 whitespace-nowrap">{{ t.date }}</td>
                <td class="py-3.5 px-5 font-semibold text-xs sm:text-sm text-slate-800 dark:text-slate-100">
                  {{ t.note || t.category }}
                </td>
                <td class="py-3.5 px-5 whitespace-nowrap">
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400">
                    <i :class="['fa-solid', categoryMeta(t.category, t.type).icon]"></i>
                    {{ t.category }}
                  </span>
                </td>
                <td class="py-3.5 px-5 text-center whitespace-nowrap">
                  <span
                    class="px-2 py-0.5 rounded-full text-xs font-semibold"
                    :class="t.type === 'income' ? 'bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400' : 'bg-rose-50 dark:bg-rose-950/80 text-rose-600 dark:text-rose-400'"
                  >
                    {{ t.type === 'income' ? 'Thu' : 'Chi' }}
                  </span>
                </td>
                <td class="py-3.5 px-5 text-right font-bold text-xs sm:text-sm whitespace-nowrap" :class="amountClass(t)">
                  {{ signedAmount(t) }}
                </td>
                <td class="py-3.5 px-5 text-center whitespace-nowrap">
                  <RowActions class="justify-center" @edit="editing = t" @remove="removeTransaction(t)" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Bottom Pagination -->
    <template v-if="pageCount > 1" #bottom>
      <div class="flex justify-center">
        <PaginationBar v-model:page="page" :page-count="pageCount" />
      </div>
    </template>

    <FabButton @click="showAdd = true" />
    <TransactionFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false" />
    <TransactionFormModal v-if="editing" :existing="editing" @close="editing = null" @saved="editing = null" />
  </PageShell>
</template>
