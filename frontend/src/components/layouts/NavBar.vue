<script setup lang="ts">
import { authStore } from "@/store/auth";
import { userStore } from "@/store/user";
import { server } from "@/utilities/utils";
import { router } from "@/router/router";

const storeAuth = authStore();
const storeUser = userStore();

const props = defineProps({
  arg: String,
  brand: {
    type: String,
    required: true,
  },
});

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
    class="navbar navbar-expand navbar-nav mr-auto navbar-dark d-print-none"
    :class="props.arg"
  >
    <div class="container">
      <a class="navbar-brand">{{ props.brand.toUpperCase() }}</a>
      <div
        class="navbar-nav mr-auto collapse navbar-collapse"
        id="navbarContent"
      >
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <slot name="navbar"></slot>
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
