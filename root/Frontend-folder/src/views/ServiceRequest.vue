<template>
  <div class="container mt-4 service-requests">
    <h1 class="text-center mb-4" v-if="loginStore.role !== 1">
      Your Service Requests
    </h1>
    <h1 class="text-center mb-4" v-else>Service Requests</h1>
    <div v-if="requests.length > 0">
      <table class="table table-bordered table-striped">
        <thead class="thead-dark">
          <tr>
            <th scope="col">#</th>
            <th scope="col">Service Name</th>
            <th
              scope="col"
              v-if="loginStore.role === 1 || loginStore.role === 3"
            >
              Provider Name
            </th>
            <th
              scope="col"
              v-if="loginStore.role === 1 || loginStore.role === 2"
            >
              Customer Name
            </th>
            <th scope="col">Message</th>
            <th scope="col">Status</th>
            <th scope="col">Created At</th>
            <th scope="col">Total Cost</th>
            <th
              scope="col"
              v-if="loginStore.role === 2 || loginStore.role === 3"
            >
              Action
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(request, index) in requests" :key="request.rqst_id">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ request['service.name'] }}</td>
            <td v-if="loginStore.role === 1 || loginStore.role === 3">
              <RouterLink
                style="color: gray"
                :to="{
                  name: 'Profile',
                  params: { id: request['serv_pro_id'] },
                }"
                >{{ request['service_pro.user.name'] }}</RouterLink
              >
            </td>
            <td v-if="loginStore.role === 1 || loginStore.role === 2">
              <RouterLink
                style="color: gray"
                :to="{
                  name: 'Profile',
                  params: { id: request['cust_id'] },
                }"
                >{{ request['customer.user.name'] }}</RouterLink
              >
            </td>
            <td>{{ request.service_msg || 'N/A' }}</td>
            <td>
              <span>
                {{ request.status }}
              </span>
            </td>
            <td>{{ request.created_at }}</td>
            <td>{{ request.total_cost ? `₹${request.total_cost}` : 'N/A' }}</td>
            <td v-if="loginStore.role === 2 || loginStore.role === 3">
              <button
                class="btn btn-primary m-2"
                @click="acceptRqst(request.rqst_id)"
                v-show="request.status === 'Pending' && loginStore.role === 2"
              >
                Accept
              </button>
              <button
                class="btn btn-danger m-2"
                @click="rejectRqst(request.rqst_id)"
                v-show="
                  request.status === 'Ongoing' || request.status === 'Pending'
                "
              >
                <span v-if="loginStore.role === 2">Reject</span>
                <span v-if="loginStore.role === 3">Cancel</span>
              </button>
              <RouterLink
                :to="{
                  name: 'AddFeedback',
                  params: { rqst_id: request.rqst_id },
                }"
                class="btn btn-primary m-2"
                v-show="
                  (request.status === 'Completed' ||
                    request.status === 'Cancelled') &&
                  (loginStore.role === 2 || loginStore.role === 3)
                "
              >
                Add Review
              </RouterLink>
              <RouterLink
                :to="{
                  name: 'CompleteService',
                  params: { rqst_id: request.rqst_id },
                }"
                class="btn btn-success m-2"
                v-show="request.status === 'Ongoing' && loginStore.role === 2"
              >
                Mark As Complete
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="text-center">
      <p class="text-muted">No service requests found.</p>
    </div>
  </div>
</template>
<script setup>
import axios from '@/axios'
import { LoginStore } from '@/stores/loginDetails'
import { ref, onMounted } from 'vue'

import { useAlertStore } from '@/stores/alertMsg'
const alertStore = useAlertStore()
const addAlert = alertStore.addAlert
const loginStore = LoginStore()
const requests = ref([])
const ignored = ref(null)
async function acceptRqst(rqst_id) {
  try {
    const response = await axios.patch(`/request/accept/${rqst_id}`)
    ignored.value = response //just to ignore the warning

    addAlert('success', 'Request Accepted')
  } catch (err) {
    addAlert('danger', 'Something Went Wrong')
    console.error('Error', err)
  }
}
async function rejectRqst(rqst_id) {
  try {
    const response = await axios.patch(`/request/reject/${rqst_id}`)
    ignored.value = response

    addAlert('success', 'Request Rejected')
  } catch (err) {
    addAlert('danger', 'Something Went Wrong')
    console.error('Error', err)
  }
}

const fetchServiceRequests = async () => {
  try {
    const response = await axios.get('/customer/service-requests')
    requests.value = response.data
  } catch (error) {
    console.error('Error fetching service requests:', error)
  }
}

onMounted(fetchServiceRequests)
</script>
