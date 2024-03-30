<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { authStore } from "@/store/auth";
import { userStore } from "@/store/user";
import { server } from "@/utilities/utils";
import { router } from "@/router/router";

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
  <nav
    class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-primary d-print-none"
  >
    <div class="container">
      <a class="navbar-brand">STAFFSEC</a>
      <div
        class="navbar-nav mr-auto collapse navbar-collapse"
        id="navbarContent"
      >
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li v-if="storeUser.userData.hasAdmin" class="nav-item">
            <router-link
              :to="{ name: 'users' }"
              class="nav-link active"
              href="#"
            >
              Пользователи
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              :to="{ name: 'persons' }"
              class="nav-link active"
            >
              Кандидаты
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              :to="{ name: 'resume' }"
              class="nav-link active"
            >
              Создать
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              :to="{ name: 'information' }"
              class="nav-link active"
            >
              Информация
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              :to="{ name: 'contacts' }"
              class="nav-link active"
            >
              Контакты
            </router-link>
          </li>
          <MessageDiv />
        </ul>
        <li class="nav-item dropdown d-flex">
          <a
            href="#"
            class="nav-link active dropdown-toggle"
            role="button"
            data-bs-toggle="dropdown"
          >
            {{
              storeUser.userData.fullName
                ? storeUser.userData.fullName
                    .split(" ")
                    .map((item) => item.charAt(0))
                    .join("")
                : ""
            }}
            <i class="bi bi-person-circle"></i>
          </a>
          <ul class="dropdown-menu">
            <li>
              <a class="dropdown-item" href="#" @click="userLogout">Выход</a>
            </li>
          </ul>
        </li>
      </div>
    </div>
  </nav>
</template>
