<template>
  <div class="container mt-4 feedback-section">
    <h1 class="text-center mb-4">User Feedback</h1>
    <div v-if="feedbacks.length > 0">
      <table class="table table-bordered table-striped">
        <thead class="thead-dark">
          <tr>
            <th scope="col">#</th>
            <th scope="col">Request id</th>
            <th scope="col">Customer Name</th>
            <th scope="col">Rated by</th>
            <th scope="col">Rating</th>
            <th scope="col">Comment</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(feedback, index) in feedbacks"
            :key="feedback.feedback_id"
          >
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ feedback.rqst_id }}</td>
            <td>
              <RouterLink
                :to="{ name: 'Profile', params: { id: feedback.cust_id } }"
                >{{ feedback['cust.user.name'] }}</RouterLink
              >
            </td>
            <td>{{ getRoles(feedback.feedback_by) }}</td>
            <td>
              <span v-for="star in 5" :key="star" class="text-warning">
                <i
                  :class="
                    star <= feedback.feedback_rating
                      ? 'fas fa-star'
                      : 'far fa-star'
                  "
                ></i>
              </span>
              <span>({{ feedback.feedback_rating }})</span>
            </td>
            <td>{{ feedback.feedback_comment }}</td>
          </tr>
        </tbody>
      </table>
      <h3 class="m-5" style="text-align: center">End of Page</h3>
    </div>
    <div v-else class="text-center">
      <p class="text-muted">No feedback available.</p>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import axios from '@/axios'

const props = defineProps({
  serv_pro_id: {
    type: Number,
    required: true,
  },
})

const feedbacks = ref([])
function getRoles(role_id) {
  return { 1: 'Admin', 2: 'Service_Pro', 3: 'Customer' }[role_id]
}
const fetchFeedback = async () => {
  try {
    const response = await axios.get(`/feedback/${props.serv_pro_id}`)
    feedbacks.value = response.data
  } catch (err) {
    console.error('Error', err)
  }
}
onMounted(fetchFeedback)
</script>
