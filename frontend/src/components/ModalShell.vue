<script setup>
defineProps({ title: { type: String, required: true } })
defineEmits(['close'])
</script>

<template>
  <div class="fixed inset-0 bg-black/30 flex items-center justify-center p-4 z-30" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl w-full sm:max-w-md p-5 space-y-4 max-h-[85vh] overflow-y-auto">
      <h2 class="font-semibold text-lg">{{ title }}</h2>
      <slot />
    </div>
  </div>
</template>
