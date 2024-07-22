import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
})

async function handleApiCall(apiFunction) {
  try {
    const response = await apiFunction()
    return response.data
  } catch (error) {
    console.error('API call failed:', error)
    throw error
  }
}

const api = {
  async getAvailablePlots() {
    return handleApiCall(() => apiClient.get('/api/v1/available-plots'))
  },

  async getDiscreteVariables() {
    return handleApiCall(() => apiClient.get('/api/v1/discrete-variables'))
  },

  async getNumericVariables() {
    return handleApiCall(() => apiClient.get('/api/v1/numeric-variables'))
  },

  async getColumnRanges() {
    return handleApiCall(() => apiClient.get('/api/v1/column-ranges'))
  },

  async getPlotVariables(plotType) {
    return handleApiCall(() => apiClient.get(`/api/v1/plot-variables/${plotType}`))
  },

  async getPlotVariables(plotType) {
    return handleApiCall(() => apiClient.get(`/api/v1/plot-variables/${plotType}`))
  },

  async generatePlot(plotType, xColumn, yColumn, colorBy, filters = null) {
    const params = new URLSearchParams({
      x_column: xColumn,
      y_column: yColumn || '',
      color_by: colorBy || '',
      filters: JSON.stringify(filters)
    })
    return handleApiCall(() =>
      apiClient.get(`/api/v1/generate-plot/${plotType}?${params.toString()}`)
    )
  },

  async uploadFile(formData, onUploadProgress) {
    return handleApiCall(() =>
      apiClient.post('/api/v1/load-dataframe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress
      })
    )
  }
}

export default api
