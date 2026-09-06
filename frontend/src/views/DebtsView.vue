<script setup>
import { ref, onMounted } from 'vue'
import { useDebtsStore } from '../stores/debts'
import { formatVND, categoryMeta } from '../utils/formatters'
import DebtFormModal from '../components/DebtFormModal.vue'
import PageShell from '../components/PageShell.vue'

const store = useDebtsStore()
const showAdd = ref(false)

function progress(d) {
  return d.total_amount > 0 ? Math.min(d.paid_amount / d.total_amount, 1) * 100 : 0
}
function remaining(d) {
  return Math.max(d.total_amount - d.paid_amount, 0)
}
function debtCategory(d) {
  return categoryMeta(d.category, d.type === 'lent' ? 'income' : 'expense')
}

onMounted(() => store.fetchAll())
</script>

<template>
  <PageShell>
    <template #sticky>
      <h1 class="text-xl sm:text-2xl font-bold text-green-800">Sổ nợ</h1>
    </template>

    <p v-if="!store.items.length" class="text-center text-gray-900 py-10 text-sm">Chưa có khoản nợ nào. Nhấn + để thêm.</p>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div>
        <h2 class="font-semibold text-red-600 mb-2">Tôi nợ</h2>
        <p v-if="!store.oweList.length" class="text-xs text-gray-900">Không có khoản nào</p>
        <router-link v-for="d in store.oweList" :key="d.id" :to="`/debts/${d.id}`" class="block bg-white rounded-2xl border p-4 mb-3">
          <div class="flex justify-between mb-2">
            <div>
              <div class="font-semibold">{{ d.person_name }}</div>
              <div class="text-xs text-gray-900">{{ debtCategory(d).icon }} {{ d.category }}</div>
              <div v-if="d.due_date" class="text-xs text-gray-900">Hạn: {{ d.due_date }}</div>
            </div>
            <div class="font-semibold" :class="remaining(d) <= 0 ? 'text-green-600' : 'text-red-600'">{{ remaining(d) <= 0 ? 'Đã xong' : formatVND(remaining(d)) }}</div>
          </div>
          <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
            <div class="h-full rounded-full" :class="remaining(d) <= 0 ? 'bg-green-500' : 'bg-red-500'" :style="{ width: progress(d) + '%' }"></div>
          </div>
        </router-link>
        <div v-if="store.oweList.length" class="flex justify-between text-sm font-semibold text-red-600 px-1">
          <span>Tổng</span><span>{{ formatVND(store.totalOwe) }}</span>
        </div>
      </div>

      <div>
        <h2 class="font-semibold text-green-600 mb-2">Cho vay</h2>
        <p v-if="!store.lentList.length" class="text-xs text-gray-900">Không có khoản nào</p>
        <router-link v-for="d in store.lentList" :key="d.id" :to="`/debts/${d.id}`" class="block bg-white rounded-2xl border p-4 mb-3">
          <div class="flex justify-between mb-2">
            <div>
              <div class="font-semibold">{{ d.person_name }}</div>
              <div class="text-xs text-gray-900">{{ debtCategory(d).icon }} {{ d.category }}</div>
              <div v-if="d.due_date" class="text-xs text-gray-900">Hạn: {{ d.due_date }}</div>
            </div>
            <div class="text-green-600 font-semibold">{{ remaining(d) <= 0 ? 'Đã xong' : formatVND(remaining(d)) }}</div>
          </div>
          <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
            <div class="h-full bg-green-500 rounded-full" :style="{ width: progress(d) + '%' }"></div>
          </div>
        </router-link>
        <div v-if="store.lentList.length" class="flex justify-between text-sm font-semibold text-green-600 px-1">
          <span>Tổng</span><span>{{ formatVND(store.totalLent) }}</span>
        </div>
      </div>
    </div>

    <button @click="showAdd = true" class="glass-fab fixed bottom-20 sm:bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-green-500 to-green-700 text-white text-2xl hover:brightness-110">+</button>
    <DebtFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false" />
  </PageShell>
</template>
