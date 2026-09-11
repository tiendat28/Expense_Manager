<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTransactionsStore } from '../stores/transactions'
import { formatVND, categoryMeta } from '../utils/formatters'
import TransactionFormModal from '../components/TransactionFormModal.vue'
import PageShell from '../components/PageShell.vue'
import FabButton from '../components/FabButton.vue'

const tx = useTransactionsStore()
const route = useRoute()
const router = useRouter()
const filter = ref('all')
const showAdd = ref(false)
const editing = ref(null)

const filtered = computed(() => {
  if (filter.value === 'all') return tx.items
  return tx.items.filter((t) => t.type === filter.value)
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
      <div class="flex rounded-lg overflow-hidden border bg-white">
        <button
          v-for="f in [['all', 'Tất cả'], ['expense', 'Chi'], ['income', 'Thu']]"
          :key="f[0]"
          class="flex-1 py-2 text-sm"
          :class="filter === f[0] ? 'bg-green-600 text-white' : ''"
          @click="filter = f[0]"
        >
          {{ f[1] }}
        </button>
      </div>
    </template>

    <p v-if="!filtered.length" class="bg-white rounded-2xl card-shadow text-center text-gray-900 py-6 text-sm">
      Không có giao dịch nào.
    </p>

    <!-- Mobile: card list -->
    <div v-else class="sm:hidden bg-white rounded-2xl card-shadow divide-y">
      <div v-for="t in filtered" :key="t.id" class="flex items-center px-4 py-3 cursor-pointer" @click="editing = t">
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
            <th class="px-4 py-3 font-medium">Ngày</th>
            <th class="px-4 py-3 font-medium">Danh mục</th>
            <th class="px-4 py-3 font-medium">Ghi chú</th>
            <th class="px-4 py-3 font-medium">Loại</th>
            <th class="px-4 py-3 font-medium text-right">Số tiền</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="t in filtered"
            :key="t.id"
            class="border-b last:border-0 cursor-pointer hover:bg-gray-50"
            @click="editing = t"
          >
            <td class="px-4 py-3 text-gray-900">{{ t.date }}</td>
            <td class="px-4 py-3 font-medium">
              <span class="mr-1.5">{{ categoryMeta(t.category, t.type).icon }}</span>{{ t.category }}
            </td>
            <td class="px-4 py-3 text-gray-900 max-w-[280px] truncate">{{ t.note || '—' }}</td>
            <td class="px-4 py-3">
              <span
                class="px-2 py-0.5 rounded-full text-xs"
                :class="t.type === 'income' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
              >
                {{ t.type === 'income' ? 'Thu' : 'Chi' }}
              </span>
            </td>
            <td class="px-4 py-3 font-medium text-right" :class="t.type === 'income' ? 'text-green-600' : 'text-red-600'">
              {{ t.type === 'income' ? '+' : '-' }}{{ formatVND(t.amount) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <FabButton @click="showAdd = true" />
    <TransactionFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false" />
    <TransactionFormModal v-if="editing" :existing="editing" @close="editing = null" @saved="editing = null" />
  </PageShell>
</template>
