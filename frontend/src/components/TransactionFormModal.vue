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
  if (!amount.value || Number(amount.value) <= 0) {
    toast.show('Vui lòng nhập số tiền hợp lệ', 'error')
    return
  }
  const payload = {
    amount: Number(amount.value),
    category: category.value,
    note: note.value.trim(),
    date: date.value,
    type: type.value,
  }
  if (props.existing) {
    await tx.update(props.existing.id, payload)
  } else {
    await tx.create(payload)
  }
  toast.show('Đã lưu giao dịch thành công!')
  emit('saved')
}
</script>

<template>
  <ModalShell :title="existing ? 'Chỉnh sửa giao dịch' : 'Thêm giao dịch mới'" @close="$emit('close')">
    <!-- Type Selector matching FinFlow -->
    <div class="grid grid-cols-2 gap-3 p-1 bg-slate-100 dark:bg-slate-800 rounded-xl">
      <button
        type="button"
        class="py-2.5 rounded-lg font-bold text-xs sm:text-sm transition cursor-pointer"
        :class="type === 'expense' ? 'bg-rose-500 text-white shadow-xs' : 'text-slate-600 dark:text-slate-300'"
        @click="switchType('expense')"
      >
        Khoản Chi (-)
      </button>
      <button
        type="button"
        class="py-2.5 rounded-lg font-bold text-xs sm:text-sm transition cursor-pointer"
        :class="type === 'income' ? 'bg-emerald-500 text-white shadow-xs' : 'text-slate-600 dark:text-slate-300'"
        @click="switchType('income')"
      >
        Khoản Thu (+)
      </button>
    </div>

    <!-- Amount Field -->
    <AmountField v-model="amount" placeholder="VD: 250000" />

    <!-- Description / Note -->
    <div>
      <label class="form-label">Nội dung diễn giải</label>
      <input
        v-model="note"
        type="text"
        placeholder="VD: Ăn tối cùng gia đình, Mua sách, Nhận lương..."
        class="form-input"
      />
    </div>

    <!-- Category & Date Grid -->
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
        <label class="form-label">Ngày giao dịch</label>
        <input v-model="date" type="date" required class="form-input" />
      </div>
    </div>

    <ModalFooter :save-label="existing ? 'Cập nhật' : 'Lưu giao dịch'" @close="$emit('close')" @save="save" />
  </ModalShell>
</template>
