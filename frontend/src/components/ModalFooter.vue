<script setup>
defineProps({
  saveLabel: { type: String, default: 'Lưu' },
  // Để trống thì không hiện nút xóa
  deleteLabel: { type: String, default: '' },
})
defineEmits(['close', 'save', 'remove'])
</script>

<template>
  <div class="flex gap-2 pt-2">
    <button type="button" class="flex-1 py-2 rounded-lg border" @click="$emit('close')">Hủy</button>
    <button type="button" class="flex-1 py-2 rounded-lg bg-green-600 text-white" @click="$emit('save')">
      {{ saveLabel }}
    </button>
  </div>
  <button
    v-if="deleteLabel"
    type="button"
    class="w-full text-red-500 text-sm py-2"
    @click="$emit('remove')"
  >
    {{ deleteLabel }}
  </button>
</template>
