<script setup>
import { ref } from 'vue'
import { useSavingsStore } from '../stores/savings'
import { useToastStore } from '../stores/toast'
import AmountField from './AmountField.vue'

const props = defineProps({ existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const store = useSavingsStore()
const toast = useToastStore()

const icons = ['🎯', '✈️', '🏠', '🚗', '💍', '🎓', '📱', '🏥']
const name = ref(props.existing?.name || '')
const targetAmount = ref(props.existing?.target_amount ?? '')
const icon = ref(props.existing?.icon || '🎯')

async function save() {
  const payload = { name: name.value, icon: icon.value, target_amount: Number(targetAmount.value) }
  if (props.existing) {
    await store.update(props.existing.id, payload)
  } else {
    await store.create(payload)
  }
  toast.show('Đã lưu thành công')
  emit('saved')
}
</script>

<template>
  <div class="fixed inset-0 bg-black/30 flex items-center justify-center p-4 z-30" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl w-full sm:max-w-md p-5 space-y-4 max-h-[85vh] overflow-y-auto">
      <h2 class="font-semibold text-lg">{{ existing ? 'Sửa mục tiêu' : 'Mục tiêu mới' }}</h2>
      <input v-model="name" type="text" placeholder="Ví dụ: Du lịch Đà Lạt" class="w-full border rounded-lg px-3 py-2" />
      <AmountField v-model="targetAmount" />
      <div class="flex gap-2 flex-wrap">
        <button v-for="opt in icons" :key="opt" @click="icon = opt"
          class="text-2xl w-10 h-10 rounded-full flex items-center justify-center"
          :class="icon === opt ? 'bg-green-100' : ''">{{ opt }}</button>
      </div>
      <div class="flex gap-2 pt-2">
        <button @click="$emit('close')" class="flex-1 py-2 rounded-lg border">Hủy</button>
        <button @click="save" class="flex-1 py-2 rounded-lg bg-green-600 text-white">Lưu</button>
      </div>
    </div>
  </div>
</template>
