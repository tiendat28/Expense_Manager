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
    class="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-40"
    @click.self="confirm.settle(false)"
  >
    <div class="bg-white rounded-2xl w-full sm:max-w-sm p-5 space-y-4">
      <div class="flex items-start gap-3">
        <span class="w-10 h-10 rounded-full bg-red-50 text-red-500 flex items-center justify-center text-lg shrink-0">🗑</span>
        <div class="min-w-0">
          <h2 class="font-semibold text-lg">{{ confirm.title }}</h2>
          <p class="text-sm text-gray-900 mt-1 break-words">{{ confirm.message }}</p>
        </div>
      </div>
      <div class="flex gap-2 pt-1">
        <button @click="confirm.settle(false)" class="flex-1 py-2 rounded-lg border">{{ confirm.cancelText }}</button>
        <button @click="confirm.settle(true)" class="flex-1 py-2 rounded-lg bg-red-500 text-white">{{ confirm.confirmText }}</button>
      </div>
    </div>
  </div>
</template>
