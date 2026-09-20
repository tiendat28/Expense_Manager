<script setup>
defineProps({
  text: { type: String, required: true },
  // Trang có bảng/thẻ thì bọc trong khung trắng cho khớp, trang danh sách trơn thì không
  boxed: { type: Boolean, default: false },
})
</script>

<template>
  <p
    class="text-center text-gray-900 text-sm"
    :class="boxed ? 'bg-white rounded-2xl card-shadow py-6' : 'py-10'"
  >
    {{ text }}
  </p>
</template>
