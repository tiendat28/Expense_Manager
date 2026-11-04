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
const color = computed(() => (isOwe.value ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'))
const barColor = computed(() => (remaining.value <= 0 || !isOwe.value ? 'bg-emerald-500' : 'bg-rose-500'))
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
    <div v-if="debt" class="space-y-6 max-w-3xl mx-auto">
      <DetailHeader @edit="showEdit = true" @remove="removeDebt" />

      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 p-6 sm:p-8 text-center card-shadow transition-colors">
        <div class="w-14 h-14 rounded-2xl mx-auto mb-3 flex items-center justify-center text-xl font-bold"
          :class="isOwe ? 'bg-rose-50 dark:bg-rose-950/80 text-rose-600 dark:text-rose-400' : 'bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400'">
          <i :class="isOwe ? 'fa-solid fa-file-signature' : 'fa-solid fa-hand-holding-dollar'"></i>
        </div>

        <h2 class="font-display font-bold text-xl text-slate-900 dark:text-white">{{ debt.person_name }}</h2>
        <p class="text-xs text-slate-400 mt-1 mb-4">
          <span class="font-semibold" :class="color">{{ isOwe ? 'Tôi nợ (Đi vay)' : 'Cho vay (Phải thu)' }}</span> • {{ category?.label }}
        </p>

        <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 mb-4 max-w-md mx-auto space-y-2">
          <div class="flex justify-between text-xs text-slate-500 dark:text-slate-400">
            <span>Đã thanh toán: <strong class="text-emerald-600 dark:text-emerald-400 font-bold">{{ formatVND(debt.paid_amount) }}</strong></span>
            <span>Tổng: <strong class="text-slate-800 dark:text-slate-200 font-bold">{{ formatVND(debt.total_amount) }}</strong></span>
          </div>

          <div class="h-2 bg-slate-200/80 dark:bg-slate-700 rounded-full overflow-hidden">
            <div class="h-full rounded-full progress-bar-fill" :class="barColor" :style="{ width: progress + '%' }"></div>
          </div>

          <div class="flex justify-between items-center text-xs pt-1">
            <span class="text-slate-400">Tiến độ: {{ Math.round(progress) }}%</span>
            <span v-if="remaining <= 0" class="text-emerald-600 dark:text-emerald-400 font-bold">
              <i class="fa-solid fa-check-double mr-1"></i> Đã tất toán!
            </span>
            <span v-else class="font-bold" :class="color">
              Còn lại: {{ formatVND(remaining) }}
            </span>
          </div>
        </div>

        <p v-if="debt.due_date" class="text-xs text-slate-400">
          <i class="fa-regular fa-calendar-check mr-1"></i> Hạn thanh toán: <strong class="text-slate-700 dark:text-slate-300">{{ debt.due_date }}</strong>
        </p>
        <p v-if="debt.note" class="text-xs text-slate-500 dark:text-slate-400 mt-2 bg-slate-50 dark:bg-slate-800 p-2.5 rounded-lg inline-block">
          {{ debt.note }}
        </p>
      </div>

      <HistoryList
        title="Lịch sử thanh toán"
        empty-text="Chưa có lần thanh toán nào."
        :items="debt.payments"
        @select="editingPayment = $event"
      />

      <button
        v-if="remaining > 0"
        class="block w-full sm:max-w-md sm:mx-auto bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-700 hover:to-green-600 text-white rounded-xl py-3 font-semibold text-sm shadow-md shadow-emerald-500/20 transition cursor-pointer"
        @click="showPayment = true"
      >
        <i class="fa-solid fa-coins mr-1.5"></i> Ghi nhận thanh toán
      </button>

      <DebtFormModal v-if="showEdit" :existing="debt" @close="showEdit = false" @saved="showEdit = false; store.fetchAll()" />
      <DebtPaymentModal v-if="showPayment" :debt="debt" @close="showPayment = false" @saved="showPayment = false; store.fetchAll()" />
      <DebtPaymentModal
        v-if="editingPayment"
        :debt="debt"
        :existing="editingPayment"
        @close="editingPayment = null"
        @saved="editingPayment = null; store.fetchAll()"
      />
    </div>
  </PageShell>
</template>
