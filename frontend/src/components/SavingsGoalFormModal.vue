<script setup>
import { ref } from 'vue'
import { useSavingsStore } from '../stores/savings'
import { useToastStore } from '../stores/toast'
import AmountField from './AmountField.vue'
import ModalShell from './ModalShell.vue'
import ModalFooter from './ModalFooter.vue'

const props = defineProps({ existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const store = useSavingsStore()
const toast = useToastStore()

const icons = ['🎯', '🛡️', '💻', '✈️', '🏠', '🚗', '💍', '🎓', '🏥', '🏖️']
const name = ref(props.existing?.name || '')
const targetAmount = ref(props.existing?.target_amount ?? '')
const icon = ref(props.existing?.icon || '🎯')

async function save() {
  if (!name.value.trim()) {
    toast.show('Vui lòng nhập tên mục tiêu', 'error')
    return
  }
  if (!targetAmount.value || Number(targetAmount.value) <= 0) {
    toast.show('Vui lòng nhập số tiền mục tiêu', 'error')
    return
  }
  const payload = { name: name.value.trim(), icon: icon.value, target_amount: Number(targetAmount.value) }
  if (props.existing) {
    await store.update(props.existing.id, payload)
  } else {
    await store.create(payload)
  }
  toast.show('Đã lưu mục tiêu tích lũy thành công!')
  emit('saved')
}
</script>

<template>
  <ModalShell :title="existing ? 'Chỉnh sửa mục tiêu' : 'Tạo mục tiêu tích lũy mới'" @close="$emit('close')">
    <div>
      <label class="form-label">Tên mục tiêu tích lũy *</label>
      <input
        v-model="name"
        type="text"
        required
        placeholder="VD: Quỹ dự phòng 6 tháng, Mua xe mới, Du lịch Nhật Bản..."
        class="form-input"
      />
    </div>

    <AmountField v-model="targetAmount" placeholder="Hạn mức mục tiêu cần đạt" />

    <div>
      <label class="form-label">Biểu tượng nhận diện</label>
      <div class="flex gap-2 flex-wrap p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800">
        <button
          v-for="opt in icons"
          :key="opt"
          type="button"
          @click="icon = opt"
          class="text-xl w-10 h-10 rounded-xl flex items-center justify-center transition cursor-pointer"
          :class="icon === opt ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30' : 'hover:bg-slate-200 dark:hover:bg-slate-700'"
        >
          {{ opt }}
        </button>
      </div>
    </div>

    <ModalFooter :save-label="existing ? 'Cập nhật' : 'Tạo mục tiêu'" @close="$emit('close')" @save="save" />
  </ModalShell>
</template>
