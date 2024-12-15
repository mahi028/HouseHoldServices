<template>
  <div class="position-fixed top-0 end-0 p-3" style="z-index: 1050">
    <div
      v-for="alert in alerts"
      :key="alert.id"
      :class="`alert alert-${alert.type} alert-dismissible fade show`"
      role="alert"
    >
      {{ alert.message }}
    </div>
  </div>
</template>

<script setup>
import { useAlertStore } from '@/stores/alertMsg'
import { ref, watch } from 'vue'
const alertStore = useAlertStore()
const alerts = ref([])

watch(
  () => alertStore.alerts,
  () => {
    alerts.value = alertStore.alerts
  },
  { deep: true },
)
</script>

<style>
.alert + .alert {
  margin-top: 30px;
}
</style>
