<script setup>
import { computed } from 'vue'
import { categoryMeta, formatVND } from '../utils/formatters'
import { useTheme } from '../composables/useTheme'

const props = defineProps({
  categoryTotals: { type: Array, default: () => [] },
})

const { isDark } = useTheme()

const series = computed(() => props.categoryTotals.map((c) => Number(c.total) || 0))
const labels = computed(() => props.categoryTotals.map((c) => c.category))
const colors = computed(() => props.categoryTotals.map((c) => categoryMeta(c.category, 'expense').hex || '#10b981'))
const total = computed(() => series.value.reduce((s, v) => s + v, 0))

function percentOf(value) {
  return total.value > 0 ? ((Number(value) / total.value) * 100).toFixed(1) : '0.0'
}

const chartOptions = computed(() => {
  const dark = isDark.value
  return {
    chart: {
      type: 'donut',
      toolbar: { show: false },
      fontFamily: 'Inter, sans-serif',
    },
    labels: labels.value,
    colors: colors.value,
    legend: { show: false }, // Use custom legend below
    dataLabels: {
      enabled: false,
    },
    stroke: {
      width: 2,
      colors: [dark ? '#0f172a' : '#ffffff'],
    },
    tooltip: {
      theme: dark ? 'dark' : 'light',
      y: {
        formatter: (v) => `${formatVND(v)} (${percentOf(v)}%)`,
      },
    },
    plotOptions: {
      pie: {
        donut: {
          size: '70%',
        },
      },
    },
  }
})
</script>

<template>
  <div v-if="series.length" class="flex flex-col justify-between h-full">
    <div class="h-52 w-full flex items-center justify-center relative">
      <apexchart type="donut" height="220" :options="chartOptions" :series="series" />
    </div>

    <!-- Custom Legend Grid matching FinFlow HTML -->
    <div class="grid grid-cols-2 gap-2 mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs">
      <div
        v-for="(cat, idx) in props.categoryTotals"
        :key="cat.category"
        class="flex items-center justify-between gap-1 truncate"
      >
        <div class="flex items-center gap-1.5 truncate">
          <span
            class="w-2.5 h-2.5 rounded-full shrink-0"
            :style="{ backgroundColor: colors[idx] }"
          ></span>
          <span class="text-slate-600 dark:text-slate-300 truncate">{{ cat.category }}</span>
        </div>
        <strong class="text-slate-800 dark:text-slate-100 shrink-0">{{ percentOf(cat.total) }}%</strong>
      </div>
    </div>
  </div>

  <div v-else class="text-slate-400 dark:text-slate-500 text-xs text-center py-12">
    <i class="fa-solid fa-chart-pie text-2xl mb-2 block opacity-40"></i>
    Chưa có dữ liệu chi tiêu trong kỳ này
  </div>
</template>
