<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'

const props = defineProps({
  numericVariables: { type: Array, required: true },
  discreteVariables: { type: Array, required: true },
  columnRanges: { type: Object, required: true }
})

const emit = defineEmits(['update:filters'])

const numericFilters = reactive({})
const discreteFilters = ref({})

onMounted(() => {
  initializeFilters()
})

const initializeFilters = () => {
  props.numericVariables.forEach((column) => {
    if (props.columnRanges[column]) {
      numericFilters[column] = [props.columnRanges[column][0], props.columnRanges[column][1]]
    }
  })

  const newDiscreteFilters = {}
  props.discreteVariables.forEach((column) => {
    newDiscreteFilters[column] = []
  })
  discreteFilters.value = newDiscreteFilters
}

watch(
  [() => props.numericVariables, () => props.discreteVariables, () => props.columnRanges],
  initializeFilters
)

watch(
  [numericFilters, discreteFilters],
  () => {
    const filters = {}

    Object.entries(numericFilters).forEach(([column, [min, max]]) => {
      if (min !== props.columnRanges[column]?.min || max !== props.columnRanges[column]?.max) {
        filters[column] = [min, max]
      }
    })

    Object.entries(discreteFilters.value).forEach(([column, values]) => {
      if (values.length > 0) {
        filters[column] = values
      }
    })

    emit('update:filters', filters)
  },
  { deep: true }
)

const updateNumericFilter = (column, value) => {
  numericFilters[column] = value
}

const updateDiscreteFilter = (column, value) => {
  if (!discreteFilters.value[column]) {
    discreteFilters.value[column] = []
  }
  const index = discreteFilters.value[column].indexOf(value)
  if (index === -1) {
    discreteFilters.value[column].push(value)
  } else {
    discreteFilters.value[column].splice(index, 1)
  }
}

const isDiscreteValueSelected = (column, value) => {
  return discreteFilters.value[column]?.includes(value) || false
}

const resetDiscreteFilter = (column) => {
  discreteFilters.value[column] = []
}

const resetNumeric = (column) => {
  numericFilters[column] = [props.columnRanges[column][0], props.columnRanges[column][1]]
}

const calculateStep = (column) => {
  const min = props.columnRanges[column][0]
  const max = props.columnRanges[column][1]
  const range = max - min

  return range / 100
}
</script>

<template>
  <div class="mt-4">
    <h3 class="text-lg font-semibold mb-2">Numeric Filters</h3>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
      <div v-for="column in numericVariables" :key="column" class="mb-2">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ column }}</label>
          <VueSlider
            v-if="numericFilters[column]"
            v-model="numericFilters[column]"
            :min="columnRanges[column][0]"
            :max="columnRanges[column][1]"
            :interval="calculateStep(column)"
            @change="updateNumericFilter(column, $event)"
          />
          <span v-if="numericFilters[column]" class="text-sm text-gray-600">
            {{ numericFilters[column][0].toFixed(2) }} -
            {{ numericFilters[column][1].toFixed(2) }}
          </span>
        </div>
        <button @click="resetNumeric(column)" class="mt-2 text-sm text-red-600 hover:text-red-800">
          Reset
        </button>
      </div>
    </div>

    <h3 class="text-lg font-semibold mt-8 mb-2">Discrete Filters</h3>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="column in discreteVariables" :key="column" class="mb-2">
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ column }}</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="value in columnRanges[column]"
            :key="value"
            @click="updateDiscreteFilter(column, value)"
            :class="[
              'px-2 py-1 text-sm rounded',
              isDiscreteValueSelected(column, value)
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700'
            ]"
          >
            {{ value }}
          </button>
        </div>
        <button
          @click="resetDiscreteFilter(column)"
          class="mt-2 text-sm text-red-600 hover:text-red-800"
        >
          Reset
        </button>
      </div>
    </div>
  </div>
</template>
