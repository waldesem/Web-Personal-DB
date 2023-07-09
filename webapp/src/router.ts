import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import LoginForm from './components/LoginForm.vue'
import MainTable from './components/MainTable.vue';
import ProFile from './components/ProFile.vue';
import StatInfo from './components/StatInfo.vue';
import AdminPage from './components/AdminPage.vue';
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
      path: '/admin/index',
      name: 'admin',
      component: AdminPage
    },
    {
      path: '/:pathMatch(.*)*',  
      name: '404', 
      component: NotFound
    }
  ],
  history: createWebHistory()
})

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('jwt_token');
  if (to.name !== 'login' && !token) next({ name: 'login' });
  else next();
});


export default router;