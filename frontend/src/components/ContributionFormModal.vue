<script setup>
import { computed, ref } from 'vue'
import { useSavingsStore } from '../stores/savings'
import { useToastStore } from '../stores/toast'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { nowISO, toLocalInput, fromLocalInput } from '../utils/date'
import AmountField from './AmountField.vue'
import ModalShell from './ModalShell.vue'
import ModalFooter from './ModalFooter.vue'

const props = defineProps({
  goalId: Number,
  goalName: { type: String, default: '' },
  existing: { type: Object, default: null },
})
const emit = defineEmits(['close', 'saved'])
const store = useSavingsStore()
const toast = useToastStore()
const confirmDelete = useConfirmDelete()

const amount = ref(props.existing?.amount ?? '')
const date = ref(props.existing ? toLocalInput(props.existing.date) : nowISO())
const title = computed(() =>
  props.existing ? 'Chỉnh sửa lần nạp' : `Nạp tích lũy vào: "${props.goalName}"`
)

async function save() {
  if (!amount.value || Number(amount.value) <= 0) {
    toast.show('Vui lòng nhập số tiền nạp', 'error')
    return
  }
  const payload = { amount: Number(amount.value), date: fromLocalInput(date.value) }
  if (props.existing) {
    await store.updateContribution(props.goalId, props.existing.id, payload)
  } else {
    await store.addContribution(props.goalId, payload)
  }
  toast.show('Đã ghi nhận nạp tiền tích lũy thành công!')
  emit('saved')
}

async function remove() {
  const deleted = await confirmDelete(
    'Bạn có chắc chắn muốn xóa lần nạp này?',
    () => store.removeContribution(props.goalId, props.existing.id)
  )
  if (deleted) emit('saved')
}
</script>

<template>
  <ModalShell :title="title" @close="$emit('close')">
    <AmountField v-model="amount" placeholder="VD: 1000000" />

    <div>
      <label class="form-label">Thời gian nạp tiền</label>
      <input v-model="date" type="datetime-local" class="form-input" />
    </div>

    <ModalFooter
      :save-label="existing ? 'Cập nhật' : 'Xác nhận nạp tiền'"
      :delete-label="existing ? 'Xóa lần nạp này' : ''"
      @close="$emit('close')"
      @save="save"
      @remove="remove"
    />
  </ModalShell>
</template>
