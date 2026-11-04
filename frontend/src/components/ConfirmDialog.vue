<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useConfirmStore } from '../stores/confirm'

const confirm = useConfirmStore()

function onKeydown(e) {
  if (confirm.open && e.key === 'Escape') confirm.settle(false)
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <div
    v-if="confirm.open"
    class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 animate-fade-in"
    @click.self="confirm.settle(false)"
  >
    <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 w-full sm:max-w-md p-6 shadow-2xl space-y-4">
      <div class="flex items-start gap-3.5">
        <div class="w-11 h-11 rounded-xl bg-rose-50 dark:bg-rose-950/80 text-rose-500 flex items-center justify-center text-lg shrink-0">
          <i class="fa-solid fa-triangle-exclamation"></i>
        </div>
        <div class="min-w-0">
          <h2 class="font-display font-bold text-base text-slate-900 dark:text-white">{{ confirm.title }}</h2>
          <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1 break-words leading-relaxed">{{ confirm.message }}</p>
        </div>
      </div>

      <div class="flex items-center justify-end gap-2.5 pt-3 border-t border-slate-100 dark:border-slate-800">
        <button
          @click="confirm.settle(false)"
          class="px-4 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs sm:text-sm font-semibold transition cursor-pointer"
        >
          {{ confirm.cancelText }}
        </button>
        <button
          @click="confirm.settle(true)"
          class="px-5 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white text-xs sm:text-sm font-semibold shadow-md shadow-rose-600/20 transition cursor-pointer"
        >
          {{ confirm.confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>
