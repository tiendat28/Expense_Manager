<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDebtsStore } from '../stores/debts'
import { formatVND, categoryMeta } from '../utils/formatters'
import { percent, remaining as remainingOf } from '../utils/progress'
import DebtFormModal from '../components/DebtFormModal.vue'
import PageShell from '../components/PageShell.vue'
import FabButton from '../components/FabButton.vue'
import PageTitle from '../components/PageTitle.vue'
import EmptyState from '../components/EmptyState.vue'

const store = useDebtsStore()
const showAdd = ref(false)
const filter = ref('unpaid')

const progress = (d) => percent(d.paid_amount, d.total_amount)
const remaining = (d) => remainingOf(d.total_amount, d.paid_amount)
const isSettled = (d) => remaining(d) <= 0
const debtCategory = (d) => categoryMeta(d.category, d.type === 'lent' ? 'income' : 'expense')

const unpaidCount = computed(() => store.items.filter((d) => !isSettled(d)).length)
const paidCount = computed(() => store.items.filter((d) => isSettled(d)).length)

const tabs = computed(() => [
  { key: 'unpaid', label: 'Chưa thanh toán', count: unpaidCount.value },
  { key: 'paid', label: 'Đã thanh toán', count: paidCount.value },
])

const matchesFilter = (d) => (filter.value === 'paid' ? isSettled(d) : !isSettled(d))
const oweList = computed(() => store.oweList.filter(matchesFilter))
const lentList = computed(() => store.lentList.filter(matchesFilter))
const hasAnyDebts = computed(() => oweList.value.length > 0 || lentList.value.length > 0)

function calcTotal(items) {
  return items.reduce((s, d) => s + (filter.value === 'paid' ? Number(d.total_amount) : remaining(d)), 0)
}

const columns = computed(() => [
  {
    key: 'owe',
    title: 'Tôi nợ',
    color: 'text-red-600',
    items: oweList.value,
    total: calcTotal(oweList.value),
    totalLabel: filter.value === 'paid' ? 'Tổng đã trả' : 'Tổng',
  },
  {
    key: 'lent',
    title: 'Cho vay',
    color: 'text-green-600',
    items: lentList.value,
    total: calcTotal(lentList.value),
    totalLabel: filter.value === 'paid' ? 'Tổng đã thu' : 'Tổng',
  },
])

onMounted(() => store.fetchAll())
</script>

<template>
  <PageShell>
    <template #sticky>
      <div class="space-y-3">
        <PageTitle text="Sổ nợ" />

        <div class="flex rounded-lg overflow-hidden border bg-white text-xs sm:text-sm max-w-xs sm:max-w-sm">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            type="button"
            class="flex-1 py-1.5 px-3 font-medium transition-colors text-center flex items-center justify-center gap-1.5"
            :class="filter === tab.key ? 'bg-green-600 text-white' : 'text-gray-700 hover:bg-gray-50'"
            @click="filter = tab.key"
          >
            <span>{{ tab.label }}</span>
            <span
              v-if="tab.count > 0"
              class="text-xs px-1.5 py-0.5 rounded-full font-semibold"
              :class="filter === tab.key ? 'bg-white/20 text-white' : 'bg-gray-100 text-gray-700'"
            >
              {{ tab.count }}
            </span>
          </button>
        </div>
      </div>
    </template>

    <EmptyState v-if="!store.items.length" text="Chưa có khoản nợ nào. Nhấn + để thêm." />
    <EmptyState
      v-else-if="!hasAnyDebts"
      boxed
      :text="filter === 'unpaid' ? 'Không có khoản nợ nào chưa thanh toán.' : 'Chưa có khoản nợ nào đã thanh toán.'"
    />
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div v-for="col in columns" :key="col.key">
        <h2 class="font-semibold mb-2" :class="col.color">{{ col.title }}</h2>
        <p v-if="!col.items.length" class="text-xs text-gray-900">Không có khoản nào</p>

        <router-link
          v-for="d in col.items"
          :key="d.id"
          :to="`/debts/${d.id}`"
          class="block bg-white rounded-2xl card-shadow p-4 mb-3"
        >
          <div class="flex justify-between mb-2">
            <div>
              <div class="font-semibold">{{ d.person_name }}</div>
              <div class="text-xs text-gray-900">{{ debtCategory(d).icon }} {{ d.category }}</div>
              <div v-if="d.due_date" class="text-xs text-gray-900">Hạn: {{ d.due_date }}</div>
            </div>
            <div class="text-right">
              <div
                class="font-semibold"
                :class="isSettled(d) || col.key === 'lent' ? 'text-green-600' : 'text-red-600'"
              >
                {{ isSettled(d) ? 'Đã xong' : formatVND(remaining(d)) }}
              </div>
              <div v-if="isSettled(d)" class="text-xs text-gray-400">
                {{ formatVND(d.total_amount) }}
              </div>
            </div>
          </div>
          <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
            <div
              class="h-full rounded-full"
              :class="isSettled(d) || col.key === 'lent' ? 'bg-green-500' : 'bg-red-500'"
              :style="{ width: progress(d) + '%' }"
            ></div>
          </div>
        </router-link>

        <div v-if="col.items.length" class="flex justify-between text-sm font-semibold px-1" :class="col.color">
          <span>{{ col.totalLabel }}</span>
          <span>{{ formatVND(col.total) }}</span>
        </div>
      </div>
    </div>

    <FabButton @click="showAdd = true" />
    <DebtFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false" />
  </PageShell>
</template>
