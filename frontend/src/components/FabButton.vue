<script setup>
defineEmits(['click'])
</script>

<template>
  <button
    @click="$emit('click')"
    class="glass-fab fixed bottom-20 sm:bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-green-500 to-green-700 text-white text-2xl hover:brightness-110"
  >+</button>
</template>
