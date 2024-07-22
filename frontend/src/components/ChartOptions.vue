<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '@/services/api'

const props = defineProps({
  availablePlots: { type: Array, required: true }
})

const emit = defineEmits(['update:options'])

const selectedPlotType = ref('histogram')
const selectedXColumn = ref('')
const selectedYColumn = ref('')
const selectedColorBy = ref([])

const plotVariables = ref({
  x: [],
  y: [],
  color: []
})

const fetchPlotVariables = async () => {
  try {
    const variables = await api.getPlotVariables(selectedPlotType.value)
    plotVariables.value = variables

    if (!plotVariables.value.x.includes(selectedXColumn.value)) {
      selectedXColumn.value = plotVariables.value.x[0] || ''
    }
    if (plotVariables.value?.y && !plotVariables.value.y.includes(selectedYColumn.value)) {
      selectedYColumn.value = plotVariables.value.y[0] || ''
    }
    if (plotVariables.value?.color && !plotVariables.value.color.includes(selectedColorBy.value)) {
      selectedColorBy.value = plotVariables.value.color[0] || []
    }
  } catch (error) {
    console.error('Failed to fetch plot variables:', error)
  }
}

onMounted(fetchPlotVariables)

watch([selectedPlotType, () => props.availablePlots], fetchPlotVariables)

watch([selectedPlotType, selectedXColumn, selectedYColumn, selectedColorBy], () => {
  emit('update:options', {
    plotType: selectedPlotType.value,
    xColumn: selectedXColumn.value,
    yColumn: selectedYColumn.value,
    colorBy: selectedColorBy.value
  })
})
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <div class="mb-2">
      <label for="plot-type" class="block text-sm font-medium text-gray-700 mb-1">Plot Type:</label>
      <select
        id="plot-type"
        v-model="selectedPlotType"
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
      >
        <option v-for="plot in availablePlots" :key="plot" :value="plot">{{ plot }}</option>
      </select>
    </div>
    <div class="mb-2">
      <label for="x-column" class="block text-sm font-medium text-gray-700 mb-1">X Column:</label>
      <select
        id="x-column"
        v-model="selectedXColumn"
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
      >
        <option v-for="column in plotVariables.x" :key="column" :value="column">
          {{ column }}
        </option>
      </select>
    </div>
    <div class="mb-2">
      <label for="y-column" class="block text-sm font-medium text-gray-700 mb-1">Y Column:</label>
      <select
        id="y-column"
        v-model="selectedYColumn"
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
      >
        <option value="">None</option>
        <option v-for="column in plotVariables?.y" :key="column" :value="column">
          {{ column }}
        </option>
      </select>
    </div>
    <div class="mb-2">
      <label for="color-by" class="block text-sm font-medium text-gray-700 mb-1">Color By:</label>
      <select
        id="color-by"
        v-model="selectedColorBy"
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
      >
        <option value="">None</option>
        <option v-for="column in plotVariables.color" :key="column" :value="column">
          {{ column }}
        </option>
      </select>
    </div>
  </div>
</template>
