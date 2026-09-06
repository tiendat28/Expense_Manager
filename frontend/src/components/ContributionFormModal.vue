<script setup>
import { ref } from 'vue'
import { useSavingsStore } from '../stores/savings'
import { useToastStore } from '../stores/toast'
import AmountField from './AmountField.vue'

const props = defineProps({ goalId: Number, goalName: { type: String, default: '' }, existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const store = useSavingsStore()
const toast = useToastStore()

const amount = ref(props.existing?.amount ?? '')
const date = ref(props.existing ? props.existing.date.slice(0, 16) : new Date().toISOString().slice(0, 16))

async function save() {
  const payload = { amount: Number(amount.value), date: date.value }
  if (props.existing) {
    await store.updateContribution(props.goalId, props.existing.id, payload)
  } else {
    await store.addContribution(props.goalId, payload)
  }
  toast.show('Đã lưu thành công')
  emit('saved')
}
async function remove() {
  await store.removeContribution(props.goalId, props.existing.id)
  emit('saved')
}
</script>

<template>
  <div class="fixed inset-0 bg-black/30 flex items-center justify-center p-4 z-30" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl w-full sm:max-w-md p-5 space-y-4 max-h-[85vh] overflow-y-auto">
      <h2 class="font-semibold text-lg">{{ existing ? 'Sửa lần nạp' : `Nạp tiền vào "${goalName}"` }}</h2>
      <AmountField v-model="amount" />
      <input v-model="date" type="datetime-local" class="w-full border rounded-lg px-3 py-2" />
      <div class="flex gap-2 pt-2">
        <button @click="$emit('close')" class="flex-1 py-2 rounded-lg border">Hủy</button>
        <button @click="save" class="flex-1 py-2 rounded-lg bg-green-600 text-white">Lưu</button>
      </div>
      <button v-if="existing" @click="remove" class="w-full text-red-500 text-sm py-2">Xóa lần nạp này</button>
    </div>
  </div>
</template>
