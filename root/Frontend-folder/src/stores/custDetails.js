import { defineStore } from 'pinia'

export const useCustStore = defineStore('custDeatails', {
  state: () => ({
    pin_code: null,
    address: null,
  }),

  actions: {
    setLoginDetails(details) {
      this.pin_code = details.pin_code
      this.address = details.address
    },

    clearLoginDetails() {
      this.pin_code = null
      this.address = null
    },
  },
  persist: true,
})
