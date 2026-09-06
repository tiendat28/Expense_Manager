<script setup>
import { ref } from 'vue'
import { useDebtsStore } from '../stores/debts'
import { useToastStore } from '../stores/toast'
import { EXPENSE_CATEGORIES, INCOME_CATEGORIES } from '../utils/formatters'
import AmountField from './AmountField.vue'
import ModalShell from './ModalShell.vue'

const props = defineProps({ existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const store = useDebtsStore()
const toast = useToastStore()

const type = ref(props.existing?.type || 'owe')
const personName = ref(props.existing?.person_name || '')
const category = ref(props.existing?.category || currentCategories()[0].value)
const totalAmount = ref(props.existing?.total_amount ?? '')
const paidAmount = ref(props.existing?.paid_amount ?? 0)
const hasDueDate = ref(!!props.existing?.due_date)
const dueDate = ref(props.existing?.due_date || new Date().toISOString().slice(0, 10))
const note = ref(props.existing?.note || '')

function currentCategories() {
  return type.value === 'owe' ? EXPENSE_CATEGORIES : INCOME_CATEGORIES
}

function switchType(t) {
  type.value = t
  category.value = currentCategories()[0].value
}

async function save() {
  const payload = {
    person_name: personName.value, type: type.value, category: category.value,
    total_amount: Number(totalAmount.value), paid_amount: Number(paidAmount.value),
    due_date: hasDueDate.value ? dueDate.value : null, note: note.value,
  }
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
  <ModalShell :title="existing ? 'Sửa khoản nợ' : 'Khoản nợ mới'" @close="$emit('close')">
      <div class="flex rounded-lg overflow-hidden border">
        <button class="flex-1 py-2 text-sm" :class="type === 'owe' ? 'bg-red-500 text-white' : ''" @click="switchType('owe')">Tôi nợ</button>
        <button class="flex-1 py-2 text-sm" :class="type === 'lent' ? 'bg-green-500 text-white' : ''" @click="switchType('lent')">Cho vay</button>
      </div>

      <input v-model="personName" type="text" placeholder="Tên người liên quan" class="w-full border rounded-lg px-3 py-2" />

      <select v-model="category" class="w-full border rounded-lg px-3 py-2">
        <option v-for="c in currentCategories()" :key="c.value" :value="c.value">{{ c.icon }} {{ c.value }}</option>
      </select>

      <AmountField v-model="totalAmount" placeholder="Tổng số tiền" />

      <div v-if="existing">
        <label class="text-xs text-gray-900">Đã trả / đã thu</label>
        <AmountField v-model="paidAmount" />
      </div>

      <label class="flex items-center gap-2 text-sm">
        <input type="checkbox" v-model="hasDueDate" /> Có ngày hạn
      </label>
      <input v-if="hasDueDate" v-model="dueDate" type="date" class="w-full border rounded-lg px-3 py-2" />

      <input v-model="note" type="text" placeholder="Ghi chú (tùy chọn)" class="w-full border rounded-lg px-3 py-2" />

      <div class="flex gap-2 pt-2">
        <button @click="$emit('close')" class="flex-1 py-2 rounded-lg border">Hủy</button>
        <button @click="save" class="flex-1 py-2 rounded-lg bg-green-600 text-white">Lưu</button>
      </div>
      <button v-if="existing" @click="remove" class="w-full text-red-500 text-sm py-2">Xóa khoản nợ này</button>
  </ModalShell>
</template>
