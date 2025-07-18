import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from '@/App.vue'
import router from '@/router'
import '@/styles.css'
import axios from 'axios'
import { useLocalStore } from '@/stores/localStorage'
import { loadUserData, checkAuthentication } from '@/utils/auth'

// Automatically detect environment and set backend URL
const getBackendURL = () => {
  const hostname = window.location.hostname;
  console.log('🌐 Current hostname:', hostname);
  
  // Production environment
  if (hostname === import.meta.env.VITE_PRODUCTION_HOSTNAME) {
    console.log('🚀 Production mode - using', import.meta.env.VITE_PRODUCTION_API_URL);
    return import.meta.env.VITE_PRODUCTION_API_URL;
  }
  
  // Local network environment
  if (hostname === import.meta.env.VITE_LOCAL_NETWORK_HOSTNAME) {
    console.log('🏠 Local network mode - using', import.meta.env.VITE_LOCAL_NETWORK_API_URL);
    return import.meta.env.VITE_LOCAL_NETWORK_API_URL;
  }
  
  // Local development fallback
  console.log('💻 Local development mode - using', import.meta.env.VITE_LOCAL_DEV_API_URL);
  return import.meta.env.VITE_LOCAL_DEV_API_URL;
};

const backendURL = getBackendURL();
console.log('🔗 Setting axios baseURL to:', backendURL);
axios.defaults.baseURL = backendURL;
axios.defaults.withCredentials = true

const pinia = createPinia();
const app = createApp(App);

app.use(pinia).use(router);

// Mount the app first
app.mount("#app");

// Initialize state after app is mounted
const initializeApp = async () => {
  try {
    // Initialize dark mode after app is mounted
    const store = useLocalStore();
    store.initializeDarkMode();
    
    // Check authentication and load user data
    const isAuthenticated = await checkAuthentication();
    if (isAuthenticated) {
      console.log('🔄 User authenticated, loading data...');
      await loadUserData(store);
    } else {
      console.log('👤 User not authenticated');
    }
  } catch (error) {
    console.log('❌ Error during app initialization:', error);
  }
};

// Initialize app state
initializeApp();

// Set up axios interceptor after app is mounted
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