<script setup lang="ts">
import { inject } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@/store/alert";
import { server } from "@/utilities/utils";
import { router } from "@/router/router";

const storeAuth = authStore();
const storeAlert = alertStore();

const fullName = inject("fullName") as string;

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
    storeAlert.alertMessage.setAlert("alert-warning", error as string);
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
            :title="fullName ? fullName : ''"
          >
            {{
              fullName
                ? fullName
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
