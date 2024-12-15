<!-- src/components/ServiceCard.vue -->
<template>
  <div class="col-md-4 mb-4">
    <div class="card shadow-sm border-0">
      <img
        :src="image"
        alt="Service image"
        class="card-img-top"
        loading="lazy"
      />
      <div class="card-body text-center">
        <h4 class="card-title">{{ name }}</h4>
        <p class="card-text">{{ description }}</p>
        <p class="card-text">Min-Time: {{ min_time }} min</p>
        <p class="card-text">Base-Price: ₹{{ base_price }}</p>
        <router-link :to="route" class="btn btn-outline-primary"
          >View Details</router-link
        ><br />
        <router-link
          class="btn btn-outline-primary"
          :to="{
            name: 'AllProfessionals',
            params: { serv_id: serv_id },
          }"
          >See Available Professionals</router-link
        >
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true,
  },
  image: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  base_price: {
    type: Number,
    required: true,
  },
  min_time: {
    type: Number,
    required: true,
  },
  serv_id: {
    type: Number,
    required: true,
  },
  route: {
    type: String,
    required: true,
  },
})
</script>

<style scoped>
.card-title {
  font-size: 1.2rem;
  font-weight: 600;
}
.card-text {
  font-size: 0.9rem;
  color: #6c757d;
}
.card-img-top {
  max-height: 200px;
  object-fit: cover;
}
</style>
