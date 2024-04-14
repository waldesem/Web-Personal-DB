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
  localStorage.removeItem("refresh_token");
  router.push({ name: "login" });
}
</script>

<template>
  <div class="d-print-none sticky-top bg-white p-3 ">
      <div class="row">
        <div class="col-8 text-center">
          <AlertMessage />
        </div>
        <div class="col-2 text-end">
          <MessageDiv />
        </div>
        <div class="col-2 text-center">
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
              <div v-if="storeUser.userData.hasAdmin" class="dropdown-item">
                <router-link
                  :to="{ name: 'users' }"
                  class="link-opacity-50-hover" href="#"
                >
                  Пользователи
                </router-link>
              </div >
              <div class="dropdown-item" >
                <a
                class="link-opacity-50-hover" href="#"
                  @click="userLogout">Выход</a>
              </div >
            </ul>
          </div>
        </div>
      </div>
  </div>
</template>
