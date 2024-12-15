<template>
  <div class="container mt-5">
    <h2>Create a Professional account</h2>
    <form @submit.prevent="submitForm" class="p-4 border rounded">
      <!-- Address -->
      <div class="mb-3">
        <label for="address" class="form-label">Address</label>
        <textarea
          id="address"
          class="form-control"
          v-model="formData.address"
          required
          placeholder="Address"
        ></textarea>
      </div>

      <!-- pin_code -->
      <div class="mb-3">
        <label for="pin_code" class="form-label">Pin Code</label>
        <input
          type="number"
          id="pin_code"
          class="form-control"
          v-model="formData.pin_code"
          required
          placeholder="Pincode"
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
import { useCustStore } from '@/stores/custDetails'

import { useAlertStore } from '@/stores/alertMsg'
const alertStore = useAlertStore()
const addAlert = alertStore.addAlert

const custStore = useCustStore()
const data = ref(null)

const formData = ref({
  address: '',
  pin_code: null,
})

const formStatus = ref({
  success: null,
  message: '',
})

const submitForm = async () => {
  try {
    const form_Data = new FormData()
    form_Data.append('address', formData.value.address)
    form_Data.append('pin_code', formData.value.pin_code)

    const response = await axios.post('/create/customer', form_Data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    data.value = response.data

    formStatus.value = {
      success: true,
      message: 'Professional account created successfully!',
    }
    addAlert('success', 'Registration Complete')
    const res = await axios.get('/get/customer')
    custStore.setLoginDetails(res.data)
    router.push({ name: 'Home' })
  } catch (error) {
    formStatus.value = {
      success: false,
      message: 'Failed to create Customer account.',
    }
    addAlert('danger', formStatus.value.message)

    console.error('Error:', error)
  }
}
</script>
