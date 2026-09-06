<script setup>
import { ref } from 'vue'
import { useBillsStore } from '../stores/bills'
import { useToastStore } from '../stores/toast'
import { EXPENSE_CATEGORIES } from '../utils/formatters'
import AmountField from './AmountField.vue'
import ModalShell from './ModalShell.vue'

const props = defineProps({ existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const store = useBillsStore()
const toast = useToastStore()

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
  await store.remove(props.existing.id)
  emit('saved')
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
      <div class="flex gap-2 pt-2">
        <button @click="$emit('close')" class="flex-1 py-2 rounded-lg border">Hủy</button>
        <button @click="save" class="flex-1 py-2 rounded-lg bg-green-600 text-white">Lưu</button>
      </div>
      <button v-if="existing" @click="remove" class="w-full text-red-500 text-sm py-2">Xóa hóa đơn này</button>
  </ModalShell>
</template>
