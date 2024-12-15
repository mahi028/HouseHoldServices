<template>
  <div class="container mt-4">
    <h1>Admin Dashboard</h1>
    <div class="row">
      <!-- Service Statistics -->
      <div class="col-md-6">
        <h3>Service Professionals</h3>
        <BarStats url="service" />
      </div>

      <div class="col-md-6">
        <h3>Requests by Service</h3>
        <BarStats url="service_request" />
      </div>

      <div class="row mt-4">
        <!-- Request Stats -->
        <div class="col-md-6">
          <h3>All Request</h3>
          <PieStats url="request" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import BarStats from '@/components/BarStats.vue'
import PieStats from '@/components/PieStats.vue'
</script>

<style>
canvas {
  max-width: 100%;
  height: 300px;
}
</style>
