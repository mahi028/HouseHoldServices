<template>
  <section class="service-details container">
    <div v-if="loading" class="text-center my-5">
      <p>Loading...</p>
    </div>

    <div v-else-if="error" class="text-center my-5">
      <p>{{ error }}</p>
    </div>

    <div v-else>
      <div class="card shadow p-4">
        <h1 class="text-center">{{ service.name }}</h1>
        <div class="text-center my-3">
          <img :src="service.image_url" alt="Service Image" class="img-fluid" />
        </div>
        <p><strong>Description:</strong> {{ service.desc }}</p>
        <p>
          <strong>Base Price:</strong> ₹{{ service.base_price }} + Charges as
          your work
          <abbr
            title="Charges may include Material used, overall time taken, complexity of work etc. Refer to the professional for more insightes. Some services for example cook, house help etc have monthly charges."
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-info-circle"
              viewBox="0 0 16 16"
            >
              <path
                d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"
              />
              <path
                d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0"
              /></svg
          ></abbr>
        </p>
        <p>
          <strong>Estimated Time:</strong> {{ service.min_time }} minutes
          <abbr
            title="This is only expected time taken for a job, it may vary according to your need or complexity of the task."
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-info-circle"
              viewBox="0 0 16 16"
            >
              <path
                d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"
              />
              <path
                d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0"
              /></svg
          ></abbr>
        </p>

        <ul>
          <li v-for="feature in service.features" :key="feature">
            {{ feature }}
          </li>
        </ul>
        <div style="display: flex; justify-content: center; width: 100%">
          <router-link
            class="btn btn-info m-2"
            :to="{
              name: 'AllProfessionals',
              params: { serv_id: service.serv_id, serv_name: service.name },
            }"
            >See Available Professional</router-link
          >
          <RouterLink
            class="btn btn-primary m-2"
            :to="{
              name: 'CreateService',
              params: { action: 'Update', serv_id: service.serv_id },
            }"
            v-if="loginStore.role === 1"
            >Update Service</RouterLink
          >
          <button
            class="btn btn-danger m-2"
            @click="deleteService"
            v-if="loginStore.role === 1"
          >
            Delete Service
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import axios from '@/axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { LoginStore } from '@/stores/loginDetails'

import { useAlertStore } from '@/stores/alertMsg'
const alertStore = useAlertStore()
const addAlert = alertStore.addAlert
import router from '@/router'
const loginStore = LoginStore()
const route = useRoute()
const service = ref({})
const loading = ref(true)
const error = ref(null)

const fetchService = async () => {
  try {
    const response = await axios.get(`/services/${route.params.serv_id}`)
    service.value = response.data
  } catch (err) {
    error.value = 'Failed to load service details. Please try again later.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const deleteService = async () => {
  try {
    const response = await axios.delete(
      '/delete/service/' + service.value.serv_id,
    )
    if (response.data.msg == 'Success') {
      addAlert('success', 'Service Deleted')
      router.push({ name: 'Home' })
    }
  } catch (error) {
    addAlert('success', 'Something went wrong')
    console.error('An Error Occured:', error)
  }
}

onMounted(fetchService)
</script>

<style scoped>
.service-details {
  max-width: 800px;
  margin: 2rem auto;
}
.img-fluid {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}
.card {
  border-radius: 12px;
}
</style>
