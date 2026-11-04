<script setup>
defineProps({
  saveLabel: { type: String, default: 'Lưu thay đổi' },
  deleteLabel: { type: String, default: '' },
})
defineEmits(['close', 'save', 'remove'])
</script>

<template>
  <div class="pt-4 border-t border-slate-100 dark:border-slate-800 space-y-2">
    <div class="flex items-center justify-end gap-2.5">
      <button
        type="button"
        class="px-4 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs sm:text-sm font-semibold transition cursor-pointer"
        @click="$emit('close')"
      >
        Hủy
      </button>
      <button
        type="button"
        class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-700 hover:to-green-600 text-white text-xs sm:text-sm font-semibold shadow-md shadow-emerald-500/20 transition cursor-pointer"
        @click="$emit('save')"
      >
        {{ saveLabel }}
      </button>
    </div>

    <button
      v-if="deleteLabel"
      type="button"
      class="w-full text-center text-xs text-rose-500 hover:text-rose-600 hover:underline pt-1 transition cursor-pointer"
      @click="$emit('remove')"
    >
      <i class="fa-regular fa-trash-can mr-1"></i> {{ deleteLabel }}
    </button>
  </div>
</template>
