<script setup lang="ts">
import { axiosAuth } from "@/auth";
import { onBeforeMount, defineAsyncComponent } from "vue";
import { stateClassify, stateUser, server } from "@/state";
import { router } from "@/router";

const AlertMessage = defineAsyncComponent(
  () => import("@components/content/elements/AlertMessage.vue")
);

onBeforeMount(async () => {
  try {
    const response = await axiosAuth.get(`${server}/classes`);
    [
      stateClassify.regions,
      stateClassify.conclusions,
      stateClassify.relations,
      stateClassify.affilations,
      stateClassify.educations,
      stateClassify.addresses,
      stateClassify.contacts,
      stateClassify.documents,
      stateClassify.poligrafs,
    ] = response.data;

    const token = localStorage.getItem("user_token") as string;
    const payload = window.atob(token).split(":");
    stateUser.userId = payload[1];
    stateUser.username = payload[2];
    stateUser.hasAdmin = payload[3] == "1";

    router.push({ name: "persons" });
  } catch (error: any) {
    console.error(error);
  }
});

async function userLogout(): Promise<void> {
  localStorage.removeItem("user_token");
  router.push({ name: "login" });
}
</script>

<template>
  <div class="container-fluid row px-3">
    <div class="col-2 d-print-none">
      <div class="navbar navbar-expand sticky-top fs-5 p-3">
        <div class="nav flex-column">
          <a class="nav-link text-danger fs-3 fw-bold">STAFFSEC FINTECH</a>
          <hr class="text-info">
          <router-link
            :to="{ name: 'persons' }"
            class="nav-link active"
          >
            Кандидаты
          </router-link>
          <hr class="text-info">
          <router-link
            :to="{ name: 'resume' }"
            class="nav-link active"
          >
            Создать
          </router-link>
          <hr class="text-info">
          <router-link
            :to="{ name: 'information' }"
            class="nav-link active"
          >
            Информация
          </router-link>
          <hr class="text-info">
          <router-link v-if="stateUser.hasAdmin" 
            :to="{ name: 'users' }"
            class="nav-link active"
          >
            Пользователи
          </router-link>
        </div>
      </div>
    </div>
    <div class="col-9" id="staffsec">
      <div class="sticky-top bg-white d-print-none p-3">
        <div class="row">
          <div class="col-10 text-center">
            <AlertMessage/>
          </div>
          <div class="col-2 text-end">
            <div class="dropdown">
              <button
                class="btn btn-link btn-lg dropdown-toggle"
                style="text-decoration: none;"
                role="button"
                data-bs-toggle="dropdown"
              >
                &#x272A; {{ stateUser.username }}
              </button>
              <ul class="dropdown-menu">
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
      <router-view v-slot="{ Component }" :key="$route.fullPath">
        <component :is="Component" />
      </router-view>
    </div>
    <div class="col-1 d-print-none"></div>
  </div>
</template>

<style scoped>
@media print {
  #staffsec {
    width: 100% !important;
  }
}
</style>
