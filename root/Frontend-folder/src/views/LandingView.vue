<template>
  <div>
    <!-- Hero Section -->
    <header class="bg-primary text-white text-center py-5">
      <div class="container">
        <h1>Welcome to Household Services</h1>
        <p class="lead">
          Reliable, affordable, and professional services at your doorstep
        </p>
        <router-link
          to="/register"
          class="btn btn-light btn-lg mt-3"
          v-show="!loginStore.isLoggedIn"
        >
          Get Started
        </router-link>
      </div>
    </header>

    <!-- Why Choose Us Section -->
    <section class="bg-light py-5">
      <div class="container">
        <h2 class="text-center mb-4">Why Choose Us?</h2>
        <div class="row">
          <div class="col-md-4 text-center mb-4">
            <i
              class="bi bi-shield-check text-primary mb-3"
              style="font-size: 2rem"
            ></i>
            <h5>Trusted Professionals</h5>
            <p>
              All our professionals are verified and trained to ensure
              high-quality services.
            </p>
          </div>
          <div class="col-md-4 text-center mb-4">
            <i
              class="bi bi-clock text-primary mb-3"
              style="font-size: 2rem"
            ></i>
            <h5>On-Time Service</h5>
            <p>
              We respect your time and ensure that our team reaches on schedule,
              every time.
            </p>
          </div>
          <div class="col-md-4 text-center mb-4">
            <i
              class="bi bi-wallet2 text-primary mb-3"
              style="font-size: 2rem"
            ></i>
            <h5>Affordable Pricing</h5>
            <p>
              Our pricing is transparent, with no hidden costs. Quality service
              within your budget.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section class="services py-5">
      <div class="container">
        <RouterLink :to="{ name: 'Home' }"
          ><h2 class="text-center mb-4">See All Of Our Services</h2></RouterLink
        >

        <!--  -->
      </div>
    </section>
    <!-- Call to Action Section -->
    <section class="bg-primary text-white text-center py-5">
      <div class="container">
        <h2>Ready to Book a Service?</h2>
        <p class="lead">
          Get your household needs met with ease and convenience.
        </p>
        <router-link
          :to="{ name: 'Register' }"
          class="btn btn-light btn-lg mt-3"
          v-if="!loginStore.isLoggedIn"
        >
          Book Now
        </router-link>
        <router-link
          :to="{ name: 'Home' }"
          class="btn btn-light btn-lg mt-3"
          v-else
        >
          Book now
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { LoginStore } from '@/stores/loginDetails'
const loginStore = LoginStore()
</script>

<style scoped>
header {
  background: linear-gradient(rgba(1, 15, 136, 0.5), rgba(0, 0, 0, 0.5));
  color: #fff;
}
header h1 {
  font-size: 2.5rem;
}
header p {
  font-size: 1.2rem;
}

.bi {
  font-size: 2rem;
}
</style>
