<script setup>
import { computed } from 'vue'

const props = defineProps({
  trend: { type: Array, default: () => [] },
  selectedYear: Number,
  selectedMonth: Number,
})
const emit = defineEmits(['select'])

const series = computed(() => [{ name: 'Chi tiêu', data: props.trend.map((t) => t.total) }])
const categories = computed(() => props.trend.map((t) => `${t.month}/${String(t.year).slice(2)}`))
const barColors = computed(() =>
  props.trend.map((t) => (t.year === props.selectedYear && t.month === props.selectedMonth ? '#16a34a' : '#bbf7d0'))
)

const chartOptions = computed(() => ({
  chart: {
    toolbar: { show: false },
    events: {
      dataPointSelection: (event, chartContext, config) => {
        const item = props.trend[config.dataPointIndex]
        if (item) emit('select', item)
      },
    },
  },
  xaxis: { categories: categories.value, labels: { style: { fontSize: '11px' } } },
  dataLabels: { enabled: false },
  plotOptions: {
    bar: {
      borderRadius: 4,
      columnWidth: '50%',
      distributed: true,
    },
  },
  colors: barColors.value,
  legend: { show: false },
  grid: { show: false },
}))
</script>

<template>
  <apexchart type="bar" height="160" :options="chartOptions" :series="series" />
</template>
