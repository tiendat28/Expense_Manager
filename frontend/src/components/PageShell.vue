<template>
  <div class="space-y-6">
    <div class="space-y-6">
      <slot />
    </div>
    <div v-if="$slots.bottom" class="pt-4">
      <slot name="bottom" />
    </div>
  </div>
</template>
