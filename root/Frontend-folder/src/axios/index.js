// src/axios.js
import axios from 'axios'
import Cookies from 'js-cookie'
const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000,
})

axiosInstance.interceptors.request.use(
  async config => {
    config.withCredentials = true

    if (!['/login', '/register'].includes(config.url)) {
      const jwtCsrfToken = Cookies.get('csrf_access_token')
      config.headers['X-CSRF-TOKEN'] = jwtCsrfToken || ''
    }

    return config
  },
  error => Promise.reject(error),
)

axiosInstance.interceptors.response.use(
  response => response, // Pass successful responses
  error => Promise.reject(error),
)

export default axiosInstance
