<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTransactionsStore } from '../stores/transactions'
import { usePagination } from '../composables/usePagination'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { formatVND, categoryMeta, EXPENSE_CATEGORIES, INCOME_CATEGORIES } from '../utils/formatters'
import TransactionFormModal from '../components/TransactionFormModal.vue'
import PageShell from '../components/PageShell.vue'
import PageTitle from '../components/PageTitle.vue'
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
const showAdd = ref(false)
const editing = ref(null)

const categoryGroups = computed(() => {
  const groups = []
  if (filter.value !== 'income') groups.push({ label: 'Chi', items: EXPENSE_CATEGORIES })
  if (filter.value !== 'expense') groups.push({ label: 'Thu', items: INCOME_CATEGORIES })
  return groups
})

const filtered = computed(() =>
  tx.items.filter(
    (t) => (filter.value === 'all' || t.type === filter.value) && (category.value === 'all' || t.category === category.value)
  )
)

const incomeTotal = computed(() =>
  filtered.value.filter((t) => t.type === 'income').reduce((sum, t) => sum + Number(t.amount), 0)
)
const expenseTotal = computed(() =>
  filtered.value.filter((t) => t.type === 'expense').reduce((sum, t) => sum + Number(t.amount), 0)
)

const { page, pageCount, paginated } = usePagination(filtered)

const amountClass = (t) => (t.type === 'income' ? 'text-green-600' : 'text-red-600')
const badgeClass = (t) => (t.type === 'income' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700')
const signedAmount = (t) => `${t.type === 'income' ? '+' : '-'}${formatVND(t.amount)}`

watch(filter, () => {
  const stillValid = categoryGroups.value.some((g) => g.items.some((c) => c.value === category.value))
  if (!stillValid) category.value = 'all'
})
watch([filter, category], () => (page.value = 1))

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
    <template #sticky>
      <div class="space-y-3">
        <div class="flex items-center justify-between gap-2">
          <PageTitle text="Giao dịch" />
          <PaginationBar v-if="pageCount > 1" v-model:page="page" :page-count="pageCount" compact class="sm:hidden" />
        </div>

        <div class="flex gap-2">
          <div class="flex flex-1 rounded-lg overflow-hidden border bg-white text-sm">
            <button
              v-for="f in [['all', 'Tất cả'], ['expense', 'Chi'], ['income', 'Thu']]"
              :key="f[0]"
              class="flex-1 py-1.5"
              :class="filter === f[0] ? 'bg-green-600 text-white' : ''"
              @click="filter = f[0]"
            >
              {{ f[1] }}
            </button>
          </div>
          <select v-model="category" class="w-36 sm:w-44 border rounded-lg bg-white px-2 py-1.5 text-sm">
            <option value="all">Tất cả danh mục</option>
            <optgroup v-for="g in categoryGroups" :key="g.label" :label="g.label">
              <option v-for="c in g.items" :key="g.label + c.value" :value="c.value">{{ c.icon }} {{ c.value }}</option>
            </optgroup>
          </select>
        </div>

        <div class="bg-white rounded-2xl px-4 py-2.5 card-shadow flex items-center justify-between text-sm">
          <div>
            <span class="text-gray-900">Thu </span>
            <span class="font-semibold text-green-600">+{{ formatVND(incomeTotal) }}</span>
          </div>
          <div>
            <span class="text-gray-900">Chi </span>
            <span class="font-semibold text-red-600">-{{ formatVND(expenseTotal) }}</span>
          </div>
        </div>
      </div>
    </template>

    <EmptyState v-if="!filtered.length" boxed text="Không có giao dịch nào." />

    <div v-else>
      <!-- Mobile: card list -->
      <div class="sm:hidden space-y-2">
        <div v-for="t in paginated" :key="t.id" class="bg-white rounded-2xl card-shadow px-4 py-3">
          <div class="flex items-start justify-between gap-2">
            <div class="min-w-0">
              <div class="font-medium truncate">{{ t.note || t.category }}</div>
              <div class="text-xs text-gray-900">
                <span class="mr-1">{{ categoryMeta(t.category, t.type).icon }}</span>{{ t.category }}
              </div>
            </div>
            <div class="text-right shrink-0">
              <div class="font-semibold" :class="amountClass(t)">{{ signedAmount(t) }}</div>
              <div class="text-xs text-gray-900">{{ t.date }}</div>
            </div>
          </div>
          <div class="flex items-center gap-2 mt-2">
            <span class="px-1.5 py-0.5 rounded-full text-xs shrink-0" :class="badgeClass(t)">
              {{ t.type === 'income' ? 'Thu' : 'Chi' }}
            </span>
            <RowActions class="ml-auto shrink-0" @edit="editing = t" @remove="removeTransaction(t)" />
          </div>
        </div>
      </div>

      <!-- Desktop: table -->
      <div class="hidden sm:block bg-white rounded-2xl card-shadow overflow-x-auto">
        <table class="w-full text-sm whitespace-nowrap">
          <thead>
            <tr class="border-b text-left text-gray-900">
              <th class="px-4 py-3 font-medium">STT</th>
              <th class="px-4 py-3 font-medium">Danh mục</th>
              <th class="px-4 py-3 font-medium text-right">Số tiền</th>
              <th class="px-4 py-3 font-medium">Loại</th>
              <th class="px-4 py-3 font-medium">Ngày</th>
              <th class="px-4 py-3 font-medium">Ghi chú</th>
              <th class="px-4 py-3 font-medium text-center">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in paginated" :key="t.id" class="border-b last:border-0 hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-900">{{ t.stt }}</td>
              <td class="px-4 py-3 font-medium">
                <span class="mr-1.5">{{ categoryMeta(t.category, t.type).icon }}</span>{{ t.category }}
              </td>
              <td class="px-4 py-3 font-medium text-right" :class="amountClass(t)">{{ signedAmount(t) }}</td>
              <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded-full text-xs" :class="badgeClass(t)">
                  {{ t.type === 'income' ? 'Thu' : 'Chi' }}
                </span>
              </td>
              <td class="px-4 py-3 text-gray-900">{{ t.date }}</td>
              <td class="px-4 py-3 text-gray-900 max-w-[280px] truncate">{{ t.note || '—' }}</td>
              <td class="px-4 py-3">
                <RowActions class="justify-center" @edit="editing = t" @remove="removeTransaction(t)" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <template v-if="pageCount > 1" #bottom>
      <PaginationBar v-model:page="page" :page-count="pageCount" class="mx-auto" />
    </template>

    <FabButton @click="showAdd = true" />
    <TransactionFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false" />
    <TransactionFormModal v-if="editing" :existing="editing" @close="editing = null" @saved="editing = null" />
  </PageShell>
</template>
