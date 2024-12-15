<template>
  <div class="not-authorized">
    <h1>Access Denied</h1>
    <p>You do not have permission to view this page.</p>
    <router-link to="/home" v-if="loginStore.role">Go to Home</router-link>
    <router-link to="/login" v-else>Login</router-link>
  </div>
</template>

<script setup>
import { LoginStore } from '@/stores/loginDetails'
const loginStore = LoginStore()
</script>

<style>
.not-authorized {
  text-align: center;
  padding: 20px;
}
</style>
