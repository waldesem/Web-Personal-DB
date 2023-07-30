import { createRouter, createWebHistory } from 'vue-router'

import axios from 'axios';
import App from './App.vue'
import LoginForm from './components/LoginForm.vue'
import MainTable from './components/MainTable.vue';
import ProFile from './components/ProFile.vue';
import StatInfo from './components/StatInfo.vue';
import AdminPage from './components/AdminPage.vue';
import NotFound from './components/NotFound.vue';
import NavBar from './components/NavBar.vue';
import ModalWin from './components/profile/ModalWin.vue';
import UploadFile from './components/profile/UploadFile.vue';
import ResumeForm from './components/profile/ResumeForm.vue';
import AnketaTab from './components/profile/AnketaTab.vue';
import RegistryTab from './components/profile/RegistryTab.vue';
import PoligrafTab from './components/profile/PoligrafTab.vue';
import InvestigateTab from './components/profile/InvestigateTab.vue';
import InquiryTab from './components/profile/InquiryTab.vue';
import CheckTab from './components/profile/CheckTab.vue';
import config from '@/config';

const router = createRouter({
  routes: [
    {
      path: '/',
      name: 'home',
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
      component: LoginForm
    },
    {
      path: '/password',
      name: 'password',
      component: LoginForm
    },
    {
      path: '/index/:flag/:page',
      name: 'index',
      component: MainTable,
    },
    {
      path: '/resume/upload',
      name: 'upload',
      component: UploadFile,
    },
    {
      path: '/resume/create',
      name: 'create',
      component: ResumeForm
    },
    {
      path: '/anketa/:flag/:id',
      name: 'anketa',
      component: AnketaTab,
    },
    {
      path: '/check/:flag/:id',
      name: 'check',
      component: CheckTab
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProFile
    },
    {
      path: '/update/:flag/:id',
      name: 'modal',
      component: ModalWin
    },
    {
      path: '/registry/:id',
      name: 'registry',
      component: RegistryTab
    },
    {
      path: '/poligraf',
      name: 'poligraf',
      component: PoligrafTab
    },
    {
      path: '/investigation/:id',
      name: 'investigation',
      component: InvestigateTab
    },
    {
      path: '/inquiry/:id',
      name: 'inquiry',
      component: InquiryTab
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
      path: '/user/update/:flaf/:id',
      component: AdminPage
    },
    {
      path: '/user/action/:flag/:id',
      component: AdminPage
    },
    {
      path: '/region/:flag',
      component: AdminPage,
      children: [
        {
          path: ':id',
          component: AdminPage
        }
      ]
    },
    {
      path: '/logs/:flag',
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

const uploadPhotoRoute = {
  path: '/photo/upload/:id',
  component: ProFile
};
router.addRoute(uploadPhotoRoute);

const messagesRoute = {
  path: '/messages/:flag',
  component: NavBar
};
router.addRoute(messagesRoute);

const personNewsRoute = {
  path: '/news',
  component: NavBar
};
router.addRoute(personNewsRoute);

const adminRoute = {
  path: '/admin/admin',
  component: AdminPage
};


router.beforeEach(async (to, from, next) => {
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