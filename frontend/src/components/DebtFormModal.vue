<script setup>
import { ref } from 'vue'
import { useDebtsStore } from '../stores/debts'
import { useToastStore } from '../stores/toast'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { EXPENSE_CATEGORIES, INCOME_CATEGORIES } from '../utils/formatters'
import { todayISO } from '../utils/date'
import AmountField from './AmountField.vue'
import ModalShell from './ModalShell.vue'
import ModalFooter from './ModalFooter.vue'

const props = defineProps({ existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const store = useDebtsStore()
const toast = useToastStore()
const confirmDelete = useConfirmDelete()

const type = ref(props.existing?.type || 'lent')
const personName = ref(props.existing?.person_name || '')
const category = ref(props.existing?.category || currentCategories()[0].value)
const totalAmount = ref(props.existing?.total_amount ?? '')
const paidAmount = ref(props.existing?.paid_amount ?? 0)
const hasDueDate = ref(!!props.existing?.due_date)
const dueDate = ref(props.existing?.due_date || todayISO())
const note = ref(props.existing?.note || '')

function currentCategories() {
  return type.value === 'owe' ? EXPENSE_CATEGORIES : INCOME_CATEGORIES
}

function switchType(t) {
  type.value = t
  category.value = currentCategories()[0].value
}

async function save() {
  if (!personName.value.trim()) {
    toast.show('Vui lòng nhập họ tên người vay / chủ nợ', 'error')
    return
  }
  if (!totalAmount.value || Number(totalAmount.value) <= 0) {
    toast.show('Vui lòng nhập tổng số tiền nợ', 'error')
    return
  }
  const payload = {
    person_name: personName.value.trim(),
    type: type.value,
    category: category.value,
    total_amount: Number(totalAmount.value),
    paid_amount: Number(paidAmount.value),
    due_date: hasDueDate.value ? dueDate.value : null,
    note: note.value.trim(),
  }
  if (props.existing) {
    await store.update(props.existing.id, payload)
  } else {
    await store.create(payload)
  }
  toast.show('Đã lưu vào sổ nợ thành công!')
  emit('saved')
}

async function remove() {
  const deleted = await confirmDelete(
    `Bạn có chắc chắn muốn xóa khoản nợ với "${props.existing.person_name}"?`,
    () => store.remove(props.existing.id)
  )
  if (deleted) emit('saved')
}
</script>

<template>
  <ModalShell :title="existing ? 'Chỉnh sửa khoản nợ' : 'Ghi sổ khoản nợ mới'" @close="$emit('close')">
    <!-- Type Selector matching FinFlow -->
    <div class="grid grid-cols-2 gap-3 p-1 bg-slate-100 dark:bg-slate-800 rounded-xl">
      <button
        type="button"
        class="py-2.5 rounded-lg font-bold text-xs sm:text-sm transition cursor-pointer"
        :class="type === 'lent' ? 'bg-emerald-500 text-white shadow-xs' : 'text-slate-600 dark:text-slate-300'"
        @click="switchType('lent')"
      >
        Cho vay (Phải thu)
      </button>
      <button
        type="button"
        class="py-2.5 rounded-lg font-bold text-xs sm:text-sm transition cursor-pointer"
        :class="type === 'owe' ? 'bg-rose-500 text-white shadow-xs' : 'text-slate-600 dark:text-slate-300'"
        @click="switchType('owe')"
      >
        Đi vay (Phải trả)
      </button>
    </div>

    <!-- Person name -->
    <div>
      <label class="form-label">Họ tên người vay / Chủ nợ *</label>
      <input
        v-model="personName"
        type="text"
        required
        placeholder="VD: Lê Hoàng Nam, Anh Tuấn..."
        class="form-input"
      />
    </div>

    <!-- Amount Field -->
    <AmountField v-model="totalAmount" placeholder="VD: 10000000" />

    <div v-if="existing">
      <label class="form-label">Số tiền đã trả / đã thu</label>
      <AmountField v-model="paidAmount" placeholder="0" />
    </div>

    <!-- Category & Due Date -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div>
        <label class="form-label">Danh mục</label>
        <select v-model="category" class="form-input">
          <option v-for="c in currentCategories()" :key="c.value" :value="c.value">
            {{ c.value }}
          </option>
        </select>
      </div>

      <div>
        <label class="form-label">Hạn thanh toán</label>
        <input v-model="dueDate" type="date" class="form-input" />
      </div>
    </div>

    <!-- Note -->
    <div>
      <label class="form-label">Lý do / Ghi chú</label>
      <input
        v-model="note"
        type="text"
        placeholder="VD: Mượn xoay vòng vốn, cọc mặt bằng..."
        class="form-input"
      />
    </div>

    <ModalFooter
      :save-label="existing ? 'Cập nhật' : 'Lưu vào sổ nợ'"
      :delete-label="existing ? 'Xóa khoản nợ này' : ''"
      @close="$emit('close')"
      @save="save"
      @remove="remove"
    />
  </ModalShell>
</template>
