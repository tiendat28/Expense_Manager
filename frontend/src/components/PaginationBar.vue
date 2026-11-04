<script setup>
const page = defineModel('page', { type: Number, required: true })
defineProps({
  pageCount: { type: Number, required: true },
  compact: { type: Boolean, default: false },
})
</script>

<template>
  <div
    class="flex w-fit items-center bg-white dark:bg-slate-900 rounded-xl border border-slate-200/80 dark:border-slate-800 shadow-xs text-slate-700 dark:text-slate-300"
    :class="compact ? 'gap-1.5 text-[11px] px-2 py-1' : 'gap-3 text-xs px-3.5 py-1.5'"
  >
    <button
      class="rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer"
      :class="compact ? 'px-1.5 leading-5' : 'px-2 py-0.5'"
      :disabled="page === 1"
      aria-label="Trang trước"
      @click="page--"
    >
      <i class="fa-solid fa-chevron-left text-[10px]"></i>
    </button>
    <span class="font-semibold whitespace-nowrap">
      {{ compact ? `${page}/${pageCount}` : `Trang ${page} / ${pageCount}` }}
    </span>
    <button
      class="rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer"
      :class="compact ? 'px-1.5 leading-5' : 'px-2 py-0.5'"
      :disabled="page === pageCount"
      aria-label="Trang sau"
      @click="page++"
    >
      <i class="fa-solid fa-chevron-right text-[10px]"></i>
    </button>
  </div>
</template>
