<script setup>
import { computed, ref } from 'vue'
import { useDebtsStore } from '../stores/debts'
import { useToastStore } from '../stores/toast'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { nowISO, toLocalInput, fromLocalInput } from '../utils/date'
import { formatVND } from '../utils/formatters'
import { remaining as remainingOf } from '../utils/progress'
import AmountField from './AmountField.vue'
import ModalShell from './ModalShell.vue'
import ModalFooter from './ModalFooter.vue'

const props = defineProps({ debt: Object, existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const store = useDebtsStore()
const toast = useToastStore()
const confirmDelete = useConfirmDelete()

const remaining = computed(() => remainingOf(props.debt.total_amount, props.debt.paid_amount))
const amount = ref(props.existing?.amount ?? (remaining.value > 0 ? remaining.value : ''))
const date = ref(props.existing ? toLocalInput(props.existing.date) : nowISO())

const isLend = computed(() => props.debt.type === 'lent')
const title = computed(() =>
  props.existing
    ? 'Chỉnh sửa lần thanh toán'
    : isLend.value
      ? `Thu nợ từ "${props.debt.person_name}"`
      : `Trả nợ cho "${props.debt.person_name}"`
)

async function save() {
  if (!amount.value || Number(amount.value) <= 0) {
    toast.show('Vui lòng nhập số tiền thanh toán', 'error')
    return
  }
  const payload = { amount: Number(amount.value), date: fromLocalInput(date.value) }
  if (props.existing) {
    await store.updatePayment(props.debt.id, props.existing.id, payload)
  } else {
    await store.addPayment(props.debt.id, payload)
  }
  toast.show(`Đã cập nhật ${isLend.value ? 'thu nợ' : 'trả nợ'} thành công!`)
  emit('saved')
}

async function remove() {
  const deleted = await confirmDelete(
    'Bạn có chắc chắn muốn xóa lần thanh toán này?',
    () => store.removePayment(props.debt.id, props.existing.id)
  )
  if (deleted) emit('saved')
}
</script>

<template>
  <ModalShell :title="title" @close="$emit('close')">
    <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-100 dark:border-slate-800 text-xs space-y-1">
      <p class="text-slate-500 dark:text-slate-400">
        Người liên quan: <strong class="text-slate-800 dark:text-slate-100">{{ debt.person_name }}</strong>
      </p>
      <p class="text-slate-500 dark:text-slate-400">
        Dư nợ còn lại: <strong class="text-rose-600 dark:text-rose-400">{{ formatVND(remaining) }}</strong>
      </p>
    </div>

    <AmountField v-model="amount" placeholder="Số tiền thanh toán đợt này" />

    <div>
      <label class="form-label">Thời gian thanh toán</label>
      <input v-model="date" type="datetime-local" class="form-input" />
    </div>

    <ModalFooter
      :save-label="existing ? 'Cập nhật' : (isLend ? 'Xác nhận thu nợ' : 'Xác nhận trả nợ')"
      :delete-label="existing ? 'Xóa lần thanh toán này' : ''"
      @close="$emit('close')"
      @save="save"
      @remove="remove"
    />
  </ModalShell>
</template>
