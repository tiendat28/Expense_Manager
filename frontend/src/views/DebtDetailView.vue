<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDebtsStore } from '../stores/debts'
import { formatVND, categoryMeta } from '../utils/formatters'
import DebtFormModal from '../components/DebtFormModal.vue'
import DebtPaymentModal from '../components/DebtPaymentModal.vue'
import PageShell from '../components/PageShell.vue'

const route = useRoute()
const router = useRouter()
const store = useDebtsStore()
const showEdit = ref(false)
const showPayment = ref(false)
const editingPayment = ref(null)

const debt = computed(() => store.items.find((d) => d.id === Number(route.params.id)))
const remaining = computed(() => (debt.value ? Math.max(debt.value.total_amount - debt.value.paid_amount, 0) : 0))
const progress = computed(() =>
  debt.value && debt.value.total_amount > 0 ? Math.min(debt.value.paid_amount / debt.value.total_amount, 1) * 100 : 0
)
const color = computed(() => (debt.value?.type === 'owe' ? 'text-red-600' : 'text-green-600'))
const category = computed(() => (debt.value ? categoryMeta(debt.value.category, debt.value.type === 'lent' ? 'income' : 'expense') : null))
const sortedPayments = computed(() =>
  debt.value ? [...debt.value.payments].sort((a, b) => new Date(b.date) - new Date(a.date)) : []
)

async function removeDebt() {
  await store.remove(debt.value.id)
  router.push({ name: 'debts' })
}

onMounted(() => {
  if (!store.items.length) store.fetchAll()
})
</script>

<template>
  <PageShell>
  <div v-if="debt">
    <div class="flex items-center justify-between mb-3">
      <button @click="router.back()" class="text-gray-900">‹ Quay lại</button>
      <div class="flex gap-3 text-sm">
        <button @click="showEdit = true" class="text-green-600">Sửa</button>
        <button @click="removeDebt" class="text-red-500">Xóa</button>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-6 text-center mb-4">
      <div :class="color" class="text-4xl mb-2">{{ debt.type === 'owe' ? '↑' : '↓' }}</div>
      <div class="font-semibold text-lg">{{ debt.person_name }}</div>
      <div class="text-sm text-gray-900 mb-3">{{ debt.type === 'owe' ? 'Tôi nợ' : 'Cho vay' }} · {{ category?.icon }} {{ debt.category }}</div>
      <div class="text-sm text-gray-900 mb-1">{{ formatVND(debt.paid_amount) }} / {{ formatVND(debt.total_amount) }}</div>
      <div class="h-2 bg-gray-100 rounded-full overflow-hidden mb-3">
        <div class="h-full rounded-full" :class="remaining <= 0 ? 'bg-green-500' : (debt.type === 'owe' ? 'bg-red-500' : 'bg-green-500')" :style="{ width: progress + '%' }"></div>
      </div>
      <div v-if="remaining <= 0" class="text-green-600 text-sm">🎉 Đã tất toán!</div>
      <div v-else :class="color" class="font-semibold text-lg">Còn lại: {{ formatVND(remaining) }}</div>
      <div v-if="debt.due_date" class="text-xs text-gray-900 mt-2">Hạn: {{ debt.due_date }}</div>
      <p v-if="debt.note" class="text-sm text-gray-900 mt-3">{{ debt.note }}</p>
    </div>

    <h3 class="font-semibold mb-2 text-sm text-gray-900">Lịch sử thanh toán</h3>
    <div class="bg-white rounded-2xl divide-y mb-24">
      <p v-if="!sortedPayments.length" class="text-center text-gray-900 py-6 text-sm">Chưa có lần thanh toán nào.</p>
      <div
        v-for="p in sortedPayments" :key="p.id"
        class="flex items-center justify-between px-4 py-3 cursor-pointer"
        @click="editingPayment = p"
      >
        <div>
          <div>{{ formatVND(p.amount) }}</div>
          <div class="text-xs text-gray-900">{{ new Date(p.date).toLocaleString('vi-VN') }}</div>
        </div>
        <span class="text-gray-300">›</span>
      </div>
    </div>

    <button
      v-if="remaining > 0" @click="showPayment = true"
      class="sticky bottom-6 block w-full sm:max-w-md sm:mx-auto bg-green-600 text-white rounded-xl py-3 font-medium"
    >
      Ghi nhận thanh toán
    </button>

    <DebtFormModal v-if="showEdit" :existing="debt" @close="showEdit = false" @saved="showEdit = false" />
    <DebtPaymentModal v-if="showPayment" :debt="debt" @close="showPayment = false" @saved="showPayment = false" />
    <DebtPaymentModal
      v-if="editingPayment" :debt="debt" :existing="editingPayment"
      @close="editingPayment = null" @saved="editingPayment = null"
    />
  </div>
  </PageShell>
</template>
