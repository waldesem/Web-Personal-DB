import axios from "axios";
import { createRouter, createWebHistory } from "vue-router";
import { server, expiredToken } from "@/utilities";

export const router = createRouter({
  routes: [
    {
      path: "/",
      name: "index",
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
        {
          path: "gpt",
          name: "gpt",
          component: () => import("@components/pages/staffsec/GptPage.vue"),
        },
      ],
    },
    { path: "/:pathMatch(.*)*", redirect: { name: "persons" } },
  ],
  history: createWebHistory(),
});

router.beforeEach(async (to, _from, next) => {
  if (["login", "index", "staffsec"].includes(to.name as string)) {
    next();
    return;
  }
  
  const accessToken = localStorage.getItem("access_token");
  const refreshToken = localStorage.getItem("refresh_token");

  if (!expiredToken(refreshToken)) {
    if (expiredToken(accessToken)) {
      try {
        const response = await axios.post(`${server}/auth/refresh`, null, {
          headers: {
            Authorization: `Bearer ${refreshToken}`,
          },
        });
        const { access_token } = response.data;
        localStorage.setItem("access_token", access_token);
        next();
        return;
      } catch (error) {
        console.error(error);
        next({ name: "login" });
        return;
      }
    } else {
      next();
      return;
    }
  }  else {
    next({ name: "login" });
    return;
  }  
});
