<script setup>
import { useTheme } from '../composables/useTheme'

defineProps({
  title: { type: String, required: true },
  error: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  submitLabel: { type: String, required: true },
  loadingLabel: { type: String, required: true },
  footerText: { type: String, required: true },
  footerLinkText: { type: String, required: true },
  footerLinkTo: { type: String, required: true },
})
defineEmits(['submit'])

const { isDark, toggleTheme } = useTheme()
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-slate-100/80 dark:bg-slate-950 px-4 transition-colors relative">
    <!-- Theme Toggle in top right -->
    <button
      type="button"
      @click="toggleTheme"
      class="absolute top-5 right-5 w-10 h-10 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-amber-400 flex items-center justify-center shadow-xs cursor-pointer"
      :title="isDark ? 'Chế độ Sáng' : 'Chế độ Tối'"
    >
      <i :class="isDark ? 'fa-solid fa-sun' : 'fa-solid fa-moon'"></i>
    </button>

    <div class="w-full max-w-md space-y-6">
      <!-- Brand Logo -->
      <div class="text-center space-y-2">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-emerald-600 via-emerald-500 to-green-500 mx-auto flex items-center justify-center text-white text-xl shadow-lg shadow-emerald-500/30">
          <i class="fa-solid fa-chart-pie"></i>
        </div>
        <h1 class="font-display font-extrabold text-2xl tracking-tight bg-gradient-to-r from-emerald-600 to-green-500 bg-clip-text text-transparent">
          FiveDream
        </h1>
        <p class="text-xs text-slate-400">Quản trị tài chính & chi tiêu cá nhân thông minh</p>
      </div>

      <!-- Auth Form Card -->
      <form @submit.prevent="$emit('submit')" class="card-surface p-8 space-y-4">
        <h2 class="font-display font-bold text-lg text-slate-900 dark:text-white text-center">{{ title }}</h2>

        <slot />

        <p v-if="error" class="text-rose-500 text-xs font-semibold">{{ error }}</p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-700 hover:to-green-600 text-white font-semibold text-sm shadow-md shadow-emerald-500/20 transition disabled:opacity-50 cursor-pointer"
        >
          {{ loading ? loadingLabel : submitLabel }}
        </button>

        <p class="text-center text-xs text-slate-500 dark:text-slate-400 pt-2">
          {{ footerText }}
          <router-link :to="footerLinkTo" class="text-emerald-600 dark:text-emerald-400 font-semibold hover:underline">
            {{ footerLinkText }}
          </router-link>
        </p>
      </form>
    </div>
  </div>
</template>
