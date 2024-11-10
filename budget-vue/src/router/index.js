import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ConnectToBank from '@/views/ConnectToBank.vue'
import LoginView from '@/views/Login.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/connect',
    name: 'Bank Connection Page',
    component: ConnectToBank
  },
  {
    path: '/login',
    name: 'Login Page',
    component: LoginView,
    meta: { hideNavbar: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
