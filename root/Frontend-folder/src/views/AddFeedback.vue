<template>
  <div class="container d-flex justify-content-center my-5">
    <div class="card p-4 shadow" style="max-width: 500px; width: 100%">
      <center>
        <h2 class="mb-4">Add Feedback for job {{ route.params.rqst_id }}</h2>
      </center>
      <form method="post" @submit.prevent="submit_form">
        <div class="mb-3">
          <label for="feedback" class="form-label">Feedback</label>
          <input
            type="text"
            name="feedback"
            id="feedback"
            class="form-control"
            v-model="form_data.feedback"
          />
        </div>
        <div>
          <label for="feedbackRating" class="form-label"
            >Feedback Rating (1-5)</label
          >
          <input
            type="range"
            name="feedbackRating"
            id="feedbackRating"
            class="form-control"
            min="1"
            max="5"
            step="1"
            v-model="form_data.feedbackRating"
          /><span>{{ form_data.feedbackRating }}</span>
        </div>
        <div>
          <button type="submit" class="btn btn-primary mt-3">Book now</button>
        </div>
      </form>
      <!-- Status Message -->
      <div v-if="formStatus.success !== null" class="mt-3">
        <p :class="formStatus.success ? 'text-success' : 'text-danger'">
          {{ formStatus.message }}
        </p>
      </div>
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

const form_data = ref({
  feedback: '',
  feedbackRating: '',
})

const formStatus = ref({
  success: null,
  message: '',
})

const data = ref(null)

async function submit_form() {
  try {
    const response = await axios.post(
      `/request/feedback/${route.params.rqst_id}`,
      form_data.value,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      },
    )

    data.value = response.data

    if (data.value.msg === 'Success') {
      addAlert('success', 'Request Created')
      router.push({ name: 'Home' })
    }
  } catch (error) {
    addAlert('danger', 'SomethingWentWrong')
    console.error('Error submitting form:', error)
  }
}
</script>

<style scoped>
.card {
  border-radius: 8px;
}
</style>
