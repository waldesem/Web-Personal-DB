import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios';
import server from '../store/server';
import App from '../App.vue';
import { appAuth } from '../store/auth';
import LoginForm from '../components/LoginForm.vue';
import PersonsList from '../components/person/PersonsList.vue';
import ProFile from '../components/person/ProFile.vue';
import StatInfo from '../components/person/StatInfo.vue';
import AdminPage from '../components/AdminPage.vue';
import NotFound from '../components/NotFound.vue';
import UsersList from '../components/admin/UsersList.vue';
import UserProfile from '../components/admin/UserProfile.vue';
import LogsList from '../components/admin/LogsList.vue';
import RegionsList from '../components/admin/RegionsList.vue';
import PersonsAdmin from '../components/admin/PersonsAdmin.vue';
import StaffPage from '../components/StaffPage.vue';
import CreateResume from '@/components/person/profile/CreateResume.vue';

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
      name: 'index',
      component: StaffPage,
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
      name: 'admin',
      component: AdminPage,
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


router.beforeEach(async (to, _from, next) => {
  const refresh_token = localStorage.getItem('refresh_token');
  const access_token = localStorage.getItem('access_token');

  const storeAuth = appAuth()

  if (to.name !== 'login') {
    if (refresh_token) {
      const expiry_refresh = (JSON.parse(atob(refresh_token.split('.')[1]))).exp;

      if (Math.floor((new Date).getTime() / 1000) >= expiry_refresh) {
        next({ name: 'login' })
        
      } else {
        if (access_token) {
          const expiry_access = (JSON.parse(atob(access_token.split('.')[1]))).exp;

          if (Math.floor((new Date).getTime() / 1000) >= expiry_access) {
            const response = await axios.post(`${server}/refresh`, null, {
              headers: {'Authorization': `Bearer ${localStorage.getItem('refresh_token')}`}
            });
            const { access_token } = response.data;
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