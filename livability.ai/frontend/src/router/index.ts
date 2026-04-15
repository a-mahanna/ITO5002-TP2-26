import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import HomeScreen from '@/views/HomeScreen.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeScreen,
    },
    {
      path: '/SuburbSearch',
      name: 'SuburbSearch',
      component: DashboardView,
    },
    {
      path: '/FindYourMatch',
      name: 'FindYourMatch',
      component: () => import('../views/FindSuburb.vue'),
    },
  ],
})

export default router
