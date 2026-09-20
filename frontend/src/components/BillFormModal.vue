<script setup>
import { ref } from 'vue'
import { useBillsStore } from '../stores/bills'
import { useToastStore } from '../stores/toast'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { EXPENSE_CATEGORIES } from '../utils/formatters'
import AmountField from './AmountField.vue'
import ModalShell from './ModalShell.vue'
import ModalFooter from './ModalFooter.vue'

const props = defineProps({ existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const store = useBillsStore()
const toast = useToastStore()
const confirmDelete = useConfirmDelete()

const name = ref(props.existing?.name || '')
const amount = ref(props.existing?.amount ?? '')
const category = ref(props.existing?.category || 'Hóa đơn')
const dueDay = ref(props.existing?.due_day ?? 5)

async function save() {
  const payload = { name: name.value, amount: Number(amount.value), category: category.value, due_day: Number(dueDay.value) }
  if (props.existing) {
    await store.update(props.existing.id, payload)
  } else {
    await store.create(payload)
  }
  toast.show('Đã lưu thành công')
  emit('saved')
}
async function remove() {
  const deleted = await confirmDelete(`Bạn có chắc chắn muốn xóa hóa đơn "${props.existing.name}"?`, () => store.remove(props.existing.id))
  if (deleted) emit('saved')
}
</script>

<template>
  <ModalShell :title="existing ? 'Sửa hóa đơn' : 'Hóa đơn mới'" @close="$emit('close')">
      <input v-model="name" type="text" placeholder="Ví dụ: Tiền điện" class="w-full border rounded-lg px-3 py-2" />
      <AmountField v-model="amount" />
      <select v-model="category" class="w-full border rounded-lg px-3 py-2">
        <option v-for="c in EXPENSE_CATEGORIES" :key="c.value" :value="c.value">{{ c.icon }} {{ c.value }}</option>
      </select>
      <div>
        <label class="text-xs text-gray-900">Ngày nhắc hàng tháng: {{ dueDay }}</label>
        <input v-model="dueDay" type="range" min="1" max="28" class="w-full" />
      </div>
      <ModalFooter :delete-label="existing ? 'Xóa hóa đơn này' : ''" @close="$emit('close')" @save="save" @remove="remove" />
  </ModalShell>
</template>
