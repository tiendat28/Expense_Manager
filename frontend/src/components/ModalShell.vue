<script setup>
defineProps({ title: { type: String, required: true } })
defineEmits(['close'])
</script>

<template>
  <div
    class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs z-50 flex items-center justify-center p-4 transition-all"
    @click.self="$emit('close')"
  >
    <div class="bg-white dark:bg-slate-900 w-full max-w-lg rounded-2xl border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden animate-fade-in text-slate-800 dark:text-slate-100 max-h-[90vh] flex flex-col">
      <!-- Modal Header -->
      <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between shrink-0">
        <h3 class="font-display font-bold text-base text-slate-900 dark:text-white">{{ title }}</h3>
        <button
          type="button"
          @click="$emit('close')"
          class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1 rounded-lg transition"
          aria-label="Đóng"
        >
          <i class="fa-solid fa-xmark text-base"></i>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 space-y-4 overflow-y-auto flex-1">
        <slot />
      </div>
    </div>
  </div>
</template>
