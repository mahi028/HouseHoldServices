import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAlertStore = defineStore('alertMesseges', () => {
  const alerts = ref([])

  function addAlert(type, message) {
    const id = Date.now()
    alerts.value.push({ id, type, message })

    setTimeout(() => {
      removeAlert(id)
    }, 3000)
  }

  function removeAlert(id) {
    alerts.value = alerts.value.filter(alert => alert.id !== id)
  }
  return { alerts, addAlert }
})
