<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useFabStore } from '../stores/fab'

const emit = defineEmits(['click'])
const fab = useFabStore()
const handler = () => emit('click')

onMounted(() => fab.register(handler))
onUnmounted(() => fab.unregister(handler))
</script>

<template>
  <button
    @click="$emit('click')"
    class="glass-fab hidden sm:flex items-center justify-center fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-green-500 to-green-700 text-white text-2xl hover:brightness-110"
  >+</button>
</template>
