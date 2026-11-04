<script setup>
import { useToastStore } from '../stores/toast'

const toast = useToastStore()
</script>

<template>
  <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-2.5 max-w-sm w-full pointer-events-none px-4 sm:px-0">
    <TransitionGroup name="toast">
      <div
        v-for="t in toast.items"
        :key="t.id"
        class="pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-2xl border shadow-xl text-xs sm:text-sm font-medium transition-all duration-300"
        :class="
          t.type === 'error'
            ? 'bg-slate-900 dark:bg-rose-950 text-white border-rose-500/40'
            : t.type === 'info'
              ? 'bg-slate-900 dark:bg-indigo-950 text-white border-indigo-500/40'
              : 'bg-slate-900 dark:bg-emerald-950 text-white border-emerald-500/40'
        "
      >
        <i
          :class="
            t.type === 'error'
              ? 'fa-solid fa-circle-exclamation text-rose-400 text-base'
              : t.type === 'info'
                ? 'fa-solid fa-circle-info text-indigo-400 text-base'
                : 'fa-solid fa-circle-check text-emerald-400 text-base'
          "
        ></i>
        <span class="flex-1">{{ t.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(12px);
}
</style>
