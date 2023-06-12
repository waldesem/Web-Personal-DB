import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import LoginView from './components/Login.vue'
import MainView from './components/Main.vue';
import ResumeView from './components/Resume.vue'
import ProfileView from './components/Profile.vue'
import StatView from './components/Stat.vue'
import NotFoundView from './components/NotFound.vue'

const router = createRouter({
  routes: [
    {
      path: '/',
      name: 'app',
      component: App
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/index/:flag',
      name: 'index',
      component: MainView
    },
    {
      path: '/resume/',
      name: 'resume',
      component: ResumeView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/information',
      name: 'information',
      component: StatView
    },
    {
      path: '/:pathMatch(.*)*',  
      name: '404', 
      component: NotFoundView
    }
  ],
  history: createWebHistory()
})

export default router;