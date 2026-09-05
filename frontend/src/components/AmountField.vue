<script setup>
defineProps({ modelValue: [String, Number], placeholder: { type: String, default: '0' } })
defineEmits(['update:modelValue'])
</script>

<template>
  <input
    type="number"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    :placeholder="placeholder"
    class="w-full text-2xl font-semibold border-b border-gray-200 focus:border-green-500 outline-none py-2"
  />
</template>
