<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { authStore } from "@/store/auth";
import { userStore } from "@/store/user";
import { server } from "@/utilities/utils";
import { router } from "@/router/router";

const AlertMessage = defineAsyncComponent(
  () => import("@components/content/elements/AlertMessage.vue")
);
const MessageDiv = defineAsyncComponent(
  () => import('@components/content/divs/MessageDiv.vue')
)

const storeAuth = authStore();
const storeUser = userStore();

async function userLogout(): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.delete(`${server}/login`);
    console.log(response.status);
  } catch (error) {
    console.log(error);
  }

  storeAuth.accessToken = "";
  storeAuth.refreshToken = "";

  router.push({ name: "login" });
}
</script>

<template>
  <div class="container-fluid p-3">
    <div class="row">
      <div class="col col-2">
        <p class="fs-3 fw-bold text-info">STAFFSEC - MTS Bank</p>
      </div>
      <div class="col col-6 text-center">
        <AlertMessage />
      </div>
      <div class="col col-2 text-end">
        <MessageDiv />
      </div>
      <div class="col col-2 text-center">
        <div class="dropdown">
          <a
            href="#"
            class="dropdown-toggle"
            role="button"
            data-bs-toggle="dropdown"
          >
            {{ storeUser.userData.userName }}
            <i class="bi bi-person-circle fs-3"></i>
          </a>
          <ul class="dropdown-menu">
            <li v-if="storeUser.userData.hasAdmin" class="dropdown-item">
              <router-link
                :to="{ name: 'users' }"
                class="link-opacity-50-hover" href="#"
              >
                Пользователи
              </router-link>
            </li>
            <li class="dropdown-item" >
              <a
              class="link-opacity-50-hover" href="#"
                @click="userLogout">Выход</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
