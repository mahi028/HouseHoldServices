<template>
  <div class="container mt-5">
    <h2>Create a Professional account</h2>
    <form @submit.prevent="submitForm" class="p-4 border rounded">
      <!-- Description -->
      <div class="mb-3">
        <label for="desc" class="form-label">Description</label>
        <textarea
          id="desc"
          class="form-control"
          v-model="formData.desc"
          required
          placeholder="Describe yourself"
        ></textarea>
      </div>

      <!-- Service name -->
      <div class="mb-3">
        <label for="dropdown" class="form-label">Service Provided</label>
        <select id="dropdown" v-model="formData.serv_id" class="form-select">
          <option
            v-for="item in items"
            :key="item.serv_id"
            :value="item.serv_id"
          >
            {{ item.name }}, {{ item.serv_id }}
          </option>
        </select>
      </div>

      <!-- Experience -->
      <div class="mb-3">
        <label for="experience" class="form-label">Experience (in years)</label>
        <input
          type="number"
          id="experience"
          class="form-control"
          v-model="formData.experience"
          required
          placeholder="Experience"
        />
      </div>

      <!-- service_area_pin_code -->
      <div class="mb-3">
        <label for="service_area_pin_code" class="form-label"
          >service_area_pin_code</label
        >
        <input
          type="number"
          id="service_area_pin_code"
          class="form-control"
          v-model="formData.service_area_pin_code"
          required
          placeholder="Pincode"
        />
      </div>

      <div class="mb-3">
        <label for="id_document" class="form-label">Id Document</label>
        <input
          type="file"
          class="form-control"
          id="id_document"
          @change="onFileChange"
          accept="id_document/*"
        />
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary">
        Complete Registration
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
import { onBeforeMount } from 'vue'
import { useProfessionalStore } from '@/stores/userDeatils'

import { useAlertStore } from '@/stores/alertMsg'
const alertStore = useAlertStore()
const addAlert = alertStore.addAlert
const professionalStore = useProfessionalStore()

const formData = ref({
  desc: '',
  serv_id: null,
  experience: null,
  service_area_pin_code: null,
  id_document: null,
})
const items = ref(null)
const loading = ref(true)
const error = ref(null)
const data = ref(null)

const formStatus = ref({
  success: null,
  message: '',
})

const onFileChange = event => {
  formData.value.id_document = event.target.files[0]
}

const submitForm = async () => {
  try {
    const form_Data = new FormData()
    form_Data.append('desc', formData.value.desc)
    form_Data.append('serv_id', formData.value.serv_id)
    form_Data.append('experience', formData.value.experience)
    form_Data.append(
      'service_area_pin_code',
      formData.value.service_area_pin_code,
    )
    form_Data.append('id_document', formData.value.id_document)
    const response = await axios.post('/create/service_pro', form_Data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    data.value = response.data

    formStatus.value = {
      success: true,
      message: 'Professional account created successfully!',
    }
    addAlert('success', 'Registration Complete')
    const res = await axios.get('/get/service_pro')
    professionalStore.setLoginDetails(res.data)
    router.push({ name: 'Home' })
  } catch (error) {
    formStatus.value = {
      success: false,
      message: error.response.data.message,
    }
    console.error('Error:', error)
  }
}
const fetchData = async () => {
  try {
    const response = await axios.get('/services')
    items.value = response.data
  } catch (err) {
    error.value = 'Failed to fetch data: ' + err.message
    console.error(err)
  } finally {
    loading.value = false
  }
}
onBeforeMount(fetchData)
</script>
