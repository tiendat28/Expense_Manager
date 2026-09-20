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
  const payload = {
    name: name.value,
    address: address.value,
    amount: Number(amount.value),
    type: type.value,
    date: date.value,
    note: note.value,
  }
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
  <ModalShell :title="existing ? 'Sửa tiền mừng' : 'Thêm tiền mừng'" @close="$emit('close')">
      <input v-model="name" type="text" placeholder="Họ và tên" class="w-full border rounded-lg px-3 py-2" />
      <input v-model="address" type="text" placeholder="Xã/Tỉnh" class="w-full border rounded-lg px-3 py-2" />
      <AmountField v-model="amount" />
      <select v-model="type" class="w-full border rounded-lg px-3 py-2">
        <option v-for="t in GIFT_MONEY_TYPES" :key="t.value" :value="t.value">{{ t.label }}</option>
      </select>
      <input v-model="date" type="date" class="w-full border rounded-lg px-3 py-2" />
      <textarea v-model="note" placeholder="Note" rows="2" class="w-full border rounded-lg px-3 py-2"></textarea>
      <ModalFooter @close="$emit('close')" @save="save" />
  </ModalShell>
</template>
