<template>
  <div class="flex flex-col min-h-full">
    <div v-if="$slots.sticky" class="sticky top-0 z-10 bg-gray-50 px-4 sm:px-6 pt-4 sm:pt-6 pb-3">
      <slot name="sticky" />
    </div>
    <div :class="['px-4 sm:px-6 space-y-4', $slots.sticky ? '' : 'pt-4 sm:pt-6', $slots.bottom ? 'pb-2' : 'pb-24']">
      <slot />
    </div>
    <!-- Chỉ dùng trên desktop: mobile đã có thanh điều hướng dưới cùng nên không ghim thêm gì ở đáy -->
    <div v-if="$slots.bottom" class="hidden sm:block sticky bottom-0 z-10 mt-auto bg-gray-50 px-6 pt-2 pb-6">
      <slot name="bottom" />
    </div>
  </div>
</template>
