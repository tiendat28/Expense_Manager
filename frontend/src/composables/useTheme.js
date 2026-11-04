import { ref, watchEffect } from 'vue'

const isDark = ref(false)

// Khởi tạo từ localStorage hoặc system preference
if (typeof window !== 'undefined') {
  const saved = localStorage.getItem('finflow_theme')
  if (saved) {
    isDark.value = saved === 'dark'
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDark.value = true
  }

  watchEffect(() => {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
      document.documentElement.classList.remove('light')
      localStorage.setItem('finflow_theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      document.documentElement.classList.add('light')
      localStorage.setItem('finflow_theme', 'light')
    }
  })
}

export function useTheme() {
  function toggleTheme() {
    isDark.value = !isDark.value
  }

  return {
    isDark,
    toggleTheme,
  }
}

