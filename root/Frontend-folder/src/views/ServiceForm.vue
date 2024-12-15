<template>
  <div class="container mt-5">
    <h2 v-show="action === 'Create'">Create a New Service</h2>
    <h2 v-show="action === 'Update'">Update Service {{ serv_id }}</h2>
    <form @submit.prevent="submitForm" class="p-4 border rounded">
      <!-- Name -->
      <div class="mb-3">
        <label for="name" class="form-label">Service Name</label>
        <input
          type="text"
          id="name"
          class="form-control"
          v-model="formData.name"
          placeholder="Enter the service name"
        />
      </div>

      <!-- Description -->
      <div class="mb-3">
        <label for="desc" class="form-label">Description</label>
        <textarea
          id="desc"
          class="form-control"
          v-model="formData.desc"
          placeholder="Enter the service description"
        ></textarea>
      </div>

      <!-- Base Price -->
      <div class="mb-3">
        <label for="base_price" class="form-label">Base Price</label>
        <input
          type="number"
          id="base_price"
          class="form-control"
          v-model="formData.base_price"
          placeholder="Enter the base price"
        />
      </div>

      <!-- Minimum Time -->
      <div class="mb-3">
        <label for="min_time" class="form-label"
          >Minimum Time (in minutes)</label
        >
        <input
          type="number"
          id="min_time"
          class="form-control"
          v-model="formData.min_time"
          placeholder="Enter the minimum time in minutes"
        />
      </div>
      <div class="mb-3">
        <label for="image" class="form-label">Service Image</label>
        <input
          type="file"
          class="form-control"
          id="image"
          @change="onFileChange"
          accept="image/*"
        />
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary">
        {{ action }} Service
      </button>
    </form>

    <!-- Status Message -->
    <div v-if="formStatus.success !== null" class="mt-3">
      <p :class="formStatus.success ? 'text-success' : 'text-danger'">
        {{ formStatus.message }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/axios'
import router from '@/router'
import { useRoute } from 'vue-router'

import { useAlertStore } from '@/stores/alertMsg'
const alertStore = useAlertStore()
const addAlert = alertStore.addAlert
const route = useRoute()

const formData = ref({
  name: '',
  desc: '',
  base_price: '',
  min_time: '',
  image: null,
})

const action = route.params.action
const serv_id = route.params.serv_id
const data = ref(null)

const formStatus = ref({
  success: null,
  message: '',
})

const onFileChange = event => {
  formData.value.image = event.target.files[0]
}

const submitForm = async () => {
  try {
    const form_Data = new FormData()

    form_Data.append('name', formData.value.name)
    form_Data.append('desc', formData.value.desc)
    form_Data.append('base_price', formData.value.base_price)
    form_Data.append('min_time', formData.value.min_time)
    form_Data.append('image', formData.value.image)

    if (action === 'Create') {
      const response = await axios.post('/create/service', form_Data, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      data.value = response.data
    } else if (action === 'Update') {
      const response = await axios.patch(
        `/update/service/${serv_id}`,
        form_Data,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
        },
      )
      data.value = response.data
    }

    formStatus.value = {
      success: true,
      message: `Service ${action}d successfully!`,
    }
    addAlert('success', formStatus.value.message)
    router.push({ name: 'Home' })
  } catch (error) {
    formStatus.value = { success: false, message: error.response.data.message }
    console.error('Error:', error)
  }
}
</script>
