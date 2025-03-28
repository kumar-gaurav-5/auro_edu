import { createRouter, createWebHistory } from 'vue-router'
import DecksView from '../views/DecksView.vue'
import ReviewView from '../views/ReviewView.vue'
import QaView from '../views/QaView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/decks'
    },
    {
      path: '/decks',
      name: 'decks',
      component: DecksView
    },
    {
      path: '/review',
      name: 'review',
      component: ReviewView
    },
    {
      path: '/qa',
      name: 'qa',
      component: QaView
    }
  ]
})

export default router