<template>
  <div v-if="!profileFound" style="text-align: center">ProfileNotFound</div>
  <div
    v-else-if="
      profile.flag_status &&
      loginStore.role !== 1 &&
      loginStore.user_id !== profile.id
    "
    style="text-align: center; color: red"
  >
    You Can't view this profile.
  </div>
  <div class="container mt-5" v-else>
    <div class="card shadow-sm">
      <div class="row g-0">
        <div class="col-md-4 text-center p-3">
          <img
            :src="profile.profile_picture_path"
            alt="Profile Picture"
            class="img-fluid"
          />
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title">{{ profile.name }}</h5>
            <p class="card-text">
              <strong>Username:</strong> {{ profile.user_name }}
            </p>
            <p class="card-text"><strong>Email:</strong> {{ profile.email }}</p>
            <p class="card-text">
              <strong>Role:</strong> {{ getRole(profile.role) }}
            </p>
            <p class="card-text" v-show="profile.contact_num">
              <strong>Contact number:</strong>
              {{ profile.contact_num }}
            </p>
            <p class="card-text">
              <strong>Flag_status: </strong>
              <span
                :style="{
                  color: profile.flag_status ? 'red' : 'green',
                }"
              >
                {{ profile.flag_status ? 'Flagged' : 'Not Flagged' }} -
              </span>

              <button
                v-if="loginStore.role === 1"
                @click="changeFlag"
                :class="{
                  'btn btn-danger': !profile.flag_status,
                  'btn btn-success': profile.flag_status,
                }"
              >
                {{ profile.flag_status ? 'Un-Flag' : 'Flag' }}
              </button>
            </p>
            <div v-if="profile.role === 2">
              <hr />
              <h6>Professional Details</h6>
              <p>
                <strong>Service Pro UID:</strong> {{ profile.service_pro_uid }}
              </p>
              <p><strong>Description:</strong> {{ profile.desc }}</p>
              <p><strong>Service Name:</strong> {{ profile.serv_name }}</p>
              <p><strong>Experience:</strong> {{ profile.experience }} years</p>
              <p>
                <strong>Service Area Pin Code:</strong>
                {{ profile.service_area_pin_code }}
              </p>
              <p v-if="loginStore.role === 1 || loginStore.role === 2">
                <strong>ID Document:</strong>
                <a :href="profile.id_document_url" target="_blank"
                  >View Document</a
                >
              </p>
              <p>
                <strong>Status:</strong>
                <span :class="statusClass(profile.status)">{{
                  profile.status
                }}</span>
              </p>
            </div>
            <div v-if="profile.role === 3">
              <hr />
              <h6>Customer Details</h6>
              <p><strong>Customer UID:</strong> {{ profile.cust_uid }}</p>
              <p><strong>Address:</strong> {{ profile.address }}</p>
              <p><strong>PinCode:</strong> {{ profile.pin_code }}</p>
            </div>
            <hr />
            <p class="card-text">
              <small class="text-muted"
                >Account created on {{ profile.date_created }}</small
              >
            </p>
            <div v-if="profile.role == 2">
              <div
                v-if="
                  route.params.id &&
                  profile.status == 'Approved' &&
                  !profile.flag_status &&
                  loginStore.role !== 1
                "
              >
                <RouterLink
                  class="btn btn-primary"
                  :to="{
                    name: 'BookService',
                    params: { service_pro_id: route.params.id },
                  }"
                  style="text-decoration: none; color: black"
                  >Book Service</RouterLink
                >
              </div>
              <div v-if="loginStore.role === 1 && profile.status != 'Approved'">
                <div>
                  <button
                    @click="changeApproval('accept')"
                    class="btn btn-success"
                    v-show="profile.status === 'Approval_Pending'"
                  >
                    Approve
                  </button>
                  |
                  <button
                    @click="changeApproval('reject')"
                    class="btn btn-danger"
                    v-show="profile.status === 'Approval_Pending'"
                  >
                    Reject
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <template v-if="profile.role === 2">
    <FeedbackView :serv_pro_id="profile.id" />
  </template>
</template>

<script setup>
import FeedbackView from '../components/FeedbackView.vue'
import { ref, onMounted, watch } from 'vue'
import axios from '@/axios'
import { useRoute } from 'vue-router'
import { LoginStore } from '@/stores/loginDetails'

import { useAlertStore } from '@/stores/alertMsg'
const alertStore = useAlertStore()
const addAlert = alertStore.addAlert

const loginStore = LoginStore()

const route = useRoute()
const profile = ref({})
const profileFound = ref(false)

const fetchProfile = async () => {
  try {
    const ext_url = route.params.id
      ? '/' + route.params.id
      : '/' + loginStore.user_id
    const { data } = await axios.get('/profile' + ext_url)
    profile.value = data
    if (profile.value.id) {
      profileFound.value = true
    }
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
}

const getRole = role => {
  const roles = { 1: 'Admin', 2: 'Service Provider', 3: 'Customer' }
  return roles[role] || 'Unknown'
}

const statusClass = status => {
  return {
    'text-success': status === 'Approved',
    'text-warning': status === 'Approval_Pending',
    'text-danger': status === 'Rejected',
  }
}

const changeApproval = async action => {
  try {
    const response = await axios.post(
      `/professional/status/${route.params?.id}/${action}`,
    )
    if (response.data.msg == 'Success') {
      addAlert('success', 'Status Changed, Reload to see changes')
    }
  } catch (error) {
    addAlert('danger', 'Something Went Wrong, Try again.')
    console.error('Error fetching profile:', error)
  }
}

const changeFlag = async () => {
  try {
    const response = await axios.post(`/flag-user/${profile.value.id}`)
    if (response.data.msg === 'Success') {
      profile.value.flag_status = response.data.flag
      addAlert('success', 'FlagChanged')
    }
  } catch (err) {
    addAlert('danger', 'Something Went wrong')
    console.error('Error', err)
  }
}

watch(
  () => route.params.id,
  () => {
    fetchProfile()
  },
)

onMounted(() => {
  fetchProfile()
})
</script>
