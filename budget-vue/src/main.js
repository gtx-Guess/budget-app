import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from '@/App.vue'
import router from '@/router'
import '@/styles.css'
import axios from 'axios'
import { useLocalStore } from '@/stores/localStorage'
import { loadUserData, checkAuthentication } from '@/utils/auth'

axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;
axios.defaults.withCredentials = true

let isRefreshing = false

axios.interceptors.response.use(
  response => response,
  async error => {
    // Don't retry refresh_token requests to avoid infinite loops
    if (error.config?.url?.includes('/api/refresh_token')) {
      return Promise.reject(error)
    }
    
    if (error.response?.status === 401 && !isRefreshing) {
      isRefreshing = true
      console.log('🔄 Attempting token refresh...')
      try {
        await axios.post('/api/refresh_token')
        console.log('✅ Refresh successful, retrying...')
        isRefreshing = false
        return axios.request(error.config)
      } catch (refreshError) {
        console.log('❌ Refresh failed, redirecting...')
        isRefreshing = false
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

const pinia = createPinia();
const app = createApp(App);

app.use(pinia).use(router);

// Initialize dark mode after Pinia is set up
const store = useLocalStore();
store.initializeDarkMode();

// Initialize user data if authenticated (handles page refresh)
const initializeUserData = async () => {
  try {
    const isAuthenticated = await checkAuthentication();
    if (isAuthenticated) {
      console.log('🔄 User authenticated, loading data...');
      await loadUserData();
    } else {
      console.log('👤 User not authenticated');
    }
  } catch (error) {
    console.log('❌ Error checking authentication:', error);
  }
};

// Initialize user data before mounting the app
initializeUserData().then(() => {
  app.mount("#app");
});