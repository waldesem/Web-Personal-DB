import axios from "axios";
import { createRouter, createWebHistory } from "vue-router";
import { server } from "@utilities/utils";
import { authStore } from "@/store/auth";

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
      path: "/staffsec",
      name: "staffsec",
      component: () => import("@components/pages/StaffsecPage.vue"),
      children: [
        {
          path: "persons",
          name: "persons",
          component: () => import("@components/pages/staffsec/PersonsPage.vue"),
        },
        {
          path: "resume",
          name: "resume",
          component: () => import("@components/pages/staffsec/ResumePage.vue"),
        },
        {
          path: "profile/:id",
          name: "profile",
          component: () => import("@components/pages/staffsec/ProfilePage.vue"),
        },
        {
          path: "information",
          name: "information",
          component: () => import("@components/pages/staffsec/InfoPage.vue"),
        },
        {
          path: "contacts",
          name: "contacts",
          component: () => import("@components/pages/staffsec/ContactPage.vue"),
        },
        {
          path: "users",
          name: "users",
          component: () => import("@components/pages/staffsec/UsersPage.vue"),
        },
        {
          path: "user/:id",
          name: "user",
          component: () => import("@components/pages/staffsec/UserProfile.vue"),
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

  if (to.name as string !== "login") {
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
