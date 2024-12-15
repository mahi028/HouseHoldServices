<!-- src/views/Home.vue -->
<template>
  <div class="container mt-5">
    <header class="text-center my-5">
      <h1>Household Services</h1>
      <p class="lead">
        Choose a service, and let our professionals take care of the rest.
      </p>
      <div
        style="
          width: 500px;
          margin-right: 100px;
          justify-content: flex-end;
          align-items: end;
          flex-direction: column;
          display: flex;
          width: 100%;
        "
      >
        <button
          @click="downloadReport"
          class="btn btn-info"
          v-show="loginStore.role === 1"
        >
          Download Service Report
        </button>
        <br />
        <div class="nav-item" style="width: 300px">
          <input
            class="form-control me-2"
            type="search"
            placeholder="Search for services"
            aria-label="Search"
            v-model="searchQuery"
          />
        </div>
      </div>
    </header>

    <section class="services">
      <div class="row">
        <ServiceCard
          :name="item.name"
          :image="item.image_url"
          :description="item.desc"
          :base_price="item.base_price"
          :min_time="item.min_time"
          :serv_id="item.serv_id"
          :route="'/services/' + item.serv_id"
          v-for="item in items"
          :key="item.id"
        />
      </div>
    </section>

    <footer class="text-center mt-5">
      <router-link
        to="/register"
        class="btn btn-primary btn-lg"
        v-if="!loginStore.isLoggedIn"
        >Book a Service</router-link
      >
    </footer>
  </div>
</template>

<script setup>
import ServiceCard from '@/components/ServiceCard.vue'
import { ref, onBeforeMount, watch } from 'vue'
import axios from '@/axios'
import { LoginStore } from '@/stores/loginDetails'

import { useAlertStore } from '@/stores/alertMsg'
const alertStore = useAlertStore()
const addAlert = alertStore.addAlert

const loginStore = LoginStore()
const searchQuery = ref(null)

const items = ref([])
const itemsCopy = ref()
const loading = ref(true)
const error = ref(null)
const ignored = ref(null)
const fetchData = async () => {
  try {
    const response = await axios.get('/services')
    items.value = response.data
    itemsCopy.value = response.data
  } catch (err) {
    error.value = 'Failed to fetch data: ' + err.message
    console.error(err)
  } finally {
    loading.value = false
  }
}

const onSearch = () => {
  const query = searchQuery.value.toLowerCase()
  if (!query) {
    items.value = [...itemsCopy.value]
  } else {
    items.value = items.value.filter(
      item =>
        item.name.toLowerCase().includes(query) ||
        item.desc.toLowerCase().includes(query),
    )
  }
}
const task_id = ref(null)
async function downloadReport() {
  try {
    const response = await axios.post('/create-report')
    if (response.data.msg === 'Success') {
      task_id.value = response.data.task_id
    }
  } catch (err) {
    if (err.response.data.message === 'No Service Request') {
      addAlert('danger', 'No Service Requests in database Yet')
    }
    console.error('Error', err)
    return
  }

  if (task_id.value) {
    const intv = setInterval(async () => {
      try {
        const result = await axios.get(`/get-report/${task_id.value}`)
        ignored.value = result
        clearInterval(intv)
        addAlert('success', 'Report Downloading will begin shortly')
        window.location.href = `http://localhost:5000/api/get-report/${task_id.value}`
      } catch (err) {
        if (err.request.status !== 421) {
          console.error('Error', err)
          clearInterval(intv)
          addAlert('danger', 'Something Went Wrong')
        }
      }
    }, 1000)
  }
}
watch(searchQuery, onSearch)
onBeforeMount(fetchData)
</script>

<style scoped>
header h1 {
  font-weight: bold;
  font-size: 2.5rem;
}
footer {
  margin-top: 30px;
}
</style>
