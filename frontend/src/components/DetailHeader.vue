<script setup>
import { useRouter } from 'vue-router'

defineEmits(['edit', 'remove'])
const router = useRouter()
</script>

<template>
  <div class="flex items-center justify-between mb-4">
    <button
      type="button"
      class="text-xs sm:text-sm font-semibold text-slate-600 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400 flex items-center gap-1.5 transition cursor-pointer"
      @click="router.back()"
    >
      <i class="fa-solid fa-arrow-left text-xs"></i>
      <span>Quay lại</span>
    </button>
    <div class="flex items-center gap-2">
      <button
        type="button"
        class="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-950/80 transition cursor-pointer"
        @click="$emit('edit')"
      >
        <i class="fa-regular fa-pen-to-square mr-1"></i> Sửa
      </button>
      <button
        type="button"
        class="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-semibold text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/80 transition cursor-pointer"
        @click="$emit('remove')"
      >
        <i class="fa-regular fa-trash-can mr-1"></i> Xóa
      </button>
    </div>
  </div>
</template>
