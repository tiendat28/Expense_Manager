<script setup>
defineEmits(['edit', 'remove'])
</script>

<template>
  <div class="flex items-center gap-1">
    <button
      type="button"
      title="Chỉnh sửa"
      aria-label="Chỉnh sửa"
      class="p-1.5 rounded-lg text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 transition cursor-pointer"
      @click.stop="$emit('edit')"
    >
      <i class="fa-regular fa-pen-to-square text-xs"></i>
    </button>
    <button
      type="button"
      title="Xóa"
      aria-label="Xóa"
      class="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/60 transition cursor-pointer"
      @click.stop="$emit('remove')"
    >
      <i class="fa-regular fa-trash-can text-xs"></i>
    </button>
  </div>
</template>
