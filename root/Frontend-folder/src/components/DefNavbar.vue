<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <RouterLink class="navbar-brand" :to="{ name: 'Landing' }"
        >Household Services</RouterLink
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'Home' }"
              >All Services</RouterLink
            >
          </li>
          <li class="nav-item" v-if="loginStore.role == 1">
            <RouterLink
              class="nav-link"
              :to="{ name: 'CreateService', params: { action: 'Create' } }"
              >New Service</RouterLink
            >
          </li>
          <li class="nav-item" v-if="loginStore.role === 1">
            <RouterLink class="nav-link" :to="{ name: 'AllProfessionals' }"
              >See Professionals</RouterLink
            >
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'ServiceRequest' }"
              >See Requests</RouterLink
            >
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'Profile' }"
              >See Profile</RouterLink
            >
          </li>
          <li class="nav-item" v-if="loginStore.role === 1">
            <RouterLink class="nav-link" :to="{ name: 'AdminDash' }"
              >Stats</RouterLink
            >
          </li>
          <li class="nav-item">
            <button class="btn btn-danger" @click="logout()">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import axios from '@/axios'
import { LoginStore } from '@/stores/loginDetails'
import { useProfessionalStore } from '@/stores/userDeatils'
import { useCustStore } from '@/stores/custDetails'
import router from '@/router'
import { useAlertStore } from '@/stores/alertMsg'
const alertStore = useAlertStore()
const addAlert = alertStore.addAlert
// import { useRoute } from 'vue-router'
import { ref } from 'vue'
import Cookies from 'js-cookie'

// const route = useRoute()
const loginStore = LoginStore()
const professionalStore = useProfessionalStore()
const custStore = useCustStore()
const ignored = ref(null)

async function logout() {
  try {
    const response = await axios.delete('/logout')
    ignored.value = response
    addAlert('success', 'logout successful')
    router.push({ name: 'Login' })
  } catch (err) {
    Cookies.remove('csrf-access-token', { path: '/', domain: 'localhost' })
    Cookies.remove('access_token_cookie', { path: '/', domain: 'localhost' })
    console.error('Error', err)
  }
  loginStore.clearLoginDetails()
  professionalStore.clearLoginDetails()
  custStore.clearLoginDetails()
}
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
}

.nav-link {
  color: #000;
}

.nav-link:hover {
  color: #0056b3;
}
</style>
