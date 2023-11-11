import { createRouter, createWebHistory } from 'vue-router'
import { authStore } from '@/store/token';
import { server } from '@share/utilities';
import axios from 'axios';
import App from '@/App.vue';
import PagesVue from '@/components/PagesVue.vue';
import LoginPage from '@components/pages/LoginPage.vue';
import PersonPage from '@components/pages/PersonPage.vue';
import ResumePage from '@components/pages/ResumePage.vue';
import ProfilePage from '@components/pages/ProfilePage.vue';
import StatPage from '@components/pages/StatPage.vue';
import AdminPage from '@components/pages/AdminPage.vue';
import AdminTables from '@components/pages/AdminTables.vue'
import ContactPage from '@components/pages/ContactPage.vue';
import NotFound from '@components/pages/NotFound.vue';
import PrintPage from '@components/pages/PrintPage.vue';
import FileManager from '@components/pages/FileManager.vue';
import MessagePage from '@components/pages/MessagePage.vue';


const router = createRouter({
  routes: [
    {
      path: '/',
      component: App
    },
    {
      path: '/login/auth',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/:group',
      name: 'group',
      component: PagesVue,
      children: [
        {
          path: 'persons',
          name: 'persons',
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
          path: 'print',
          name: 'print',
          component: PrintPage
        },
        {
          path: 'information',
          name: 'information',
          component: StatPage
        },
        {
          path: 'users',
          name: 'users',
          component: AdminPage
        },
        {
          path: 'table',
          name: 'table',
          component: AdminTables,
        },
        {
          path: 'contacts',
          name: 'contacts',
          component: ContactPage
        },
        {
          path: 'manager',
          name: 'manager',
          component: FileManager
        },
        {
          path: 'messages',
          name: 'messages',
          component: MessagePage
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
});

router.beforeEach(async (to, _from, next) => {
  const refresh_token = localStorage.getItem('refresh_token');
  const access_token = localStorage.getItem('access_token');

  const storeAuth = authStore()

  if (to.name !== 'login') {
    if (refresh_token) {

      const expiry_refresh = (JSON.parse(atob(refresh_token.split('.')[1]))).exp;

      if (Math.floor((new Date).getTime() / 1000) >= expiry_refresh) {
        next({ name: 'login' });
        
      } else {

        if (access_token) {
          const expiry_access = (JSON.parse(atob(access_token.split('.')[1]))).exp;

          if (Math.floor((new Date).getTime() / 1000) >= expiry_access) {
            const response = await axios.post(`${server}/refresh`, null, {
              headers: {'Authorization': `Bearer ${localStorage.getItem('refresh_token')}`}
            });
            const { access_token } = response.data;
            
            if (access_token){
              localStorage.setItem('access_token', access_token);
              storeAuth.setAccessToken(access_token);
              next();

            } else {
              router.push({ name: 'login' });
            };

          } else {
            next();
          };
          
        } else {
          next({ name: 'login' });
        };
      };
      
    } else {
      next({ name: 'login' });
    };
    
  } else {
    next();
  }
});

export default router;