<template>
  <StackingAlert />
  <DefNavbar v-if="loginStore.isLoggedIn" />
  <AltNavbar v-else />
  <RouterView />
</template>

<script setup>
import DefNavbar from './components/DefNavbar.vue'
import AltNavbar from './components/AltNavbar.vue'
import { LoginStore } from './stores/loginDetails'
import StackingAlert from './components/StackingAlert.vue'
const loginStore = LoginStore()
</script>
