import { defineStore } from 'pinia'

export const LoginStore = defineStore('loginDetails', {
  state: () => ({
    user_name: null,
    name: null,
    user_id: null,
    role: null,
    isLoggedIn: false,
  }),

  actions: {
    setLoginDetails(details) {
      this.user_name = details.user_name
      this.name = details.name
      this.user_id = details.id
      this.role = details.role
      this.isLoggedIn = true
    },

    clearLoginDetails() {
      this.user_name = null
      this.name = null
      this.user_id = null
      this.role = null
      this.isLoggedIn = false
    },
  },
  persist: true,
})
