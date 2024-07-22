<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import Plotly from 'plotly.js-dist'
import api from '@/services/api'

const props = defineProps({
  plotType: { type: String, required: true },
  xColumn: { type: String, required: true },
  yColumn: { type: String, default: '' },
  colorBy: { type: String, default: '' },
  filters: { type: Object, default: () => ({}) }
})

const chartDiv = ref(null)
const data = ref(null)
const layout = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchChartData = async () => {
  if (!props.xColumn) return
  try {
    loading.value = true
    error.value = null
    const response = await api.generatePlot(
      props.plotType,
      props.xColumn,
      props.yColumn,
      props.colorBy,
      props.filters
    )
    data.value = response?.data?.data
    layout.value = response?.data?.layout
  } catch (err) {
    error.value = 'Failed to fetch chart data'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchChartData()
  if (chartDiv.value && data.value && layout.value) {
    Plotly.newPlot(chartDiv.value, data.value, layout.value)
  }
})

onUnmounted(() => {
  if (chartDiv.value) {
    Plotly.purge(chartDiv.value)
  }
})

watch(
  [
    () => props.plotType,
    () => props.xColumn,
    () => props.yColumn,
    () => props.colorBy,
    () => props.filters
  ],
  async () => {
    await fetchChartData()
    if (chartDiv.value && data.value && layout.value) {
      Plotly.react(chartDiv.value, data.value, layout.value)
    }
  },
  { deep: true }
)
</script>

<template>
  <div class="mt-8">
    <div v-if="loading" class="text-center text-gray-600">Loading...</div>
    <div v-else-if="error" class="text-center text-red-600">{{ error }}</div>
    <div v-else ref="chartDiv" class="w-full h-96"></div>
  </div>
</template>
