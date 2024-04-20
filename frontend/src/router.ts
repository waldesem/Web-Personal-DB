import axios from "axios";
import { createRouter, createWebHistory } from "vue-router";
import { authStore } from "@/store/auth";
import { server, readToken } from "@/utilities";

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
        {
          path: "gpt",
          name: "gpt",
          component: () => import("@components/pages/staffsec/GptPage.vue"),
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

  if ((to.name as string) === "login") {
    next();
    return;
  }

  if (!storeAuth.refreshToken) {
    next({ name: "login" });
    return;
  }

  if (
    Math.floor(new Date().getTime() / 1000) >=
    readToken(storeAuth.refreshToken, "exp")
  ) {
    next();
    return;
  }

  if (!storeAuth.accessToken) {
    next({ name: "login" });
    return;
  }

  if (
    Math.floor(new Date().getTime() / 1000) < readToken(storeAuth.accessToken, "exp")
  ) {
    next();
    return;
  }

  try {
    const response = await axios.post(`${server}/refresh`, null, {
      headers: {
        Authorization: `Bearer ${storeAuth.refreshToken}`,
      },
    });

    const { access_token } = response.data;

    if (access_token) {
      storeAuth.accessToken = access_token;
      next();
    } else {
      next({ name: "login" });
    }
  } catch (error) {
    next({ name: "login" });
  }
});
