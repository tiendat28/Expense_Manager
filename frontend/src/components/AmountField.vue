<script setup>
defineProps({ modelValue: [String, Number], placeholder: { type: String, default: '0' } })
defineEmits(['update:modelValue'])
</script>

<template>
  <div class="relative">
    <label class="form-label">Số tiền (VNĐ) *</label>
    <div class="relative">
      <input
        type="number"
        min="0"
        step="1000"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :placeholder="placeholder"
        class="w-full px-4 py-3 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white font-display font-bold text-xl sm:text-2xl focus:outline-none focus:border-emerald-500 transition"
      />
      <span class="absolute right-4 top-1/2 -translate-y-1/2 text-sm font-bold text-slate-400">₫</span>
    </div>
  </div>
</template>
