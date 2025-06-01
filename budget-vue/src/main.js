import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from '@/App.vue'
import router from '@/router'
import '@/styles.css'
import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;
axios.defaults.withCredentials = true

axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      console.log('🔄 Attempting token refresh...')
      try {
        await axios.post('/api/refresh_token')
        console.log('✅ Refresh successful, retrying...')
        return axios.request(error.config)
      } catch (refreshError) {
        console.log('❌ Refresh failed, redirecting...')
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

const pinia = createPinia();

createApp(App).use(pinia).use(router).mount('#app');