<script setup>
defineProps({ text: { type: String, required: true } })
</script>

<template>
  <h1 class="text-xl sm:text-2xl font-bold text-green-800">{{ text }}</h1>
</template>
