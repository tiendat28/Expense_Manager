<script setup>
import { computed, ref } from 'vue'
import { useDebtsStore } from '../stores/debts'
import { useToastStore } from '../stores/toast'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { nowISO, toLocalInput, fromLocalInput } from '../utils/date'
import AmountField from './AmountField.vue'
import ModalShell from './ModalShell.vue'
import ModalFooter from './ModalFooter.vue'

const props = defineProps({ debt: Object, existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const store = useDebtsStore()
const toast = useToastStore()
const confirmDelete = useConfirmDelete()

const amount = ref(props.existing?.amount ?? '')
const date = ref(props.existing ? toLocalInput(props.existing.date) : nowISO())
const title = computed(() => props.existing
  ? 'Sửa lần thanh toán'
  : (props.debt.type === 'owe' ? `Ghi nhận đã trả cho "${props.debt.person_name}"` : `Ghi nhận đã thu từ "${props.debt.person_name}"`))

async function save() {
  const payload = { amount: Number(amount.value), date: fromLocalInput(date.value) }
  if (props.existing) {
    await store.updatePayment(props.debt.id, props.existing.id, payload)
  } else {
    await store.addPayment(props.debt.id, payload)
  }
  toast.show('Đã lưu thành công')
  emit('saved')
}
async function remove() {
  const deleted = await confirmDelete('Bạn có chắc chắn muốn xóa lần thanh toán này?', () => store.removePayment(props.debt.id, props.existing.id))
  if (deleted) emit('saved')
}
</script>

<template>
  <ModalShell :title="title" @close="$emit('close')">
      <AmountField v-model="amount" />
      <input v-model="date" type="datetime-local" class="w-full border rounded-lg px-3 py-2" />
      <ModalFooter :delete-label="existing ? 'Xóa lần thanh toán này' : ''" @close="$emit('close')" @save="save" @remove="remove" />
  </ModalShell>
</template>
