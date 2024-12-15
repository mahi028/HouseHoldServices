<template>
  <div class="container my-4">
    <h3 class="text-center mb-4">List of Professionals</h3>
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
    <div class="table-responsive" v-if="professionals">
      <table class="table table-striped table-bordered align-middle">
        <thead class="table-dark">
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Description</th>
            <th scope="col">Service Name</th>
            <th scope="col">
              Experience (Years)
              <span
                @click="toggleSort('experience')"
                style="cursor: pointer"
                class="ms-2"
              >
                <i
                  :class="{
                    'bi bi-arrow-up':
                      sortBy === 'experience' && sortOrder === 'asc',
                    'bi bi-arrow-down':
                      sortBy === 'experience' && sortOrder === 'desc',
                    'bi bi-arrow-down-up': sortBy !== 'experience',
                  }"
                ></i>
              </span>
            </th>
            <th scope="col">Service Area</th>
            <th scope="col">
              Rating
              <span
                @click="toggleSort('rating')"
                style="cursor: pointer"
                class="ms-2"
              >
                <i
                  :class="{
                    'bi bi-arrow-up':
                      sortBy === 'rating' && sortOrder === 'asc',
                    'bi bi-arrow-down':
                      sortBy === 'rating' && sortOrder === 'desc',
                    'bi bi-arrow-down-up': sortBy !== 'rating',
                  }"
                ></i>
              </span>
            </th>
            <th scope="col" v-show="loginStore.role === 1">Status</th>
            <th scope="col" v-show="loginStore.role === 1">Flag Status</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="professional in sortedProfessionals"
            :key="professional.id"
          >
            <td>{{ professional.id }}</td>
            <th>{{ professional['user.name'] }}</th>
            <td>{{ professional.desc }}</td>
            <td>
              <RouterLink
                style="color: gray"
                :to="{
                  name: 'Service',
                  params: { serv_id: professional.serv_id },
                }"
                >{{ professional['service.name'] }}</RouterLink
              >
            </td>
            <td>{{ professional.experience }}</td>
            <td>{{ professional.service_area_pin_code }}</td>
            <td>{{ professional.rating || 'N/A' }}</td>
            <td v-show="loginStore.role === 1">{{ professional.status }}</td>
            <td v-show="loginStore.role === 1">
              {{ professional['user.flag_status'] ? 'Flagged' : 'Not Flagged' }}
            </td>
            <td v-if="loginStore.role === 1">
              <RouterLink
                class="btn btn-info"
                :to="{
                  name: 'Profile',
                  params: { id: professional.id },
                }"
                style="text-decoration: none; color: black"
                >See Account</RouterLink
              >
            </td>
            <td v-else>
              <RouterLink
                class="btn btn-info"
                :to="{
                  name: 'Profile',
                  params: { id: professional.id },
                }"
                style="text-decoration: none; color: black"
                >See Account</RouterLink
              >
              |
              <RouterLink
                class="btn btn-info"
                :to="{
                  name: 'BookService',
                  params: { service_pro_id: professional.id },
                }"
                style="text-decoration: none; color: black"
                >Book Service</RouterLink
              >
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="text-center mb-4">
      <h3>No Professionals Found</h3>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from '@/axios'
import { LoginStore } from '@/stores/loginDetails'

const props = defineProps({
  serv_id: { type: Number, required: false },
  serv_name: { type: String, required: false },
})

const loginStore = LoginStore()

const professionals = ref([])
const professionalsCopy = ref([])
const sortBy = ref('sort')
const sortOrder = ref(null)
const searchQuery = ref(null)

const onSearch = () => {
  const query = searchQuery.value.toLowerCase()
  if (!query) {
    professionals.value = [...professionalsCopy.value]
  } else {
    professionals.value = professionals.value.filter(professional =>
      professional['user.name'].toLowerCase().includes(query),
    )
  }
}

async function fetchProfessionals() {
  try {
    const response = await axios.get(
      `/get/professionals?serv_id=${props.serv_id || 'null'}&name=${props.serv_name || 'null'}`,
    )
    professionals.value = response.data
    professionalsCopy.value = response.data
  } catch (error) {
    professionals.value = null
    console.error('Error fetching professionals:', error)
  }
}

const sortedProfessionals = computed(() => {
  if (!sortBy.value) return professionals.value
  return [...professionals.value].sort((a, b) => {
    const valA = a[sortBy.value]
    const valB = b[sortBy.value]

    if (valA == null || valB == null) return 0
    if (sortOrder.value === 'asc') {
      return valA > valB ? 1 : -1
    } else {
      return valA < valB ? 1 : -1
    }
  })
})

function toggleSort(column) {
  if (sortBy.value === column) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.value = column
    sortOrder.value = 'asc'
  }
}
watch(searchQuery, onSearch)
onMounted(fetchProfessionals)
</script>
