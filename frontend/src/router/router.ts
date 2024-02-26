import axios from "axios";
import { createRouter, createWebHistory } from "vue-router";
import { server } from "@utilities/utils";
import { authStore } from "@/store/token";

export const router = createRouter({
  routes: [
    {
      path: "/",
      name: "auth",
      component: () => import("@/App.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@components/pages/LoginPage.vue"),
    },
    {
      path: "/:group",
      name: "group",
      component: () => import("@components/PagesVue.vue"),
      children: [
        {
          path: "persons",
          name: "persons",
          component: () => import("@components/pages/PersonPage.vue"),
        },
        {
          path: "resume",
          name: "resume",
          component: () => import("@components/pages/ResumePage.vue"),
        },
        {
          path: "profile/:id",
          name: "profile",
          component: () => import("@components/pages/ProfilePage.vue"),
        },
        {
          path: "information",
          name: "information",
          component: () => import("@components/pages/InfoPage.vue"),
        },
        {
          path: "users",
          name: "users",
          component: () => import("@components/pages/AdminPage.vue"),
        },
        {
          path: "user/:id",
          name: "user",
          component: () => import("@components/pages/UserPage.vue"),
        },
        {
          path: "table",
          name: "table",
          component: () => import("@components/pages/TablesPage.vue"),
        },
        {
          path: "contacts",
          name: "contacts",
          component: () => import("@components/pages/ContactPage.vue"),
        },
        {
          path: "manager",
          name: "manager",
          component: () => import("@components/pages/FilePage.vue"),
          props: (route) => ({ path: route.query.path }),
        },
      ],
    },
    {
      path: "/:pathMatch(.*)*",
      name: "404",
      component: () => import("@components/pages/NotFound.vue"),
    },
  ],
  history: createWebHistory(),
});

router.beforeEach(async (to, _from, next) => {
  const storeAuth = authStore();

  if (!["auth", "login", "group", "404"].includes(to.name as string)) {
    if (storeAuth.refreshToken) {
      const expiry_refresh = JSON.parse(atob(storeAuth.refreshToken.split(".")[1])).exp;

      if (Math.floor(new Date().getTime() / 1000) < expiry_refresh) {
        if (storeAuth.accessToken) {
          const expiry_access = JSON.parse(
            atob(storeAuth.accessToken.split(".")[1])
          ).exp;

          if (Math.floor(new Date().getTime() / 1000) >= expiry_access) {
            const response = await axios.post(`${server}/refresh`, null, {
              headers: {
                Authorization: `Bearer ${storeAuth.refreshToken}`,
              },
            });
            const { access_token } = response.data;

            if (access_token) {
              storeAuth.accessToken =  access_token;
              next();
            } else {
              next({ name: "login" });
            }
          } else {
            next();
          }
        } else {
          next({ name: "login" });
        }
      } else {
        next({ name: "login" });
      }
    } else {
      next({ name: "login" });
    }
  } else {
    next();
  }
});
