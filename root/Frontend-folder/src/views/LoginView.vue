<template>
  <div class="container d-flex justify-content-center my-5">
    <div class="card p-4 shadow" style="max-width: 500px; width: 100%">
      <center>
        <h2 class="mb-4">Login</h2>
      </center>
      <form method="post" @submit.prevent="submit_form">
        <div class="mb-3">
          <label for="user_name" class="form-label">Username</label>
          <input
            type="text"
            name="user_name"
            id="user_name"
            class="form-control"
            v-model="form_data.user_name"
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            name="password"
            id="password"
            class="form-control"
            v-model="form_data.password"
          />
        </div>

        <center>
          <button type="submit" class="btn btn-primary mt-3">Login</button>
        </center>

        <center class="mt-3">
          <span>
            New User?
            <RouterLink
              :to="{ name: 'Register' }"
              class="link-secondary link-underline link-underline-opacity-0 link-underline-opacity-75-hover"
            >
              Register
            </RouterLink>
          </span>
        </center>
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
import { LoginStore } from '@/stores/loginDetails'
import { useProfessionalStore } from '@/stores/userDeatils'
import { useCustStore } from '@/stores/custDetails'

import { useAlertStore } from '@/stores/alertMsg'
const alertStore = useAlertStore()
const addAlert = alertStore.addAlert

const loginStore = LoginStore()
const professionalStore = useProfessionalStore()
const custStore = useCustStore()

const form_data = ref({
  user_name: '',
  password: '',
})

const formStatus = ref({
  success: null,
  message: '',
})

const data = ref(null)

async function fetch_csrf() {
  try {
    const response = await axios.get('/get_csrf_token')
    return response.data.csrf_token
  } catch (error) {
    console.error('Error fetching CSRF token:', error)
    formStatus.value.success = false
    formStatus.value.message = 'Failed to fetch CSRF token'
    return ''
  }
}

async function check_service_pro() {
  try {
    const response = await axios.get('/get/service_pro')

    professionalStore.setLoginDetails(response.data)
  } catch (error) {
    if (error.response && error.response.status == 404) {
      router.push({ name: 'CreateServicePro' })
    } else {
      console.error('Error checking service pro:', error)
    }
  }
}
async function check_cust() {
  try {
    const response = await axios.get('/get/customer')

    custStore.setLoginDetails(response.data)
  } catch (error) {
    if (error.response && error.response.status === 404) {
      router.push({ name: 'CreateCustomer' })
    } else {
      console.error('Error checking service pro:', error)
    }
  }
}

async function submit_form() {
  try {
    const formCsrfToken = await fetch_csrf()

    const response = await axios.post('/login', form_data.value, {
      headers: {
        'X-CSRF-TOKEN': formCsrfToken,
        'Content-Type': 'application/json',
      },
    })

    data.value = response.data

    if (data.value.msg === 'login successful') {
      loginStore.setLoginDetails(data.value.user)

      formStatus.value.success = true
      formStatus.value.message = 'Logged in successfully'
      addAlert('success', formStatus.value.message)

      if (loginStore.role === 2) {
        check_service_pro()
      } else if (loginStore.role === 3) {
        check_cust()
      }

      // Redirect to Home page after login
      router.push({ name: 'Home' })
    }
  } catch (error) {
    console.log(error)
    formStatus.value.success = false
    formStatus.value.message = error.response.data
    alertStore.addAlert('danger', formStatus.value.message)

    console.error('Error submitting form:', error)
  }
}
</script>

<style scoped>
.card {
  border-radius: 8px;
}
</style>
