<script setup>
defineEmits(['edit', 'remove'])
</script>

<template>
  <div class="flex items-center gap-0.5">
    <button
      type="button"
      title="Chỉnh sửa"
      aria-label="Chỉnh sửa"
      class="p-1.5 rounded-lg text-green-600 hover:bg-green-50"
      @click.stop="$emit('edit')"
    >
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931z" />
        <path d="M16.862 4.487L19.5 7.125" />
      </svg>
    </button>
    <button
      type="button"
      title="Xóa"
      aria-label="Xóa"
      class="p-1.5 rounded-lg text-red-500 hover:bg-red-50"
      @click.stop="$emit('remove')"
    >
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4.5 6.5h15M9.5 6.5V5a1.5 1.5 0 011.5-1.5h2A1.5 1.5 0 0114.5 5v1.5M6.5 6.5l.73 12.1A2 2 0 009.23 20.5h5.54a2 2 0 002-1.9l.73-12.1" />
        <path d="M10 10.5v6M14 10.5v6" />
      </svg>
    </button>
  </div>
</template>
