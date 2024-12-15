<template>
  <div class="container d-flex justify-content-center my-5">
    <div class="card p-4 shadow" style="max-width: 600px; width: 100%">
      <center>
        <h2 class="mb-4">Register</h2>
      </center>
      <form method="post" @submit.prevent="submit_form">
        <div class="mb-3">
          <label for="name" class="form-label">Name</label>
          <input
            type="text"
            name="name"
            id="name"
            class="form-control"
            v-model="formData.name"
          />
        </div>

        <div class="mb-3">
          <label for="user_name" class="form-label">Username</label>
          <input
            type="text"
            name="user_name"
            id="user_name"
            class="form-control"
            v-model="formData.user_name"
          />
        </div>

        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            name="email"
            id="email"
            class="form-control"
            v-model="formData.email"
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            name="password"
            id="password"
            class="form-control"
            v-model="formData.password"
          />
        </div>

        <div class="mb-3">
          <label for="conf_password" class="form-label">Confirm Password</label>
          <input
            type="password"
            name="conf_password"
            id="conf_password"
            class="form-control"
            v-model="formData.conf_password"
          />
        </div>

        <div class="mb-3">
          <label for="contact_num" class="form-label">Contact Number</label>
          <input
            type="text"
            name="contact_num"
            id="contact_num"
            class="form-control"
            v-model="formData.contact_num"
          />
        </div>

        <div class="mb-3">
          <label for="role" class="form-label">Role</label>
          <select
            name="role"
            id="role"
            class="form-select"
            v-model="formData.role"
          >
            <option value="" disabled>Select Role</option>
            <option value="2">Professional</option>
            <option value="3">Customer</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="image" class="form-label">Profile Image</label>
          <input
            type="file"
            class="form-control"
            id="image"
            @change="onFileChange"
            accept="image/*"
            required
          />
        </div>

        <center>
          <button type="submit" class="btn btn-primary mt-3">Register</button>
        </center>

        <center class="mt-3">
          <span>
            Already a User?
            <RouterLink
              :to="{ name: 'Login' }"
              class="link-secondary link-underline link-underline-opacity-0 link-underline-opacity-75-hover"
            >
              Login
            </RouterLink>
          </span>
        </center>
      </form>
    </div>
  </div>
</template>

<script setup>
import axios from '@/axios'
import { ref } from 'vue'
import router from '@/router'

import { useAlertStore } from '@/stores/alertMsg'
const alertStore = useAlertStore()
const addAlert = alertStore.addAlert

const data = ref('')
const formData = ref({
  name: '',
  user_name: '',
  email: '',
  password: '',
  conf_password: '',
  contact_num: '',
  role: '',
  image: null,
})

const onFileChange = event => {
  formData.value.image = event.target.files[0]
}

async function fetch_csrf() {
  try {
    const response = await axios.get('/get_csrf_token')
    return response.data.csrf_token
  } catch (error) {
    console.error('Error fetching CSRF token:', error)
    return ''
  }
}

async function submit_form() {
  try {
    const form_Data = new FormData()

    form_Data.append('name', formData.value.name)
    form_Data.append('user_name', formData.value.user_name)
    form_Data.append('email', formData.value.email)
    form_Data.append('password', formData.value.password)
    form_Data.append('conf_password', formData.value.conf_password)
    form_Data.append('contact_num', formData.value.contact_num)
    form_Data.append('role', formData.value.role)
    form_Data.append('image', formData.value.image)

    const formCsrfToken = await fetch_csrf()
    const response = await axios.post('/register', form_Data, {
      headers: {
        'X-CSRF-TOKEN': formCsrfToken,
        'Content-Type': 'multipart/form-data',
      },
    })
    data.value = response.data
    addAlert('success', 'Registerd Successfully, Please login.')
    router.push({ name: 'Login' })
  } catch (error) {
    addAlert('danger', 'Something went wrong')
    console.error('Error submitting form:', error)
  }
}
</script>

<style scoped>
.card {
  border-radius: 8px;
}
</style>
