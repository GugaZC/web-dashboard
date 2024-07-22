<script setup>
import { ref, onMounted, watch } from 'vue'
import Chart from '@/components/Chart.vue'
import ChartOptions from '@/components/ChartOptions.vue'
import FilterOptions from '@/components/FilterOptions.vue'
import FileUpload from '@/components/FileUpload.vue'
import api from '@/services/api'

const availablePlots = ref([])
const discreteVariables = ref([])
const numericVariables = ref([])
const columnRanges = ref({})
const chartOptions = ref({
  plotType: 'histogram',
  xColumn: '',
  yColumn: '',
  colorBy: ''
})
const filters = ref({})

const loadOptionsData = async () => {
  availablePlots.value = await api.getAvailablePlots()
  discreteVariables.value = await api.getDiscreteVariables()
  numericVariables.value = await api.getNumericVariables()
  columnRanges.value = await api.getColumnRanges()
}

onMounted(async () => {
  try {
    await loadOptionsData()
  } catch (error) {
    console.error('Failed to fetch initial data:', error)
  }
})

const handleUploadSuccess = async () => {
  updateChartOptions({ plotType: 'histogram', xColumn: '', yColumn: '', colorBy: '' })
  await loadOptionsData()
  filters.value = {}
}

const handleUploadError = () => {}

const updateChartOptions = (newOptions) => {
  chartOptions.value = { ...newOptions }
}

const updateFilters = (newFilters) => {
  filters.value = { ...newFilters }
}

watch([chartOptions, filters], () => {}, { deep: true })
</script>

<template>
  <div class="container mx-auto px-4 py-4">
    <FileUpload @upload-success="handleUploadSuccess" @upload-error="handleUploadError" />
    <ChartOptions :availablePlots="availablePlots" @update:options="updateChartOptions" />
    <FilterOptions
      :numericVariables="numericVariables"
      :discreteVariables="discreteVariables"
      :columnRanges="columnRanges"
      @update:filters="updateFilters"
    />
    <Chart
      class="w-full"
      :plotType="chartOptions.plotType"
      :xColumn="chartOptions.xColumn"
      :yColumn="chartOptions.yColumn"
      :colorBy="chartOptions.colorBy"
      :filters="filters"
    />
  </div>
</template>
