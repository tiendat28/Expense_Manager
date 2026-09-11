<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTransactionsStore } from '../stores/transactions'
import { formatVND, categoryMeta, EXPENSE_CATEGORIES, INCOME_CATEGORIES } from '../utils/formatters'
import TransactionFormModal from '../components/TransactionFormModal.vue'
import PageShell from '../components/PageShell.vue'
import PageTitle from '../components/PageTitle.vue'
import FabButton from '../components/FabButton.vue'

const PAGE_SIZE = 10

const tx = useTransactionsStore()
const route = useRoute()
const router = useRouter()
const filter = ref('all')
const category = ref('all')
const page = ref(1)
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

const pageCount = computed(() => Math.max(1, Math.ceil(filtered.value.length / PAGE_SIZE)))
const paginated = computed(() => {
  const start = (page.value - 1) * PAGE_SIZE
  return filtered.value.slice(start, start + PAGE_SIZE).map((t, i) => ({ ...t, stt: start + i + 1 }))
})

watch(filter, () => {
  const stillValid = categoryGroups.value.some((g) => g.items.some((c) => c.value === category.value))
  if (!stillValid) category.value = 'all'
})
watch([filter, category], () => (page.value = 1))
watch(pageCount, (count) => {
  if (page.value > count) page.value = count
})

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
        <PageTitle text="Giao dịch" />

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

    <p v-if="!filtered.length" class="bg-white rounded-2xl card-shadow text-center text-gray-900 py-6 text-sm">
      Không có giao dịch nào.
    </p>

    <!-- Mobile: card list -->
    <div v-else class="sm:hidden bg-white rounded-2xl card-shadow divide-y">
      <div v-for="t in paginated" :key="t.id" class="flex items-center px-4 py-3 cursor-pointer" @click="editing = t">
        <span class="w-8 text-center text-lg">{{ categoryMeta(t.category, t.type).icon }}</span>
        <div class="flex-1 ml-2 min-w-0">
          <div class="truncate">{{ t.note || t.category }}</div>
          <div class="text-xs text-gray-900">{{ t.category }} · {{ t.date }}</div>
        </div>
        <div :class="t.type === 'income' ? 'text-green-600' : 'text-red-600'" class="font-medium">
          {{ t.type === 'income' ? '+' : '-' }}{{ formatVND(t.amount) }}
        </div>
      </div>
    </div>

    <!-- Desktop: table -->
    <div v-if="filtered.length" class="hidden sm:block bg-white rounded-2xl card-shadow overflow-x-auto">
      <table class="w-full text-sm whitespace-nowrap">
        <thead>
          <tr class="border-b text-left text-gray-900">
            <th class="px-4 py-3 font-medium">STT</th>
            <th class="px-4 py-3 font-medium">Danh mục</th>
            <th class="px-4 py-3 font-medium text-right">Số tiền</th>
            <th class="px-4 py-3 font-medium">Loại</th>
            <th class="px-4 py-3 font-medium">Ngày</th>
            <th class="px-4 py-3 font-medium">Ghi chú</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="t in paginated"
            :key="t.id"
            class="border-b last:border-0 cursor-pointer hover:bg-gray-50"
            @click="editing = t"
          >
            <td class="px-4 py-3 text-gray-900">{{ t.stt }}</td>
            <td class="px-4 py-3 font-medium">
              <span class="mr-1.5">{{ categoryMeta(t.category, t.type).icon }}</span>{{ t.category }}
            </td>
            <td class="px-4 py-3 font-medium text-right" :class="t.type === 'income' ? 'text-green-600' : 'text-red-600'">
              {{ t.type === 'income' ? '+' : '-' }}{{ formatVND(t.amount) }}
            </td>
            <td class="px-4 py-3">
              <span
                class="px-2 py-0.5 rounded-full text-xs"
                :class="t.type === 'income' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
              >
                {{ t.type === 'income' ? 'Thu' : 'Chi' }}
              </span>
            </td>
            <td class="px-4 py-3 text-gray-900">{{ t.date }}</td>
            <td class="px-4 py-3 text-gray-900 max-w-[280px] truncate">{{ t.note || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="pageCount > 1" class="flex w-fit mx-auto items-center gap-4 text-xs bg-white rounded-2xl card-shadow px-4 py-2">
      <button class="px-2.5 py-1 rounded-lg border disabled:opacity-40" :disabled="page === 1" @click="page--">‹</button>
      <span class="text-gray-900">Trang {{ page }} / {{ pageCount }}</span>
      <button class="px-2.5 py-1 rounded-lg border disabled:opacity-40" :disabled="page === pageCount" @click="page++">›</button>
    </div>

    <FabButton @click="showAdd = true" />
    <TransactionFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false" />
    <TransactionFormModal v-if="editing" :existing="editing" @close="editing = null" @saved="editing = null" />
  </PageShell>
</template>
