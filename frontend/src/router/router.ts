import { createRouter, createWebHistory } from 'vue-router'
import { server } from '@share/utilities';
import axios from 'axios';
import App from '@/App.vue';

const PagesVue = () => import('@components/PagesVue.vue');
const LoginPage = () => import('@components/pages/LoginPage.vue');
const PersonPage = () => import('@components/pages/PersonPage.vue');
const ResumePage = () => import('@components/pages/ResumePage.vue');
const ProfilePage = () => import('@components/pages/ProfilePage.vue');
const InfoPage = () => import('@components/pages/InfoPage.vue');
const AdminPage = () => import('@components/pages/AdminPage.vue');
const TablesPage = () => import('@components/pages/TablesPage.vue');
const ContactPage = () => import('@components/pages/ContactPage.vue');
const PrintPage = () => import('@components/pages/PrintPage.vue');
const FilePage = () => import('@components/pages/FilePage.vue');
const MessagePage = () => import('@components/pages/MessagePage.vue');
const UserPage = () => import('@components/pages/UserPage.vue');
const NotFound = () => import('@components/pages/NotFound.vue');

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
          component: InfoPage
        },
        {
          path: 'users',
          name: 'users',
          component: AdminPage
        },
        {
          path: 'user/:id',
          name: 'user',
          component: UserPage
        },
        {
          path: 'table',
          name: 'table',
          component: TablesPage,
        },
        {
          path: 'contacts',
          name: 'contacts',
          component: ContactPage
        },
        {
          path: 'manager',
          name: 'manager',
          component: FilePage
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