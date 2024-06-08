<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { stateUser } from "@/state";
import { router } from "@/router";

const AlertMessage = defineAsyncComponent(
  () => import("@components/content/elements/AlertMessage.vue")
);
async function userLogout(): Promise<void> {
  localStorage.removeItem("user_token");
  router.push({ name: "login" });
}
</script>

<template>
  <div class="d-print-none sticky-top bg-white p-3 ">
      <div class="row">
        <div class="col-10 text-center">
          <AlertMessage/>
        </div>
        <div class="col-2 text-end">
          <div class="dropdown">
            <button
              class="btn btn-link dropdown-toggle"
              role="button"
              data-bs-toggle="dropdown"
              :title="stateUser.fullname"
            >
              {{ stateUser.username }}
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
