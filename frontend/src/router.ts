import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
  routes: [
    {
      path: "/",
      name: "index",
      component: () => import("@/App.vue"),
      children: [
        {
          path: "login",
          name: "login",
          component: () => import("@components/pages/LoginPage.vue"),
        },
        {
          path: "staffsec",
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
              path: "users",
              name: "users",
              component: () => import("@components/pages/staffsec/UsersPage.vue"),
            },
            {
              path: "user/:id",
              name: "user",
              component: () => import("@components/pages/staffsec/ProfileUser.vue"),
            },
          ],
        },
      ],
    },
    { path: "/:pathMatch(.*)*", redirect: { name: "persons" } },
  ],
  history: createWebHistory(),
});
