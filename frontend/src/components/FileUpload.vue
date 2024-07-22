<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const emit = defineEmits(['upload-success', 'upload-error'])

const file = ref(null)
const uploading = ref(false)
const uploadProgress = ref(0)

const handleFileChange = (event) => {
  file.value = event.target.files[0]
}

const uploadFile = async () => {
  if (!file.value) {
    alert('Please select a file first')
    return
  }

  uploading.value = true
  uploadProgress.value = 0

  try {
    const formData = new FormData()
    formData.append('file', file.value)

    const response = await api.uploadFile(formData, (progressEvent) => {
      uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
    })

    emit('upload-success', response)
  } catch (error) {
    console.error('File upload failed:', error)
    emit('upload-error', error)
  } finally {
    uploading.value = false
    file.value = null
  }
}
</script>

<template>
  <div class="mt-4 flex items-start justify-start">
    <input
      type="file"
      @change="handleFileChange"
      class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
    />
    <button
      @click="uploadFile"
      :disabled="!file || uploading"
      class="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
    >
      {{ uploading ? 'Uploading...' : 'Upload' }}
    </button>
    <div v-if="uploading" class="mt-2">
      <div class="bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
        <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: `${uploadProgress}%` }"></div>
      </div>
      <p class="text-sm text-gray-500 mt-1">{{ uploadProgress }}% uploaded</p>
    </div>
  </div>
</template>
