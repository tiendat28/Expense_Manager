<script setup>
import { computed } from 'vue'
import { formatVND } from '../utils/formatters'
import { useTheme } from '../composables/useTheme'

const props = defineProps({
  trend: { type: Array, default: () => [] },
  selectedYear: Number,
  selectedMonth: Number,
})
const emit = defineEmits(['select'])
const { isDark } = useTheme()

const series = computed(() => [{ name: 'Tổng chi tiêu', data: props.trend.map((t) => Number(t.total) || 0) }])
const categories = computed(() => props.trend.map((t) => `Tháng ${t.month}`))

const barColors = computed(() => {
  const dark = isDark.value
  const list = props.trend.map((item) => {
    if (item && item.year === props.selectedYear && item.month === props.selectedMonth) {
      return '#10b981' // Brand emerald-500 for selected month
    }
    return dark ? '#475569' : '#94a3b8' // Visible slate for other months on white/dark bg
  })
  return list.length ? list : ['#10b981']
})

const chartOptions = computed(() => {
  const dark = isDark.value
  const textColor = dark ? '#94a3b8' : '#475569'
  const gridColor = dark ? 'rgba(51, 65, 85, 0.45)' : 'rgba(203, 213, 225, 0.8)'

  return {
    chart: {
      type: 'bar',
      toolbar: { show: false },
      fontFamily: 'Inter, sans-serif',
      events: {
        dataPointSelection: (event, chartContext, config) => {
          const item = props.trend[config.dataPointIndex]
          if (item) emit('select', item)
        },
      },
    },
    colors: barColors.value,
    plotOptions: {
      bar: {
        borderRadius: 6,
        columnWidth: '45%',
        distributed: true,
      },
    },
    dataLabels: { enabled: false },
    legend: { show: false },
    grid: {
      borderColor: gridColor,
      strokeDashArray: 4,
      yaxis: { lines: { show: true } },
      xaxis: { lines: { show: false } },
    },
    xaxis: {
      categories: categories.value,
      labels: {
        style: { colors: textColor, fontSize: '11px', fontWeight: 600 },
      },
      axisBorder: { show: false },
      axisTicks: { show: false },
    },
    yaxis: {
      labels: {
        style: { colors: textColor, fontSize: '11px', fontWeight: 500 },
        formatter: (val) => {
          if (!val) return '0'
          if (val >= 1000000) {
            const tr = val / 1000000
            return `${Number.isInteger(tr) ? tr : tr.toFixed(1)}tr`
          }
          return `${Math.round(val / 1000)}k`
        },
      },
    },
    tooltip: {
      theme: dark ? 'dark' : 'light',
      y: {
        formatter: (val) => formatVND(val),
      },
    },
  }
})
</script>

<template>
  <apexchart type="bar" height="240" :options="chartOptions" :series="series" />
</template>
