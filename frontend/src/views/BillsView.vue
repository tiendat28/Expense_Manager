<script setup>
import { ref, onMounted } from 'vue'
import { useBillsStore } from '../stores/bills'
import { formatVND, categoryMeta } from '../utils/formatters'
import BillFormModal from '../components/BillFormModal.vue'
import PageShell from '../components/PageShell.vue'
import FabButton from '../components/FabButton.vue'
import PageTitle from '../components/PageTitle.vue'

const store = useBillsStore()
const showAdd = ref(false)
const editing = ref(null)

function isPaidThisMonth(bill) {
  const now = new Date()
  const key = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  return bill.last_paid_month === key
}

onMounted(() => store.fetchAll())
</script>

<template>
  <PageShell>
    <template #sticky>
      <PageTitle text="Hóa đơn" />
    </template>

    <p v-if="!store.items.length" class="text-center text-gray-900 py-10 text-sm">Chưa có hóa đơn định kỳ nào. Nhấn + để thêm.</p>
    <div class="bg-white rounded-2xl card-shadow divide-y">
      <div v-for="bill in store.items" :key="bill.id" class="flex items-center px-4 py-3">
        <span class="w-8 text-center text-lg">{{ categoryMeta(bill.category, 'expense').icon }}</span>
        <div class="flex-1 ml-2 cursor-pointer" @click="editing = bill">
          <div class="flex items-center gap-1">
            {{ bill.name }}
            <span v-if="!bill.is_active" class="text-xs text-gray-300">🔕</span>
          </div>
          <div class="text-xs text-gray-900">Ngày {{ bill.due_day }} hàng tháng · {{ formatVND(bill.amount) }}</div>
        </div>
        <span v-if="isPaidThisMonth(bill)" class="text-green-600 text-xs">Đã trả</span>
        <button v-else @click="store.markPaid(bill.id)" class="text-xs border rounded-full px-3 py-1">Đã trả</button>
      </div>
    </div>

    <FabButton @click="showAdd = true" />
    <BillFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false" />
    <BillFormModal v-if="editing" :existing="editing" @close="editing = null" @saved="editing = null" />
  </PageShell>
</template>
