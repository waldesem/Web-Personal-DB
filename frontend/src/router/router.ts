import { createRouter, createWebHistory } from 'vue-router'
import { appAuth } from '@store/auth';
import server from '@/store/server';
import axios from 'axios';
import App from '@/App.vue';
import LoginPage from '@pages/LoginPage.vue';
import StaffVue from '@components/StaffVue.vue';
import PersonPage from '@pages/PersonPage.vue';
import ResumePage from '@pages/ResumePage.vue';
import ProfilePage from '@pages/ProfilePage.vue';
import StatPage from '@pages/StatPage.vue';
import AdminVue from '@components/AdminVue.vue';
import UsersListPage from '@pages/UsersListPage.vue';
import UserPage from '@pages/UserPage.vue';
import NotFound from '@pages/NotFound.vue';
import ContactPage from '@pages/ContactPage.vue';

// Маршруты приложения  
const router = createRouter({
  routes: [
    {
      path: '/',
      component: App
    },
    {
      path: '/auth',
      name: 'app',
      component: App
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/staff',
      name: 'staff',
      component: StaffVue,
      children: [
        {
          path: 'persons',
          name: 'staffsec',
          component: PersonPage
        },
        {
          path: 'resume',
          name: 'resume',
          component: ResumePage
        },
        {
          path: 'profile/:id',
          name: 'profile',
          component: ProfilePage
        },
        {
          path: 'information',
          name: 'information',
          component: StatPage
        }
      ]
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminVue,
      children: [
        {
          path: 'users',
          name: 'users',
          component: UsersListPage
        },
        {
          path: 'user/:id',
          name: 'shape',
          component: UserPage,
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',  
      name: '404', 
      component: NotFound
    },
    {
      path: 'contacts',
      name: 'contacts',
      component: ContactPage
    }
  ],
  history: createWebHistory()
});

// Защита маршрутов с использованием токенов аутентификации и хранилища данных Pinia
router.beforeEach(async (to, _from, next) => {
  const refresh_token = localStorage.getItem('refresh_token');
  const access_token = localStorage.getItem('access_token');

  const storeAuth = appAuth()

  if (to.name !== 'login') {
    if (refresh_token) {
      // Проверка действительности refresh_token
      const expiry_refresh = (JSON.parse(atob(refresh_token.split('.')[1]))).exp;
      // Проверка действительности токена
      if (Math.floor((new Date).getTime() / 1000) >= expiry_refresh) {
        next({ name: 'login' })
        
      } else {
        // Проверка действительности access_token
        if (access_token) {
          const expiry_access = (JSON.parse(atob(access_token.split('.')[1]))).exp;
          // Проверка действительности токена
          if (Math.floor((new Date).getTime() / 1000) >= expiry_access) {
            const response = await axios.post(`${server}/refresh`, null, {
              headers: {'Authorization': `Bearer ${localStorage.getItem('refresh_token')}`}
            });
            const { access_token } = response.data;
            // Сохранение access_token в хранилище
            localStorage.setItem('access_token', access_token);
            storeAuth.setAccessToken(access_token);
            next()
            
          } else {
            next()
          }
          
        } else {
          next({ name: 'login' })
        }
      }
      
    } else {
      next({ name: 'login' })
    }
    
  } else {
    next()
  }
});

export default router;