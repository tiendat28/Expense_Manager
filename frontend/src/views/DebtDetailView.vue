<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDebtsStore } from '../stores/debts'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { formatVND, categoryMeta } from '../utils/formatters'
import { percent, remaining as remainingOf } from '../utils/progress'
import DebtFormModal from '../components/DebtFormModal.vue'
import DebtPaymentModal from '../components/DebtPaymentModal.vue'
import DetailHeader from '../components/DetailHeader.vue'
import HistoryList from '../components/HistoryList.vue'
import PageShell from '../components/PageShell.vue'

const route = useRoute()
const router = useRouter()
const store = useDebtsStore()
const confirmDelete = useConfirmDelete()
const showEdit = ref(false)
const showPayment = ref(false)
const editingPayment = ref(null)

const debt = computed(() => store.items.find((d) => d.id === Number(route.params.id)))
const remaining = computed(() => (debt.value ? remainingOf(debt.value.total_amount, debt.value.paid_amount) : 0))
const progress = computed(() => (debt.value ? percent(debt.value.paid_amount, debt.value.total_amount) : 0))
const isOwe = computed(() => debt.value?.type === 'owe')
const color = computed(() => (isOwe.value ? 'text-red-600' : 'text-green-600'))
const barColor = computed(() => (remaining.value <= 0 || !isOwe.value ? 'bg-green-500' : 'bg-red-500'))
const category = computed(() =>
  debt.value ? categoryMeta(debt.value.category, isOwe.value ? 'expense' : 'income') : null
)

async function removeDebt() {
  const message = `Bạn có chắc chắn muốn xóa khoản nợ với "${debt.value.person_name}"?`
  if (await confirmDelete(message, () => store.remove(debt.value.id))) {
    router.push({ name: 'debts' })
  }
}

onMounted(() => {
  if (!store.items.length) store.fetchAll()
})
</script>

<template>
  <PageShell>
    <div v-if="debt">
      <DetailHeader @edit="showEdit = true" @remove="removeDebt" />

      <div class="bg-white rounded-2xl card-shadow p-6 text-center mb-4">
        <div :class="color" class="text-4xl mb-2">{{ isOwe ? '↑' : '↓' }}</div>
        <div class="font-semibold text-lg">{{ debt.person_name }}</div>
        <div class="text-sm text-gray-900 mb-3">
          {{ isOwe ? 'Tôi nợ' : 'Cho vay' }} · {{ category?.icon }} {{ debt.category }}
        </div>
        <div class="text-sm text-gray-900 mb-1">
          {{ formatVND(debt.paid_amount) }} / {{ formatVND(debt.total_amount) }}
        </div>
        <div class="h-2 bg-gray-100 rounded-full overflow-hidden mb-3">
          <div class="h-full rounded-full" :class="barColor" :style="{ width: progress + '%' }"></div>
        </div>
        <div v-if="remaining <= 0" class="text-green-600 text-sm">🎉 Đã tất toán!</div>
        <div v-else :class="color" class="font-semibold text-lg">Còn lại: {{ formatVND(remaining) }}</div>
        <div v-if="debt.due_date" class="text-xs text-gray-900 mt-2">Hạn: {{ debt.due_date }}</div>
        <p v-if="debt.note" class="text-sm text-gray-900 mt-3">{{ debt.note }}</p>
      </div>

      <HistoryList
        title="Lịch sử thanh toán"
        empty-text="Chưa có lần thanh toán nào."
        :items="debt.payments"
        @select="editingPayment = $event"
      />

      <button
        v-if="remaining > 0"
        class="sticky bottom-6 block w-full sm:max-w-md sm:mx-auto bg-green-600 text-white rounded-xl py-3 font-medium"
        @click="showPayment = true"
      >
        Ghi nhận thanh toán
      </button>

      <DebtFormModal v-if="showEdit" :existing="debt" @close="showEdit = false" @saved="showEdit = false" />
      <DebtPaymentModal v-if="showPayment" :debt="debt" @close="showPayment = false" @saved="showPayment = false" />
      <DebtPaymentModal
        v-if="editingPayment"
        :debt="debt"
        :existing="editingPayment"
        @close="editingPayment = null"
        @saved="editingPayment = null"
      />
    </div>
  </PageShell>
</template>
