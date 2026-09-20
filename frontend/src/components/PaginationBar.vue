<script setup>
const page = defineModel('page', { type: Number, required: true })
defineProps({
  pageCount: { type: Number, required: true },
  // Bản gọn để đặt cạnh tiêu đề trên mobile
  compact: { type: Boolean, default: false },
})
</script>

<template>
  <div
    class="flex w-fit items-center bg-white rounded-2xl card-shadow"
    :class="compact ? 'gap-1.5 text-[11px] px-1.5 py-1' : 'gap-4 text-xs px-4 py-2'"
  >
    <button
      class="rounded-lg border disabled:opacity-40"
      :class="compact ? 'px-1.5 leading-5' : 'px-2.5 py-1'"
      :disabled="page === 1"
      aria-label="Trang trước"
      @click="page--"
    >
      ‹
    </button>
    <span class="text-gray-900 whitespace-nowrap">{{ compact ? `${page}/${pageCount}` : `Trang ${page} / ${pageCount}` }}</span>
    <button
      class="rounded-lg border disabled:opacity-40"
      :class="compact ? 'px-1.5 leading-5' : 'px-2.5 py-1'"
      :disabled="page === pageCount"
      aria-label="Trang sau"
      @click="page++"
    >
      ›
    </button>
  </div>
</template>
