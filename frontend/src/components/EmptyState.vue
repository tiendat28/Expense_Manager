<script setup>
defineProps({
  text: { type: String, required: true },
  boxed: { type: Boolean, default: false },
})
</script>

<template>
  <div
    class="text-center text-slate-400 dark:text-slate-500 text-xs sm:text-sm py-8 px-4"
    :class="boxed ? 'bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow' : ''"
  >
    <i class="fa-regular fa-folder-open text-2xl mb-2 block text-slate-300 dark:text-slate-600"></i>
    <p>{{ text }}</p>
  </div>
</template>
