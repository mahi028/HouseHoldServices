import { defineStore } from 'pinia'

export const useProfessionalStore = defineStore('professionalDeatails', {
  state: () => ({
    desc: null,
    serv_id: null,
    experience: null,
    service_area_pin_code: null,
    id_document_url: null,
  }),

  actions: {
    setLoginDetails(details) {
      this.desc = details.desc
      this.serv_id = details.serv_id
      this.experience = details.experience
      this.service_area_pin_code = details.service_area_pin_code
      this.id_document_url = details.id_document_url
    },

    clearLoginDetails() {
      this.desc = null
      this.serv_id = null
      this.experience = null
      this.service_area_pin_code = null
      this.id_document_url = null
    },
  },
  persist: true,
})
