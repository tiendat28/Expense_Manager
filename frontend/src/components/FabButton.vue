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
  <!-- Nút dấu + ở góc dưới bên phải đã được lược bỏ trên laptop; trên điện thoại sử dụng nút + ở giữa thanh điều hướng dưới -->
</template>
