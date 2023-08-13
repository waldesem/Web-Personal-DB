import axios from 'axios';
import { createRouter, createWebHistory } from 'vue-router'
import { appAuth } from '@store/auth';
import server from '@/store/server';
import App from '@/App.vue';
import LoginForm from '@pages/LoginForm.vue';
import PersonsList from '@pages/PersonsList.vue';
import ProFile from '@pages/ProFile.vue';
import StatInfo from '@pages/StatInfo.vue';
import NotFound from '@pages/NotFound.vue';
import UsersList from '@pages/UsersList.vue';
import UserProfile from '@pages/UserProfile.vue';
import LogsList from '@pages/LogsList.vue';
import RegionsList from '@pages/RegionsList.vue';
import PersonsAdmin from '@pages/PersonsAdmin.vue';
import CreateResume from '@pages/CreateResume.vue';

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
      component: LoginForm,
    },
    {
      path: '/index',
      redirect: 'persons',
      children: [
        {
          path: 'persons',
          name: 'persons',
          component: PersonsList
        },
        {
          path: 'resume',
          name: 'resume',
          component: CreateResume
        },
        {
          path: 'profile/:id',
          name: 'profile',
          component: ProFile,
        },
        {
          path: 'information',
          name: 'information',
          component: StatInfo
        }
      ]
    },
    {
      path: '/admin',
      redirect: 'main',
      children: [
        {
          path: ':flag',
          name: 'main',
          component: PersonsAdmin
        },
        {
          path: 'users',
          name: 'users',
          component: UsersList
        },
        {
          path: 'user/:id',
          name: 'shape',
          component: UserProfile,
        },
        {
          path: 'logs',
          name: 'logs',
          component: LogsList,
        },
        {
          path: 'regions',
          name: 'regions',
          component: RegionsList,
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',  
      name: '404', 
      component: NotFound
    }
  ],
  history: createWebHistory()
})

// Защита маршрутов с использованием токенов аутентификации и хранилища данных Pinia
router.beforeEach(async (to, _from, next) => {
  const refresh_token = localStorage.getItem('refresh_token');
  const access_token = localStorage.getItem('access_token');

  const storeAuth = appAuth()  // Хранилище данных Pinia

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