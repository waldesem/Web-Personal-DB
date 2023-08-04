import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios';
import config from '../config.ts';
import App from '../App.vue';
import LoginForm from '../components/LoginForm.vue';
import PersonsList from '../components/PersonsList.vue';
import ProFile from '../components/ProFile.vue';
import StatInfo from '../components/StatInfo.vue';
import AdminPage from '../components/AdminPage.vue';
import NotFound from '../components/NotFound.vue';
import UsersList from '../components/admin/UsersList.vue';
import UserProfile from '../components/admin/UserProfile.vue';
import LogsList from '../components/admin/LogsList.vue';
import RegionsList from '../components/admin/RegionsList.vue';
import PersonsAdmin from '../components/admin/PersonsAdmin.vue';


const router = createRouter({
  routes: [
    {
      path: '/',
      component: App
    },
    {
      path: '/auth',
      name: 'app',
      component: App,
      children:  [
        {
          path: 'login',
          name: 'login',
          component: LoginForm
        },
        {
          path: 'password',
          redirect: { name: 'login' }
        },
      ]
    },
    {
      path: '/index/:flag/:page',
      name: 'index',
      component: PersonsList,
    },
    {
      path: '/messages/:flag',
      redirect: { name: 'app' }
    },
    {
      path: '/resume/upload',
      redirect: { name: 'app' }
    },
    {
      path: '/resume/create',
      redirect: { name: 'app' }
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProFile,
      children: [
        {
          path: 'anketa/:flag',
          redirect: { name: 'app' }
        },
        {
          path: 'photo',
          redirect: { name: 'app' }
        },
        {
          path: 'check/:flag',
          redirect: { name: 'app' }
        },
        {
          path: 'registry',
          redirect: { name: 'app' }
        },
        {
          path: 'poligraf',
          redirect: { name: 'app' }
        },
        {
          path: 'investigation',
          redirect: { name: 'app' }
        },
        {
          path: 'inquiry',
          redirect: { name: 'app' }
        },
        {
          path: 'update/:flag',
          redirect: { name: 'app' }
        },
      ]
    },
    {
      path: '/information',
      name: 'information',
      component: StatInfo
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPage
    },
    {
      path: '/admin/:flag/:page',
      name: 'main',
      component: PersonsAdmin
    },
    {
      path: '/person/:id/:flag',
      redirect: { name: 'admin' }
    },
    {
      path: '/users',
      name: 'users',
      component: UsersList,
      children: [
        {
          path: ':id',
          name: 'shape',
          component: UserProfile,
          children: [
            {
              path: 'post/:flag',
              redirect: { name: 'users' }
              },
              {
              path: 'get/:flag',
              redirect: { name: 'users' }
              },
            ]
        }
      ]
    },
    {
      path: '/logs',
      name: 'logs',
      component: LogsList,
      children: [
        {
          path: ':flag',
          redirect: { name: 'logs' }
        }
      ]
    },
    {
      path: '/region',
      name: 'regions',
      component: RegionsList,
      children: [
        {
          path: ':id/:flag',
          redirect: { name: 'regions' }
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
  
  if (to.name !== 'login') {
    if (refresh_token) {
      const expiry_refresh = (JSON.parse(atob(refresh_token.split('.')[1]))).exp;

      if (Math.floor((new Date).getTime() / 1000) >= expiry_refresh) {
        next({ name: 'login' })
        
      } else {
        if (access_token) {
          const expiry_access = (JSON.parse(atob(access_token.split('.')[1]))).exp;

          if (Math.floor((new Date).getTime() / 1000) >= expiry_access) {
            const response = await axios.post(`${config.appUrl}/refresh`, null, {
              headers: {'Authorization': `Bearer ${localStorage.getItem('refresh_token')}`}
            });
            const { access_token } = response.data;
            localStorage.setItem('access_token', access_token);
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