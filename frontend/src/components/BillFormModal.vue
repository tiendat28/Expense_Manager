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
  if (!name.value.trim()) {
    toast.show('Vui lòng nhập tên hóa đơn', 'error')
    return
  }
  if (!amount.value || Number(amount.value) <= 0) {
    toast.show('Vui lòng nhập số tiền', 'error')
    return
  }
  const payload = {
    name: name.value.trim(),
    amount: Number(amount.value),
    category: category.value,
    due_day: Number(dueDay.value),
  }
  if (props.existing) {
    await store.update(props.existing.id, payload)
  } else {
    await store.create(payload)
  }
  toast.show('Đã lưu hóa đơn thành công!')
  emit('saved')
}

async function remove() {
  const deleted = await confirmDelete(
    `Bạn có chắc chắn muốn xóa hóa đơn "${props.existing.name}"?`,
    () => store.remove(props.existing.id)
  )
  if (deleted) emit('saved')
}
</script>

<template>
  <ModalShell :title="existing ? 'Chỉnh sửa hóa đơn' : 'Thêm hóa đơn định kỳ'" @close="$emit('close')">
    <div>
      <label class="form-label">Tên hóa đơn *</label>
      <input
        v-model="name"
        type="text"
        required
        placeholder="VD: Điện sinh hoạt EVN, Internet Viettel, Tiền nhà..."
        class="form-input"
      />
    </div>

    <AmountField v-model="amount" placeholder="VD: 1500000" />

    <div>
      <label class="form-label">Danh mục</label>
      <select v-model="category" class="form-input">
        <option v-for="c in EXPENSE_CATEGORIES" :key="c.value" :value="c.value">
          {{ c.value }}
        </option>
      </select>
    </div>

    <div class="space-y-1.5 p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800">
      <div class="flex justify-between text-xs font-semibold text-slate-700 dark:text-slate-300">
        <span>Ngày nhắc hẹn hàng tháng</span>
        <span class="text-emerald-600 dark:text-emerald-400 font-bold">Ngày {{ dueDay }}</span>
      </div>
      <input
        v-model="dueDay"
        type="range"
        min="1"
        max="28"
        class="w-full accent-emerald-600 cursor-pointer"
      />
      <p class="text-[11px] text-slate-400">Được nhắc hẹn trước ngày {{ dueDay }} hàng tháng</p>
    </div>

    <ModalFooter
      :save-label="existing ? 'Cập nhật' : 'Lưu hóa đơn'"
      :delete-label="existing ? 'Xóa hóa đơn này' : ''"
      @close="$emit('close')"
      @save="save"
      @remove="remove"
    />
  </ModalShell>
</template>
