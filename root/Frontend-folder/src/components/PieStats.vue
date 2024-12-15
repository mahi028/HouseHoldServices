<template>
  <Doughnut :data="chartData" :options="chartOptions" v-if="loaded" />
</template>
<script setup>
import 'chart.js/auto'
import { Doughnut } from 'vue-chartjs'
import axios from '@/axios'
import { onMounted, ref } from 'vue'
const props = defineProps({
  url: {
    type: String,
    required: true,
  },
})
function generateRandomColors(n) {
  for (let i = 0; i < n; i++) {
    const r = Math.floor(Math.random() * 256)
    const g = Math.floor(Math.random() * 256)
    const b = Math.floor(Math.random() * 256)
    const randomColor = `rgb(${r}, ${g}, ${b})`
    colors.value.push(randomColor)
  }
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    tooltip: {
      enabled: true,
    },
  },
  animation: {
    animateScale: true,
    animateRotate: true,
  },
}

const loaded = ref(false)
const colors = ref([])

const chartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Request Statistics',
      backgroundColor: colors,
      data: [],
      hoverOffset: 4,
    },
  ],
})

const fetchData = async () => {
  try {
    const response = await axios.get('/dashboard/stats/' + props.url)
    const data = response.data

    chartData.value.labels = data.labels
    chartData.value.datasets[0].data = data.stats
    generateRandomColors(data.labels.length)
    loaded.value = true
  } catch (err) {
    console.error('Error fetching data:', err)
  }
}

onMounted(fetchData)
</script>
