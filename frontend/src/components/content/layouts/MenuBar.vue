<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { axiosAuth } from "@/auth";
import { stateUser, stateClassify } from "@/state";
import { server } from "@/utilities";
import { router } from "@/router";

const AlertMessage = defineAsyncComponent(
  () => import("@components/content/elements/AlertMessage.vue")
);
const MessageDiv = defineAsyncComponent(
  () => import('@components/content/divs/MessageDiv.vue')
)
async function userLogout(): Promise<void> {
  try {
    const response = await axiosAuth.delete(`${server}/auth/login`);
    console.log(response.status);
  } catch (error) {
    console.log(error);
  }

  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  router.push({ name: "login" });
}
</script>

<template>
  <div class="d-print-none sticky-top bg-white p-3 ">
      <div class="row">
        <div class="col-10 text-center">
          <AlertMessage/>
        </div>
        <div class="col-1 text-start">
          <MessageDiv/>
        </div>
        <div class="col-1 text-end">
          <div class="dropdown">
            <button
              class="btn btn-link dropdown-toggle"
              role="button"
              data-bs-toggle="dropdown"
              :title="stateClassify.users[stateUser.userId]"
            >
              <i class="bi bi-person-circle fs-3"></i>
            </button>
            <ul class="dropdown-menu">
              <li v-if="stateUser.hasAdmin" class="dropdown-item">
                <router-link
                  :to="{ name: 'users' }"
                  class="link-opacity-50-hover"
                >
                  Пользователи
                </router-link>
              </li >
              <li class="dropdown-item" >
                <a
                  class="link-opacity-50-hover" href="#"
                  @click="userLogout">
                  Выход
                </a>
              </li >
            </ul>
          </div>
        </div>
      </div>
  </div>
</template>
