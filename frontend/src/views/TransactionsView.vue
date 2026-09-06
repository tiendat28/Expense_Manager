<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTransactionsStore } from '../stores/transactions'
import { formatVND, categoryMeta } from '../utils/formatters'
import TransactionFormModal from '../components/TransactionFormModal.vue'
import PageShell from '../components/PageShell.vue'

const tx = useTransactionsStore()
const filter = ref('all')
const showAdd = ref(false)
const editing = ref(null)

const filtered = computed(() => {
  if (filter.value === 'all') return tx.items
  return tx.items.filter((t) => t.type === filter.value)
})

onMounted(() => tx.refreshAll())
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

    <div class="bg-white rounded-2xl card-shadow divide-y">
      <p v-if="!filtered.length" class="text-center text-gray-900 py-6 text-sm">Không có giao dịch nào.</p>
      <div v-for="t in filtered" :key="t.id" class="flex items-center px-4 py-3 cursor-pointer" @click="editing = t">
        <span class="w-8 text-center text-lg">{{ categoryMeta(t.category, t.type).icon }}</span>
        <div class="flex-1 ml-2">
          <div>{{ t.note || t.category }}</div>
          <div class="text-xs text-gray-900">{{ t.category }} · {{ t.date }}</div>
        </div>
        <div :class="t.type === 'income' ? 'text-green-600' : 'text-red-600'" class="font-medium">
          {{ t.type === 'income' ? '+' : '-' }}{{ formatVND(t.amount) }}
        </div>
      </div>
    </div>

    <button @click="showAdd = true" class="glass-fab fixed bottom-20 sm:bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-green-500 to-green-700 text-white text-2xl hover:brightness-110">+</button>
    <TransactionFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false" />
    <TransactionFormModal v-if="editing" :existing="editing" @close="editing = null" @saved="editing = null" />
  </PageShell>
</template>
