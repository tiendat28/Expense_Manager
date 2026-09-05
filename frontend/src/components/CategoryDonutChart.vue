<script setup>
import { computed } from 'vue'
import { categoryMeta, formatVND } from '../utils/formatters'

const props = defineProps({
  categoryTotals: { type: Array, default: () => [] },
})

const series = computed(() => props.categoryTotals.map((c) => c.total))
const labels = computed(() => props.categoryTotals.map((c) => c.category))
const colors = computed(() => props.categoryTotals.map((c) => categoryMeta(c.category, 'expense').color))
const total = computed(() => series.value.reduce((s, v) => s + v, 0))

function percentOf(value) {
  return total.value > 0 ? ((value / total.value) * 100).toFixed(1) : '0.0'
}

const chartOptions = computed(() => ({
  chart: { toolbar: { show: false } },
  labels: labels.value,
  colors: colors.value,
  legend: {
    position: 'bottom',
    fontSize: '12px',
    formatter: (label, opts) => `${label} — ${percentOf(opts.w.globals.series[opts.seriesIndex])}%`,
  },
  dataLabels: {
    enabled: true,
    formatter: (val) => `${val.toFixed(1)}%`,
    style: { fontSize: '11px', fontWeight: 600 },
    dropShadow: { enabled: false },
  },
  stroke: { width: 2 },
  tooltip: { y: { formatter: (v) => `${formatVND(v)} (${percentOf(v)}%)` } },
  plotOptions: { pie: { donut: { size: '65%' } } },
}))
</script>

<template>
  <apexchart v-if="series.length" type="donut" height="280" :options="chartOptions" :series="series" />
  <p v-else class="text-gray-900 text-sm text-center py-10">Chưa có dữ liệu chi tiêu để hiển thị</p>
</template>
