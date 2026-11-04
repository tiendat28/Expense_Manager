<script setup>
import { ref } from 'vue'
import { useGiftMoneyStore } from '../stores/giftMoney'
import { useToastStore } from '../stores/toast'
import { GIFT_MONEY_TYPES } from '../utils/giftMoney'
import { todayISO } from '../utils/date'
import AmountField from './AmountField.vue'
import ModalShell from './ModalShell.vue'
import ModalFooter from './ModalFooter.vue'

const props = defineProps({ existing: { type: Object, default: null } })
const emit = defineEmits(['close', 'saved'])
const store = useGiftMoneyStore()
const toast = useToastStore()

const name = ref(props.existing?.name || '')
const address = ref(props.existing?.address || '')
const amount = ref(props.existing?.amount ?? '')
const type = ref(props.existing?.type || 'wedding')
const date = ref(props.existing?.date || todayISO())
const note = ref(props.existing?.note || '')

async function save() {
  if (!name.value.trim()) {
    toast.show('Vui lòng nhập tên người mừng / khách mời', 'error')
    return
  }
  if (!amount.value || Number(amount.value) <= 0) {
    toast.show('Vui lòng nhập số tiền mừng', 'error')
    return
  }
  const payload = {
    name: name.value.trim(),
    address: address.value.trim(),
    amount: Number(amount.value),
    type: type.value,
    date: date.value,
    note: note.value.trim(),
  }
  if (props.existing) {
    await store.update(props.existing.id, payload)
  } else {
    await store.create(payload)
  }
  toast.show('Đã ghi sổ tiền mừng thành công!')
  emit('saved')
}
</script>

<template>
  <ModalShell :title="existing ? 'Chỉnh sửa tiền mừng' : 'Ghi sổ tiền mừng (Hiếu Hỉ)'" @close="$emit('close')">
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <div>
        <label class="form-label">Tên khách / Bạn bè *</label>
        <input
          v-model="name"
          type="text"
          required
          placeholder="VD: Trần Bích Ngọc, Anh Duy..."
          class="form-input"
        />
      </div>

      <div>
        <label class="form-label">Địa chỉ / Quê quán</label>
        <input
          v-model="address"
          type="text"
          placeholder="VD: Hà Nội, Đồng nghiệp cũ..."
          class="form-input"
        />
      </div>
    </div>

    <AmountField v-model="amount" placeholder="Số tiền mừng" />

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <div>
        <label class="form-label">Dịp sự kiện</label>
        <select v-model="type" class="form-input">
          <option v-for="t in GIFT_MONEY_TYPES" :key="t.value" :value="t.value">
            {{ t.label }}
          </option>
        </select>
      </div>

      <div>
        <label class="form-label">Ngày sự kiện</label>
        <input v-model="date" type="date" required class="form-input" />
      </div>
    </div>

    <div>
      <label class="form-label">Ghi chú đối chiếu</label>
      <textarea
        v-model="note"
        placeholder="Ghi chú thêm (VD: Trước đây từng mừng 1.000.000 ₫)..."
        rows="2"
        class="form-input"
      ></textarea>
    </div>

    <ModalFooter :save-label="existing ? 'Cập nhật' : 'Lưu vào sổ Hiếu Hỉ'" @close="$emit('close')" @save="save" />
  </ModalShell>
</template>
