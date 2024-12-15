import './assets/main.css'

import { createApp } from 'vue'
import pinia from './stores'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import { LoginStore } from './stores/loginDetails'
import StackingAlert from './components/StackingAlert.vue'

const app = createApp(App)

app.use(pinia)
app.use(router)
app.config.globalProperties.$axios = axios
app.component('StackingAlert', StackingAlert)

app.mount('#app')

router.beforeEach((to, from, next) => {
  const loginStore = LoginStore()

  if (to.meta.roles) {
    const userRole = loginStore.role

    if (to.meta.roles.includes(userRole)) {
      next()
    } else {
      next({ name: 'NotFound' })
    }
  } else {
    next()
  }
})
