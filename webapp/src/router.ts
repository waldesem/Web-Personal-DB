import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import LoginForm from './components/LoginForm.vue'
import MainTable from './components/MainTable.vue';
import ProFile from './components/ProFile.vue';
import StatInfo from './components/StatInfo.vue';
import NotFound from './components/NotFound.vue';

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
      component: LoginForm
    },
    {
      path: '/index/:flag',
      name: 'index',
      component: MainTable
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProFile
    },
    {
      path: '/information',
      name: 'information',
      component: StatInfo
    },
    {
      path: '/:pathMatch(.*)*',  
      name: '404', 
      component: NotFound
    }
  ],
  history: createWebHistory()
})

export default router;