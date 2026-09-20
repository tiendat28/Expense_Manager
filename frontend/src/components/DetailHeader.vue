<script setup>
import { useRouter } from 'vue-router'

defineEmits(['edit', 'remove'])
const router = useRouter()
</script>

<template>
  <div class="flex items-center justify-between mb-3">
    <button type="button" class="text-gray-900" @click="router.back()">‹ Quay lại</button>
    <div class="flex gap-3 text-sm">
      <button type="button" class="text-green-600" @click="$emit('edit')">Sửa</button>
      <button type="button" class="text-red-500" @click="$emit('remove')">Xóa</button>
    </div>
  </div>
</template>
