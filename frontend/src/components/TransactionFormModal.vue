<script setup>
import { ref } from 'vue'
import { useTransactionsStore } from '../stores/transactions'
import { useToastStore } from '../stores/toast'
import { EXPENSE_CATEGORIES, INCOME_CATEGORIES } from '../utils/formatters'
import { todayISO } from '../utils/date'
import AmountField from './AmountField.vue'
import ModalShell from './ModalShell.vue'
import ModalFooter from './ModalFooter.vue'

const props = defineProps({ existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const tx = useTransactionsStore()
const toast = useToastStore()

const type = ref(props.existing?.type || 'expense')
const amount = ref(props.existing?.amount ?? '')
const category = ref(props.existing?.category || EXPENSE_CATEGORIES[0].value)
const note = ref(props.existing?.note || '')
const date = ref(props.existing?.date || todayISO())

function currentCategories() {
  return type.value === 'expense' ? EXPENSE_CATEGORIES : INCOME_CATEGORIES
}

function switchType(t) {
  type.value = t
  category.value = t === 'expense' ? EXPENSE_CATEGORIES[0].value : INCOME_CATEGORIES[0].value
}

async function save() {
  const payload = {
    amount: Number(amount.value), category: category.value,
    note: note.value, date: date.value, type: type.value,
  }
  if (props.existing) {
    await tx.update(props.existing.id, payload)
  } else {
    await tx.create(payload)
  }
  toast.show('Đã lưu thành công')
  emit('saved')
}

</script>

<template>
  <ModalShell :title="existing ? 'Sửa giao dịch' : 'Thêm giao dịch'" @close="$emit('close')">
      <div class="flex rounded-lg overflow-hidden border">
        <button class="flex-1 py-2 text-sm" :class="type === 'expense' ? 'bg-red-500 text-white' : 'bg-white'" @click="switchType('expense')">Chi</button>
        <button class="flex-1 py-2 text-sm" :class="type === 'income' ? 'bg-green-500 text-white' : 'bg-white'" @click="switchType('income')">Thu</button>
      </div>

      <AmountField v-model="amount" />

      <select v-model="category" class="w-full border rounded-lg px-3 py-2">
        <option v-for="c in currentCategories()" :key="c.value" :value="c.value">{{ c.icon }} {{ c.value }}</option>
      </select>

      <input v-model="note" type="text" placeholder="Ghi chú" class="w-full border rounded-lg px-3 py-2" />
      <input v-model="date" type="date" class="w-full border rounded-lg px-3 py-2" />

      <ModalFooter @close="$emit('close')" @save="save" />
  </ModalShell>
</template>
