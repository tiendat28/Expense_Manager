<template>
  <div>
    <div v-if="$slots.sticky" class="sticky top-0 z-10 bg-gray-50 px-4 sm:px-6 pt-4 sm:pt-6 pb-4">
      <slot name="sticky" />
    </div>
    <div :class="['px-4 sm:px-6 pb-24 space-y-4', $slots.sticky ? '' : 'pt-4 sm:pt-6']">
      <slot />
    </div>
  </div>
</template>
